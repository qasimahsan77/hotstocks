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
            return  render(request, 'app/signup.html', {'formError': form.error_messages})
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
                    return render(request, 'app/login_user.html')
        except Exception as E:
            print(E)
            return render(request, 'app/login_user.html')
        pass
    else:
        return render(request, 'app/login_user.html')
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
            {'title':'Home Page','year':datetime.now().year,'DbResult':Result,
             })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
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
