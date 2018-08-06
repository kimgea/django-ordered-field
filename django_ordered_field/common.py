from django.utils.timezone import now


def get_values(model_instance, cache_name, values=None):
    if values is None:
        return getattr(model_instance, cache_name)
    else:
        return values


def generate_parent_link_name(model_instance):
    # Potential problem if Django changes its name generation
    return model_instance.__class__.__name__.lower() + "_ptr"


def extra_updates(updates, extra):
    for field_name, new_data in extra.items():
        if callable(new_data):
            updates[field_name] = new_data()
        else:
            updates[field_name] = new_data


def auto_now_field_update(model_instance, updates):
    date_now = now()
    for field in model_instance._meta.get_fields():
        if getattr(field, 'auto_now', False):
            updates[field.name] = date_now


def position_boundary_checks(current_value, max_position):
    if current_value >= max_position:
        return max_position
    elif max_position >= current_value >= 0:
        # positive position; valid index
        return current_value
    elif abs(current_value) <= (max_position + 1):
        # negative position; valid index
        # Add 1 to max_position to make this behave like a negative lists index.
        # -1 means the last position, not the last position minus 1
        return max_position + 1 + current_value
    # negative position; invalid index
    raise IndexError("Index out of bound")


def get_cleaned_current_and_updated_values(
        add, model_instance, cache_name, values=None):

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


def order_is_not_changed(current_value, updated_value):
    return current_value == updated_value or updated_value is None


def should_instance_be_updated(instance):
    # Do not update extra fields on self if self is new
    return instance.pk is None or instance._state.adding
