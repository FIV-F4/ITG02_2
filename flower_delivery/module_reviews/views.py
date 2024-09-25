"""
Путь: module_reviews/views.py
Представления для управления отзывами о продуктах.
"""

from django.shortcuts import render, get_object_or_404, redirect
from module_catalog.models import Products
from .forms import ReviewForm

def product_reviews(request, product_id):
    """
    Отображает отзывы для указанного продукта и позволяет оставить новый отзыв.
    """
    product = get_object_or_404(Products, id=product_id)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_reviews', product_id=product_id)
    else:
        form = ReviewForm()

    return render(request, 'module_reviews/product_reviews.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })
