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
    model = RecyclingPoint
    fields = ('real_id_point', 'name_point', 'address_point',
              'latitude_point', 'longitude_point')
    success_url = reverse_lazy('core:home')
    template_name = "ecopoints/ecopoints_form.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form_class.__dict__['base_fields']['latitude_point'].widget = (
            forms.TextInput())
        form_class.__dict__['base_fields']['longitude_point'].widget = (
            forms.TextInput())
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
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
    model = RecyclingPoint
    template_name = "ecopoints/ecopoints_approved_list.html"

    def get_queryset(self):
        return RecyclingPoint.objects.filter(city=self.request.user.municipality.city, is_active=True)

@method_decorator([login_required, municipality_required], name='dispatch')
class InactivesRecyclingPointListView(ListView):
    model = RecyclingPoint
    template_name = "ecopoints/ecopoints_list.html"

    def get_queryset(self):
        return RecyclingPoint.objects.filter(city=self.request.user.municipality.city, is_active=False, recyclingpointrequest__was_evaluated=False)


@method_decorator([login_required, municipality_required], name='dispatch')
class EvaluatedRecyclingPointRequestList(ListView):
    model = RecyclingPointRequest
    template_name = "ecopoints/history_ecopoints_list.html"

    def get_queryset(self):
        return RecyclingPointRequest.objects.filter(request_municipality_id=self.request.user.municipality.id, was_evaluated=True)


def status_ecopoint(request):
    if request.method == 'GET' and request.is_ajax():
        ecopoint_id = request.GET.get('point_request_id')
        ecopoint = RecyclingPoint.objects.get(id=ecopoint_id)
        print(ecopoint_id)
        request_ecopoint = RecyclingPointRequest.objects.get(request_recyclingpoint_id=ecopoint_id)
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
        points = RecyclingPoint.objects.filter(is_active=False, recyclingpointrequest__was_evaluated=False)
        ecopoint.save()
        return render(request, 'ecopoints/response/ecopoints_list.html', {'recyclingpoint_list': points})
    else:
        raise Http404

@method_decorator([login_required, municipality_required], name='dispatch')
class RecyclingPointDetailView(DetailView):
    model = RecyclingPoint
    template_name = "ecopoints/detail_ecopoint_info.html"

@method_decorator([login_required, person_required], name='dispatch')
class RecyclingPointMapView(ListView):
    model = RecyclingPoint
    template_name = "ecopoints/ecopoints_map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["citys"] = City.objects.all()
        context["countrys"] = Country.objects.all()
        return context
