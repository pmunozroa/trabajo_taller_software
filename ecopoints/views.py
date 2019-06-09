from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import OrderBy
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView

from registration.decorators import municipality_required, person_required
from registration.models import City, Municipality, Country

from .models import RecyclingPoint, RecyclingPointRequest

# Create your views here.


@method_decorator([login_required, person_required], name='dispatch')
class RecyclingPointCreateView(CreateView):

    """
    Renderiza el template y formulario para creación de :model:`ecopoints.RecyclingPoint`.

    Requiere que el usuario esté logeado y sea persona.

    ***Context:***

    ``model``
    Instancia de :model:`ecopoints.RecyclingPoint`.

    ``fields``
    Filtro de campos a mostrar en el formulario.

    ``success_url``
    URL de redirección si el formulario es valido y almacenado sin problemas.

    ***Template:*** 

    :template:`ecopoints/ecopoints_form.html`
    """

    model = RecyclingPoint
    fields = ('real_id_point', 'name_point', 'address_point',
              'latitude_point', 'longitude_point')
    success_url = reverse_lazy('core:home')
    template_name = "ecopoints/ecopoints_form.html"

    def get_form(self, form_class=None):
        
        """
        Obtiene la instancia del formulario actual para cambiar el tipo de input para los campos de
        """

        if form_class is None:
            form_class = self.get_form_class()
        form_class.__dict__['base_fields']['latitude_point'].widget = (
            forms.TextInput())
        form_class.__dict__['base_fields']['longitude_point'].widget = (
            forms.TextInput())
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        
        """
        Si el formulario es valido, añade la Comuna y Ciudad del :model:`registration.Person` logeado, luego genera un registro de la acción realizada instanciando un objeto tipo :model:`ecopoints.RecyclingPointRequest`.
        """
        
        self.object = form.save(commit=False)
        self.object.country = self.request.user.person.country
        self.object.city = self.request.user.person.city
        self.object.save()
        recycling_request = RecyclingPointRequest()
        recycling_request.request_user_id = self.request.user.person.id
        recycling_request.request_municipality_id = Municipality.objects.get(
            city=self.request.user.person.city_id).id
        recycling_request.request_recyclingpoint_id = RecyclingPoint.objects.get(
            id=self.object.id).id
        recycling_request.save()
        return super().form_valid(form)


@method_decorator([login_required, municipality_required], name='dispatch')
class RecyclingPointListView(ListView):
    
    """
    Renderiza el template que contiene el listado de los objetos registrados :model:`ecopoints.RecyclingPoint` y los filtra para limitar que cada municipalidad solo visualize los que están en su comuna y que haya sido evaluado y aprobado.

    Requiere que el usuario esté logeado y sea municipalidad.

    ***Context:***

    ``model``
    Instancia de :model:`ecopoints.RecyclingPoint`.

    ***Template:*** 

    :template:`ecopoints/ecopoints_approved_list.html`
    """
    
    model = RecyclingPoint
    template_name = "ecopoints/ecopoints_approved_list.html"

    def get_queryset(self):
        
        """
         Filtra el queryset de la clase para solo mostrar los objetos :model:`ecopoints.RecyclingPoint` que tengan asociada la comuna de la municipalidad logeada en la instancia y que esté evaluado y aprobado.
        """
        
        return RecyclingPoint.objects.filter(city=self.request.user.municipality.city, is_active=True)


@method_decorator([login_required, municipality_required], name='dispatch')
class InactivesRecyclingPointListView(ListView):
    
    """
    Renderiza el template que contiene el listado de los objetos registrados :model:`ecopoints.RecyclingPoint` y los filtra para limitar que cada municipalidad solo visualize los que están en su comuna y que no hayan sido evaluados aún.

    Requiere que el usuario esté logeado y sea municipalidad.

    ***Context:***

    ``model``
    Instancia de :model:`ecopoints.RecyclingPoint`.

    ***Template:*** 

    :template:`ecopoints/ecopoints_list.html`
    """
    
    model = RecyclingPoint
    template_name = "ecopoints/ecopoints_list.html"

    def get_queryset(self):
        
        """
         Filtra el queryset de la clase para solo mostrar los objetos :model:`ecopoints.RecyclingPoint` que tengan asociada la comuna de la municipalidad logeada en la instancia y que no haya sido evaluado.
        """
        
        return RecyclingPoint.objects.filter(city=self.request.user.municipality.city, is_active=False, recyclingpointrequest__was_evaluated=False)


