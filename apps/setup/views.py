from django.views.generic import (TemplateView)
from web_project import TemplateLayout


# Create your views here.
class ServerTestView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context.update({
            "msg":"سلام"
        })

        return context

