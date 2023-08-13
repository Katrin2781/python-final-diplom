from django.urls import path
from shop_backend.views import PartnerUpdate


app_name = 'shop_backend'
urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    ]