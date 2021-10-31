from django.urls import path
from . import views


urlpatterns = [
       path("", views.MainPageView.as_view(), name="main_page"),
       path("posts", views.PostsView.as_view(), name="posts"),
       path("posts/<slug:slug>", views.IndividualPageView.as_view(), name="individual_page"),
       path("read-later", views.ReadMeLateView.as_view(), name="read-later")


]
