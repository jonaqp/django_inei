function UpdateElements(el, prefix, number_prefix) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + number_prefix;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);

    $(el).find('input, select, textarea').each(function(j, input) {
          $(input).attr('id', $(input).attr('id').replace(id_regex, replacement));
          $(input).attr('name', $(input).attr('name').replace(id_regex, replacement));
          $("#id_"+replacement+"-ORDER").val(parseInt(number_prefix)+1);
    });

}

function AddFormset(btn, prefix) {
    var form_count = $('#id_' + prefix + '-TOTAL_FORMS');
    var total_form_count = parseInt(form_count.val());
    var content_prefix = $('#content_'+prefix);
    var row = content_prefix.find('.dynamic-form:first').clone(true).get(0);
    $(row).removeAttr('id').insertAfter(content_prefix.find('.dynamic-form:last')).find('.formset-icon-remove').removeClass('hidden');
    $(row).attr('id', prefix+"-"+total_form_count+"-row");
    $('#id_'+prefix+"-"+total_form_count+"-id").val('');

    $(row).children().not(':last').each(function () {
         UpdateElements(this, prefix, total_form_count);
         $(this).val('');
    });
    form_count.val(total_form_count + 1);
}

function RemoveFormset(btn, prefix) {
    var current_id = $(btn).parents('.dynamic-form').attr('id');
    var id_number = current_id.split('-')[1];
    var formset_id = $("#id_"+prefix+"-"+id_number+"-id").val();

     if (formset_id == "" ){
        $(btn).parents('.dynamic-form').remove();
    }else{
        $('#'+current_id ).addClass('hidden');
        $("#id_"+prefix+"-"+id_number+"-DELETE").attr('checked', true);
    }

    var forms = $('#content_'+prefix).find('.dynamic-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    $('#id_' + prefix + '-INITIAL_FORMS').val(forms.length);
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
        var replacement = prefix + '-' + i;
        $(forms.get(i)).attr('id', $(forms.get(i)).attr('id').replace(id_regex, replacement));

        $(forms.get(i)).children().not(':last').each(function (index, value) {
            UpdateElements(this, prefix, i);
        });
    }

}


 function add_formset_global(formset_prefix){
     return AddFormset(this, formset_prefix);
 }

 function remove_formset_global(el, formset_prefix){
     return RemoveFormset(el, formset_prefix);
 }
