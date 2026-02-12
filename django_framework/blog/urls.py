from django.urls import path
from . import views

app_name = 'blog'  # 应用命名空间

urlpatterns = [
    # 文章相关URL
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # 分类和标签URL
    path('category/<int:pk>/', views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<int:pk>/', views.TagPostListView.as_view(), name='tag_posts'),
    
    # 搜索URL
    path('search/', views.SearchPostListView.as_view(), name='search'),
    
    # 评论URL
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    
    # 用户资料URL
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # AJAX功能URL
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
]