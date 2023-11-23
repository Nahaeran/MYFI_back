from django.conf import settings
from rest_framework.response import Response
from .models import Exchange
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import ExchangeSerializer


EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01'


@api_view(['GET'])
def index (request):
    response = requests.get(EXCHANGE_API_URL).json()
    exist_response = Exchange.objects.all()
   
    if response: # 가 있다면기존 데이터를 업데이트
        if not exist_response: # 쿼리셋이 비어있다면
                serializer = ExchangeSerializer(data=response, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        else: # exist_response가 존재한다면
            Exchange.objects.all().delete()
            serializer = ExchangeSerializer(data=response, many=True)     
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    # 없다면
    serializer = ExchangeSerializer(exist_response, many=True)
    return Response(serializer.data)

