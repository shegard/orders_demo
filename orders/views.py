from datetime import datetime, timedelta

from django.db import connection
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import views, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import OrderItem


class ToOrderView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to='/order/')


class OrderView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response({}, template_name='orders/orders.html')


class ItemView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response({}, template_name='orders/items.html')


class OrderListView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):

        now = timezone.now()
        start = request.query_params.get('from', now - timedelta(days=30))
        end = request.query_params.get('to', now)
        if isinstance(start, str):
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
        if isinstance(end, str):
            end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')

        orders_items = OrderItem.objects.filter(order__created_date__range=[start, end]).order_by().values_list(
            'order__number', 'order__created_date',
            'product_name', 'product_price', 'amount'
        )
        items_by_order = {}
        for order_num, order_date, name, price, amount in orders_items:
            key = (order_num, order_date)
            if key not in items_by_order:
                items_by_order[key] = {
                    'total': 0,
                    'items': []
                }
            items_by_order[key]['total'] += price * amount
            items_by_order[key]['items'].append('{} x {}'.format(name, amount))

        orders = []
        for key, value in items_by_order.items():
            order_num, order_date = key
            price, items = value['total'], value['items']
            orders.append({
                'number': order_num,
                'date': order_date.strftime('%Y-%m-%d %H:%M'),
                'price': price,
                'items': items
            })

        queries = []
        for query in connection.queries:
            nice_sql = query['sql'].replace(',', ', ')
            sql = "[%s] %s" % (query['time'], nice_sql)
            queries.append(sql)

        return Response({'results': sorted(orders, key=lambda x: x['date'], reverse=True)[:100], 'queries': queries})


class OrderItemListView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):

        max_amount = OrderItem.objects.aggregate(Max('amount')).get('amount__max')
        top_items = OrderItem.objects.filter(amount=max_amount).order_by('-order__created_date').values_list(
            'product_name', 'product_price', 'order__created_date'
        )

        items = []
        for name, price, order_date in top_items:
            items.append({
                'name': name,
                'price': price,
                'order_date': order_date.strftime('%Y-%m-%d %H:%M'),
            })

        queries = []
        for query in connection.queries:
            nice_sql = query['sql'].replace(',', ', ')
            sql = "[%s] %s" % (query['time'], nice_sql)
            queries.append(sql)

        return Response({'results': items[:100], 'queries': queries})
