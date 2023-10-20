import uuid
from crum import get_current_user
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .managers import CustomUserManager

class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_by = models.CharField(max_length=100, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:
                self.created_by = user.username
            else:
                self.update_by = user.username
        except:
            pass

        models.Model.save(self)

    class Meta:
        abstract = True

class ModelBaseAudited(models.Model):
    institution_id = models.IntegerField(verbose_name="Institución Code", blank=True, null=True, editable=False)
    detail = models.CharField(max_length=1024, verbose_name="Detalle", blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    deleted_reason = models.CharField(max_length=191, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:
                self.created_by = user.username
            else:
                self.update_by = user.username
        except:
            pass

        models.Model.save(self)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("Usuario"), max_length=191, unique=True)
    first_name = models.CharField(verbose_name=_("Nombres"), max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Apellidos"), max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    foto = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        verbose_name='Archive Photo',
        max_length=1024,
        blank=True, null=True
    )

    # Login con Emaeil:
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    # Login con Emaeil:
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return '{}'.format(self.username)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def get_foto_url(self):
        return self.foto.url
