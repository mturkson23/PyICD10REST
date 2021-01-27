from icd10api.models import Code, Category
from rest_framework import serializers

class CodeSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        queryset= Category.objects.all(),
        slug_field='id'
    )    
    class Meta:
        model = Code
        fields = ['category', 'diagnosis_code', 'short_description', 'full_description']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['short_code', 'title']
