//'use strict';


var stripe = Stripe(STRIPE_PUBLIC_KEY);

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};

window.id = $("#id_addresses").val();
$(document).on("change", "#id_addresses", function() {
  window.id = $(this).children("option:selected").val()
})

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
  var displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
ev.preventDefault();


  $.ajax({
    type: "POST",
    url: 'http://localhost:8000/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
      address_id: id,
    },
    success: function (json) {
      console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1: json.add1,
                line2: json.add2,
                country: json.country,
                state: json.state,
                city: json.city,
            },
            name: json.first_name + ' ' + json.last_name,
          },
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
          var displayError = document.getElementById('card-errors');
          displayError.textContent = result.error.message;
          $('#card-errors').addClass('alert alert-danger');
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://localhost:8000/payment/orderplaced/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) {
      window.location.replace("http://localhost:8000/payment/error/")
    },
  });



});
