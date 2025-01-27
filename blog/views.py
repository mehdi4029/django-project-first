import jdatetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.template.context_processors import request

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.template.loader import render_to_string
from pyexpat.errors import messages
from blog.models import *

# Create your views here.

def showMainPage(request):
      if request.user.is_authenticated :
        categoriesObjects = Category.objects.all()
        all_categories_published_self_posts = {}
        now = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        user_self_important = Post.objects.filter(Q(author=request.user, is_important=True , poststatus="published" ,publish_date__lt = now) | Q(author=request.user, is_important=True , poststatus="draft") ) [:4]
        important_news = Post.objects.filter(poststatus='published', is_important = True ,  publish_date__lt = now).exclude(author=request.user)[:4]
        for x in categoriesObjects:
              all_categories_published_self_posts.update(
                  {
                      x.name : Post.objects.filter(Q(category=x, publish_date__lt = now ,poststatus='published' ) | Q(category=x ,author=request.user, poststatus='draft'))[:4]
                  }
              )
        context = {
            'important_news' : important_news,
            'user_self_important' : user_self_important,
            'all_self_and_published_categories_published_posts' : list(all_categories_published_self_posts.items()),
        }
        # if other_users_post and user_self_posts and important_news:
      return HttpResponse(render(request , 'mainPage.html' , context))
def loginUser(request) :
     if not request.user.is_authenticated :
      return HttpResponse(render(request,'login.html' , {'next' : request.GET.get('next')}))
     else :
         return redirect('/blog/home')

def signInUser(request) :
      return  HttpResponse(render(request , 'sign-in.html'))
def validationForm(request) :
      if request.method == 'POST' :
          username = request.POST.get('username')
          password = request.POST.get('password')
          email = request.POST.get('email')
          if not User.objects.filter(username=username).exists() :
               return redirect('/blog/')

          user = authenticate(request , username = username , password = password)
          if (user is None) :
               return redirect('/blog/')
          if User.objects.filter(username=username)[0].email == email :
              login(request,user)
              return redirect('/blog/home/')
          return redirect('/blog/') #for default and preventing errors


def createUser(request) :
      if request.method == "POST" :
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            if User.objects.filter(username=username).exists() :
                 return redirect('blog/sign-in/')
            user = User.objects.create_user(username = username)
            user.email = email
            user.set_password(password)
            user.save()
      return redirect('/blog/')
def getUser(request,username):
       if User.objects.filter(username=username).exists():
           return JsonResponse({'message' : 'this username already taken'})
       else :
           return JsonResponse({'message' : 'user created succcessfully'})

def logoutUser(request) :
    logout(request)
    return redirect('/blog/')


def showPanel(request) :
    if not request.user.is_superuser :
         link_id =   link_id=['create-post-btn' , 'delete-post-btn' , 'manipulate-btn' , 'comment-management-btn']
         link_titles= ['ایجاد پست' , 'حذف پست' , 'تغییر پست' , 'مدیریت کامنت']
         link_images = ['<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>']
    else :
        link_id = ['create-post-btn', 'delete-post-btn', 'manipulate-btn' , 'create-category-btn', 'delete-category-btn' , 'update-category-btn' , 'comment-management-btn' ]
        link_images = ['<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>','<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>' , '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>' , '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>']
        link_titles = ['ایجاد پست' , 'حذف پست' , 'تغییر پست' ,'ایجاد کتگوری' ,'حذف کتگوری','آپدیت کتگوری', 'مدیریت کامنت ها']
    return JsonResponse({
        'link_titles' : link_titles,
        'link_ids' : link_id ,
        'link_images' : link_images ,
        'username' : request.user.username ,
        'email' : request.user.email ,
    })

def renderPanel(request) :
    return render(request , 'user-panel.html')

def CreatePostForm(request) :
    temp = render_to_string('form-fragment.html',{
        'categories' : Category.objects.all() ,
    },  request=request )
    return JsonResponse({
        'form' : temp
    })

def createCategoryRequest(request) :
    temp = render_to_string('create-category-form-frag.html', request=request )
    return JsonResponse({
        'cat-form' : temp
    })
def createCategory(request) :
     category = Category.objects.create(name=request.POST.get('name'))
     category.save()
     return redirect('/blog/render-panel')
