# 路由分支系统
# py manage.py runserver 启动项目
# py manage.py startapp name 创建新的应用
# namespace:name
# kwargs={key: value}
# views目录下放渲染函数 <type: name> -> int str(默认) slug uuid
# templates放前端模板文件
# 为了后期的维护方便和模板开发，我们可以将templates创建在对应的应用中
"""
# DTL(Django Templates Language)语法:
CSRF保护：{% csrf_token %} 是Django防止跨站请求伪造的安全措施，用于防御恶意网站的攻击。
表单必需：在POST表单中必须添加{% csrf_token %}，否则Django会返回403错误。
自动生成：它会自动生成一个隐藏的input字段，包含加密的token值。
自动验证：Django中间件会自动验证这个token，无需手动处理。
URL反向解析：{% url 'url_name' %} 根据URL配置中的name属性生成真实URL。
解耦优势：修改URL路径时只需改urls.py，模板中的{% url %}会自动更新。
带参数URL：可传参：{% url 'article_detail' article.id %}。
命名空间：支持命名空间：{% url 'app_name:view_name' %}。
模板链接：常用于<a href="{% url 'home' %}">和<form action="{% url 'submit' %}">。
配合使用：通常表单中同时使用两者：<form action="{% url 'submit' %}" method="post">{% csrf_token %}。
继承特性

引用:
{{ var_name }} 字典使用点号语法

标签:
{% if %}
{% elif %}
{% else %}
{% endif %}

{% for %}
{% empty %} -> 判空
{% endfor %}

{% with simplekey=key %}
{% endwith %}

{% spaceless %}
{% endspaceless %}

# 转义与否
{% autoescape on/off %}
{% endautoescape %}

# 常用过滤器
{{ var_name | add:num }}
{{ var_name | cut:str_demo }}
{{ var_name | default:default_value }} # 值为False
{{ var_name | default_if_none:default_value }}
{{ var_name | floatformat:n }}
{{ var_name | truncatechars:n }}

# 包含
{% include demo.html with name=value %}

# 继承
father.html
{% block name %}
{% endblock %}

son.html
{% extends 'father.html' %}
{% block name %}
content
{% endblock %}

# 静态资源加载
{% load static %}
{% static 'demo.js' %}
"""

# 主软件包内容: urls wsgi asgi __init__ settings
# 在主软件包的settings中进行项目的设置/配置:
"""
# 新建软件包内容: migrations包 __init__ admin apps models tests urls views
# 路由配置:
# from django.shortcuts import render -> return render(request, "index.html", context={name: value}
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import path, include, reverse
# from django.contrib import admin
# from django.conf.urls.static import static
# urlpatterns = [...] + static(settings.MEDIA_URL, document_root_settings.MEDIA_ROOT)
"""

