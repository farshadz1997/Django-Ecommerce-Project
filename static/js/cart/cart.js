jQuery(document).ready(function($){
    
    // Delete Item
    $(document).on('click', '#delete-button', function (e) {
        e.preventDefault();
        var prodid = $(this).data('index');
        $.ajax({
        type: 'POST',
        url: '/cart/delete/',
        data: {
            productid: $(this).data('index'),
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: 'post'
        },
        success: function (json) {
            $('.cart_item[data-index="' + prodid + '"]').remove();
            if (json.qty == 0) {
                $('.actions').hide("slow");
                $('#empty-cart').show("slow");
                $('.cart_totals').hide('slow');
            };
            $('#basket-total-price').html(json.cart_subtotal);
            $('#basket-qty').html(json.qty);
            $('#subtotal').html(json.subtotal);
            $('#cart-subtotal').html(json.cart_subtotal);
        },
        error: function (xhr, errmsg, err) {}
        });
    })

    // Update Item
    $(document).on('click', '#update-button', function (e) {
        e.preventDefault();
        var prodid = $(this).data('index');
        var dict = [];
        // loop over elements with class "select"
        $('.cart_item').each(function () {
            var id = $(this).data('index');
            var qty = $(this).find('#select-'+id).val();
            dict.push({'productid': id, 'productqty': qty});
        });
        $.ajax({
        type: 'POST',
        url: '/cart/update/',
        data: {
            products: JSON.stringify(dict), 
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: 'post'
        },
        success: function (json) {
            $('#basket-total-price').html(json.cart_subtotal);
            $('#basket-qty').html(json.qty);
            $('#subtotal').html(json.subtotal);
            $('#cart-subtotal').html(json.cart_subtotal);
            for (let item in json.products){
                $('#select-'+json.products[item]['productid']).html(json.products[item]["productqty"]);
                $('#product-total-'+json.products[item]["productid"]).html(json.products[item]["productTotalPrice"]);
            };
            if ($('#errors').hasClass('alert alert-warning')) {
                $('#errors').removeClass('alert alert-warning');
                $('#errors').html('');
            }
            $('#errors').addClass('alert alert-success');
            $('#errors').html('Your cart has been updated');
        },
        error: function (xhr, errmsg, err) {}
        });
    })

    // plus 1 to value of element with id select
    $(document).on('click', '.plus', function (e) {
        e.preventDefault();
        var item_id = $(this).attr("data-product_id");
        var current_value = $(document).find('#select-'+item_id).val();
        var max = parseInt($(document).find('#select-'+item_id).attr("max"));
        if (parseInt(current_value) < max) {
            $(document).find('#select-'+item_id).val(parseInt(current_value) + 1);
        }
    })

    // minus 1 to value of element with id select
    $(document).on('click', '.minus', function (e) {
        e.preventDefault();
        var item_id = $(this).attr("data-product_id");
        var current_value = $(document).find('#select-'+item_id).val();
        if (current_value == 1){
            return false;
        }
        $(document).find('#select-'+item_id).val(parseInt(current_value) - 1);
    })

    //add to cart buttons for offers products
    $(document).on('click', '.add_to_cart_button', function(e) {
        e.preventDefault();
        var prodid = $(this).attr('data-product_id');
        $.ajax({
            type: 'POST',
            url: "/cart/add/",
            data: {
                productid: prodid,
                productqty: 1,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: 'post',
            },
        success: function (json) {
            $('#basket-total-price').html(json.subtotal);
            $('#basket-qty').html(json.qty);
            location.href = "/cart/";
        },
        error: function (xhr, errmsg, err) {}
        });
    })

    $(document).on('change', '.input-text,qty,text', function(e) {
        e.preventDefault()
        var value = parseInt($(this).val());
        var max = parseInt($(this).attr("max"));
        if ($('#errors').hasClass('alert alert-success')) {
            $('#errors').removeClass('alert alert-success');
            $('#errors').html('');
        }
        if (value > max){
            $(this).val(max);
            $('#errors').addClass('alert alert-warning');
            $('#errors').html('You can not add more than '+ max +' items for this product.');
            return false
        }
        if (value < 1){
            $(this).val(1);
            $('#errors').addClass('alert alert-warning');
            $('#errors').html('Minimum number of items is 1.');
            return false
        }
    })
    
    $("#checkout").on("click", function(e){
        e.preventDefault();
    })
})