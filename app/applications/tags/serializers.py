from rest_framework import serializers

from applications.tags.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'owner', 'contacts', 'name', ]
        read_only_fields = ['owner', ]
