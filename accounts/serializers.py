from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from financial_instruments.serializers import ContractDepositSerializer, ContractSavingSerializer



class CustomRegisterSerializer(RegisterSerializer):
    # 추가할 필드들을 정의합니다.
    username = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False)
   
    
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img', 'id', 'username', 'name', 'email', 'age', 'money', 'salary')
        read_only_fields = ('id','username', 'name',)


class UserInfoSerializer(serializers.ModelSerializer):
        profile_img = serializers.ImageField(use_url=True)
        contract_deposit = ContractDepositSerializer(many=True)
        contract_saving = ContractSavingSerializer(many=True)
        class Meta:
            model = User
            fields = '__all__'
            read_only_fields = ('id','username', 'name',)
            
            




