from rest_framework import viewsets
from .models import Location, Department, Category, SubCategory, MetaData, SKU
from .serializers import (
    LocationSerializer, DepartmentSerializer, CategorySerializer, SubCategorySerializer,
    MetaDataSerializer, SKUSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import viewsets
from .models import Location, Department, Category, SubCategory, MetaData
from .serializers import (
    LocationSerializer,
    DepartmentSerializer,
    CategorySerializer,
    SubCategorySerializer,
    MetaDataSerializer
)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        location_id = self.kwargs['location_pk']
        department_ids = MetaData.objects.filter(location_id=location_id).values_list('department_id', flat=True).distinct()
        return Department.objects.filter(id__in=department_ids)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        location_id = self.kwargs['location_pk']
        department_id = self.kwargs['department_pk']
        category_ids = MetaData.objects.filter(location_id=location_id, department_id=department_id).values_list('category_id',
                                                                                      flat=True).distinct()
        return Category.objects.filter(id__in=category_ids)

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        location_id = self.kwargs['location_pk']
        department_id = self.kwargs['department_pk']
        category_id = self.kwargs['category_pk']
        subcategory_id = MetaData.objects.filter(location_id=location_id, department_id=department_id, category_id=category_id).values_list(
            'subcategory_id',
            flat=True).distinct()
        return SubCategory.objects.filter(id__in=subcategory_id)

class MetaDataViewSet(viewsets.ModelViewSet):
    serializer_class = MetaDataSerializer

    def get_queryset(self):
        location_id = self.kwargs['location_pk']
        department_id = self.kwargs['department_pk']
        category_id = self.kwargs['category_pk']
        subcategory_id = self.kwargs['subcategory_pk']
        return MetaData.objects.filter(
            location_id=location_id,
            department_id=department_id,
            category_id=category_id,
            subcategory_id=subcategory_id
        )

class SKUMetaDataView(APIView):
    def get(self, request):
        location = request.query_params.get('location')
        department = request.query_params.get('department')
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')

        if not all([location, department, category, subcategory]):
            return Response(
                {"detail": "location, department, category, and subcategory are required parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            metadata = MetaData.objects.get(
                location__name=location,
                department__name=department,
                category__name=category,
                subcategory__name=subcategory
            )
        except MetaData.DoesNotExist:
            return Response(
                {"detail": "No metadata found for the given parameters."},
                status=status.HTTP_404_NOT_FOUND
            )

        skus = SKU.objects.filter(metadata=metadata)
        serializer = SKUSerializer(skus, many=True)
        return Response(serializer.data)
