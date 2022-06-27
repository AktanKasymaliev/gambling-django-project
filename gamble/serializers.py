from gamble.models import Session

from rest_framework import serializers

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ("user", "round_played")
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_id'] = instance.user.id
        representation['user'] = instance.user.username
        return representation