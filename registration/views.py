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
    template_name = "registration/lobby.html"


class PersonSignUpView(NotLoginRequiredMixin, CreateView):
    model = User
    form_class = PersonSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'person'
        kwargs['registre_type'] = 'Persona o Empresa'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('registration:login') + '?register'


def load_cities(request):
    if request.method == 'GET' and request.is_ajax():
        country_id = request.GET.get('country')
        cities = City.objects.filter(country_id=country_id).order_by('name')
        return render(request, 'registration/response/city_dropdown.html', {'cities': cities})
    else:
        raise Http404


class MunicipalitySignUpView(NotLoginRequiredMixin, CreateView):
    model = User
    form_class = MunicipalitySignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'municipality'
        kwargs['registre_type'] = 'Municipalidad'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('registration:login') + '?register'


class LoginTemplateView(LoginView):
    template_name = "registration/login.html"


@method_decorator([login_required, municipality_required], name='dispatch')
class PersonDetailView(DetailView):
    model = User
    template_name = "registration/detail_user_info.html"


@method_decorator([login_required, person_required], name='dispatch')
class MunicipalityDetailView(DetailView):
    model = User
    template_name = "registration/detail_muni_info.html"

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Municipality, city_id=self.request.user.person.city_id)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
