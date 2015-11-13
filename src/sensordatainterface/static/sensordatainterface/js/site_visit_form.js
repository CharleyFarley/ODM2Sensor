function addActionForm(that) {
    var button = $(that).parents('tbody');
    var form = $('#action-form').children();
    var thisForm = form.clone();

    //Move add button and insert delete button
    thisForm.insertBefore(button);
    button.prev().prepend(
        '<tr><th></th><td><a class="btn btn-remove-action btn-danger col-xs-2 col-sm-2" onclick="javascript:deleteActionForm(this)">- Remove Action</a></td></tr>'
    );

    setChildActionDateTimePicker(thisForm);

    //add handler for when the actiontypecv is changed
    $(thisForm).find('.select-two[name="actiontypecv"]').change(function () {
        var selected = $(this).val();
        var currentActionForm = $(this).parents('tbody');
        handleActionTypeChange(selected, currentActionForm);
    });

    //Fix error with select2
    $(thisForm).find(".select2-container").remove();
    $(thisForm).find(".select-two").select2();

    // This bit of code solves the problem of th checkbox not sending status when is unchecked.
    // ie. it will not send False to the server
    $(thisForm).find('.maintenance[type="checkbox"]').change(setIsFactoryServiceFlag);

    handleActionTypeChange('Field activity', thisForm);

   setFormFields($(thisForm));

    //hide custom fields for all action form types
    $(thisForm).find(".calibration").not('option').parents('tr').hide();
    $(thisForm).find(".maintenance").not('option').parents('tr').hide();
}

function setChildActionDateTimePicker(childForm) {
    var siteVisitForm = $('.form-table').children().first();
    var beginDTInitialValue = moment(siteVisitForm.find("[name='begindatetime']").val());
    var endDTInitialValue = moment(siteVisitForm.find("[name='enddatetime']").val());

    //restart datetimepicker
    $(childForm).find('.datetimepicker').datetimepicker(
        {
            format: 'YYYY-MM-DD HH:mm'
        }).on('changeDate', beginDateTimeChanged);

    //set initial bounds on dates depending on site visit dates
    setIndividualBounds(childForm);

    //Initialize data and UTCOffset for children action forms
    //set the value of the begin time in the action form to the site visit form begin time
    childForm.find("[name='begindatetime']").parent('.datetimepicker').data('DateTimePicker').date(beginDTInitialValue);
    childForm.find("[name='enddatetime']").parent('.datetimepicker').data('DateTimePicker').date(endDTInitialValue);

    beginDateTimeChanged(childForm, false);

    childForm.find("[name='begindatetimeutcoffset']").val(siteVisitForm.find("[name='begindatetimeutcoffset']").val());
    childForm.find("[name='enddatetimeutcoffset']").val(siteVisitForm.find("[name='enddatetimeutcoffset']").val());

    setDTPickerClose($(childForm).find('[name="begindatetime"]'));
}

function setIsFactoryServiceFlag() {
    var thisCheckBox = $(this);
    var hiddenCheckBox = thisCheckBox.parents('tbody').find('#id_isfactoryservicebool');
    if (thisCheckBox[0].checked) {
        hiddenCheckBox.attr('value', 'True');
    } else {
        hiddenCheckBox.attr('value', 'False');
    }
}

function deleteActionForm(that) {
    $(that).parents('tbody').remove();
}

function addEquipmentField(that) {
    // Change this function to add a nested form for equipment used...
    var newField = $($('#action-form').find('[name="equipmentused"]').parents('tr').clone());
    var select2Elem = newField.find('[name="equipmentused"]');
    newField.insertBefore($(that).parents('tr'));
    select2Elem.next('.select2-container').remove();
    select2Elem.select2();
    select2Elem.next('.select2-container').attr('style', 'width:85%');
}

function setMultipleFieldsNumber(event) {
    var object = event.data.object;
    var multipleObjElems = $('.input-group tbody').find('[name="' + object + '"]');

    for (var i = 0; i < multipleObjElems.length; i++) {
        var multipleObjElem = $(multipleObjElems[i]);
        var selectedValue = multipleObjElem.val();
        var multipleObjCount = !selectedValue? 0 : selectedValue.length;
        multipleObjElem.parents('tbody').find('[name="' + object + 'number"]').val(multipleObjCount);
    }

}

function setEquipmentUsedFilter() {
    //add handler for when the actiontypecv is changed
    $('form').find('.select-two[name="samplingfeatureid"]').change(function () {
        filterEquipmentBySite($(this).val(), $('form [name="equipmentused"]'));
    });
}

function setChildBoundsListener() {
    // Set boundaries of child form datetime fields according to datetime fields of parent site visit
    var siteVisitForm = $('form').find('tbody')[0];
    $(siteVisitForm).find('.datetimepicker').on('dp.change', setChildActionFormBounds);
}

function setChildActionFormBounds(ev) {
    var childForms = $('.form-table').children('tbody').has('[name="enddatetime"]');
    for (var i = 1; i < childForms.length; i++)
        setIndividualBounds($(childForms[i]))
}

$(document).ready(function () {
    var formItems = $('form.input-group');
    formItems.submit({object: 'equipmentused'}, setMultipleFieldsNumber);
    formItems.submit({object: 'calibrationstandard'}, setMultipleFieldsNumber);
    formItems.submit({object: 'calibrationreferenceequipment'}, setMultipleFieldsNumber);

    setChildBoundsListener();
    setEquipmentUsedFilter();

    $('tbody').has('[name="actiontypecv"]').find('.maintenance[type="checkbox"]').change(setIsFactoryServiceFlag);

});
