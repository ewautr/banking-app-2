from django.shortcuts import render, get_object_or_404, redirect
from .models import Ledger, Customer, Account
from django.db.models import Q
from django.contrib.auth.models import User

# Customer view
def index(request):
    customer = get_object_or_404(Customer, user=request.user)
    accounts = Account.objects.filter(customer=customer.pk)
    context = {
        'customer': customer,
        'accounts': accounts
     }
    return render(request, 'banking_app/index.html', context)

# Customer view - account activity
def activity(request, account_id):
    activities = Ledger.objects.filter(account=account_id)
    context = {
        'activities': activities,
    }
    return render(request, 'banking_app/activity.html', context)

# Customer view - transfering money
def transfers(request, account_id):
    currentAccount = get_object_or_404(Account, pk=account_id)
    allAccounts = Account.objects.exclude(pk=account_id)
    context = {
        'currentAccount': currentAccount,
        'allAccounts': allAccounts
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        debit_account = request.POST['fromAccount']
        credit_account = request.POST['toAccount']
        text = request.POST['text']

        Ledger.transaction(int(amount), debit_account, credit_account, text)

        return redirect('banking_app:index')
    return render(request, 'banking_app/transfers.html', context)

# Employee view
def employee(request):
    customers = Customer.objects.all()
    accounts = Account.objects.all()
    context = {'customers': customers, 'accounts': accounts}

    return render(request, 'banking_app/employee.html', context)

# Employee view - adding a new customer
def add_customer(request): 
    context = {}

    if request.method == 'POST':
        user_name = request.POST['user_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        rank = request.POST['rank']

        if password != confirmPassword:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }
            return render(request, 'banking_app/add_customer.html', context)

        new_user = User.objects.create_user(user_name, email, password)

        customer = Customer()
        customer.user = new_user
        customer.phone = phone
        customer.rank = rank
        customer.save()

    return render(request, 'banking_app/add_customer.html', context)

# Employee view - editing a customer
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    context = { 'customer': customer }

    if request.method == 'POST':
        user = customer.user
        user.user_name = request.POST['user_name']
        customer.phone = request.POST['phone']
        customer.rank = request.POST['rank']
        customer.save()
        user.save()
        return redirect('banking_app:employee')

    return render(request, 'banking_app/edit_customer.html', context)

# Employee view - adding a new account
def add_account(request):
    customers = Customer.objects.all()
    context = {'customers': customers}

    if request.method == 'POST':
        customerPK = request.POST['customer']
        account_type = request.POST['account_type']
        customer = get_object_or_404(Customer, pk=customerPK)

        account = Account()
        account.customer = customer
        account.account_type = account_type
        account.save()

        return redirect('banking_app:employee')

    return render(request, 'banking_app/add_account.html', context)