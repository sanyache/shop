$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);
    form.on('submit', function(e){
        e.preventDefault();
        var nmb = $('#number').val();
        var submit_btn = $('#submit_btn');
        var product_id =  submit_btn.data("product_id");
        var name = submit_btn.data("name");
        var price = submit_btn.data("price");
        
        var data = {};
        var url = form.attr("action");
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        data.product_id = product_id;
        data.nmb = nmb;
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data){
                console.log(data.products_total_nmb);
                $('#basket_total_nmb').text("("+data.products_total_nmb+")");
            },
            error: function(){
                console.log(url);
                console.log("error");
            },
            
        })
        $('.basket-items ul').append('<li>'+ name +', '+ nmb + 'шт.' + 'по '+ price + 'грн '+ '<a class="delete-item" href="">x</a>'+ '</li>');

    });

    $('.basket-container').mouseover(function(){
        $('.basket-items').removeClass('d-none')
    });
    $('.basket-container').mouseout(function(){
        $('.basket-items').addClass('d-none')
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        $(this).closest('li').remove();
    });
});