$(document).ready(function() {
  $(".project").on('click', function(){
    project = $(this).text().substring(2, $(this).text().length-1)
    $.get("/vote", {project: project}, function(data){
      if (data == "0")
        window.location.href="success"
      else if(data == "-1"){
        window.location.href="invalid"
        console.log("Unknown Email");
      }
    })
  });

  $('#usr').keypress(function (e) {
    if (e.which == 13) {
      var email = $(this).val();
      $.get("/authenticate", {email: email}, function(data){
        if (data == "0")
          window.location.href="projects"
        else if(data == "-1")
          window.location.href="invalid"
        else if(data == "-2")
          window.location.href="repeat"
      })
    }
  });

  setTimeout(function(){$(".winner").fadeIn('slow');}, 2000);
});