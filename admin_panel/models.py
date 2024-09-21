from django.db import models
from django.contrib.auth.models import User



# this all are model for customar 



class customar(models.Model):
    REGULAR = 'Regular'
    NON_REGULAR = 'Non-Regular'
    CUSTOMER_TYPE_CHOICES = [
        (REGULAR, 'Regular'),
        (NON_REGULAR, 'Non-Regular'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default=NON_REGULAR,
        blank=False
        
    )
    name = models.CharField(max_length=100 , blank=False)
    address = models.TextField(max_length=1000 , blank=False)
    fhone = models.CharField(max_length=15 , blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
        
    def __str__(self):
        return f"{self.name} ({self.customer_type})"
    

class customar_ditail(models.Model):
    customer = models.ForeignKey(customar, on_delete=models.CASCADE)
    buy_product = models.TextField(max_length=1000)
    given_money =  models.IntegerField()
    get_money = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=100, decimal_places=10 , default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    pay_at = models.DateTimeField(null=True , blank=True)

    def __str__(self):
        return f"{self.customer} - {self.total_amount}"
    

class mounth_name(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"
class total_cost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_mounth = models.ForeignKey(mounth_name, on_delete=models.CASCADE)
    store_rent = models.IntegerField(default=0)
    bill = models.IntegerField(default=0)
    employs_sallary = models.IntegerField(default=0)
    buy_product_list = models.TextField(max_length=10000,blank=True ,null=True)
    by_product_rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    


class owed_detail(models.Model):
    owed_customer = models.ForeignKey(customar, on_delete=models.CASCADE , blank=True)
    owed_money_for_product = models.CharField(max_length=200000)
    given_money = models.IntegerField()
    owed_money = models.IntegerField()
    given_product_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owed_customer} - {self.owed_money}"