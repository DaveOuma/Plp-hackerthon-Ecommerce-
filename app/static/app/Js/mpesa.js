$(document).ready(function() {
    $('#payment-form').on('submit', function(event) {
      event.preventDefault();
      var phone_number = $('#phone-number').val();
      var amount = $('#amount').val();
      $.ajax({
        url: '{% url "initiate_payment" %}',
        type: 'POST',
        dataType: 'json',
        data: {
          'phone_number': phone_number,
          'amount': amount,
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
          $('#payment-response').html(response.message);
        },
        error: function(xhr, errmsg, err) {
          $('#payment-response').html('An error occurred: ' + errmsg);
        }
      });
    });
  });