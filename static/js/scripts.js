$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

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
        console.log(total_amount);
    });
    calculatingBasketAmout();
});