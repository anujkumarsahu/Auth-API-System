from rest_framework import renderers
import json

class Renderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and any(isinstance(value, list) and 'ErrorDetail' in str(value) for value in data.values()):
            response = {"errors": data}
        else:
            response = {"data": data}
        return json.JSONEncoder().encode(response)
