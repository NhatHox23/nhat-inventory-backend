from django.shortcuts import get_object_or_404


def get_or_none(model, *args, **kwargs):
    """Query get or return None"""
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def get_or_404(model, *args, **kwargs):
    """super().get_object_or_404"""
    return get_object_or_404(klass=model, *args, **kwargs)
