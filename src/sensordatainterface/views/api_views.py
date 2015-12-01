import json
from django.http import HttpResponse
from datetime import datetime
from sensordatainterface.models import Equipment, SamplingFeature, Action


def get_equipment_by_site(request):
    if request.method == 'POST':
        site_selected = request.POST.get('site_selected')

        equipment_deployed = Equipment.objects.filter(
            equipmentused__actionid__featureaction__samplingfeatureid=site_selected
        )

        response_data = prepare_equ_used_options(equipment_deployed)
    else:
        response_data = {'error_message': "There was an error with the request. Incorrect method?"}

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def get_sitevisit_dates(request):
    if request.method == 'POST':
        site_visit_id = int(request.POST.get('site_visit'))
        site_visit = Action.objects.get(actionid=site_visit_id)
        response_data = {
            'visit_id': site_visit_id,
            'begin_date': site_visit.begindatetime.strftime('%Y-%m-%d %H:%M'),
            'end_date': site_visit.enddatetime.strftime('%Y-%m-%d %H:%M')
        }
    else:
        response_data = {'error_message': "There was an error with the request. Incorrect method?"}

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def get_equipment_by_action(request):
    if request.method == 'POST':
        action_id = request.POST.get('action_id')

        # deployments = Action.objects.filter(
        #     actiontypecv='Equipment deployment',
        #     relatedaction__relatedactionid=action_id,
        #     relatedaction__relationshiptypecv='Is child of'
        # )

        sampling_feature = SamplingFeature.objects.filter(
            featureaction__actionid=action_id,
            featureaction__samplingfeatureid__samplingfeaturetypecv='Site'
        )[0].samplingfeatureid

        # might need to extend query to use feature action, but this should suffice
        # If the equipment that should be shown is the exquipment in deployments under the site visit selected,
        # make the query filter by the parent action through relatedactions
        equipment_deployed = Equipment.objects.filter(
            equipmentused__actionid__featureaction__samplingfeatureid=sampling_feature
        )

        response_data = prepare_equ_used_options(equipment_deployed)
    else:
        response_data = {'error_message': "There was an error with the request. Incorrect method?"}

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

def prepare_equ_used_options(equipment_deployed):
    response_data = {}

    for equipment in equipment_deployed:
        response_data[equipment.equipmentid] = str(equipment.equipmentcode) \
                                               + ": " + equipment.equipmentserialnumber \
                                               + " (" + equipment.equipmenttypecv \
                                               + equipment.equipmentmodelid.modelname + ")"

    return response_data

