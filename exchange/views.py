from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests


EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01'


@api_view(['GET'])
def index (request):
    response = requests.get(EXCHANGE_API_URL).json()
    print(response)
    return Response(response)