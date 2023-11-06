from django.urls import path
from biznews import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('post-by-category/<int:category_id>/', views.PostByCategoryView.as_view(), name="post-by-category"),
    path('post-by-tag/<int:tag_id>/', views.PostByTagView.as_view(), name="post-by-tag"),
    path('post-list/', views.PostListView.as_view(), name="post-list"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('comment/', views.CommentView.as_view(), name="comment"),
     path('post-search/', views.PostListView.as_view(), name="post-search"),
    
    
]
