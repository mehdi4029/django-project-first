from django.urls import path,include
import blog.views

app_name = 'blog'

urlpatterns = [
    path('', blog.views.loginUser, name='validationF,orm') ,
    path('home/' , blog.views.showMainPage , name='showMainPage') ,
    path('form-validation/' , blog.views.validationForm , name='loginUser') ,
    path('sign-in/' , blog.views.signInUser , name='signInUser') ,
    path('create/' , blog.views.createUser , name='createUser') ,
    path('getUser/<str:username>/' , blog.views.getUser , name='getUser') ,
    path('logout/' , blog.views.logoutUser , name='logoutUser') ,
    path('show-panel' , blog.views.showPanel , name="showPanel") ,
    path('render-panel' , blog.views.renderPanel , name="renderPanel") ,
    path('loadCreateForm' , blog.views.CreatePostForm , name='returnCreateForm') ,
    path ('createPost' , blog.views.createPost , name="createPost") ,
    path('createCategoryRequest' , blog.views.createCategoryRequest , name='createCategoryRequest') ,
    path('createCategory' , blog.views.createCategory , name="createCategory") ,
    path('deleteCategory' , blog.views.deleteCategoryRequest, name='deleteCategoryRequest') ,
    path('deleteCat/<str:identifier>' , blog.views.deleteCategory, name="deleteCategory") ,
    path('updateCategory' , blog.views.updateCategoryRequest , name="updateCategory") ,
    path('updateCat/' , blog.views.updateCategory, name="updateCategory") ,
    path('deletePostRequest' , blog.views.deletePostRequest , name="deletePostRequest") ,
    path('deletePost/<int:id>' , blog.views.deletePost , name="deletePost") ,
    path('updatePostRequest' , blog.views.updatePostRequest , name="updatePostRequest") ,
    path('fetchManipulateForm/<int:Id>' , blog.views.fetchManipulateForm , name="fetchManipulateForm") ,
    path('submitPostChanges/<int:Id>' , blog.views.submitPostChanges , name="submitPostChanges") ,
    path('detailView/<int:Id>' , blog.views.detailView , name="detailView") ,
    path('Archive' , blog.views.showImportantArchive , name="archiveImportant") ,
    path('commentsList' , blog.views.showComments, name="commentsList") ,
    path('deleteComment/<int:Id>' , blog.views.deleteComment, name="deleteComment"),
    path('getSearchResult' , blog.views.getSearchResult , name="getSearchResult") ,
    path('getCsrfToken' , blog.views.getToken, name="getToken") ,
]



# my super-user > username = mahdi , password = mahdi4029 , email = mahdishafaati9@gmail.com