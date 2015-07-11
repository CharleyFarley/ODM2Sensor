function removeCommas(table) {
    var lastColumn = table.rows[0].cells.length - 1;

    for (var i = 1; i < table.rows.length; i++) {
        data = table.rows[i].cells[lastColumn].innerHTML.trim();
        table.rows[i].cells[lastColumn].innerHTML = data.substr(0, data.length - 1);
    }
}

function setNavActive() {
    $(".active").removeClass("active");

    var currentPath = window.location.pathname;

    if (currentPath.indexOf("inventory") > 0) {
        $("#inventory-nav").addClass("active");
    } else if (currentPath.indexOf("sites") > 0) {
        $("#sites-nav").addClass("active");
    } else if (currentPath.indexOf("site-visits") > 0) {
        $("#visits-nav").addClass("active");
    } else if (currentPath.indexOf("control-vocabularies") > 0) {
        $("#vocabulary-nav").addClass("active");
    }
}

function setDeleteConfirmation() {
    /*http://ethaizone.github.io/Bootstrap-Confirmation/*/
    $('#danger-button').confirmation({
        placement: 'bottom',
        title: 'Are you sure you want to delete?',
        popout: true,
        btnCancelClass: 'btn-default',
        onCancel: function () {
            $('#danger-button').confirmation('hide');
        }
    });
}

function set_delete_icon() {
    $('.delete-icon').confirmation({
        placement: 'left',
        title: 'Are you sure?',
        btnCancelClass: 'btn-default',
        onCancel: function () {
            $('.delete-icon').confirmation('hide');
        },
        onConfirm: function () {
            var tableClicked = $(this).parents('.dataTables_wrapper').attr('id');
            var table = $('#' + tableClicked);
            var searchText = table.find('input[type="search"]')[0].value;

            sessionStorage.setItem('tableClicked', tableClicked);
            var tablePage = table.find('.paginate_button.current')[0].getAttribute('data-dt-idx');

            if (searchText != "") {
                sessionStorage.setItem('searchTerm', searchText);
                if (tablePage > 0) {
                    sessionStorage.setItem('tablePage', tablePage);
                }
            } else {
                sessionStorage.setItem('tablePage', tablePage);
            }

        }
    });
}

function setDateTimePicker() {
    initDTPicker();//Checked

    //If adding actionforms add endtime functionality
    //if (typeof (beginDTChanged) == 'function') {
    //    currentDateTimePicker.on('dp.change', beginDTChanged);
    //    var siteVisitEndDTElem = $('.form-table').children().first().find("[name='enddatetime']");
    //    setFormEndTime(siteVisitEndDTElem, new Date());
    //}

    //When begindatetime changes, set maxDate on enddatetime
    var tBodies = $('form tbody');
    tBodies.each(function () {
        beginDateTimeChanged(this, true);
    });

}

function beginDateTimeChanged(thisTBody, trigger) {
    var endDTElem = $(thisTBody).find('[name="enddatetime"]').parent('.datetimepicker');
    var event = $(thisTBody).find('[name="begindatetime"]')
        .parent('.datetimepicker')
        .on('dp.change', function (ev) {
            var date = moment($(ev.currentTarget).data().date);
            setEndMinDate(thisTBody, date);
        });

    if (trigger && endDTElem.length > 0) {
        event.trigger('dp.change');
        endDTElem.children('input').blur();
        endDTElem.data('DateTimePicker').hide();
    }
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

function setIndividualBounds(actionTBody) {
    var siteVisit = $('.form-table').children('tbody').first();
    var beginSVDate = moment($(siteVisit).find('[name="begindatetime"]').val());
    var endSVDate = moment($(siteVisit).find('[name="enddatetime"]').val());

    var beginDateTimeObj = actionTBody.find('[name="begindatetime"]').parents('.datetimepicker').data('DateTimePicker');
    var endDateTimeObj = actionTBody.find('[name="enddatetime"]').parents('.datetimepicker').data('DateTimePicker');


    beginDateTimeObj.maxDate(endSVDate);
    beginDateTimeObj.minDate(beginSVDate);

    endDateTimeObj.maxDate(endSVDate);
    endDateTimeObj.minDate(beginSVDate);

}

function setEndMinDate(thisTBody, newDate) {
    $(thisTBody).find('[name="enddatetime"]').parent('.datetimepicker').data('DateTimePicker').minDate(newDate).show();
}

function initDTPicker() {
    /* http://tarruda.github.io/bootstrap-datetimepicker/ */
    var dateElements = [];
    // Push elements to get calendar widget
    dateElements.push($('#id_equipmentpurchasedate'));// All checked below
    dateElements.push($("[name='begindatetime']"));
    dateElements.push($("[name='enddatetime']"));
    dateElements.push($("[name='referencematerialpurchasedate']"));
    dateElements.push($("[name='referencematerialexpirationdate']"));

    dateElements.forEach(function (element) {//function checked
        element.wrap("<div class='datetimepicker input-group date'></div");
        element.after(
            $("<span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span>")
        );

    });

    var currentDateTimePicker = $('.datetimepicker');
    currentDateTimePicker.datetimepicker({
        format: 'YYYY-MM-DD HH:mm'
    });
}

function setFormFields() {
    $('input').addClass('form-control');
    $("[type='checkbox']").removeClass('form-control');
    $('textarea').addClass('form-control');
    $('select').addClass('select-two');

    $(".select-two").select2();

    //set styling issues with form fields.
    $('.select2-container').css('width', '85%');
    $('form input, form textarea').css('width', '85%');
    $('form input[type="submit"]').css('width', '66%');
    $('.datetimepicker input').css('width', '100%'); //Checked
}

$(document).ready(function () {
    setDateTimePicker();

    setChildBoundsListener();

    setFormFields();

    setNavActive();

    setDeleteConfirmation();

    set_delete_icon();

    $('.dataTables_paginate').click(function () {
        set_delete_icon();
    });

    $('.dataTables_filter').find('input[type="search"]').change(function () {
        set_delete_icon();
    });

    if (typeof (initVocabulariesTabs) == "function") {
        initVocabulariesTabs($);
    }

});
