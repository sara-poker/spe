from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper




def filter_country(country, queryset):
    if country == "0":
        return queryset
    return queryset.filter(vpn_country=country)


def filter_country_server(country_server, queryset):
    if country_server == "0":
        return queryset
    return queryset.filter(vpns__server_country_id=country_server).distinct()


class FrontPagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,  # Get the current url path (active URL) from request
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        return context


