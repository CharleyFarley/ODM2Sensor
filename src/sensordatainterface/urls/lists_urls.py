from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from sensordatainterface.views.list_views import *
from sensordatainterface.models import Sites, FeatureAction, EquipmentUsed, Equipment, EquipmentModel, \
    MaintenanceAction, InstrumentOutputVariable, Action
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.db.models import Q

urlpatterns = [
    #################################################################################################
    #                         Home Tab
    #################################################################################################
    # Home Page Generic View
    url(r'^home/$', TemplateView.as_view(template_name='home/home.html'), name='home'),
    url(r'^home/$', RedirectView.as_view(url=reverse_lazy('home')), name='home_login'),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),

    #################################################################################################
    #                         Site Tab
    #################################################################################################
    # Site Generic View
    url(r'^sites/$', GenericListView.as_view(model=Sites, queryset=sites_queryset, context_object_name='Sites', template_name='sites/sites.html'), name='sites'),

    #################################################################################################
    #                         Actions Tab
    #################################################################################################
    # Site Visits Generic View
    url(r'^actions/site-visits/$', GenericListView.as_view(queryset=site_visits_queryset, context_object_name='SiteVisits', template_name='site-visits/visits.html'), name='site_visits'),
    url(r'^actions/site-visits/site/(?P<site_id>[-_\w]+)/$', SiteVisitsBySite.as_view(), name='site_visits_by_site'),

    # Deployments Generic View
    url(r'^actions/deployments/$', GenericListView.as_view(queryset=deployments_queryset, context_object_name='Deployments', template_name='site-visits/deployment/deployments.html'), name='deployments'),
    url(r'^actions/deployments/site/(?P<current>[-_\w]+)/(?P<site_id>[-_\w]+)/$', EquipmentDeploymentsBySite.as_view(), name='deployments_by_site'),
    url(r'^actions/deployments/equipment/(?P<equipment_id>[-_\w]+)/$', EquipmentDeployments.as_view(), name='deployments_by_equipment'),

    # Calibrations Generic Views
    url(r'^actions/calibrations/$',
       GenericListView.as_view(
           queryset=Action.objects.filter(
               Q(actiontypecv='Instrument calibration')
               & Q(calibrationaction__isnull=False)
           ),
           context_object_name='Calibrations',
           template_name='site-visits/calibration/calibrations.html'
       ),
       name='calibrations'),

    url(r'^actions/calibrations/equipment/(?P<equipment_id>[-_\w]+)/$',
       EquipmentCalibrations.as_view(),
       name='calibrations_by_equipment'),

    url(r'^actions/calibration-methods/',
       CalibrationMethods.as_view(),
       name='calibration_methods'),

    url(r'^actions/calibration-standards/',
       CalibrationStandards.as_view(),
       name='calibration_standards'),

    url(r'^actions/results/$',
       GenericListView.as_view(
           model=Result,
           context_object_name='Results',
           template_name='site-visits/results/results.html'
       ),
       name='results'),

    #Field Activities Generic View
    url(r'^actions/other-actions/$', #!!!
       GenericListView.as_view(
           queryset=Action.objects.filter(
               (
                   ~Q(actiontypecv='Equipment deployment') &
                   ~Q(actiontypecv='Instrument deployment') &
                   ~Q(actiontypecv='Instrument calibration')
               ),
               relatedaction__relationshiptypecv='Is child of',
               relatedaction__relatedactionid__actiontypecv='Site Visit'
           ),
           context_object_name='FieldActivities',
           template_name='site-visits/field-activities/activities.html'
       ),
       name='field_activities'),

    #Inventory Generic View
    url(r'^inventory/equipment/$',
       GenericListView.as_view(
           model=Equipment,
           context_object_name='Inventory',
           template_name='equipment/inventory.html'
       ),
       name='equipment'),

    #Factory Service Generic View
    url(r'^inventory/factory-service/$',
       GenericListView.as_view(
           queryset=EquipmentUsed.objects.filter(actionid__maintenanceaction__isfactoryservice=True),
           context_object_name='FactoryService',
           template_name='equipment/factory-service/service-events.html'
       ),
       name='factory_service'),

    #Factory Service list for an equipment
    url(r'^inventory/factory-service/equipment/(?P<equipment_id>[-_\w]+)/$', EquipmentFactoryServiceHistory.as_view(),
       name='service_events_by_equipment'),

    #Sensor Output Variables Generic View
    url(r'^inventory/sensor-output-variables/$',
       GenericListView.as_view(
           model=InstrumentOutputVariable,
           context_object_name='OutputVariables',
           template_name='equipment/sensor-output-variables/variables.html'
       ),
       name='sensor_output'),

    #Equipment Models Generic View
    url(r'^inventory/equipment-models/$',
       GenericListView.as_view(
           model=EquipmentModel,
           context_object_name='Models',
           template_name='equipment/models/models.html'
       ),
       name='models'),



    #################################################################################################
    #                         People Tab
    #################################################################################################
    url(r'^people/humans/$',
        Humans.as_view(),
        name='humans'),

    url(r'^people/organizations/$',
        OrganizationsView.as_view(),
        name='organizations'),


    #################################################################################################
    #                         Controlled Vocabularies Tab
    #################################################################################################
    url(r'^vocabularies/action-type/$',
        ActionType.as_view(),
        name='action_type'),

    url(r'^vocabularies/equipment-type/$',
        EquipmentType.as_view(),
        name='equipment_type'),

    url(r'^vocabularies/method-type/$',
        MethodType.as_view(),
        name='method_type'),

    url(r'^vocabularies/organization-type/$',
        OrganizationType.as_view(),
        name='organization_type'),

    url(r'^vocabularies/sampling-feature-type/$',
        SamplingFeatureType.as_view(),
        name='sampling_feature_type'),

    url(r'^vocabularies/site-type/$',
        SiteType.as_view(),
        name='site_type'),

    url(r'^vocabularies/spatial-offset-type/$',
        SpatialOffsetType.as_view(),
        name='spatial_offset_type'),


    #################################################################################################
    #                         Considering Deletion
    #################################################################################################

    # url(r'^control-vocabularies/$',
    #     Vocabularies.as_view(),
    #     name='vocabularies')
]
