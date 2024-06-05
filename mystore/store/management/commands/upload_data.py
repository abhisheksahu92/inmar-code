import csv
from django.core.management.base import BaseCommand
from store.models import MetaData, SKU,Location,Category,SubCategory,Department
from django.shortcuts import get_object_or_404
from django.conf import settings
import os,pandas as pd
class Command(BaseCommand):
    help = 'Upload metadata and SKU data from CSV files'

    def handle(self, *args, **kwargs):
        Location.objects.all().delete()
        Department.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        MetaData.objects.all().delete()
        SKU.objects.all().delete()
        location = settings.BASE_DIR
        metadata_file = os.path.join(location,'store','management','commands','metadata.csv')
        sku_file = os.path.join(location,'store','management','commands','skudata.csv')

        if metadata_file:
            self.upload_metadata(metadata_file)

        if sku_file:
            self.upload_skus(sku_file)

    def upload_metadata(self, filepath):
        df = pd.read_csv(filepath)
        for row in df.to_dict('records'):
            location, _ = Location.objects.get_or_create(name=row['Location'])
            department, _ = Department.objects.get_or_create(name=row['Department'])
            category, _ = Category.objects.get_or_create(name=row['Category'])
            subcategory, _ = SubCategory.objects.get_or_create(name=row['SubCategory'])

            MetaData.objects.get_or_create(
                location=location,
                department=department,
                category=category,
                subcategory=subcategory
            )
        self.stdout.write(self.style.SUCCESS('Successfully uploaded metadata'))

    def upload_skus(self, filepath):
        df = pd.read_csv(filepath)
        df['LOCATION'] = df['LOCATION'].str.strip()
        df['DEPARTMENT'] = df['DEPARTMENT'].str.strip()
        df['CATEGORY'] = df['CATEGORY'].str.strip()
        df['SUBCATEGORY'] = df['SUBCATEGORY'].str.strip()
        for row in df.to_dict('records'):
            try:
                location, _ = Location.objects.get_or_create(name=row['LOCATION'])
                department, _ = Department.objects.get_or_create(name=row['DEPARTMENT'])
                category, _ = Category.objects.get_or_create(name=row['CATEGORY'])
                subcategory, _ = SubCategory.objects.get_or_create(name=row['SUBCATEGORY'])
                metadata,_ = MetaData.objects.get_or_create(
                    location=location,
                    department=department,
                    category=category,
                    subcategory=subcategory
                )

                SKU.objects.create(
                    sku=row['SKU'],
                    name=row['NAME'],
                    metadata=metadata
                )
            except Exception as e:
                print(row)
                continue
        self.stdout.write(self.style.SUCCESS('Successfully uploaded SKU data'))
