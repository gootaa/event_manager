from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    A customized user model to make
    email field required and unique.
    """
    email = models.EmailField(('email address'), unique=True)
