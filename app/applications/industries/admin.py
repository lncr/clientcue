from django.contrib import admin

from applications.industries.models import Industry


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields =('title',)
    list_filter = ['title', ]


admin.site.register(Industry, IndustryAdmin)
