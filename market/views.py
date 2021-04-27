import json
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.conf import settings
from market import tasks, models, serializers


class QuotesView(APIView):

    def get(self, request):
        try:
            rate_data = {
                "exchange_rate": "",
                "date_time": ""
            }
            currency = models.Currency.objects.all()
            currency_serializer = serializers.CurrencySerializer(currency, many=True)
            response = currency_serializer.data

            rate = currency[0].rate.last()
            rate_data['exchange_rate'] = rate.exchange_rate
            rate_data['date_time'] = rate.date
            response[0]['rate'] = rate_data
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
            resp_status = tasks.fetch_exchange_every_hour()
            if resp_status:
                return JsonResponse(
                    {"message": "updated successfully"},
                    safe=False,
                    status=status.HTTP_201_CREATED)

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
