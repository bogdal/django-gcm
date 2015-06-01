from django.utils.module_loading import import_module


def load_object(object_path):

    module_path, object_name = object_path.rsplit('.', 1)
    module = import_module(module_path)

    return getattr(module, object_name)
