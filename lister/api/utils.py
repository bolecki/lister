from django.core.serializers.json import Serializer as BuiltinSerializer

class Serializer(BuiltinSerializer):
    def get_dump_object(self, obj):
        return self._current
