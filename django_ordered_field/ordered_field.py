import copy
from django.db import models
from django.utils.timezone import now
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.signals import (post_delete, post_save, pre_delete, pre_save)


class OrderedField(models.IntegerField, FieldCacheMixin):

    description = "Position in an ordered table"

    def __init__(self, verbose_name=None, name=None, default=-1,
                 update_auto_now=True, extra_field_updates=None,
                 parent_link_name=None, *args, **kwargs): #TODO: rename parent_link_name, confusing with inheritance_with_parent_link_tester
        if 'unique' in kwargs:
            raise TypeError(
                "{0} can't have a unique constraint.".
                format(self.__class__.__name__))
        super(OrderedField, self).__init__(
            verbose_name=verbose_name, name=name, default=default, *args, **kwargs)
        self.update_auto_now = update_auto_now
        self.extra_field_updates = extra_field_updates if extra_field_updates is not None else {}
        self.parent_link_name = parent_link_name

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.update_auto_now is not None:
            kwargs["update_auto_now"] = self.update_auto_now
        if self.extra_field_updates is not None:
            kwargs["extra_field_updates"] = self.extra_field_updates
        if self.parent_link_name is not None:
            kwargs["parent_link_name"] = self.parent_link_name
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, private_only=False):
        super(OrderedField, self).contribute_to_class(cls, name, private_only)

        for constraint in cls._meta.unique_together:
            if self.name in constraint:
                raise TypeError(
                    "{0} can't be part of a unique constraint.".
                    format(self.__class__.__name__))
        setattr(cls, self.name, self)
        self.add_signals(cls)

    def add_signals(self, cls):
        prefix = ".".join([cls._meta.label_lower, self.name])
        """pre_delete.connect(self.prepare_delete,
                           sender=cls,
                           dispatch_uid=".".join([prefix, "pre_delete"]))"""
        post_delete.connect(self.update_on_delete,
                            sender=cls,
                            dispatch_uid=".".join([prefix, "post_delete"]))
        pre_save.connect(self.update_pre_save,
                         sender=cls,
                         dispatch_uid=".".join([prefix, "pre_save"]))
        post_save.connect(self.update_on_save,
                          sender=cls,
                          dispatch_uid=".".join([prefix, "post_save"]))

    def get_cache_name(self):
        return self.name + "_cache"     # TODO: check if this si correct

    def get_queryset(self, model_instance):
        model = type(model_instance)
        if self.parent_link_name is not None:
            try:    # TODO: clean, and make one place
                model = model._meta.get_field(self.parent_link_name).remote_field.model
            except:
                if model_instance.__class__.__name__.lower() + "_ptr" != self.parent_link_name:
                    #print(model_instance.__class__.__name__.lower() + "_ptr")
                    model = model._meta.get_field(self.parent_link_name).remote_field.model
        return model._default_manager.all()  # TODO: check all()

    def extra_updates_on_change(self, model_instance, updates):
        self._auto_now_field_update(model_instance, updates)
        self._extra_updates(updates, self.extra_field_updates)

    def _auto_now_field_update(self, model_instance, updates):
        if self.update_auto_now:
            date_now = now()
            for field in model_instance._meta.get_fields():
                if getattr(field, 'auto_now', False):
                    updates[field.name] = date_now

    def _extra_updates(self, updates, extra):
        for field_name, new_data in extra.items():
            if callable(new_data):
                updates[field_name] = new_data()
            else:
                updates[field_name] = new_data

    def get_next_sibling(self, model_instance):
        try:
            return self.get_queryset(model_instance). \
                filter(**{'%s__gt' % self.name: getattr(
                    model_instance, self.get_cache_name())[0]})[0]
        except IndexError:
            return None

    def update_on_delete(self, sender, instance, **kwargs):
        next_sibling = self.get_next_sibling(instance)
        if next_sibling:
            decrement_by = 1
            queryset = self.get_queryset(next_sibling)
            current = getattr(instance, self.get_cache_name())[0]
            updates = {self.name: models.F(self.name) - decrement_by}
            self.extra_updates_on_change(instance, updates)
            queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)

    def update_pre_save(self, sender, instance, values=None, updates=None, **kwargs):
        current_value, updated_value = get_values(instance, self.get_cache_name(), values)

        if current_value == updated_value or updated_value is None:
            return  # Order was not changed

        if (instance.pk is None or instance._state.adding):
            return  # Do not update extra fields on self if self is new

        if updates is None:
            # Inherited classes can send in custome update values
            # used for custom updates when item changes collection
            updates = {}
            self._extra_updates(updates, self.extra_field_updates)

        for key, value in updates.items():
            setattr(instance, key, value)

    def update_on_save(self, sender, instance, created, values=None, **kwargs):
        """
            TODO: Rename. It updates other rows, reflect that... or a new method that this one calls
        """
        current_value, updated_value = get_values(instance, self.get_cache_name(), values)

        if current_value == updated_value:
            return  # Order was not changed     #TODO: change collection but into same position, looks like that will fail, test it

        if current_value is None and created:
            current_value = -1   # TODO: ???  loosk strange. Find out why I made this

        queryset = self.get_queryset(instance).exclude(pk=instance.pk)

        updates = {}
        self.extra_updates_on_change(instance, updates)

        if created:
            # increment positions gte updated or node moved from another collection
            queryset = queryset.filter(**{'%s__gte' % self.name: updated_value})
            updates[self.name] = models.F(self.name) + 1
        elif updated_value > current_value:
            # decrement positions gt current and lte updated
            queryset = queryset.filter(**{'%s__gt' % self.name: current_value,
                                          '%s__lte' % self.name: updated_value})
            updates[self.name] = models.F(self.name) - 1
        else:
            # increment positions lt current and gte updated
            queryset = queryset.filter(**{'%s__lt' % self.name: current_value,
                                          '%s__gte' % self.name: updated_value})
            updates[self.name] = models.F(self.name) + 1
        queryset.update(**updates)
        setattr(instance, self.get_cache_name(), (updated_value, None))

    def pre_save(self, model_instance, add):
        cache_name = self.get_cache_name()

        current_value, updated_value = self._get_cleaned_current_and_updated_values(
            add, model_instance, cache_name)

        is_new = current_value is None  # NB: not the same as add
        min_position, max_position = self._get_max_min_positions(
            model_instance, is_new) # TODO: refactor this. no need to return min. min is always 0

        position = self._position_boundary_checks(
            add, updated_value, min_position, max_position)

        if add and position == max_position:
            setattr(model_instance, cache_name, (None, position))#(position, None)) #TODO: fixed some, but broke others
        else:
            setattr(model_instance, cache_name, (current_value, position))
        return position

    def _get_cleaned_current_and_updated_values(
            self, add, model_instance, cache_name, values=None):

        current_value, updated_value = get_values(model_instance, cache_name, values)

        if add and current_value is not None:
            # some cleanup if adding new record but current_value has an existing value
            # Happens when value is set in constructor
            # If order is not given during construction then current_value is given -1 as default
            if updated_value is None:
                # happens when new order is given in constructor instead of assigned later
                updated_value = current_value
            current_value = None

        # existing instance, position not modified; no cleanup required
        if current_value is not None and updated_value is None:
            return current_value, current_value

        # Never managed to get updated_value = None at this place.
        # But if it hapens, then add code to handle it

        return current_value, updated_value

    def _get_max_min_positions(self, model_instance, is_new):
        current_count = self.get_queryset(model_instance).count()
        if is_new:
            max_position = current_count
        else:
            max_position = current_count - 1
        return 0, max_position

    def __get__(self, instance, owner):
        current, updated = getattr(instance, self.get_cache_name())
        return current if updated is None else updated

    def __set__(self, instance, value):
        if value is None:
            value = self.default
        cache_name = self.get_cache_name()
        try:
            current, updated = getattr(instance, cache_name)
        except AttributeError:
            current, updated = value, None
        else:
            updated = value
        instance.__dict__[self.name] = value
        setattr(instance, cache_name, (current, updated))

    def _position_boundary_checks(self, add, current_value, min_position, max_position):
        #if (add and current_value == -1) or current_value >= max_position:
        #    return max_position
        if current_value >= max_position:
            return max_position
        elif max_position >= current_value >= min_position:
            # positive position; valid index
            return current_value
        elif abs(current_value) <= (max_position + 1):
            # negative position; valid index
            # Add 1 to max_position to make this behave like a negative lists index.
            # -1 means the last position, not the last position minus 1
            return max_position + 1 + current_value
        # negative position; invalid index
        raise IndexError(self.name + " index out of bound")


def get_values(model_instance, cache_name, values=None):
    if values is None:
        return getattr(model_instance, cache_name)
    else:
        return values   # not safe from people sending in wrong stuff


# TODO: look for a way to have only a single add_signals.... check if it can look inside class._meta to deside signals to add from that
# Best would be to get it inside the function...

def add_signals_for_proxy(class_with_function, sender_class, field_name):
    prefix = ".".join([sender_class._meta.label_lower, field_name])
    post_delete.connect(class_with_function._meta.get_field(field_name).update_on_delete,
                        sender=sender_class,
                        dispatch_uid=".".join([prefix, "post_delete"]))
    add_signals(class_with_function, sender_class, field_name)

def add_signals(class_with_function, sender_class, field_name):
    prefix = ".".join([sender_class._meta.label_lower, field_name])
    pre_save.connect(class_with_function._meta.get_field(field_name).update_pre_save,
                     sender=sender_class,
                     dispatch_uid=".".join([prefix, "pre_save"]))
    post_save.connect(class_with_function._meta.get_field(field_name).update_on_save,
                      sender=sender_class,
                      dispatch_uid=".".join([prefix, "post_save"]))
