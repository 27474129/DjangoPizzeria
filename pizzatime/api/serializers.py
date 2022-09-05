from rest_framework import serializers



class OrdersSerialiser(serializers.Serializer):
    phone = serializers.CharField(max_length=80)
    address = serializers.CharField(max_length=255)
    apartment = serializers.CharField(max_length=50)
    floor = serializers.CharField(max_length=50)
    contactless = serializers.BooleanField()
    price = serializers.CharField(max_length=50)
    goods = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=50)
    is_delivery = serializers.BooleanField()
    point_pk = serializers.IntegerField(default=0)
