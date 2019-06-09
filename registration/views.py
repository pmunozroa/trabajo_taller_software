from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView

from registration.decorators import municipality_required, person_required

from .forms import MunicipalitySignUpForm, PersonSignUpForm
from .models import City, Municipality, User

# Create your views here.


class NotLoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('core:home'))
        return super(NotLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class SignUpCreateView(NotLoginRequiredMixin, TemplateView):
    """
    Renderiza el template de registro, extiende de NotLoginRequiredMixin, el cual verifica que el usuario no esté Logeado para registarse.

    Requiere que el usuario no esté logeado.

    ***Context:***

    ***Template:*** 

    :template:`registration/lobby.html`
    """
    template_name = "registration/lobby.html"


class PersonSignUpView(NotLoginRequiredMixin, CreateView):
    
    """
    Renderiza el template y formulario para creación de :model:`registration.User`.

    Requiere que el usuario no esté logeado.

    ***Context:***

    ``model``
    Instancia de :model:`registration.User`.
    
    ``form_class``
    Instancia del formulario PersonSignUpForm para crear :model:`registration.Person` asociada a la instancia de :model:`registration.User`.

    ***Template:*** 

    :template:`registration/signup.html`
    """
    
    model = User
    form_class = PersonSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        
        """
        Añade al diccionario de instancia, user_type que contiene el valor persona y registre_type que contiene el valor Persona o Empresa.
        """
        
        kwargs['user_type'] = 'person'
        kwargs['registre_type'] = 'Persona o Empresa'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        
        """
        Metodo que redirecciona al template login con el parametro ?register para indicar que se realizó con exito y mostrar un mensaje para el usuario.
        """
        
        return reverse_lazy('registration:login') + '?register'


def load_cities(request):
    
    """
    Renderiza listado de :model:`registration.City` registrados  y los filtra según la el ID de :model:`registration.Country` solicitada.

    Requiere que la solicitud sea GET y tipo AJAX.

    ***Context:***

    ``country_id``
    ID de :model:`registration.Country` a instanciar.
    
    ``cities``
    Listado de :model:`ecopoints.RecyclingPoint` asociada al ``country_id``.

    ***Template:*** 

    :template:`registration/response/city_dropdown.html`
    """
    
    if request.method == 'GET' and request.is_ajax():
        country_id = request.GET.get('country')
        cities = City.objects.filter(country_id=country_id).order_by('name')
        return render(request, 'registration/response/city_dropdown.html', {'cities': cities})
    else:
        raise Http404


class MunicipalitySignUpView(NotLoginRequiredMixin, CreateView):
    
    """
    Renderiza el template y formulario para creación de :model:`registration.User`.

    Requiere que el usuario no esté logeado.

    ***Context:***

    ``model``
    Instancia de :model:`registration.User`.
    
    ``form_class``
    Instancia del formulario MunicipalitySignUpForm para crear :model:`registration.Municipality` asociada a la instancia de :model:`registration.User`.

    ***Template:*** 

    :template:`registration/signup.html`
    """
    
    model = User
    form_class = MunicipalitySignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        
        """
        Añade al diccionario de instancia, user_type que contiene el valor municipality y registre_type que contiene el valor Municipalidad.
        """
        
        kwargs['user_type'] = 'municipality'
        kwargs['registre_type'] = 'Municipalidad'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        
        """
        Metodo que redirecciona al template login con el parametro ?register para indicar que se realizó con exito y mostrar un mensaje para el usuario.
        """
        
        return reverse_lazy('registration:login') + '?register'


class LoginTemplateView(LoginView):
    """
    Renderiza el template Login
    
    ***Context:***

    ***Template:*** 
    
    :template:`registration/login.html`
    """
    template_name = "registration/login.html"


@method_decorator([login_required, municipality_required], name='dispatch')
class PersonDetailView(DetailView):
    
    """
    Renderiza el template que contiene detalles de la instancia :model:`registration.User` solicitada.

    Requiere que el usuario esté logeado y sea municipalidad.

    ***Context:***

    ``model``
    Instancia de :model:`registration.User`.

    ***Template:*** 

    :template:`registration/detail_user_info.html`
    """
    
    model = User
    template_name = "registration/detail_user_info.html"


@method_decorator([login_required, person_required], name='dispatch')
class MunicipalityDetailView(DetailView):
    """
    Renderiza el template que contiene detalles de la instancia :model:`registration.Municipality` asociada al usuario.

    Requiere que el usuario esté logeado y sea persona.

    ***Context:***

    ``model``
    Instancia de :model:`registration.User`.

    ***Template:*** 

    :template:`registration/detail_muni_info.html`
    """
        
    model = User
    template_name = "registration/detail_muni_info.html"

    def get(self, request, *args, **kwargs):
        
        """
        Fuerza al contexto a solo instanciar :model:`registration.Municipality` asociada al usuario, si no existe ninguna, lanza 404 forzado.
        """
        
        self.object = get_object_or_404(Municipality, city_id=self.request.user.person.city_id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
