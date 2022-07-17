jQuery(document).ready(function($){

    $(document).on('click', '.add_to_cart_button, .add-to-cart-link', function(e) {
        e.preventDefault();
        if ($(this).attr('id') == 'add-button') {
            return false;
        };
        var prodid = $(this).attr('data-product_id');
        var qty = 1;
        $.ajax({
            type: 'POST',
            url: '/cart/add/',
            data: {
                productid: prodid,
                productqty: qty,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: 'post',
            },
        success: function (json) {
            $('#basket-total-price').html(json.subtotal);
            $('#basket-qty').html(json.qty);
        },
        error: function (xhr, errmsg, err) {}
        });
    })

    // Add to cart button in detail page for main product
    $(document).on('click', '#add-button', function (e) {
        var defaultValue = $('#select').val();
        e.preventDefault();
        var value = parseInt($('.input-text,qty,text').val());
        var max = parseInt($('.input-text,qty,text').attr('max'));
        if (value > max){
            $(this).val(max);
            $('#errors').addClass('alert alert-warning');
            $('#errors').html('You can not add more than '+ max +' items for this product.');
            return false
        }
        if ($('#select').val() <= parseInt(0)) {
            alert('Quantity must be greater than 0');
            $('#select').val(defaultValue);
            return false;
        };
        $(this).prop('disabled', true);
        $.ajax({
            type: 'POST',
            url: '/cart/add/',
            data: {
                productid: $('#add-button').val(),
                productqty: $('#select').val(),
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: 'post'
            },
            success: function (json) {
                $('#add-button').prop('disabled', false);
                if (json.error){
                    console.log(json.error);
                    $('#errors').html(json.error);
                    $('#errors').addClass('alert alert-danger');
                    return false
                }
                if ($('#errors').hasClass('alert') ) {
                    $('#errors').removeClass();
                    $('#errors').html('');
                }
                var msg = $('#errors').addClass('alert alert-success');
                msg.html(json.qty + ' item added to your basket.');
                $('#basket-total-price').html(json.subtotal);
                $('#basket-qty').html(json.qty);
            },
            error: function (xhr, errmsg, err) {}
        });
    });
})