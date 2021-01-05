from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from django.db.models import Q 
from . import forms
# Create your views here.
from django.shortcuts import redirect, get_object_or_404
import random
from django.conf import settings

@login_required
def bank_index(request):
    total_balance = 0
    num=0
    customers = User.objects.all()
    #customers = models.Profile.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        customers = customers.filter(
            Q(profile__account_number = search_query))
    
    for customer in customers:
        if hasattr(customer, "profile"):
            num += 1
            total_balance += customer.profile.account_balance

    #for customer in customers:
    #    total_balance += customer.account_balance

    return render(request, "bank/index.html",
        {
            "customers": customers,
            "search_query": search_query,
            "total_balance":  "{:.2f}".format(total_balance),
            "num": num,
        }
    )

## adding a new user
def register(request):
    if request.method == 'POST':
        user_form = forms.RegisterForm(data=request.POST, files=request.FILES)
        profile_form = forms.ProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            rand = random.randint(1,100000)
            user = user_form.save(commit=False)
            user_profile = profile_form.save(commit=False)
            if user_profile.phone_number:
                user.username = user_profile.phone_number + str(rand)
            else:
                user.username = str(rand)

            user.save()

            user_profile.user = user
            user_profile.account_number = str(settings.ACCOUNT_NUMBER_START_FROM + user.id)
            user_profile.save()

            messages.success(request, f"Account Succesfully Created with an account number '{user_profile.account_number}'. ")
            return redirect("/bank/index")
        else:
            messages.warning(request, "invalid data entry. plase check and try again")
    else:
        user_form = forms.RegisterForm()
        profile_form = forms.ProfileForm()
    
    return render(request, "registration/register.html",{
        "user_form": user_form,
        "profile_form": profile_form,
    })

@login_required
def deposite(request, pk:int):
    user = get_object_or_404(models.User, pk=pk)

    if request.method == 'POST':
        form = forms.DepositeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            deposite = form.save(commit=False)
            deposite.user = user
            deposite.save()
            messages.success(request, f"Succesfully deposited GH₵{deposite.amount} to {user.profile.account_number}.  Current balance GH₵{deposite.user.profile.account_balance} ")
            return redirect('/bank/index')
        else:
            messages.warning(request, "Deposite Error. Not Successful")
    else:
        form = forms.DepositeForm()
    
    return render(request, "bank/deposite.html", {"form":form, "user": user,})



@login_required
def withdrawal(request, pk:int):
    user = get_object_or_404(models.User, pk=pk)

    if request.method == 'POST':
        form = forms.WithdrawalForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            if user.profile.account_balance >= withdrawal.amount:
                withdrawal.user = user
                withdrawal.save()
                messages.success(request, f"Succesfully withdrawn GH₵{withdrawal.amount} from {user.profile.account_number}. Current balance GH₵{withdrawal.user.profile.account_balance}  ")
                return redirect("/bank/index")
            else:
                messages.warning(request, f"Not Enough Funds")
        else:
            messages.warning(request, "withdrawal Error. Not Successful")
    else:
        form = forms.WithdrawalForm()
    
    return render(request, "bank/withdrawal.html", {"form":form, "user": user,})

@login_required
def profile(request, pk:int):
    profile = get_object_or_404(models.Profile, user_id=pk)
    return render(request, "bank/profile.html",{"profile":profile,})

@login_required
def transactions(request, pk:int, year=None, month=None, day=None):
    user = get_object_or_404(models.User, pk=pk)

    if year and month and day:
        deposites = models.Deposite.objects.filter(date_created__year=year, date_created__month=month, date_created__day=day, user=user)
        withdrawals = models.Withdrawal.objects.filter(date_created__year=year, date_created__month=month, date_created__day=day, user=user)
    elif year and month:
        deposites = models.Deposite.objects.filter(date_created__year=year, date_created__month=month, user=user)
        withdrawals = models.Withdrawal.objects.filter(date_created__year=year, date_created__month=month, user=user)
    elif year:
        deposites = models.Deposite.objects.filter( user=user, date_created__year=year)
        withdrawals = models.Withdrawal.objects.filter(user=user, date_created__year=year)
    else:
        deposites = models.Deposite.objects.filter(user=user)
        withdrawals = models.Withdrawal.objects.filter(user=user)
    return render(request, "bank/transactions.html",
        {   "deposites":deposites,
            "withdrawals":withdrawals,
            "year": year,
            "month": month,
            "day": day,
            "user": user,
        }
    )

def edit_profile(request, pk:int):
    user = get_object_or_404(models.User, pk=pk)
    profile = get_object_or_404(models.Profile, user=user)
    if request.method == 'POST':
        user_form = forms.RegisterForm(data=request.POST, files=request.FILES, instance=user)
        profile_form = forms.ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile successfully updated")
            return redirect(user.profile.get_absolute_url())
        else:
            messages.warning(request, "Error.please check and try again.")
    else:
        user_form = forms.RegisterForm(instance=user)
        profile_form = forms.ProfileForm(instance=profile)
    
    return render(request, "bank/edit_profile.html", {"user_form": user_form, "profile_form": profile_form})


def delete_account(request, pk:int):
    user = get_object_or_404(models.User, pk=pk)
    user.delete()
    user.save()
    messages.success(request, "Account Deleted successfully")
    return redirect("/")