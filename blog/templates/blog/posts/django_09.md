Django 임시저장 기능 만들기
===
 이번 포스트에서는 포스트를 생성하거나 수정 후 발행버튼을 눌러야만 포스트가 보이도록 수정해보겠습니다.
# 1. 생성, 수정시 발행시간이 현재시간으로 표시되는 부분 삭제
```python
# blog/views.py
def post_new(request):
...
            post.author = request.user
            post.published_date = timezone.now() # 삭제
            post.save()
...
def post_edit(request, pk):
...
            post.author = request.user
            post.published_date = timezone.now() # 삭제
            post.save()
...
```

# 2. 미발행된 포스트 목록 페이지 만들기
## 2.1. 기본 템플릿에 버튼 추가
```xml
# blog/templates/blog/base.html
            {% if user.is_authenticated %}
                <a href="{% url 'post_new' %}" class="top-menu"><span class="glyphicon glyphicon-plus"></span></a>
                <a href="{% url 'post_draft_list' %}" class="top-menu"><span class="glyphicon glyphicon-edit"></span></a> # 추가
            {% endif %}
```
## 2.2. View 함수 추가
```python
# blog/views.py
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
```

## 2.3. 관련 템플릿 생성
```xml
# blog/templates/blog/post_draft_list.html
{% extends 'blog/base.html' %}

{% block content %}
    {% for post in posts %}
        <div class="post">
            <p class="date">created: {{ post.created_date|date:'d-m-Y' }}</p>
            <h1><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h1>
            <p>{{ post.text|truncatechars:200 }}</p>
        </div>
    {% endfor %}
{% endblock %}
```

## 2.4. Url 코드 추가
```python
# blog/urls.py
path('drafts', views.post_draft_list, name='post_draft_list'),
```

## 2.5. 결과 확인
![blog_main](images/django_blog/09/01_blog_main.png)
![blog_draft](images/django_blog/09/02_blog_draft.png)

# 3. 발행기능 만들기
## 3.1. 포스트 템플릿에 발행버튼 추가
```xml
# blog/templates/blog/post_detail.html
{% if post.published_date %}
    <div class="date">
        {{ post.published_date }}
    </div>
{% else %}
    <a class="btn btn-default" href="{% url 'post_publish' pk=post.pk %}">Publish</a>
{% endif %}
```

## 3.2. View 함수 추가
```python
# blog/views.py
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
```

## 3.3. 모델에 발행일을 저장하는 함수 추가
```python
# blog/models.py
def publish(self):
    self.published_date = timezone.now()
    self.save()
```

## 3.4. Url 코드 추가
```python
# blog/urls.py
url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
```
## 3.5. 결과 확인
![blog_before_publish](images/django_blog/09/03_blog_before_publish.png)
![blog_after_publish](images/django_blog/09/04_blog_after_publish.png)