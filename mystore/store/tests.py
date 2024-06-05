from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Location, Department, Category, SubCategory, MetaData, SKU

class MetaDataAPITests(APITestCase):
    def setUp(self):
        # Create some initial data for the tests
        self.location = Location.objects.create(name="Perimeter")
        self.department = Department.objects.create(name="Bakery")
        self.category = Category.objects.create(name="Bakery Bread")
        self.subcategory = SubCategory.objects.create(name="Bagels")

        self.metadata = MetaData.objects.create(
            location=self.location,
            department=self.department,
            category=self.category,
            subcategory=self.subcategory
        )

        self.sku1 = SKU.objects.create(sku=1, name="SKUDESC1", metadata=self.metadata)
        self.sku2 = SKU.objects.create(sku=14, name="SKUDESC14", metadata=self.metadata)

    def test_get_locations(self):
        url = reverse('location-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Perimeter')

    def test_get_departments_for_location(self):
        url = reverse('location-department-list', args=[self.location.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Bakery')

    def test_get_categories_for_department(self):
        url = reverse('department-category-list', args=[self.location.id, self.department.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Bakery Bread')

    def test_get_subcategories_for_category(self):
        url = reverse('category-subcategory-list', args=[self.location.id, self.department.id, self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Bagels')

    def test_get_skus_by_metadata(self):
        url = reverse('skus_by_metadata')
        response = self.client.get(url, {
            'location': 'Perimeter',
            'department': 'Bakery',
            'category': 'Bakery Bread',
            'subcategory': 'Bagels'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['sku'], 1)
        self.assertEqual(response.data[1]['sku'], 14)
