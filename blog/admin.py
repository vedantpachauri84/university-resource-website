from django.contrib import admin
from .models import Paper, Notes, Resources, Contact,Blog

# Register your models here.
admin.site.register(Paper)
admin.site.register(Notes)
admin.site.register(Resources)
admin.site.register(Contact)
admin.site.register(Blog)