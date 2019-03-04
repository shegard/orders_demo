let queries_holder = $('.queries_holder');
let tbody = $(`#items_table tbody`);

$.ajax({
  url: `/items/`,
  type: 'GET',
  dataType: 'json',
  contentType: 'application/json',
  beforeSend: function (jqXHR, settings) {
  },
  success: function (data, textStatus, jqXHR) {
    queries_holder.empty();
    tbody.empty();

    let queries = data['queries'], items = data['results'];

    queries_holder.append($(`<p>Queries: ${queries.length}</p>`));
    queries_holder.append($(`<p>${queries.join('</p><p>')}</p>`));

    for (let item of items) {
      let row = $(`<tr><td>${item['name']}</td><td>${item['price'].toFixed(2)}</td><td>${item['order_date']}</td></tr>`);
      tbody.append(row);
    }

  },
  error: function (jqXHR, textStatus, errorThrown) {
  },
  complete: function (jqXHR, textStatus) {
  }
});