def createPost(request) :
    conversion_month_dict = {
        'فروردین' : '۰۱' , 'اردیبهشت' : '۰۲' , 'خرداد' : '۰۳' , 'تیر' : '۰۴' , 'مرداد' : '۰۵' , 'شهریور' : '۰۶' , 'مهر' : '۰۷' , 'آبان' : '۰۸' , 'آذر' : '۰۹' , 'دی' : '۱۰' , 'بهمن' : '۱۱' , 'اسفند' : '۱۲' ,
    }
    conversion_number_dict = {
         '۰۱' : '01' , '۰۲' : '02' , '۰۳' : '03' , '۰۴' : '04' , '۰۵' : '05' , '۰۶' : '06' , '۰۷' : '07' , '۰۸' : '08' , '۰۹' : '09' , '۱۰' : '10' , '۱۱' : '11' , '۱۲' : '12' , '۱۳' : '13' , '۱۴' : '14' , '۱۵' : '15' , '۱۶' : '16' , '۱۷' : '17' , '۱۸' : '18' , '۱۹' : '19' , '۲۰' : '20' , '۲۱' : '21' , '۲۲' : '22' , '۲۳' : '23' , '۲۴' : '24' , '۲۵' : '25' , '۲۶' : '26' , '۲۷' : '27' , '۲۸' : '28' , '۲۹' : '29' , '۳۰' : '30' , '۳۱' : '31' , '۳۲' : '32' , '۳۳' : '33' , '۳۴' : '34' , '۳۵' : '35' , '۳۶' : '36' , '۳۷' : '37' , '۳۸' : '38' , '۳۹' : '39' , '۴۰' : '40' , '۴۱' : '41' , '۴۲' : '42' , '۴۳' : '43' , '۴۴' : '44' , '۴۵' : '45' , '۴۶' : '46' , '۴۷' : '47' , '۴۸' : '48' , '۴۹' : '49' , '۵۰' : '50' , '۵۱' : '51' , '۵۲' : '52' , '۵۳' : '53' , '۵۴' : '54' , '۵۵' : '55' , '۵۶' : '56' , '۵۷' : '57' , '۵۸' : '58' , '۵۹' : '59' , '۶۰' : '60' ,  '۱' : '01' , '۲' : '02' , '۳' : '03' , '۴' : '04' , '۵' : '05' , '۶' : '06' , '۷' : '07' , '۸' : '08' , '۹' : '09'
    }
    title = request.POST.get('title')
    body = request.POST.get('body')
    image = request.FILES.get('img')
    status = request.POST.get('status')
    is_important = request.POST.get('is_important')
    is_important = True if is_important=='on' else False
    if status == 'پیش نویس' :
         status = 'draft'
    else :
         status = 'published'
    selectedCategory = request.POST.get('selectedCat')
    if request.POST.get('date') :
        x = request.POST.get('date').split(' ')
        hour_min = x[5].split(':')
        publish_date = conversion_number_dict[x[3][0:2]] + conversion_number_dict[x[3][2:]] + '-' + conversion_number_dict[conversion_month_dict[x[2]]] + '-' + conversion_number_dict[x[1]] + ' ' + conversion_number_dict[hour_min[0]] + ':' + conversion_number_dict[hour_min[1]]
        post = Post.objects.create(publish_date=publish_date, is_important=is_important , poststatus=status , title=title , body=body , author=request.user , category = Category.objects.filter(name=selectedCategory)[0] , image=image)
        post.save()
        return redirect('/blog/render-panel')
    if not request.POST.get('date') :
        post = Post.objects.create(title=title ,is_important=is_important, poststatus=status , body=body , author=request.user , category = Category.objects.filter(name=selectedCategory)[0] , image=image)
        post.save()
        return redirect('/blog/render-panel')


def deleteCategoryRequest(request) :
     allCategories = Category.objects.all()
     temp = render_to_string('delete-category-fragment.html' ,{
         'allCategories' : allCategories ,
     }, request=request)
     return JsonResponse({
         'template' : temp
     })

def deleteCategory(request,identifier) :
       Category.objects.filter(name=identifier).delete()
       return redirect('/blog/render-panel')

def updateCategoryRequest(request):
    allCategories = Category.objects.all()
    temp = render_to_string('update-category-fragment.html',{
        'allCategories' : allCategories ,
    }, request=request)
    return JsonResponse({
        'template': temp
    })

def updateCategory(request):
     prevName = request.POST.get('previously-name')
     newName = request.POST.get('new-name')
     myCat = Category.objects.get(name=prevName)
     myCat.name = newName
     myCat.save()
     return redirect('/blog/render-panel')

def deletePostRequest(request):
     if request.user.is_superuser :
          all_available_posts = Post.objects.all()
     else :
          all_available_posts = Post.objects.filter(author = request.user)
     temp = render_to_string('delete-post-fragment.html' , {
          'allPosts' : all_available_posts
     },request=request)
     return JsonResponse({
         'template' : temp
     })

