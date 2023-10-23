from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CategoriaCliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'identificacion',
        'categoria',
        'detalle',
        'genero',
        'email',
        'status'
    )
    list_per_page = 20
    search_fields = ('codigo','identificacion','email')
    list_filter = (
        'categoria',
        'deleted',
    )
    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(Cliente, ClienteAdmin)
