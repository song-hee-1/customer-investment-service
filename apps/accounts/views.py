from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from django.db import transaction

from apps.accounts.models import Account, Transfer
from apps.investments.models import Investment

import bcrypt

from . serializers import StockHoldingSerializer, InvestDetailSerializer, InvestSerializer,\
    TransferInputSerializer, TransferOutputSerializer


class GetHoldingInvestListAPI(generics.ListAPIView):
    serializer_class = StockHoldingSerializer

    def get_queryset(self):
        return Investment.objects.all()


class GetDetailInvestAPI(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestDetailSerializer


class GetInvestAPI(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = InvestSerializer


class TransferAPI(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferInputSerializer

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        # phase1 API
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data
        account_number = data['account_number']
        user_name = data['user_name']
        transfer_amount = data['transfer_amount']

        encode_signature = (str(account_number) + user_name + str(transfer_amount)).encode('utf-8')
        encrypt_signature = bcrypt.hashpw(encode_signature, bcrypt.gensalt())

        self.perform_create(input_serializer)
        output_serializer = TransferOutputSerializer(input_serializer.instance)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # phase2 API
