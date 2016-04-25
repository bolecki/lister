from django.core.serializers.json import Serializer

class FilteredSerializer(Serializer):
    def get_dump_object(self, obj):
        return self._current
