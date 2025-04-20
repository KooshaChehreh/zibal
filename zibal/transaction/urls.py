from django.urls import path
from .views import transaction_report

urlpatterns = [
    path('transaction-report/', transaction_report, name='transaction-report'),
]