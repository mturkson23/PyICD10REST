# from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from icd10api.models import Category, Code

from icd10api.serializers import CodeSerializer, CategorySerializer

CATEGORY_URL = reverse('v1:category-list')

def sample_category(**params):
    """
    Create and return a sample category
    """
    defaults = {
        'short_code': "A00",
        'title': "Test Category",
    }
    defaults.update(params)
    return Category.objects.create(**defaults)

class CategoryApiTests(APITestCase):
    """
    Test category API functions for basic CRUD operations
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        """
        Test creating category records with POST
        """
        payload = {
            'short_code': 'A0000',
            'title': 'Test Category',
        }
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(short_code=res.data['short_code'])

        # check if returned values match payload
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(category, key))

    def test_retrieve_categories(self):
        """
        Test retrieving list of categories with GET
        """
        sample_category(short_code='A000', title='Test category A')
        sample_category(short_code='B000', title='Test category B')

        res = self.client.get(CATEGORY_URL)

        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data.get('results'), serializer.data)

    def test_update_category(self):
        """
        Test updating a category with PATCH
        """
        category = sample_category(short_code='A000', title='Test category A')

        payload = {'title': 'TEST CATEGORY A'}
        url = f'{CATEGORY_URL}{category.id}/'
        self.client.patch(url, payload)

        category.refresh_from_db()
        self.assertEqual(category.title, payload['title'])

    def test_delete_category(self):
        """
        Test creating category records with DELETE
        """
        category = sample_category(short_code='A000', title='Test category A')
        # similar to update we fetch the record, then issue delete
        url = f'{CATEGORY_URL}{category.id}/'
        res = self.client.delete(url)
        # target_category = Category.objects.get(short_code="A000")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

# we could do further checks for idempotency of the requests but django rest framework has got that covered