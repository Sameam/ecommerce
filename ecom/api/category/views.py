from rest_framework import viewsets
from .serialize import CategorySerializer
from .models import Category


# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
  # write a query and django will work on the sql query by itself 
  queryset = Category.objects.all().order_by('name')
  # make it into json format
  serializer_class = CategorySerializer
  
  
  