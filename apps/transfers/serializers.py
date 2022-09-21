from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.db.models import F
from django.db import transaction

from apps.transfers.models import Transfer
from apps.investments.models import Investment
from apps.accounts.models import Account, User
from apps.stocks.models import Stock

import bcrypt


class TransferVerifyInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        exclude = ['signature', 'status']

    @transaction.atomic()
    def create(self, validated_data):
        account_number = validated_data.get('account_number')
        user_name = validated_data.get('user_name')
        transfer_amount = validated_data.get('transfer_amount')

        if not Account.objects.filter(account_number=account_number).exists():
            raise ValidationError('ERROR : 계좌번호가 유효하지 않습니다.')
        if not User.objects.filter(username=user_name).exists():
            raise ValidationError('ERROR : 사용자 이름이 유효하지 않습니다.')
        # 입력받은 계좌 정보의 사용자 이름과 입력받은 사용자 이름이 일치하는지 확인
        if Account.objects.filter(account_number=account_number).values(
                'user_id__username')[0]['user_id__username'] != user_name:
            raise ValidationError('ERROR : 계좌 명의가 일치하지 않습니다.')

        if None not in (account_number, user_name, transfer_amount):
            # 입력받은 각 값은 문자형(유니코드)이므로 hash를 위해 바이트형으로 인코딩하고, DB에는 문자형(유니코드)로 저장
            encode_signature = (str(account_number) + user_name + str(transfer_amount)).encode('utf-8')
            encrypt_signature = bcrypt.hashpw(encode_signature, bcrypt.gensalt())
            decode_signature = encrypt_signature.decode('utf-8')
        else:
            raise ValidationError('ERROR : 계좌번호, 사용자 이름, 이체금액은 필수 입력 필드입니다')

        return Transfer.objects.create(signature=decode_signature, **validated_data)


class TransferVerifyOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['transfer_identifier']


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['transfer_identifier', 'signature']

    def to_representation(self, instance):
        response = {"status": "true"}
        return response

    @transaction.atomic()
    def create(self, validated_data):
        signature = validated_data.get('signature')
        encode_signature = signature.encode('utf-8')  # checkpw 이용을 위한 인코딩

        try:
            account_number = Transfer.objects.filter(signature=signature).values()[0]['account_number']
            user_name = Transfer.objects.filter(signature=signature).values()[0]['user_name']
            transfer_amount = Transfer.objects.filter(signature=signature).values()[0]['transfer_amount']
        except Exception as e:
            raise ValidationError(f"ERROR : 유효하지 못한 데이터입니다.")

        decryption = \
            str(account_number).encode('utf-8') + user_name.encode('utf-8') + str(transfer_amount).encode('utf-8')

        if not bcrypt.checkpw(decryption, encode_signature):
            raise ValidationError("ERROR : 인증 데이터가 동일하지 않습니다.")

        transfer = Transfer.objects.get(signature=signature)
        transfer_status = transfer.status

        if not transfer_status:
            try:
                account = Account.objects.get(account_number=account_number)
                account.account_total_investment_principal = F('account_total_investment_principal') + transfer_amount
                account.save()

                stock_id = Stock.objects.get(isin="CASH")
                account_id = Account.objects.filter(account_number=account_number).values()[0]['id']
                Investment.objects.create(quantity=1, account_id=account_id, investment_stock=stock_id,
                                          investment_principal=transfer_amount)

                transfer.status = "True"
                transfer.save()

            except Exception as e:
                raise ValidationError(f"ERROR : 정보를 업데이트하는 중에 오류가 발생하였습니다. {e}")

        else:
            raise ValidationError("ERROR : 이미 처리된 데이터입니다.")

        return Response({"Success : 성공적으로 투자금이 입금되었습니다."})
