from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_kwargs):
        user = self.model(username=username, **extra_kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, **extra_kwargs):
        extra_kwargs.setdefault("is_superuser", True)
        extra_kwargs.setdefault("is_staff", True)
        extra_kwargs.setdefault("is_active", True)
        return self.create_user(username=username, password=password, **extra_kwargs)
