from django.db import models


# region Order
class Order(models.Model):

    number = models.BigIntegerField(verbose_name='Number')
    created_date = models.DateTimeField(verbose_name='Created date')

    # region std
    def __str__(self):
        return 'Order{:0>9}'.format(self.number)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    # endregion

    # region properties
    # endregion

    # region methods
    # endregion

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
# endregion


# region OrderItem
class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Order')
    product_name = models.CharField(max_length=20, verbose_name='Product name')
    product_price = models.FloatField(verbose_name='Product price')
    amount = models.IntegerField(verbose_name='Amount')

    # region std
    def __str__(self):
        return self.product_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    # endregion

    # region properties
    # endregion

    # region methods
    # endregion

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
# endregion
