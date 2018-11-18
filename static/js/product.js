$(function(){
    

    
    var loadForm = function() {
        var btn = $(this);
        
        $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-order").modal('show');
          },
          success: function (data) { 
            $("#modal-order .modal-content").html(data.html_form);
            action = btn.attr("data-url");
            $("#form").attr("action", action);
          },
          error:function(){
            console.log(url);
          }
        });
        return false;
  }
  var saveForm =  function () {
    var form = $(this);
    //var reload = $('#submit').data('reload');
      $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) { 
          $("#reply_list").html(data.html_order_list);
          $("#modal-order").modal('hide');
        }
        else {
          
          $("#modal-order .modal-content").html(data.html_form);
        }
      },
      error: function(data){
        console.log(form.attr("action"));
      }
    });
    //location.assign(reload);
    return false;
  }; 

  //Create replay
  $("#reply_add").on("click", ".js-create-reply", loadForm);
  $("#modal-order").on("submit", ".js-reply-create-form", saveForm);
  //Create answer
  $(".answer").on("click", ".js-create-reply", loadForm);
  //$("#modal-order").on("submit", ".js-reply-create-form", saveForm);
}); 