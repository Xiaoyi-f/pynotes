from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    """文章分类模型"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=50, verbose_name='标签名称')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """文章模型 - 核心模型"""
    # 文章状态选择
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL标识')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    
    # 分类和标签关系
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='posts', verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='标签')
    
    # 状态和时间字段
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    
    # SEO相关字段
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='SEO描述')
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']  # 按创建时间倒序排列
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """获取文章绝对URL"""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """保存时自动设置发布时间"""
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        """判断文章是否已发布"""
        return self.status == 'published' and self.published_at and self.published_at <= timezone.now()


class Comment(models.Model):
    """评论模型"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='评论时间')
    is_approved = models.BooleanField(default=False, verbose_name='是否审核通过')
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.author.username} 对 {self.post.title} 的评论'


class UserProfile(models.Model):
    """用户资料扩展模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    website = models.URLField(blank=True, verbose_name='个人网站')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f'{self.user.username} 的资料'
    
    def get_avatar_url(self):
        """获取头像URL"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'  # 默认头像


# 信号处理器：创建用户时自动创建用户资料
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# 信号处理器：保存用户时同时保存用户资料
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# 注册信号
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)


# 为已有用户创建资料（如果不存在）
def create_profiles_for_existing_users():
    """为系统中已有的用户创建资料"""
    for user in User.objects.all():
        try:
            user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)


# 在应用启动时执行
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        # 导入信号处理器
        import blog.models
        # 为已有用户创建资料
        from django.db import transaction
        with transaction.atomic():
            create_profiles_for_existing_users()