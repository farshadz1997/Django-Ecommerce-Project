//'use strict';


var stripe = Stripe('pk_test_51LABjGJ95xMRPOPu7R5TnmrhGVXbvTMDTHGZOjcuPQNuNJ0NPOZkzcWuPhtyNKXEGx9D13xs9pi4IR1vxaPz0njR00XArZFN6S');

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

var FirstName = document.getElementById("id_first_name").value;
var LastName = document.getElementById("id_last_name").value;
var PhoneNumber = document.getElementById("id_phone_number").value;
var Add1 = document.getElementById("id_address_line_1").value;
var Add2 = document.getElementById("id_address_line_2").value;
var country = document.getElementById("id_country").value;
var state = document.getElementById("id_state").value;
var city = document.getElementById("id_town_city").value;
var email = document.getElementById("id_email").value;
var postcode = document.getElementById("id_postcode").value;


  $.ajax({
    type: "POST",
    url: 'http://localhost:8000/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
      full_name: FirstName + ' ' + LastName,
      phone_number: PhoneNumber,
      add1: Add1,
      add2: Add2,
      city: city,
      post_code: postcode,
    },
    success: function (json) {
      console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:Add1,
                line2:Add2,
                country:country,
                state:state,
                city:city,
            },
            name: FirstName + ' ' + LastName
          },
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
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
      windows.location.replace("http://localhost:8000/payment/error/")
    },
  });



});
