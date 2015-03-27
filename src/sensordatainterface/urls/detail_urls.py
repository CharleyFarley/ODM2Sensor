from django.conf.urls import patterns, include, url
from sensordatainterface.views import GenericListView, GenericDetailView
from sensordatainterface.models import Sites, FeatureAction, EquipmentUsed, Equipment, EquipmentModel, \
    MaintenanceAction, InstrumentOutputVariable, Variable
import datetime
from django.db.models import Q
urlpatterns = patterns('',
                       # Site detail
                       url(r'^site-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='Site',
                               queryset=Sites.objects.using('odm2').all(),
                               slug_field='samplingfeatureid',
                               template_name='sites/details.html'),
                               name='site-detail'),

                       # Site Visit detail
                       url(r'^visit-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='SiteVisit',
                               queryset=FeatureAction.objects.using('odm2').all(),
                               slug_field='actionid',
                               template_name='site-visits/details.html'),
                               name='site-visit-detail'),

                        # Deployment detail
                       url(r'^deployment-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='Deployment',
                               queryset=EquipmentUsed.objects.using('odm2').filter(
                                   Q(equipmentid__equipmentownerid__affiliation__affiliationenddate__isnull=True) |
                                   Q(equipmentid__equipmentownerid__affiliation__affiliationenddate__lt=datetime.datetime.now())
                               ),
                               slug_field='actionid',
                               template_name='site-visits/deployment/details.html'),
                               name='deployment-detail'),

                       # Calibration detail
                       url(r'^calibration-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='Calibration',
                               queryset=EquipmentUsed.objects.using('odm2').all(),
                               slug_field='actionid',
                               template_name='site-visits/calibration/details.html'),
                               name='calibration-detail'),

                        # Field Activity detail
                       url(r'^field-activity-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='Activity',
                               queryset=FeatureAction.objects.using('odm2').all(),
                               slug_field='actionid',
                               template_name='site-visits/field-activities/details.html'),
                               name='field-activity-detail'),

                        # Equipment detail
                       url(r'^equipment-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='Equipment',
                               queryset=Equipment.objects.using('odm2').all(),
                               slug_field='equipmentid',
                               template_name='equipment/details.html'),
                               name='equipment-detail'),

                        #to do: Factory Service detail - no detail pages for reference.
                       # url(r'^factory-service-detail/(?P<slug>[-_\w]+)/$', SiteDetailView.as_view(
                       #         context_object_name='FactoryService',
                       #         queryset=Equipment.objects.using('odm2').all(),
                       #         slug_field='equipmentid',
                       #         template_name='equipment/details.html'),
                       #         name='equipment-detail'),

                        # Sensor Output Variable detail
                       url(r'^output-variable-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='OutputVariable',
                               queryset=InstrumentOutputVariable.objects.using('odm2').all(),
                               slug_field='variableid',
                               template_name='equipment/sensor-output-variables/details.html'),
                               name='equipment-detail'),

                       # Sensor Output Variable detail
                       url(r'^models-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='Model',
                               queryset=EquipmentModel.objects.using('odm2').all(),
                               slug_field='equipmentmodelid',
                               template_name='equipment/models/details.html'),
                               name='equipment-detail'),

                       # Following detail urls are not in the main navigation (i.e. in the navbar)
                       # Measured Variable detail
                       url(r'^measured-variable-detail/(?P<slug>[-_\w]+)/$', GenericDetailView.as_view(
                               context_object_name='MeasuredVariable',
                               queryset=Variable.objects.using('odm2').all(),
                               slug_field='variableid',
                               template_name='sites/measured-variable-details.html'),
                               name='equipment-detail'),
)