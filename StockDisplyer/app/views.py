"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from newscatcher import Newscatcher
from datetime import datetime
import pymysql
import sshtunnel
from app.forms import Signup

def signup(request):
    form = Signup(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            try:
                if not User.objects.filter(username=form.cleaned_data['username']).exists():
                    with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                                      ssh_username='Bigbusiness', ssh_password='Mistamonsta!@',
                                                      remote_bind_address=('Bigbusiness.mysql.pythonanywhere-services.com', 3306)) as tunnel:
                        connection = pymysql.connect(user='Bigbusiness', password='Database123',
                                                     host='127.0.0.1', port=tunnel.local_bind_port,
                                                     database='Bigbusiness$StockDatabase',)
                        Cursor = connection.cursor()
                        Cursor.execute("""INSERT INTO UserAccount(username, first_name, last_name, email, password1, password2) VALUES (%s,%s,%s,%s,%s,%s)""",
                                       (form.cleaned_data['username'], form.cleaned_data['first_name'], form.cleaned_data['last_name'], form.cleaned_data['email'],form.cleaned_data['password1'],form.cleaned_data['password2']))
                        connection.commit()
                        user = form.save()
                        user.refresh_from_db()
                        username = form.cleaned_data['username']
                        raw_password = form.cleaned_data['password1']
                        user = authenticate(username=username,password=raw_password)
                        login(request,user)
                        return redirect('home')
                else:
                    return  render(request, 'app/signup.html', {'formError': form.error_messages,'title':'Signup'})
                pass
            except:
                return  render(request, 'app/signup.html', {'formError': form.error_messages,'title':'Signup'})
            pass
        else:
            return  render(request, 'app/signup.html', {'formError': form.error_messages,'title':'Signup'})
        pass
    else:
        return  render(request, 'app/signup.html',{'title':'Signup'})
    pass
    return  render(request, 'app/signup.html', {'form': form,'title':'Signup'})
    pass

def login_user(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                ssh_username='Bigbusiness', ssh_password='Mistamonsta!@',
                remote_bind_address=('Bigbusiness.mysql.pythonanywhere-services.com', 3306)) as tunnel:
                connection = pymysql.connect(user='Bigbusiness', password='Database123',
                    host='127.0.0.1', port=tunnel.local_bind_port,
                    database='Bigbusiness$StockDatabase',)
                Cursor = connection.cursor()
                Cursor.execute("SELECT first_name,last_name,username,email,password1 FROM UserAccount Where username LIKE %s", ("%" + username + "%",))
                Result = Cursor.fetchall()
                connection.close()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'app/login_user.html',{'title':'login'})
        except Exception as E:
            print(E)
            return render(request, 'app/login_user.html',{'title':'login'})
        pass
    else:
        return render(request, 'app/login_user.html',{'title':'login'})
    pass

@login_required(login_url='login')
def home(request):
    with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
        ssh_username='Bigbusiness', ssh_password='Mistamonsta!@',
        remote_bind_address=('Bigbusiness.mysql.pythonanywhere-services.com', 3306)) as tunnel:
        connection = pymysql.connect(user='Bigbusiness', password='Database123',
            host='127.0.0.1', port=tunnel.local_bind_port,
            database='Bigbusiness$StockDatabase',)
        Cursor = connection.cursor()
        Cursor.execute("SELECT Symbol,Name,Last,stockchange,Chg,chgD,stockHigh,stockLow,VOLUME,stockTime FROM Stock")
        Result = Cursor.fetchall()
        connection.close()
        assert isinstance(request, HttpRequest)
        return render(request,
            'app/index.html',
            {'title':'Home','year':datetime.now().year,'DbResult':Result,
             })

def news(request):
    newstitle = []
    newslink = []
    publishdate = []
    imagelink = []
    websitelist = ['https://finance.yahoo.com/', 'https://edition.cnn.com/']
    topiclist = ['finance', 'news']
    webtopic = 0
    while webtopic < len(websitelist):
        fy = Newscatcher(website=websitelist[webtopic], topic=topiclist[webtopic])
        results = fy.get_news()
        articles = results['articles']
        for Items in articles:
            try:
                newstitle.append(Items.get('title'))
            except:
                newstitle.append('n/a')
            pass
            try:
                newslink.append(Items.get('link'))
            except:
                newslink.append('n/a')
            pass
            try:
                publishdate.append(Items.get('published'))
            except:
                publishdate.append('n/a')
            pass
            try:
                imagelink.append(Items.get('media_content').__getitem__(0).get('url'))
            except:
                imagelink.append('n/a')
            pass
        pass
        webtopic += 1
    pass
    return render(request,
        'app/news.html',
        {
            'title':'News',
            'newsResult':list(zip(newstitle,newslink,publishdate,imagelink))
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
