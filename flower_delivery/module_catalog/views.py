from django.shortcuts import render,redirect, get_object_or_404
from .models import Products
from django.contrib.auth.decorators import login_required


def catalog(request):
    Productss = Products.objects.all()
    return render(request, 'module_catalog/catalog.html', {'products': Productss})
