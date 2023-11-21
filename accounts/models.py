from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=300, blank=True, null=True)
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')
    financial_products = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    desire_amount_saving = models.IntegerField(blank=True, null=True)
    desire_amount_deposit = models.IntegerField(blank=True, null=True)
    deposit_period = models.IntegerField(blank=True, null=True)
    saving_period = models.IntegerField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username
        # 기존 코드를 참고하여 새로운 필드들을 작성해줍니다.
        data = form.cleaned_data
        username = data.get("username")
        name = data.get("name")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        profile_img = data.get("profile_img")
        financial_product = data.get("financial_products")
        age = data.get("age")
        money = data.get("money")
        salary = data.get("salary")
        desire_amount_saving = data.get("desire_amount_saving")
        desire_amount_deposit = data.get("desire_amount_deposit")
        deposit_period = data.get("deposit_period")
        saving_period = data.get("saving_period")
        

        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if name:
            user_field(user, "name", name)
        if profile_img:
            user.profile_img = profile_img
        if age:
            user.age = age
        if money:
            user.money = money
        if salary:
            user.salary = salary
        if desire_amount_deposit:
            user.desire_amount_deposit = desire_amount_deposit
        if desire_amount_saving:
            user.desire_amount_saving = desire_amount_saving
        if deposit_period:
            user.deposit_period = deposit_period
        if saving_period:
            user.saving_period = saving_period
        if financial_product:
            financial_products = user.financial_products.split(',')
            financial_products.append(financial_product)
            if len(financial_products) > 1:
                financial_products = ','.join(financial_products)
            user_field(user, "financial_products", financial_products)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user


