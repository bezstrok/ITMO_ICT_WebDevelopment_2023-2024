from django.db import models
from django.utils import timezone

from backend.broker.models import Broker
from backend.product.choices import TradeStatus
from backend.product.models import ProductBatch
from backend.utils.models import AbstractTimeStampedModel


class Trade(AbstractTimeStampedModel):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=TradeStatus.choices, default=TradeStatus.OPEN)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='trades')
    product_batch = models.ForeignKey(ProductBatch, on_delete=models.CASCADE, related_name='trades')
    
    @property
    def is_closed(self):
        return self.status == TradeStatus.CLOSED
    
    def save(self, *args, **kwargs):
        if self.status == TradeStatus.CLOSED and not self.end_time:
            self.end_time = timezone.now()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Trade {self.id}"
