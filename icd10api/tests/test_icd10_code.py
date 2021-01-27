# from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from icd10api.models import Category, Code

from icd10api.serializers import CodeSerializer, CategorySerializer
from icd10api.views import CodeViewSet

# CODE_URL = '/v1/code/'
CODE_URL = reverse('v1:code-list')

def sample_category(**params):
    """
    Create and return a sample category
    """
    defaults = {
        'short_code': "A000",
        'title': "Test Category",
    }
    defaults.update(params)
    return Category.objects.create(**defaults)

def sample_code(category, **params):
    """
    Create and return a sample icd10 code
    """
    # category = sample_category()
    defaults = {
        'category': category,
        'diagnosis_code': 'ABCD',
        'short_description': 'This is a short description',
        'full_description': 'This is a longer fuller more expansive verbose description. -vvv',
    }
    defaults.update(params)
    return Code.objects.create(**defaults)

class CodeApiTests(APITestCase):
    """
    Test icd10 code API functions for basic CRUD operations
    """

    def setUp(self):
        self.client = APIClient()    

    def test_create_code(self):
        """
        Test creating icd10 code record entries with POST
        """
        req_category = sample_category()
        # factory = APIRequestFactory()
        payload = {
            'category': req_category.id,
            'diagnosis_code': 'ABCD',
            'short_description': 'This is a short description',
            'full_description': 'This is a longer fuller more expansive verbose description. -vvv',
        }
        res = self.client.post(CODE_URL, payload)
        # could also use factory
        # request = factory.post(CODE_URL, payload)
        # res = view(request)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        code = Code.objects.get(category_id=res.data['category'], diagnosis_code=res.data['diagnosis_code'])
        res_category = code.category

        # check if returned category values match payload category
        self.assertEqual(req_category.id, res_category.id)

    def test_retrieve_code(self):
        """
        Test retrieving list of icd10 codes with GET
        """
        category = sample_category()

        sample_code(category)
        sample_code(category, diagnosis_code='EFGH', short_description='Test category B')

        res = self.client.get(CODE_URL)
        codes = Code.objects.all().order_by('-id')
        serializer = CodeSerializer(codes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data.get('results'), serializer.data)

    def test_update_code(self):
        """
        Test updating a code with PATCH
        """
        category = sample_category()
        code = sample_code(category)

        # res = self.client.post(CODE_URL, payload)
        payload = {'diagnosis_code': 'EFGH'}
        url = f'{CODE_URL}{code.id}/'
        self.client.patch(url, payload)
        code.refresh_from_db()
        self.assertEqual(code.diagnosis_code, payload['diagnosis_code'])

    def test_delete_code(self):
        """
        Test creating icd10 code records with DELETE
        """
        category = sample_category()
        code = sample_code(category)
        # similar to update we fetch the record, then issue delete
        url = f'{CODE_URL}{code.id}/'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

# we could do further checks for idempotency of the requests but django rest framework has got that covered