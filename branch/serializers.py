from rest_framework import serializers

from .models import Branch


class BranchInputSerializer(serializers.Serializer):

    name = serializers.CharField(help_text="Branch name. Maximum 100 characters.", required=True)
    current_balance = serializers.FloatField(help_text="Branch's current balance.", required=True)


class BranchResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ('id', 'name', 'current_balance', 'previous_balance')
