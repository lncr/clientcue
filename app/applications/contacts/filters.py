from django_filters import rest_framework as filters

from applications.contacts.models import Contact


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ContactsFilterSet(filters.FilterSet):

    tags = NumberInFilter(field_name='tags', method='tags_filter')

    class Meta:
        model = Contact
        fields = ['tags', 'created_at', ]

    def tags_filter(self, queryset, name, value):
        return queryset.filter(tags__in=value).distinct()
