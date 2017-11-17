from django.shortcuts import render
from .models import Book, User

# Create your views here.
def index(request):
    # User.objects.get(id=1).friendships.add(User.objects.get(id=2))
    # User.objects.get(id=2).friendships.add(User.objects.get(id=3))
    friends = User.objects.get(id=1).friendships.all()
    User.objects.get(id=2).friendships.add(User.objects.get(id=1))
    User.objects.get(id=1).friendships.add(User.objects.get(id=1))
    gfriends = User.objects.get(id=2).friendships.all()

    # get all the books
    allbooks = Book.objects.all()
    # who uploaded the first book?

    uploader = Book.objects.first().uploader

    # Get all the books uploaded by the first user

    books = User.objects.first().books_uploaded.all()
    
    # Get all the likers of the first book
    likers = Book.objects.get(id=1).likers.all()

    # Get all the books liked by the first user
    # Book.objects.get(id=3).likers.add(User.objects.get(id=1))
    first_books = User.objects.get(id=1).liked_books.all()
    
    
   
    print Book.objects.all()
   
    context = {
        'allbooks':allbooks,
        'first_uploader': uploader,
        'books_by_first': books,
        'first_likers':likers,
        'first_user_likes':first_books,
        'first_friends': friends,
        'gonzo_friends': gfriends
    }
    return render(request, 'books/index.html', context)