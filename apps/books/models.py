from __future__ import unicode_literals

from django.db import models

class UserManager(models.Manager):
    def validate(self, data):
        errors = []
        if len(data['username']) < 2:
            errors.append('The username is too short')
        if len(data['username']) > 45:
            errors.append('The username is too long')
        if len(errors)==0:
            try:
                user = self.get(username=data['username'])
                print "Found the user already"
                return (True, user)
            except:
                print "Creating the user"
                user = self.create(username=data['username'])
                return (True, user)
        return (False, errors) 
    
    def friending(self, friendid, userid):
        errors = []
        print "is friend", friendid, userid
        if int(friendid) == int(userid):
            print "same same"
            errors.append("You may not friend yourself. That's weird.")
        try:
            friend = self.get(id=friendid)
        except:
            errors.append('We cannot find your desired friend in our database')
        try:
            user = self.get(id=userid)
        except:
            errors.append('You must be logged in to be friends with our uploaders')
        if len(errors)==0:
            if user in friend.friendships.all():
                errors.append("You're already friends with this uploader!")
                return (False, errors)
            else:
                friend.friendships.add(user)
                return (True, friend)
        return (False, errors)

    def unfriending(self, friendid, userid):
        errors = []
        if int(friendid) == int(userid):
            errors.append("You may not unriend yourself. That's weird.")
        try:
            friend = self.get(id=friendid)
        except:
            errors.append('We cannot find your former friend in our database')
        try:
            user = self.get(id=userid)
        except:
            errors.append('You must be logged in to unfriend our uploaders')
        if len(errors)==0:
            if user not in friend.friendships.all():
                errors.append("You're already not friends with this uploader!")
                return (False, errors)
            else:
                friend.friendships.remove(user)
                return (True, friend)
        return (False, errors)


class BookManager(models.Manager):
    def validate(self, data, id):
        errors = []
        if len(data['title']) < 2:
            errors.append('The book title is too short')
        if len(data['title']) > 45:
            errors.append('The book title is too long')
        try:
            user = User.objects.get(id=id)
            print "Hey we found the user"
        except:
            errors.append('You must be logged in to create a book')
            print "We couldn't find the user"
        if len(errors) == 0:
            newbook = self.create(name=data['title'], desc=data['desc'], uploader=user)
            return (True, newbook)
        else:
            return (False, errors)
    
    def createlike(self, bookid, userid):
        errors = []
        try:
            book = self.get(id=bookid)

        except:
            errors.append('This book does not exist in our database')
        try:
            user = User.objects.get(id=userid)
        except:
            errors.append('You must be logged in to like a book')
        if len(errors) == 0:
            if user in book.likers.all():
                errors.append("You already liked this book!")
                return (False, errors)
            else:
                book.likers.add(user)
                return (True, book)
        else:
            return (False, errors)
    
    def removelike(self, bookid, userid):
        errors = []
        try:
            book = self.get(id=bookid)
        except:
            errors.append('This book does not exist in our database')
        try:
            user = User.objects.get(id=userid)
        except:
            errors.append('You must be looged in to unlike a book')
        if len(errors) == 0:
            if user not in book.likers.all():
                errors.append("You can't unlike this book without liking it first!")
                return (False, errors)
            else:
                book.likers.remove(user)
                return (True, book)
        else:
            return (False, errors)
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 45)
    friendships = models.ManyToManyField('self')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    name = models.CharField(max_length = 45)
    desc = models.CharField(max_length = 225)
    uploader = models.ForeignKey(User, related_name="books_uploaded")
    likers = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
