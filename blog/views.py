from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = search_post_file()
    print(posts)
    return render(request, 'blog/post_list.html', {'posts': posts})

from django.shortcuts import render, get_object_or_404

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

from .forms import PostForm
from django.shortcuts import redirect

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

import os
import re
import json

def search_post_file():
    filenames = os.listdir('./blog/templates/blog/posts')
    return get_file_info_list(filenames)

def get_file_info_list(filenames):
    file_info_list = []
    regex = re.compile(r'<!--\{(.|\n|\r)*\}-->')
    for filename in filenames:
        if(filename.endswith('.html')):
            f = open('./blog/templates/blog/posts/'+filename, 'r')
            data = f.read()
            info = regex.search(data).group().replace('<!--', '').replace('-->', '')
            json_info = json.loads(info)
            file_info_list.append(json_info)
            f.close()
    return file_info_list
