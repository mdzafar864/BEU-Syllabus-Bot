from .base_handlers import register_base_handlers
from .syllabus_handlers import register_syllabus_handlers
from .admin_handlers import register_admin_handlers
from .callbacks import register_callback_handlers

__all__ = [
    'register_base_handlers',
    'register_syllabus_handlers',
    'register_admin_handlers',
    'register_callback_handlers'
]