def deletePost(request,id):
    desired_post = Post.objects.filter(id=id)
    desired_post.delete()
    return redirect('/blog/render-panel')

def updatePostRequest(request) :
    if request.user.is_superuser :
         all_available_posts = Post.objects.all()
    else :
         all_available_posts = Post.objects.filter(author = request.user)

    temp = render_to_string('manipulate-post-fragment.html', {
        'allPosts': all_available_posts
    }, request=request)
    return JsonResponse({
        'template': temp
    })

def fetchManipulateForm(request, Id) :
      myPost = Post.objects.filter(id=Id)[0]
      temp = render_to_string('manipulate-post-form-fragment.html' , {
          'categories' : Category.objects.all() ,
          'myPost' : myPost
      } , request=request )
      return JsonResponse({
          'template' : temp ,
          'myPostTitle' : myPost.title ,
          'myPostBody' : myPost.body ,
          'myPostStatus' : myPost.poststatus ,
          'myPostImportant' : myPost.is_important ,
          'myPostCat' : myPost.category.name ,
      })

def submitPostChanges(request,Id) :
     title = request.POST.get('title')
     body = request.POST.get('body')
     selectedCat = request.POST.get('selectedCat')
     status = request.POST.get('status')
     if status == 'پیش نویس':
         status = 'draft'
     else:
         status = 'published'
     is_important = True if request.POST.get('is_important')=='on' else False
     image = request.FILES.get('img')
     finalImage = image if image!=None else Post.objects.filter(id=Id)[0].image
     # return HttpResponse(finalImage)
     post = Post.objects.get(id=Id)
     post.title = title
     post.body = body
     post.poststatus = status
     post.category = Category.objects.filter(name=selectedCat)[0]
     post.image = finalImage
     post.is_important = is_important
     post.save()
     return redirect('/blog/render-panel')

def showComments(request):
    if request.user.is_superuser :
        myComments = Comment.objects.all()
    else :
        myComments = Comment.objects.filter(author = request.user)
    temp = render_to_string('comments-list-fragment.html' , {
        "myComments" : myComments
    } , request=request)
    return JsonResponse({
        'template' : temp
    })

def deleteComment(request,Id) :
     myComment = Comment.objects.filter(id=Id)[0]
     myComment.delete()
     return JsonResponse({
         'url' : '/blog/render-panel'
     })
def detailView(request,Id) :
     if request.method == 'GET' :
          myComments = Comment.objects.filter(related_to_post = Post.objects.get(id=Id))
          myPost = Post.objects.get(id=Id)
          return HttpResponse(render(request,'postDetailView.html' , {
              'myPost' : myPost,
              'myComments' : myComments
          }))
     if request.method == 'POST' :
          referer = request.META.get('HTTP_REFERER')
          comment = Comment(author=request.user , body=request.POST.get('comment-body') , related_to_post=Post.objects.get(id=Id))
          comment.save()
          return redirect(referer)


def showImportantArchive(request):
    now = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if request.GET.get('value')=='important':
          category = request.GET.get('value')
          myPosts = Post.objects.filter(Q(is_important=True , poststatus='published' , publish_date__lt = now) | Q(is_important=True, author=request.user, poststatus='draft'))
    else :
          category = request.GET.get('value')
          myPosts = Post.objects.filter(Q(category=Category.objects.get(name=category) , publish_date__lt = now ,poststatus='published' ) | Q(category=Category.objects.get(name=category) ,author=request.user, poststatus='draft'))
    paginator = Paginator(myPosts,10)
    page = paginator.get_page(request.GET.get('page'))
    # return HttpResponse(page)
    return render(request,'Archive.html' , {
        'myPosts' : page ,
        'category' : category ,
    })


@csrf_exempt
def getToken(request) :
    return JsonResponse({'csrftoken': request.COOKIES.get('csrftoken')})
def getSearchResult(request) :
       now = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M")
       data =  json.loads(request.body.decode('utf-8'))
       searchText = data['searchText']
       posts = Post.objects.filter(Q(poststatus='published' , publish_date__lt = now) | Q(poststatus='draft' , author=request.user))
       posts = list(posts)
       Posts = []
       for post in posts :
           if searchText in post.title :
               Posts.append(post)
       temp = render_to_string('search-post-fragment.html' , {
           'myPosts' : Posts
       } , request=request)
       return JsonResponse({
           'template' : temp
       })