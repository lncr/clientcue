from rest_framework import serializers

from applications.contacts.models import Contact



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'owner', 'phone_number', 'name', 'created_at', 'rating', ]
        read_only_fields = ['owner', 'created_at', ]


class FileActionSerializer(serializers.Serializer):

    file = serializers.FileField(use_url=False)
