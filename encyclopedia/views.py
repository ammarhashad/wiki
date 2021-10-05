from django.shortcuts import render
import markdown2
from . import util
import os
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import random


def upper_topic():
    global topics
    topics = util.list_entries()
    global topics_upper
    topics_upper = list(map(str.upper, topics))
    global dict_value
    dict_value = {}
    for (a, b) in zip(topics_upper, topics):
        dict_value[a] = b

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, name):
    topics = util.list_entries()
    dict_topic = {}
    dict_topic_captial = {}

    for top in topics:
        dict_topic_captial[top.upper()] = top
        html_page = markdown2.markdown(util.get_entry(top))
        dict_topic[top] = str(html_page)

    if name.upper() in dict_topic_captial.keys():
        return render(request,"encyclopedia/topic.html",{
            'topic_name': dict_topic_captial[name.upper()],
            'body':dict_topic[dict_topic_captial[name.upper()]]
        })
    return render(request,"encyclopedia/layout.html",{
        'error':'<h1 style="font-size:40px">Page not found</h1><br>Sorry, requested page was not found.'
    })

def search(request):
    upper_topic()
    search_title = request.GET.get('q')
    if search_title.upper() in topics_upper:
        return HttpResponseRedirect(reverse("topic", args=[dict_value[search_title.upper()]]))

    researh_list = []
    for t in topics_upper:
        if search_title.upper() in t:
            researh_list.append(dict_value[t])

    if researh_list:
        return render(request,'search/search.html',{
            'header':'Search Results',
            'Result':set(researh_list)
        })

    return render(request,'search/search.html',{
                'header':'Your search topic is not found',
                'masge':"This is the list of all topic we have",
                'Result':topics
            })


def create(request):
    return render(request, 'create/create.html')

def save_create(request):
    upper_topic()
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('textarea')
        if title.upper() in topics_upper:
            return render(request, 'create/exist.html',{
                'topic':dict_value[title.upper()]
            })

        util.save_entry(title, body)
        body = markdown2.markdown(util.get_entry(title))
        return render(request, 'encyclopedia/topic.html',{
            'body': body,
            'topic_name':title
        })

def edit(request):
    topic_name = request.GET.get('topic_name')
    body = util.get_entry(topic_name)
    return render(request, 'edit/edit.html',{
        'topic_title': topic_name,
        'body': body
    })

def save(request):
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('textarea')
        txt = ""
        c  = 0
        for i in body.split('\n'):
            if i == '\r' and body.split('\r')[c + 1] == '\n':
                continue
            txt += i
            c += 1
        util.save_entry(title, txt)
        body = markdown2.markdown(util.get_entry(title))
        return render(request, 'encyclopedia/topic.html',{
            'body': body,
            'topic_name':title
        })

def random_func(request):
    topics = util.list_entries()
    random_num = random.randint(0,len(topics) - 1)
    html_page = markdown2.markdown(util.get_entry(topics[random_num]))
    return render(request,"encyclopedia/topic.html",{
        'topic_name': topics[random_num],
        'body': html_page
    })
