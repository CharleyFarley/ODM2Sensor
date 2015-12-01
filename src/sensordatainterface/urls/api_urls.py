from django.conf.urls import patterns, url
from sensordatainterface.views import api_views

urlpatterns = patterns('',
    url(r'^api/get-equipment-by-site/$', api_views.get_equipment_by_site, name='get_equipment_by_site'),
    url(r'^api/get-equipment-by-action/$', api_views.get_equipment_by_action, name='get_equipment_by_action'),
    url(r'^api/get-site-visit-dates/$', api_views.get_sitevisit_dates, name='get_site_visit_dates'),
)


