from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # path('', views.index, name='index'),
    path("create", views.DailyWorkSheetCreateAPIView.as_view()),
    path("retrieve/<pk>/", views.DailyWorkSheetRetrieveAPIView.as_view()),
    path("update/<pk>/", views.DailyWorkSheetUpdateAPIView.as_view()),
    path("delete/<pk>/", views.DailyWorkSheetDeleteAPIView.as_view()),
    path("list/", views.DailyWorkSheetListAPIView.as_view()),
    path("pdf/<pk>", views.DownloadView.as_view()),
    path("send-email-maisha/", views.email_tonny),
    path("send-email-maisha-attach/", views.email_tonny_attach),
]
