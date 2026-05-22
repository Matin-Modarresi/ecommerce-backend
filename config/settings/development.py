from .base import *
from .components.database import *
from .components.logging import *
from .components.celery import *
import environ

env = environ.Env()

DEBUG = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
