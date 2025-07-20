from django.views.generic import (TemplateView)
from web_project import TemplateLayout
from apps.setup.models import Country
from apps.test.models import Isp

# Create your views here.
class ServerTestView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        country = Country.objects.filter().order_by('persian_name')
        isp = Isp.objects.filter().order_by('name')

        context['country'] = country
        context['isp'] = isp

        return context

