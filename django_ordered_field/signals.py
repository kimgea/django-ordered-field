from django.db.models.signals import pre_save, post_save, post_delete


def add_signals_save(class_with_function, sender_class, field_name):
    prefix = ".".join([sender_class._meta.label_lower, field_name])
    pre_save.connect(class_with_function._meta.get_field(field_name).pre_save_handler,
                     sender=sender_class,
                     dispatch_uid=".".join([prefix, "pre_save"]))
    post_save.connect(class_with_function._meta.get_field(field_name).post_save_handler,
                      sender=sender_class,
                      dispatch_uid=".".join([prefix, "post_save"]))


def add_signals_full(class_with_function, sender_class, field_name):
    prefix = ".".join([sender_class._meta.label_lower, field_name])
    post_delete.connect(class_with_function._meta.get_field(field_name).post_delete_handler,
                        sender=sender_class,
                        dispatch_uid=".".join([prefix, "post_delete"]))
    add_signals_save(class_with_function, sender_class, field_name)


def add_signals_for_inheritance(class_with_function, sender_class, field_name):
    add_signals_save(class_with_function, sender_class, field_name)


def add_signals_for_proxy(class_with_function, sender_class, field_name):
    add_signals_full(class_with_function, sender_class, field_name)
