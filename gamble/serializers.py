from gamble.models import SlotMachine

from rest_framework import serializers

class GetTheRandomBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = SlotMachine
        fields = "__all__"