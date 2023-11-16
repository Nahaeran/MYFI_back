from django.db import models

# Create your models here.
class Bank(models.Model):
    Bank_code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)


class Deposit(models.Model):
    deposit_code = models.CharField(max_length=20)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    dcls_month = models.CharField(max_length=20)
    join_way = models.CharField(max_length=20)
    mtrt_int = models.TextField(blank=True)
    spcl_cnd = models.TextField(blank=True)
    join_deny = models.IntegerField(blank=True)
    join_member = models.TextField(blank=True)
    etc_note = models.TextField(blank=True)
    max_limit = models.IntegerField()


class Saving(models.Model):
    saving_code = models.CharField(max_length=20)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    dcls_month = models.CharField(max_length=20)
    join_way = models.CharField(max_length=20)
    mtrt_int = models.TextField(blank=True)
    spcl_cnd = models.TextField(blank=True)
    join_deny = models.IntegerField(blank=True)
    join_member = models.TextField(blank=True)
    etc_note = models.TextField(blank=True)
    max_limit = models.IntegerField()


class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=10)
    save_trm = models.CharField(max_length=3)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()




