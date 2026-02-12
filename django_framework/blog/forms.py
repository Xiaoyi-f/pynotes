from django import forms
from .models import Post, Comment, UserProfile
from django.utils.text import slugify
import uuid

class PostForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'status', 'meta_description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入文章标题'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '请输入文章内容'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'SEO描述，有助于搜索引擎优化'
            }),
        }
    
    def save(self, commit=True):
        """保存时自动生成slug"""
        instance = super().save(commit=False)
        if not instance.slug:
            # 生成唯一的slug
            base_slug = slugify(instance.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            instance.slug = slug
        
        if commit:
            instance.save()
            self.save_m2m()  # 保存多对多关系（tags）
        return instance


class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入您的评论...'
            }),
        }


class ProfileForm(forms.ModelForm):
    """用户资料表单"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'website', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '介绍一下自己吧...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '所在城市'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果avatar字段存在，添加文件输入样式
        if 'avatar' in self.fields:
            self.fields['avatar'].widget.attrs.update({
                'class': 'form-control'
            })