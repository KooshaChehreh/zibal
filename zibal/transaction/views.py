from django.http import JsonResponse
from rest_framework.decorators import api_view
from transaction.serializers import TransactionInputSerializer
from .models import Transaction
from khayyam import JalaliDatetime
from datetime import datetime
import pytz


@api_view(['GET'])
def transaction_report(request):
    # Validate query parameters using the serializer
    serializer = TransactionInputSerializer(data=request.GET)
    if not serializer.is_valid():
        return JsonResponse({'error': serializer.errors}, status=400)

    # Extract validated data
    mode = serializer.validated_data['mode']
    report_type = serializer.validated_data['type']
    merchant_id = serializer.validated_data.get('merchantId')

    # Build the MongoDB query
    query = {}
    if merchant_id:
        query['merchantId'] = merchant_id

    # Prepare the aggregation pipeline
    pipeline = []

    # Step 1: Match transactions (filter by merchantId if provided)
    if merchant_id:
        pipeline.append({'$match': {'merchantId': merchant_id}})

    # Step 2: Group by date (daily, weekly, or monthly)
    if report_type == 'daily':
        date_format = '%Y-%m-%d'  # Group by day
        group_id = {
            '$dateToString': {
                'format': '%Y-%m-%d',
                'date': '$createdAt',
                'timezone': 'UTC',
            }
        }
    elif report_type == 'weekly':
        date_format = '%Y-%U'  # Year and Week number
        group_id = {
            '$dateToString': {
                'format': '%Y-%U',
                'date': '$createdAt',
                'timezone': 'UTC',
            }
        }
    elif report_type == 'monthly':
        date_format = '%Y-%m'  # Year and Month
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

    # Step 3: Sort by date
    pipeline.append({'$sort': {'_id': 1}})

    # Execute aggregation
    results = Transaction.objects.aggregate(*pipeline)

    # Step 4: Convert dates to Jalali and format output
    report = []
    for result in results:
        gregorian_date = datetime.strptime(result['_id'], date_format)
        jalali_date = JalaliDatetime(gregorian_date).strftime('%Y/%m/%d')  # Convert to Jalali format
        report.append({
            'key': jalali_date,
            'value': result['total']
        })

    # Return the report as JSON
    return JsonResponse(report, safe=False)