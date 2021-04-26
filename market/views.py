import json
import requests
from django.http import JsonResponse
from .models import Rate, Currency
from .serializers import RateSerializer, CurrencySerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.conf import settings


API_KEY = settings.API_KEY
EXCHANGE_BTC_USD_URL = settings.EXCHANGE_BTC_USD_URL


class QuotesView(APIView):

    def get(self, request):
        try:
            currency = Currency.objects.all()
            currency_serializer = CurrencySerializer(currency, many=True)
            response = currency_serializer.data
            return JsonResponse(
                response,
                safe=False,
                status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return JsonResponse(
                {'error': str(e)},
                safe=False,
                status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return JsonResponse(
                {'error': 'Something terrible went wrong'},
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def post(self, request):
        try:
            user_name = request.data['user_name']
            user_password = request.data['password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                data = {'authenticated': True}
                return JsonResponse(
                    data,
                    safe=False,
                    status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return JsonResponse(
                {'error': str(e)},
                safe=False,
                status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return JsonResponse(
                {'error': 'Something terrible went wrong'},
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
