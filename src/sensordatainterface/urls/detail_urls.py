from django.conf.urls import patterns, url
from sensordatainterface.views import GenericDetailView, DeploymentMeasVariableDetailView
from sensordatainterface.models import Sites, FeatureAction, EquipmentUsed, Equipment, EquipmentModel, \
    InstrumentOutputVariable, Organization
import datetime
from django.db.models import Q

urlpatterns = patterns('',
                       # Site detail
                       url(r'^sites/site-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Site',
                           model=Sites,
                           slug_field='samplingfeatureid',
                           template_name='sites/details.html'),
                           name='site_detail'),

                       # Site Visit detail
                       url(r'^site-visits/visit-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='SiteVisit',
                           model=FeatureAction,
                           slug_field='actionid',
                           template_name='site-visits/details.html'),
                           name='site_visit_detail'),

                       # Deployment detail
                       url(r'^site-visits/deployment-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Deployment',
                           queryset=EquipmentUsed.objects.filter(
                               Q(equipmentid__equipmentownerid__affiliation__affiliationenddate__isnull=True) |
                               Q(equipmentid__equipmentownerid__affiliation__affiliationenddate__lt=datetime.datetime.now())
                           ),
                           slug_field='actionid',
                           template_name='site-visits/deployment/details.html'),
                           name='deployment_detail'),

                       # Calibration detail
                       url(r'^site-visits/calibration-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Calibration',
                           model=EquipmentUsed,
                           slug_field='actionid',
                           template_name='site-visits/calibration/details.html'),
                           name='calibration_detail'),

                       # Field Activity detail
                       url(r'^site-visits/field-activity-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Activity',
                           model=FeatureAction,
                           slug_field='actionid',
                           template_name='site-visits/field-activities/details.html'),
                           name='field_activity_detail'),

                       # Equipment detail
                       url(r'^inventory/equipment-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Equipment',
                           model=Equipment,
                           slug_field='equipmentid',
                           template_name='equipment/details.html'),
                           name='equipment_detail'),

                       # to do: Factory Service detail - no detail pages for reference.
                       # url(r'^inventory/factory-service-detail/(?P<slug>[-_\w]+)/$', SiteDetailView.as_view(
                       #         context_object_name='FactoryService',
                       #         model=Equipment,
                       #         slug_field='equipmentid',
                       #         template_name='equipment/details.html'),
                       #         name='equipment-detail'),

                       # Sensor Output Variable detail
                       url(r'^inventory/output-variable-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='OutputVariable',
                           model=InstrumentOutputVariable,
                           slug_field='instrumentoutputvariableid',
                           template_name='equipment/sensor-output-variables/details.html'),
                           name='output_variable_detail'),

                       # Models detail
                       url(r'^inventory/models-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Model',
                           model=EquipmentModel,
                           slug_field='equipmentmodelid',
                           template_name='equipment/models/details.html'),
                           name='models_detail'),

                       url(r'^inventory/vendor-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                           context_object_name='Vendor',
                           model=Organization,
                           slug_field='organizationid',
                           template_name='equipment/models/vendor-detail.html'),
                           name='vendor_detail'),

                       # Following detail urls are not in the main navigation (i.e. in the navbar)
                       # Measured Variable detail
                       url(r'^sites/measured-variable-detail/(?P<pk>[-_\w]+)/(?P<equipmentused>[-_\w]+)/$',
                           DeploymentMeasVariableDetailView.as_view(),
                           name='measured_variable_detail'),


)