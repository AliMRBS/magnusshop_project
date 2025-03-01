from django.db import models
from django.contrib.auth.models import User
import json
import uuid
from django.utils import timezone
from finance.utils.aghayepardakht import apardakht_request_handler, apardakht_payment_checker


class Gateway(models.Model):
    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_ZARINPAL = 'zarinpal'
    FUNCTION_PARSIAN = 'parsian'
    FUNCTION_AGHAYEPARDAKHT = 'aghayepardakht'

    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, 'Saman'),
        (FUNCTION_SHAPARAK, 'Shaparak'),
        (FUNCTION_ZARINPAL, 'Zarinpal'),
        (FUNCTION_PARSIAN, 'Parsian'),
        (FUNCTION_AGHAYEPARDAKHT, 'Aghayepardakht'),
    )

    title = models.CharField(max_length=100, verbose_name="gateway title")
    gateway_request_url = models.CharField(max_length=150, verbose_name="request url", null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name="verify url", null=True, blank=True)
    gateway_code = models.CharField(max_length=15, verbose_name="gateway code", choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(verbose_name="is enable", default=True)
    auth_data = models.TextField(verbose_name="auth_data", null=True, blank=True)

    class Meta:
        verbose_name = "Gateway"
        verbose_name_plural = "Gateways"

    def __str__(self):
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_ZARINPAL: None,
            self.FUNCTION_PARSIAN: None,
            self.FUNCTION_AGHAYEPARDAKHT: apardakht_request_handler,
        }
        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_ZARINPAL: None,
            self.FUNCTION_PARSIAN: None,
            self.FUNCTION_AGHAYEPARDAKHT: apardakht_payment_checker,
        }
        return handlers[self.gateway_code]

    @property
    def credentials(self):
        return json.loads(self.auth_data)


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name="invoice_number", unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(verbose_name="payment amount", editable=True)
    gateway = models.ForeignKey(Gateway, related_name="payments", null=True, blank=True, verbose_name="gateway", on_delete=models.SET_NULL)
    is_paid = models.BooleanField(verbose_name="is paid status", default=False)
    payment_log = models.TextField(verbose_name="logs", blank=True)
    user = models.ForeignKey(User, verbose_name="USER", null=True, on_delete=models.SET_NULL)
    transid = models.CharField(max_length=64, verbose_name="transid", blank=True)


    class Meta:
        verbose_name = "Payments"
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.invoice_number.hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid

    def get_handler_data(self):
        return dict(
            amount=self.amount,
            mobile=getattr(self.user, 'mobile', None),
            email=self.user.email,
            description=str(self.title),
            callback_url='http://127.0.0.1:8000/finance/verify/',
            )

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            data = self.get_handler_data()
            link, transid = handler(**data)
            if transid is not None:
                self.transid = transid
                self.save()
            return link

    @property
    def title(self):
        return str("Instant payment")

    def status_changed(self):
        return self.is_paid != self._b_is_paid

    def verify(self, data):

        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            result = handler(**data)
            self.is_paid = result[0]
            self.save()        
        return self.is_paid
        

    @classmethod
    def get_gateway(cls):
        return Gateway.objects.filter(is_enable=True).first()

    
    def save_log(self, data, scope='Request handler', save=True):
        generated_log = "[{}][{}] {}\n".format(timezone.now(), scope, data)
        if self.payment_log != '':
            self.payment_log += generated_log
        else:
            self.payment_log = generated_log
        if save:
            self.save()