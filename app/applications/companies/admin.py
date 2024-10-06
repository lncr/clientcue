from django.contrib import admin
from .models import Review
from applications.companies.models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('industry', 'name', 'id')
    search_fields =('name',)
    list_filter = ['industry', ]

admin.site.register(Company, CompanyAdmin)
admin.site.register(Review)
