import os
from datetime import datetime, timedelta, timezone as datetime_tz
from random import randint, uniform

from django.core.management.base import BaseCommand
from django.core.management.color import supports_color
from django.db.models import Count, Max
from django.db.models.functions import Coalesce

from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Creates orders for testing'

    @property
    def colors(self):
        b = supports_color() or os.environ.get('PYCHARM_HOSTED') or os.environ.get('PYCHARM_DJANGO_MANAGE_MODULE')
        return {
            'red': '\033[031m' if b else '',
            'green': '\033[032m' if b else '',
            'yellow': '\033[033m' if b else '',
            'reset': '\033[0m' if b else ''
        }

    def add_arguments(self, parser):
        parser.add_argument('amount', nargs='?', default=50, type=int, help='amount to create', metavar='N')

    def handle(self, *args, **options):

        reference = datetime(2018, 1, 1, 9, 0, 0, 0, datetime_tz.utc)
        new_order_number = Order.objects.order_by().aggregate(max_number=Coalesce(Max('number'), 0))['max_number'] + 1
        new_orders_amount = options['amount']

        orders_to_create = []
        for i in range(new_orders_amount):
            num = new_order_number + i
            orders_to_create.append(Order(
                number=num,
                created_date=reference + timedelta(hours=num - 1)
            ))
        orders = Order.objects.bulk_create(orders_to_create)

        # to get id (non-PostgreSQL db)
        orders = (Order.objects.filter(number__gte=new_order_number)
                  # .annotate(cnt_items=Count('items')).filter(cnt_items=0)
                  .order_by('id'))

        order_items_to_create = []
        for order_id, order_number in orders.values_list('id', 'number'):
            for i in range(randint(1, 5)):
                order_items_to_create.append(OrderItem(
                    order_id=order_id,
                    product_name='Товар{}-{}'.format(order_number, i + 1),
                    product_price=uniform(100, 9999),
                    amount=randint(1, 10)
                ))
        items = OrderItem.objects.bulk_create(order_items_to_create)

        print('Created {} orders and {} order items'.format(len(orders_to_create), len(order_items_to_create)))
