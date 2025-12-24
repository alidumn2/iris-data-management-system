from rest_framework import serializers
from .models import Iris

class IrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iris
        fields = '__all__' # Tüm sütunları (sepal, petal, species) JSON'a çevirir