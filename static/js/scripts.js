$(document).ready(function(){
    var form = $('#form_buying_product');
    function loadMore(){
        var page = 1;
        $('a.load-more').click(function(event){ 
            var link = location.href;
            var num_pages = $(this).data('pages');
            page += 1;
            if( page <= num_pages){
                link =  link+"?page="+ page;
                    $.ajax({
                    'url': link,
                    'dataType': 'html',
                    'type': 'get',
                    'success': function(data, status, xhr){ 
                        html = $(data).find('.items');
                        $('.products').append(html);
                    
                    }
                });
            } 
            if( page == num_pages ){
                $(this).hide();
            }
            return false;
         });
    
    }
    function loadPage(){
        $('a.load-page').click(function(event){
          var link = $(this).attr('href')
          console.log(link);
          $.ajax({
            'url': link,
            'dataType': 'json',
            'type': 'get',
            'success': function(data, status, xhr){ 
                $("#order-table tbody").html(data.html_form);
            
            }
        });
        return false;
        });
      }

    function basketUpdating(product_id, nmb, is_delete){
        var data = {};
        var url = form.attr("action");
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        data.product_id = product_id;
        data.nmb = nmb;
        if (is_delete){
            data["is_delete"] = true;
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data){
                var f = data.products;
                $('.basket-items ul').html('');
                $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                for(var i=0; i < data.products.length; ++i){

                    $('.basket-items ul').append('<li>'+ f[i].name +', '+ f[i].nmb + 'шт.' + 'по '+ f[i].price_per_item + 'грн '+ 
                        '<a class="delete-item" href="" data-product_id="'+f[i].id+'">x</a>'+ '</li>');                  
                }
            },
            error: function(){
                console.log(url);
                console.log("error");
            },
            
        });
    }
    form.on('submit', function(e){
        e.preventDefault();
        var nmb = $('#number').val();
        var submit_btn = $('#submit_btn');
        var product_id =  submit_btn.data("product_id");
        var name = submit_btn.data("name");
        var price = submit_btn.data("price");
        
        basketUpdating(product_id, nmb, is_delete=false);

    });
    $('.increase').click(function(){
        var modal = $('#myModal');
        var modalImg = document.getElementById('img00');
        var captionText = document.getElementById('caption');
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
        modal.modal('show');
        
    });

    $('.basket-container').mouseover(function(){
        $('.basket-items').removeClass('d-none')
    });
    $('.basket-container').mouseout(function(){
        $('.basket-items').addClass('d-none')
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id")
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true);
    });

    $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
        if (!$(this).next().hasClass('show')) {
          $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
        }
        var $subMenu = $(this).next(".dropdown-menu");
        $subMenu.toggleClass('show');
      
      
        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
          $('.dropdown-submenu .show').removeClass("show");
        });
      
      
        return false;
      });

    function calculatingBasketAmout(){
        var total_order_amount = 0;
        var data = $('.total-product-in-basket-amount');
        for(var i=0; i < data.length; ++i){
            total_order_amount += parseFloat(data[i].innerText);
        }
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    }  
    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = parseInt($(this).val());
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-in-basket-price-per-item').text()).toFixed(2);
        total_amount = current_nmb * current_price ;
        current_tr.find('.total-product-in-basket-amount').text(total_amount);
        calculatingBasketAmout();
        
    });
    function calculatingOrderAmout(){
        var total_order_amount = 0;
        var data = $('.total-product-in-order-amount');
        for(var i=0; i < data.length; ++i){
            var id ='is-active_'+ data[i].getAttribute('data-id');
            check = document.getElementById(id).checked;
            if (check == true) {
                total_order_amount += parseFloat(data[i].innerText);
             }    
        }
        document.getElementById('id_total_price').value = total_order_amount;
        //total_price.text(total_order_amount.toFixed(2));
    }  
    $(document).on('change', ".product-in-order-nmb", function(){
        var current_nmb = parseInt($(this).val());
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-in-order-price-per-item').text()).toFixed(2);
        total_amount = current_nmb * current_price ;
        current_tr.find('.total-product-in-order-amount').text(total_amount);
        calculatingOrderAmout();
        
    });
    $(document).on('change', ".checkbox", function changeAction(){
        var current_nmb = parseInt($(this).val());
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-in-order-price-per-item').text()).toFixed(2);
        total_amount = current_nmb * current_price ;
        current_tr.find('.total-product-in-order-amount').text(total_amount);
        calculatingOrderAmout();
        
    });
    
    loadMore();
    loadPage();
    calculatingBasketAmout();
    calculatingOrderAmout();
    
    
});