@method_decorator([login_required, municipality_required], name='dispatch')
class EvaluatedRecyclingPointRequestList(ListView):
    
    """
    Renderiza el template que contiene el listado de los objetos evaluados :model:`ecopoints.RecyclingPointRequest` y los filtra para limitar que cada municipalidad solo visualize los que están en su comuna, mostrando si fueron aprobados o rechazados.

    Requiere que el usuario esté logeado y sea municipalidad.

    ***Context:***

    ``model``
    Instancia de :model:`ecopoints.RecyclingPointRequest`.

    ***Template:*** 

    :template:`ecopoints/history_ecopoints_list.html`
    """
    
    model = RecyclingPointRequest
    template_name = "ecopoints/history_ecopoints_list.html"

    def get_queryset(self):
        
        """
         Filtra el queryset de la clase para solo mostrar los objetos :model:`ecopoints.RecyclingPointRequest` que tengan asociada la comuna de la municipalidad logeada en la instancia y que haya sido evaluado.
        """
        
        return RecyclingPointRequest.objects.filter(request_municipality_id=self.request.user.municipality.id, was_evaluated=True)


def status_ecopoint(request):
    
    """
    Renderiza listado de :model:`ecopoints.RecyclingPoint` registrados  y los filtra para limitar que cada municipalidad solo visualize los que están en su comuna y que no hayan sido evaluados aún.

    Requiere que la solicitud sea GET y tipo AJAX.

    ***Context:***

    ``ecopoint_id``
    ID de :model:`ecopoints.RecyclingPoint` a instanciar y actualizar el estado.
    
    ``ecopoint``
    Instancia de :model:`ecopoints.RecyclingPoint` asociada al ``ecopoint_id``.
    
    ``request_ecopoint``
    Instancia de :model:`ecopoints.RecyclingPointRequest` asociada a ``ecopoint``.
    
    ``points``
    Obtiene un nuevo listado de :model:`ecopoints.RecyclingPoint` limitado por la comuna de la municipalidad y que aun no han sido evaluadas.

    ***Template:*** 

    :template:`ecopoints/response/ecopoints_list.html`
    """
    
    if request.method == 'GET' and request.is_ajax():
        ecopoint_id = request.GET.get('point_request_id')
        ecopoint = RecyclingPoint.objects.get(id=ecopoint_id)
        request_ecopoint = RecyclingPointRequest.objects.get(
            request_recyclingpoint_id=ecopoint_id)
        request_ecopoint.was_evaluated = True
        if request.GET.get('change_type') == 'approved':
            ecopoint.is_active = True
            request_ecopoint.was_approved = True
        elif request.GET.get('change_type') == 'declined':
            ecopoint.is_active = False
            request_ecopoint.was_approved = False
        else:
            raise Http404
        request_ecopoint.save()
        points = RecyclingPoint.objects.filter(city=request.user.municipality.city,
            is_active=False, recyclingpointrequest__was_evaluated=False)
        ecopoint.save()
        return render(request, 'ecopoints/response/ecopoints_list.html', {'recyclingpoint_list': points})
    else:
        raise Http404


@method_decorator([login_required, municipality_required], name='dispatch')
class RecyclingPointDetailView(DetailView):
    
    """
    Renderiza el template que contiene detalles de la instancia :model:`ecopoints.RecyclingPoint` solicitada.

    Requiere que el usuario esté logeado y sea municipalidad.

    ***Context:***

    ``model``
    Instancia de :model:`ecopoints.RecyclingPoint`.

    ***Template:*** 

    :template:`ecopoints/detail_ecopoint_info.html`
    """
    
    model = RecyclingPoint
    template_name = "ecopoints/detail_ecopoint_info.html"


@method_decorator([login_required, person_required], name='dispatch')
class RecyclingPointMapView(ListView):
    
    """
    Renderiza el template del mapa que posiciona a todos los registros de :model:`ecopoints.RecyclingPoint`.

    Requiere que el usuario esté logeado y sea persona.

    ***Context:***

    ``model``
    Instancia de :model:`ecopoints.RecyclingPoint`.

    ***Template:*** 

    :template:`ecopoints/detail_ecopoint_info.html`
    """
    
    model = RecyclingPoint
    template_name = "ecopoints/ecopoints_map.html"

    def get_context_data(self, **kwargs):
        
        """
        Añade al diccionario del contexto, citys que contiene todos los objetos de :model:`registration.City` y countrys que contiene todos los objetos de :model:`registration.Country`
        """
        
        context = super().get_context_data(**kwargs)
        context["citys"] = City.objects.all()
        context["countrys"] = Country.objects.all()
        return context
