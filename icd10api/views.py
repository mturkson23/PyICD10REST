# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.versioning import NamespaceVersioning

from icd10api.models import Code, Category
from icd10api.serializers import CategorySerializer, CodeSerializer
# Create your views here.

class CodeVersioning(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class CodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ICD10 codes to be viewed or edited
    """
    versioning_class = CodeVersioning
    queryset = Code.objects.all().order_by('-id')
    serializer_class = CodeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ICD10 categories to be viewed or edited
    """
    versioning_class = CodeVersioning
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]



