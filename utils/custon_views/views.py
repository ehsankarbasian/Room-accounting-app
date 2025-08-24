from rest_framework import status
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin


class RawTemplateView(TemplateResponseMixin, ContextMixin, View):
    
    def render_to_response(self, context, status=status.HTTP_200_OK, **response_kwargs):
        response_kwargs['status'] = status
        return super().render_to_response(context, **response_kwargs)
