from rest_framework import serializers


class BranchInputSerializer(serializers.Serializer):

    name = serializers.CharField(help_text="Branch name. Maximum 100 characters.", required=True)
    current_balance = serializers.FloatField(help_text="Branch's current balance.", required=True)
