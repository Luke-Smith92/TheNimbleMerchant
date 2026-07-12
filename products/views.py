from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def all_products(request):
    """Show all products."""
    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Show individual product details."""
    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)


@staff_member_required
def add_product(request):
    """Allow staff members to add a new product."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()
            return redirect("product_detail", product_id=product.id)
    else:
        form = ProductForm()

    context = {
        "form": form,
        "page_title": "Add Product",
        "button_text": "Add Product",
    }

    return render(request, "products/product_form.html", context)


@staff_member_required
def edit_product(request, product_id):
    """Allow staff members to edit an existing product."""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():
            product = form.save()
            return redirect("product_detail", product_id=product.id)
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "product": product,
        "page_title": "Edit Product",
        "button_text": "Save Changes",
    }

    return render(request, "products/product_form.html", context)


@staff_member_required
def delete_product(request, product_id):
    """Allow staff members to delete an existing product."""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.delete()
        return redirect("products")

    context = {
        "product": product,
    }

    return render(
        request,
        "products/delete_product.html",
        context,
    )