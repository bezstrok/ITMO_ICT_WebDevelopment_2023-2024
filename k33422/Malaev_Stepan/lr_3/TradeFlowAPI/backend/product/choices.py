from django.db import models
from django.utils.translation import gettext_lazy as _


class TradeStatus(models.TextChoices):
    OPEN = 'open', _('Open')
    CLOSED = 'closed', _('Closed')
    PENDING = 'pending', _('Pending')
    
    @classmethod
    def unavailable(cls):
        return cls.CLOSED, cls.PENDING
