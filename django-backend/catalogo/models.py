from django.db import models
from crum import get_current_user
from seguridad.models import ModelBase, ModelBaseAudited
from seguridad.constants import Gender


class CategoriaCliente(ModelBase):
    codigo = models.CharField(max_length=10, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-created_at']

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if self.codigo:
            self.codigo = self.codigo.upper()

        if self.nombre:
            self.nnombreame = self.nombre.upper()

        ModelBase.save(self)

# Create your models here.
class Cliente(ModelBaseAudited):
    categoria = models.ForeignKey(CategoriaCliente, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Categoría')
    codigo = models.CharField(max_length=15, blank=True, null=True, verbose_name='Código')
    identificacion = models.CharField(max_length=10, verbose_name="C.Identidad", blank=True, null=True, unique=True)
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    detalle = models.CharField(max_length=191, blank=True, null=True, verbose_name="Nombres y apellidos")
    genero = models.CharField(
        verbose_name="Genero",
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=10,
    )
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", blank=True, null=True)
    direccion = models.CharField(max_length=1024, verbose_name="Dirección", blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    email = models.CharField(max_length=150, verbose_name="Email", blank=True, null=True)

    def __str__(self):
        return f"{self.detalle}"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):

        if self.codigo:
            self.codigo = self.codigo.upper()

        if self.nombres:
            self.nombres = self.nombres.upper()

        if self.apellidos:
            self.apellidos = self.apellidos.upper()

        if self.email:
            self.email = self.email.lower()

        self.detalle = f"{self.nombres} {self.apellidos}".strip()

        ModelBaseAudited.save(self)
