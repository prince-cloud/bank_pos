from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
import datetime
from . import models
from . import forms
# Create your views here.

def index(request):
    return render(request, 'index.html')

def pos_index(request):
    return render (request, 'pos/index.html', 
    {
            'supply_form': forms.SupplyForm(),
            'product_form': forms.ProductForm(),
            'expense_form': forms.ExpenseForm(),
    })

@login_required
def products_list(request):
    
    products_list = models.Product.objects.all()
    
    search_query = request.GET.get('q')
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains = search_query) |
            Q(description__icontains = search_query) 
        )
    #items = models.Product.objects.all()

    return render(
        request,
        'pos/products_list.html',
        {
            'products': products_list,
            'purchase_form': forms.PurchaseForm(),
        }
    )

@login_required
def add_purchase(request):
    if request.method == 'POST':
        form = forms.PurchaseForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Item successfuly purchased")
            return redirect('pos:products_list')
        else:
            messages.warning(request, "Error. Transaction Faield")
    else:
        form = forms.PurchaseForm()

    return redirect('pos:products_list')


@login_required
def add_supply(request):
    if request.method == "POST":
        form = forms.SupplyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supply added Successfully")
            redirect_url = request.GET.get("next")
            if redirect_url is not None:
                redirect(redirect_url)
        else:
            messages.warning(request, "There was an error in the data entered")

    return redirect('pos:products_list')


@login_required
def add_product(request):
    if request.method == "POST":
        form = forms.ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Successfully added")
            redirect_url = request.GET.get("next")
            if redirect_url is not None:
                redirect(redirect_url)
    return redirect('pos:products_list')

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = forms.ExpenseForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Expense Successfully added')
            #if redirect_url is not None:
                #redirect(redirect_url)
    return redirect('pos:add_expense')

@login_required
def history(request):
    return render(request, "pos/history.html")


@login_required
def supply_history(request):
    supplies = models.Supply.objects.all()
    return render(request, 'pos/supply_history.html',
    {
        'supplies': supplies,
    })


@login_required
def sales_expenses(request, year=None, month=None, day=None, item=None):
    if year and month and day:
        purchases = models.Purchase.objects.filter(date_created__year=year, date_created__month=month, date_created__day=day)
        expenses = models.Expense.objects.filter(date__year=year, date__month=month, date__day=day)
    elif year and month:
        purchases = models.Purchase.objects.filter(date_created__year=year, date_created__month=month)
        expenses = models.Expense.objects.filter(date__year=year, date__month=month)
    elif year:
        purchases = models.Purchase.objects.filter(date_created__year=year)
        expenses = models.Expense.objects.filter(date__year=year)
    else:
        purchases = models.Purchase.objects.all()
        expenses = models.Expense.objects.all()

    total_purchases = 0
    total_expenses = 0
    for i in purchases:
        total_purchases += i.price
    for x in expenses:
        total_expenses += x.amount
    
    net_total = total_purchases - total_expenses

    if item:
        itempurchases = purchases.objects.filter(product=item)

    return render(
        request, 
        'pos/purchase_history.html', 
        {
            'purchases': purchases,
            'expenses': expenses,
            'year': year,
            'month': month,
            'day': day,
            'total_purchases': total_purchases,
            'total_expenses': total_expenses,
            'net_total': net_total,
            'item': item,
        }
    )

@login_required
def statistics(request):
    products = models.Product.objects.filter(available_quantity=0)
    return render(request, "pos/statistics.html", {
        "products": products,
    })