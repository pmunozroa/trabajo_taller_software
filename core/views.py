from django.views.generic import TemplateView


# Create your views here.


class HomeView(TemplateView):
    """
    Renderiza el template home
    
    ***Context:***

    ***Template:*** 
    
    :template:`core/home.html`
    """
    template_name = "core/home.html"

class AboutView(TemplateView):
    """
    Renderiza el template About Us
    
    ***Context:***

    ***Template:*** 
    
    :template:`core/about.html`
    """
    template_name = "core/about.html"