let now = new Date();
let utc_now = moment.tz(now, 'UTC');
let utc_30days_ago = utc_now.clone().subtract(30, 'days');

$(`#from_input`).val(utc_30days_ago.format('YYYY-MM-DDTHH:mm'));
$(`#to_input`).val(utc_now.format('YYYY-MM-DDTHH:mm'));


let queries_holder = $('.queries_holder');
let filters_holder = $('.filters_holder');
let tbody = $(`#orders_table tbody`);
filters_holder.on('click', 'button', function (e) {

  let from = moment.tz($(`#from_input`).val(), 'UTC');
  let to = moment.tz($(`#to_input`).val(), 'UTC');
  let qp = {'from': from.format('YYYY-MM-DDTHH:mm:ssZZ'), 'to': to.format('YYYY-MM-DDTHH:mm:ssZZ')};

  $.ajax({
    url: `/orders/`,
    type: 'GET',
    dataType: 'json',
    contentType: 'application/json',
    data: qp,
    beforeSend: function (jqXHR, settings) {
    },
    success: function (data, textStatus, jqXHR) {
      queries_holder.empty();
      tbody.empty();

      let queries = data['queries'], orders = data['results'];

      queries_holder.append($(`<p>Queries: ${queries.length}</p>`));
      queries_holder.append($(`<p>${queries.join('</p><p>')}</p>`));

      for (let order of orders) {
        let row = $(`<tr><td>${order['date']}</td><td>${order['number']}</td><td>${order['price'].toFixed(2)}</td><td>${order['items'].join('<br>')}</td></tr>`);
        tbody.append(row);
      }

    },
    error: function (jqXHR, textStatus, errorThrown) {
    },
    complete: function (jqXHR, textStatus) {
    }
  });
});

filters_holder.find('button').click();
