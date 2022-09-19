from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.accounts.models import Account, Transfer
from apps.investments.models import Investment

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

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        self.perform_create(input_serializer)
        output_serializer = TransferOutputSerializer(input_serializer.instance)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
