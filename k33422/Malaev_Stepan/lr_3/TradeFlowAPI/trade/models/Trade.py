from django.db import models
from django.utils.translation import gettext_lazy as _

from .audit import TimeStampedModel


class TradeStatus(models.TextChoices):
    OPEN = 'open', _('Open')
    CLOSED = 'closed', _('Closed')
    PENDING = 'pending', _('Pending')


class Trade(TimeStampedModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=15, choices=TradeStatus.choices, default=TradeStatus.OPEN)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    broker = models.ForeignKey('Broker', on_delete=models.CASCADE)
    product_batch = models.ForeignKey('ProductBatch', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Trade {self.id}"
