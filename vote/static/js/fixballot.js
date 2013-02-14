$(function() {
  var ballot = $.parseJSON($("#ballot_data").text());

  for (var i = 0; i < ballot.length; i++) {
    $("#ballot_list").append('<li class="ui-state-default">' + ballot[i] + '</li>');
  }
});
