from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, Basket, Customer, Address, Order
from django.contrib.auth.models import User
from store.forms import OrderAddressForm




def home(request):
    user = request.user
    products = Product.objects.all()

    latest = []
    most_popular = []
    just_for_you = []

    for product in products:
        latest.append(product)
        if product.times_ordered > 0:
            most_popular.append(product)
    latest.reverse()
    latest = latest[0:10]
    most_popular = most_popular[0:5]
    
    if user.is_authenticated:
        try:
            customer = Customer.objects.get(name=user)
        except Customer.DoesNotExist:
            Customer.objects.create(name=user, total_items=0)
            context = {
                "most_popluar": most_popular,
                "latest": latest,
            }
            return render(request, "store/home.html", context)
        else:
            customer = get_object_or_404(Customer, name=user)
            basket = customer.basket_set.filter(open_basket=True)
            totalItems = 0
        
            for product in basket:
                totalItems += product.quantity
                sub = product.product.sub_category
                filter_by_sub = Product.objects.filter(sub_category=sub)
                for item in filter_by_sub:
                    if item.id != product.product.id:
                        just_for_you.append(item)
            customer.total_items = totalItems
            customer.save()
            context = {
                    "most_popluar": most_popular,
                    "latest": latest,
                    "just_for_you": just_for_you
                }
        return render(request, "store/home.html", context)
    else:
        context = {
                    "most_popluar": most_popular,
                    "latest": latest,
                }
    return render(request, "store/home.html", context)


def side_categories(request):
    # context_processor  for base.html side categories
    products = Product.objects.all()
    categories = {}
    new_products = {}

    for product in products:
        categories.setdefault(product.category, product.id)
        new_products.setdefault(product.sub_category, product)
    context = {
        "categories": categories,
        "new_products": new_products
    }
    return  context


def category(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category = product.category
    products = Product.objects.filter(category=category)
    context = {
        "category": category,
        "products": products
    }
    return  render(request, "store/category.html", context)


def sub_category(request, pk):
    sub_category = get_object_or_404(Product, pk=pk).sub_category
    products = Product.objects.filter(sub_category=sub_category)
    context = {
        "sub_category": sub_category,
        "products": products,
    }
    return render(request, "store/sub_category.html", context)


def shop_by_brand(request):
    products = Product.objects.all()
    brands = {}
    for product in products:
        brands.setdefault(product.company, product)
    return render(request, "store/shop_by_brand.html", {"brands": brands})


def brand_name(request, pk):
    product = get_object_or_404(Product, pk=pk)
    brand_name = product.company
    products = Product.objects.filter(company=brand_name)
    return render(request, "store/brand_name.html", {"products": products, "brand_name": brand_name})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


@login_required
def add_to_basket(request, pk):
    user = request.user
    customer = Customer.objects.get(name=user)
    product = Product.objects.get(pk=pk)
    baskets = customer.basket_set.filter(open_basket=True)
    counter = 0
    for basket in baskets:
        if basket.product.product_name == product.product_name:
            counter += 1
            basket.quantity += 1
            customer.total_items +=1
            product.times_ordered +=1
            basket.save()
            product.save()
            customer.save()
    if counter == 0:
        Basket.objects.create(customer=customer, product=product, quantity=1)
        customer.total_items +=1
        product.times_ordered +=1
        product.save()
        customer.save()
    return redirect("store:home")


@login_required
def my_basket(request, pk):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    baskets = customer.basket_set.filter(open_basket=True)
    total_amount_due = 0
    for basket in baskets:
        total_amount_due += basket.quantity * basket.product.price
    context = {
        "total_amount_due": total_amount_due,
        "baskets": baskets
    }
    return render(request, "store/my_basket.html", context)


@login_required
def add_item(request, pk):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    basket = customer.basket_set.get(pk=pk)
    product = Product.objects.get(pk=basket.product.id)
    product.times_ordered += 1
    basket.quantity += 1
    basket.save()
    product.save()
    return redirect("store:my_basket", pk=user.pk)


@login_required
def delete_item(request, pk):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    basket = customer.basket_set.get(pk=pk)
    product = Product.objects.get(pk=basket.product.id)
    product.times_ordered -= 1
    product.save()
    if basket.quantity == 1:
        basket.delete()
    else:
        basket.quantity -= 1
        basket.save()
    return redirect("store:my_basket", pk=user.pk)


@login_required
def shipping_address(request):
    user = request.user
    if request.method == "POST":
        form = OrderAddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            customer = Customer.objects.get(name=user)
            address.customer = customer
            address.save()
            # create order
            baskets = customer.basket_set.filter(open_basket=True)
            for basket in baskets:
                Order.objects.create(customer=customer, basket=basket)
                basket.open_basket = False # set open baskets to False
                basket.save()
            orders = customer.order_set.filter(open_order=True)
            total_amount_due = 0
            total_items = 0
            for order in orders:
                total_items += order.basket.quantity
                total_amount_due += order.basket.quantity * order.basket.product.price
            context = {
                "orders": orders,
                "total_items": total_items,
                "total_amount_due": total_amount_due
            }
            return render(request, "store/payment.html", context)
    else:
        address = Address.objects.filter(customer__name=user).first()
        form = OrderAddressForm(instance=address)
        customer = get_object_or_404(Customer, name=user)
        baskets = customer.basket_set.filter(open_basket=True)
        if not baskets:
            return redirect("store:home")
        else:
            return render(request, "store/shipping_address.html", {"form": form})


@login_required
def payment(request):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    orders = customer.order_set.filter(open_order=True)
    total_amount_due = 0
    total_items = 0
    for order in orders:
        total_items += order.basket.quantity
        total_amount_due += order.basket.quantity * order.basket.product.price
    context = {
        "orders": orders,
        "total_items": total_items,
        "total_amount_due": total_amount_due
    }
    return render(request, "store/payment.html", context)



def update_basket(request):
    user = request.user
    if user.is_authenticated:
        customer = get_object_or_404(Customer, name=user)
        baskets = customer.basket_set.filter(open_basket=True)
        total_amount_due = 0
        totalItems = 0
        for basket in baskets:
            total_amount_due += basket.quantity * basket.product.price
            totalItems += basket.quantity
        user.customer.total_items = totalItems
        context = {
            "total_amount_due": total_amount_due,
            "baskets": baskets
        }
        return context
    else:
        return {}