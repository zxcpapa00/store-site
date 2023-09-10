from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from products.models import Basket
from .forms import OrderForm
from .models import Order
from common.views import TitleMixin
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET


class SuccessView(TitleMixin, TemplateView):
    """Успешное оформление заказа"""
    template_name = 'orders/success.html'
    title = 'Спасибо за заказ'


class CancelView(TitleMixin, TemplateView):
    """Ошибка заказа"""
    template_name = 'orders/cancel.html'


class OrderCreateView(TitleMixin, CreateView):
    """Создание заказа"""
    model = Order
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create')
    title = 'Оформление заказа'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=303)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = session.metadata.order_id
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
    print("Fulfilling order")


class OrdersView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Заказы'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user).order_by('-created')
        return orders


class DetailOrderView(DetailView):
    model = Order
    template_name = 'orders/order.html'



