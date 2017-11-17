from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Book, User

# Create your views here.
def index(request):
    context = {}
    if 'userid' not in request.session:
        context['logged'] = False
    else:
        context['user'] = User.objects.get(id=request.session['userid'])
        context['logged'] = True
        
    context['books'] = Book.objects.annotate(like_count = Count('likers'))
    
    print "all users", User.objects.all()
    

    print "all book", Book.objects.all()
   

    return render(request, 'books/index.html', context)

def join(request):
    if request.method=="POST":
        result = User.objects.validate(request.POST)
        if result[0]:
            request.session['userid'] = result[1].id
        else:
            messages.warning(request, "Your username must be between 2 and 45 characters long")

    return redirect('/')

def create(request):
    if request.method == "POST":
        if 'userid' not in request.session:
            print "We're not in session in the views"
            messages.warning(request, "You must be logged in to add a book")
        else:
            result = Book.objects.validate(request.POST, request.session['userid'])
            if result[0] == False:
                for message in result[1]:
                    messages.warning(request, message)
            else:
                messages.success(request, "We added your book to our database!")
        
    return redirect('/')

# This is a get request! All the information needed to create a like is in the url and session. Therefore, someone can reach this route just by typing into the nav bar. What if they try to go to /like/777, does this book id exist? What will happen if you're not guarding against this?
def addlike(request, id):
    if 'userid' not in request.session:
        messages.warning(request, "You must be logged in to like a book")
        return redirect('/')
    result = Book.objects.createlike(id, request.session['userid'])
    if result[0] == False:
        for m in result[1]:
            messages.warning(request, m)
    return redirect('/')

def removelike(request, id):
    if 'userid' not in request.session:
        messages.warning(request, "You must be logged in to like a book")
        return redirect('/')
    result = Book.objects.removelike(id, request.session['userid'])
    if result[0] == False:
        for m in result[1]:
            messages.warning(request, m)
    return redirect('/')

def addfriend(request, id):
    if 'userid' not in request.session:
        messages.warning(request, "You must be logged in to be friends with our uploaders")
        return redirect('/')
    result = User.objects.friending(id, request.session['userid'])
    if result[0] == False:
        for m in result[1]:
            messages.warning(request, m)
    return redirect('/')

def removefriend(request, id):
    if 'userid' not in request.session:
        messages.warning(request, "You must be logged in to unfriend our uploaders")
        return redirect('/')
    result = User.objects.unfriending(id, request.session['userid'])
    if result[0] == False:
        for m in result[1]:
            messages.warning(request, m)
    return redirect('/')

def show(request, id):
    context = {}
    if 'userid' in request.session:
        context['logged'] = True
        context['user'] = User.objects.get(id=request.session['userid'])
    try:
        theuser = User.objects.get(id=id)
        context['show'] = theuser
        return render(request, 'books/show.html', context)
    except:
        messages.warning(request, "We cannot show any details about this user who doesn't exist in our database.")
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')