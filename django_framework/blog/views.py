from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Post, Category, Tag, Comment, UserProfile
from .forms import PostForm, CommentForm, ProfileForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.


class PostListView(ListView):
    """文章列表视图 - 使用类视图"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5  # 每页显示5篇文章
    
    def get_queryset(self):
        """获取已发布的文章"""
        return Post.objects.filter(status='published', published_at__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        """添加额外的上下文数据"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['popular_posts'] = Post.objects.filter(status='published').order_by('-views_count')[:5]
        return context


class PostDetailView(DetailView):
    """文章详情视图"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get_queryset(self):
        """只能查看已发布的文章"""
        return Post.objects.filter(status='published', published_at__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        """添加评论表单和相关数据"""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id)[:3]
        return context
    
    def get(self, request, *args, **kwargs):
        """增加浏览次数"""
        response = super().get(request, *args, **kwargs)
        # 增加浏览次数
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return response


class PostCreateView(LoginRequiredMixin, CreateView):
    """创建文章视图"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """表单验证成功时设置作者"""
        form.instance.author = self.request.user
        messages.success(self.request, '文章创建成功！')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新文章视图"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """表单验证成功时添加提示信息"""
        messages.success(self.request, '文章更新成功！')
        return super().form_valid(form)
    
    def test_func(self):
        """权限检查：只有作者才能编辑"""
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """删除文章视图"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        """删除成功时添加提示信息"""
        messages.success(self.request, '文章删除成功！')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """权限检查：只有作者才能删除"""
        post = self.get_object()
        return self.request.user == post.author


class CategoryPostListView(ListView):
    """分类文章列表视图"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """根据分类筛选文章"""
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(
            category=category,
            status='published',
            published_at__lte=timezone.now()
        )
    
    def get_context_data(self, **kwargs):
        """添加当前分类信息"""
        context = super().get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


class TagPostListView(ListView):
    """标签文章列表视图"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """根据标签筛选文章"""
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return Post.objects.filter(
            tags=tag,
            status='published',
            published_at__lte=timezone.now()
        )
    
    def get_context_data(self, **kwargs):
        """添加当前标签信息"""
        context = super().get_context_data(**kwargs)
        context['current_tag'] = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return context


class SearchPostListView(ListView):
    """搜索文章列表视图"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """根据搜索关键词筛选文章"""
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                status='published',
                published_at__lte=timezone.now()
            ).distinct()
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        """添加搜索关键词"""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


@login_required
def add_comment(request, slug):
    """添加评论功能 - 函数视图"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论发表成功！')
            return redirect('blog:post_detail', slug=slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})


@login_required
def profile_view(request):
    """用户资料查看视图"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'blog/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    """用户资料编辑视图"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '资料更新成功！')
            return redirect('blog:profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'blog/profile_edit.html', {'form': form})


@require_POST
@login_required
def like_post(request, slug):
    """点赞文章功能 - AJAX"""
    post = get_object_or_404(Post, slug=slug)
    # 这里可以实现点赞逻辑，比如使用Redis或数据库记录
    # 为了简化，我们只是返回当前浏览次数作为示例
    data = {
        'success': True,
        'likes': post.views_count,  # 临时使用浏览次数作为点赞数
        'message': '点赞成功！'
    }
    return JsonResponse(data)
