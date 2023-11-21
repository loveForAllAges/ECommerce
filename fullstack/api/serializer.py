from rest_framework import serializers

from search.models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ('request',)
