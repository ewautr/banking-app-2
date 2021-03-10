from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(null=True, max_length=200)
    
    class Rank(models.TextChoices):
        BASIC = 'Basic'
        SILVER = 'Silver'
        GOLD = 'Gold'

    rank = models.CharField(choices=Rank.choices, default=Rank.BASIC, max_length=200)

    def __str__(self):
        return f"{self.user} - {self.phone} - {self.rank}"

    @property
    def can_make_loan(self):
        if self.rank == 'Basic':
            return False
        else:
            return True


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class AccountType(models.TextChoices):
        BANK_ACCOUNT = 'Bank Account'
        LOAN = 'Loan'

    account_type = models.CharField(choices=AccountType.choices, default=AccountType.BANK_ACCOUNT, max_length=200)

    def __str__(self): 
        return f"{self.customer} - {self.account_type}"

    # @property
    # def balance(self):
    #     minusAmount = Ledger.objects.filter(fromAccount=self.pk).aggregate(Sum('amount'))
    #     plusAmount = Ledger.objects.filter(toAccount=self.pk).aggregate(Sum('amount'))
    #     finalBalance = plusAmount - minusAmount
    #     return finalBalance

class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="fromAccount")
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    text = models.CharField(null=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)

# every transaction is 2 rows

    def __str__(self):
        return f"{self.fromAccount} - {self.toAccount} - {self.account} - {self.text} - {self.timestamp} - {self.transaction_id}"

    @classmethod
    def transaction(cls, amount, debit_account, credit_account, text):
        # make uuid, make 2 leger instances with the same uuid, on one on the amount on one of the minus amount, handle as a transaction (atomic)
        pass