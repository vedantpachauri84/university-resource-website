from rest_framework import serializers
from .models import Notes
class personmodelserializwers(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=('title','Subject','file')