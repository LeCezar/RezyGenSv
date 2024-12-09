from django.urls import include, path
from rest_framework import routers

from chatai import views

app_name = "chatai"

router = routers.DefaultRouter()
router.register(r'authorTypes', views.AuthorTypeViewSet)
router.register(r'conversations', views.ConversationViewSet)

urlpatterns = [
    path("api/", include(router.urls), name="index"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
