from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/',views.AuthorList.as_view(),name='author_list'),
    path('author/<int:pk>', views.AuthorDetail.as_view(), name='author-detail'),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(),name='my_borrowed'),
    path('borrowed/',views.MarkReturnedView.as_view(),name='borrowed-lib'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/',views.AuthorCreate.as_view(),name='author-create'),
    path('author/<int:pk>/update/',views.AuthorUpdate.as_view(),name='author-update'),
    path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author-delete'),
    path('book/create/',views.BookCreateView.as_view(),name='book-create'),
    path('book/<int:pk>/update/',views.BookUpdateView.as_view(),name='book-update'),
    path('book/<int:pk>/delete/',views.BookDeleteView.as_view(),name='book-delete'),

]
