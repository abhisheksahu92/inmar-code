from django.urls import path, include
from rest_framework_nested import routers
from .views import LocationViewSet, DepartmentViewSet, CategoryViewSet, SubCategoryViewSet,SKUMetaDataView

router = routers.DefaultRouter()
router.register(r'location', LocationViewSet)

locations_router = routers.NestedDefaultRouter(router, r'location', lookup='location')
locations_router.register(r'department', DepartmentViewSet, basename='location-department')

departments_router = routers.NestedDefaultRouter(locations_router, r'department', lookup='department')
departments_router.register(r'category', CategoryViewSet, basename='department-category')

categories_router = routers.NestedDefaultRouter(departments_router, r'category', lookup='category')
categories_router.register(r'subcategory', SubCategoryViewSet, basename='category-subcategory')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(locations_router.urls)),
    path('api/v1/', include(departments_router.urls)),
    path('api/v1/', include(categories_router.urls)),
    path('api/v1/skus_by_metadata/', SKUMetaDataView.as_view(), name='skus_by_metadata'),
]

