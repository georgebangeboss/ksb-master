from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("create", views.DailyWorkSheetCreateAPIView.as_view()),
    path("retrieve/<pk>/", views.DailyWorkSheetRetrieveAPIView.as_view()),
    path("update/<pk>/", views.DailyWorkSheetUpdateAPIView.as_view()),
    path("delete/<pk>/", views.DailyWorkSheetDeleteAPIView.as_view()),
    path("list/", views.DailyWorkSheetListAPIView.as_view()),
    path("printpdf/<pk>", views.DownloadView.as_view()),
]
