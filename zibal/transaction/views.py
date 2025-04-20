from django.http import JsonResponse
from rest_framework.decorators import api_view
from transaction.serializers import TransactionInputSerializer
from .models import Transaction
from khayyam import JalaliDatetime
from datetime import datetime
import pytz


@api_view(['GET'])
def transaction_report(request):
    serializer = TransactionInputSerializer(data=request.GET)
    if not serializer.is_valid():
        return JsonResponse({'error': serializer.errors}, status=400)

    mode = serializer.validated_data['mode']
    report_type = serializer.validated_data['type']
    merchant_id = serializer.validated_data.get('merchantId')

    query = {}
    if merchant_id:
        query['merchantId'] = merchant_id

    pipeline = []

    if merchant_id:
        pipeline.append({'$match': {'merchantId': merchant_id}})

    if report_type == 'daily':
        date_format = '%Y-%m-%d'  
        group_id = {
            '$dateToString': {
                'format': '%Y-%m-%d',
                'date': '$createdAt',
                'timezone': 'UTC',
            }
        }
    elif report_type == 'weekly':
        date_format = '%Y-%U'  
        group_id = {
            '$dateToString': {
                'format': '%Y-%U',
                'date': '$createdAt',
                'timezone': 'UTC',
            }
        }
    elif report_type == 'monthly':
        date_format = '%Y-%m' 
        group_id = {
            '$dateToString': {
                'format': '%Y-%m',
                'date': '$createdAt',
                'timezone': 'UTC',
            }
        }

    pipeline.append({
        '$group': {
            '_id': group_id,
            'total': {'$sum': '$amount'} if mode == 'amount' else {'$sum': 1},
        }
    })

    pipeline.append({'$sort': {'_id': 1}})

    results = Transaction.objects.aggregate(*pipeline)

    report = []
    for result in results:
        gregorian_date = datetime.strptime(result['_id'], date_format)
        jalali_date = JalaliDatetime(gregorian_date).strftime('%Y/%m/%d')  
        report.append({
            'key': jalali_date,
            'value': result['total']
        })

    return JsonResponse(report, safe=False)