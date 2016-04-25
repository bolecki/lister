from django.core.serializers.json import Serializer as BuiltinJSONSerializer

class Serializer(BuiltinJSONSerializer):
    def get_dump_object(self, obj):
        return self._current
