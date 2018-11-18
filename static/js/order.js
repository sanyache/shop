
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
          $("#order-table tbody").html(data.html_order_list);
          $("#modal-order").modal('hide');
        }
        else {
          alert('error');
          $("#modal-order .modal-content").html(data.html_form);
        }
      }
    });
    //location.assign(reload);
    return false;
  }; 
  var searchOrder = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('q'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '/order/orders/search_tph/?q=%QUERY',
    remote: {
      url: '/order/orders/search_tph/?q=%QUERY',
      wildcard: '%QUERY'
    }
  });
  
  $('#search_order .typeahead').typeahead({
    //hint:true,
    //highlight: true,
    //autoselect: true,
    minLength:1,
    limit: 10,
  }, {
    name: 'searchOrder',
    displayKey: 'q',
    source: searchOrder,
    templates:{
      empty: 'Не має в базі',
    }
  });
  // Create product 
  $(".js-create-order").click(loadForm);
  $("#modal-order").on("submit", ".js-order-create-form", saveForm);
  
  //Delete order
  $("#order-table").on("click", ".js-delete-order", loadForm);
  $("#modal-order").on("submit", ".js-order-delete-form", saveForm);
  //Delete product
  //$("#order-table").on("click", ".js-delete-order", loadForm);
  //$("#modal-order").on("submit", ".js-order-delete-form", saveForm);
  //Search-order
  $("#search_order").on("submit", saveForm);
  //Search-product
  $("#search_product").on("submit", saveForm);
});