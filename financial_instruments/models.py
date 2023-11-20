from django.db import models
from django.conf import settings


class Deposit(models.Model):
    deposit_code = models.CharField(max_length=100) # fin_prdt_cd 
    fin_co_no = models.CharField(max_length=100)
    kor_co_nm = models.CharField(max_length=100)
    name = models.CharField(max_length=100) # fin_prdt_nm
    dcls_month = models.CharField(max_length=20)
    join_way = models.CharField(max_length=100)
    mtrt_int = models.TextField(blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_member = models.TextField(blank=True, null=True)
    etc_note = models.TextField(blank=True, null=True)
    max_limit = models.IntegerField(blank=True, null=True)
    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_deposit')


class Saving(models.Model):
    saving_code = models.CharField(max_length=100) # fin_prdt_cd 
    fin_co_no = models.CharField(max_length=100)
    kor_co_nm = models.CharField(max_length=100)
    name = models.CharField(max_length=100) # fin_prdt_nm
    dcls_month = models.CharField(max_length=20)
    join_way = models.CharField(max_length=100)
    mtrt_int = models.TextField(blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_member = models.TextField(blank=True, null=True)
    etc_note = models.TextField(blank=True, null=True)
    max_limit = models.IntegerField(blank=True, null=True)
    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_saving')


class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=2)
    save_trm = models.CharField(max_length=3)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)


class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=2)
    rsrv_type_nm = models.CharField(max_length=10)
    save_trm = models.CharField(max_length=3)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
