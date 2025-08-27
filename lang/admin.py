from django.contrib import admin
from .models import Lang
# Register your models here.
class LangAdmin(admin.ModelAdmin):
    list_display = ('language', 'updated_at')
    search_fields = ('language',)

admin.site.register(Lang, LangAdmin)