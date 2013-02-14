$(function() {
  var options = $.parseJSON($("#template").text());

  for (var i = 0; i < options.length; i++) {
    $("#sortable").append('<li sortable_choice="' + i + '" class="ui-state-default">' + options[i] + '</li>');
  }

  $( "#sortable" ).sortable();
  $( "#sortable" ).disableSelection();

  $("#submit-id-submit").click(function() {
    var data_array = $("#sortable").sortable("toArray", {attribute: 'sortable_choice'});
    var data_str = JSON.stringify(data_array);
    console.log(data_array);
    $("#id_data").val(data_str);
  });
});
