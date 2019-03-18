from django.urls import path, include
from .views import *

urlpatterns = [
    path('', CommonView.as_view(template_name="provernalog/index.html", title="Главная"), name="index"),
    path('add-service/', CommonView.as_view(template_name="provernalog/add_service.html", title="О сервисе"), name="add_service"),
    path('search-res/', SearchView.as_view(), name="search_res"),
    path('privacy-policy/', CommonView.as_view(template_name='provernalog/privacy.html',
                                               title="Политика конфиденциальности"), name="privacy"),
    path('analytics/', analytics, name="analytics"),
    path('analytics/<str:region>/', analytics, name="analytics_region"),
    path('report/<int:report_id>/', report, name="report"),
]
