from .base import *  # noqa

try:
    from .celery import *  # noqa
except ImportError:
    pass  # Celery not installed

try:
    from .local import *  # noqa
except ImportError:
    pass  # Local settings not found
