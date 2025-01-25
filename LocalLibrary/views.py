from django.shortcuts import render,get_object_or_404
from .models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# from django.contrib.auth.decorators

# Create your views here.
def home(request):

    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    num_instances_available =BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()
    genre_obj=Genre.objects.all()
    num_visits=request.session.get('num_visits',0)
    num_visits+=1
    request.session['num_visits']=num_visits

    context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'tanim':genre_obj,
            'num_visits': num_visits,
        }


    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model=Book
    context_object_name='book_list'
    paginate_by=4

    # queryset=Book.objects.filter(title__icontains='war')[:5] instead we will use get_queryset() method
    template_name='D:/Django/env/templetes/book_list.html'

    def get_queryset(self):
        return Book.objects.filter()[:5] # you may add filter (title__icontains='war')
    
    def get_context_data(self, **kwargs):
        context= super(BookListView,self).get_context_data(**kwargs)
        # just add some additional data
        context['tanim']="Hello this is Tanim,Learing Django perfectly!!"
        return context
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name= r'D:\Django\env\templetes\book_detail.html'

class AuthorList(generic.ListView):

    model=Author
    context_object_name='author_list'
    paginate_by=5
    template_name= 'authorlist.html'

class AuthorDetail(generic.DetailView):
    model=Author
    template_name= r"D:\Django\env\templetes\authordetails.html"


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    model=BookInstance
    template_name= 'bookinstance_list_borrowes_user.html'
    paginate_by=5

    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower=self.request.user).filter(
                status__exact='o'
            ).order_by('due_back')

        )

class MarkReturnedView(PermissionRequiredMixin,generic.ListView):
    model=BookInstance
    permission_required='LocalLibrary.can_mark_returned'
    template_name= r'D:\Django\env\templetes\Librarian_view.html'

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )

from .forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required,permission_required
@login_required
@permission_required('LocalLibrary.can_mark_returned',raise_exception=True)
def renew_book_librarian(request,pk):

    book_instance=get_object_or_404(BookInstance,pk=pk)

    #check whether it is a POST request

    if request.method=='POST':

        form=RenewBookForm(request.POST) # maps renewal_date (defined in RenewBookForm) from request.POST and set to form field

        if form.is_valid(): #method is automatically available because your RenewBookForm inherits from forms.Form

            book_instance.due_back=form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed-lib'))
        
    else:

        proposed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date':proposed_renewal_date})  #-datetime.timedelta(days=2) to check the  past error working or not

    context={
        'form':form,
        'book_instance':book_instance,
    }

    return render(request,'book_renew_librarian.html',context=context)


# lets create generic edit view to create,update,delete author 

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(PermissionRequiredMixin, CreateView):

    model=Author
    fields=['first_name','last_name','date_of_birth','date_of_death']
    initial={'date_of_death':'morse mal!!'}
    permission_required='LocalLibrary.can_add_author'
    template_name= r'D:\Django\env\templetes\author_form.html'

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model=Author

    fields='__all__'
    permission_required='LocalLibrary.can_change_author'
    template_name= r'D:\Django\env\templetes\author_form.html'

class AuthorDelete(PermissionRequiredMixin,DeleteView):

    model=Author
    success_url=reverse_lazy('author_list')
    permission_required='LocalLibrary.can_delete_author'
    template_name= r'D:\Django\env\templetes\author_confirm_delete.html'

    def form_valid(self,form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('author-delete',kwargs={'pk':self.object.pk})
            )

class BookCreateView(PermissionRequiredMixin,CreateView):
    model=Book
    fields='__all__'
    permission_required='LocalLibrary.can_add_book'
    template_name= r'D:\Django\env\templetes\book_form.html'

class BookUpdateView(PermissionRequiredMixin,UpdateView):
    model=Book
    fields='__all__'
    permission_required='LocalLibrary.can_edit_book'
    template_name= r'D:\Django\env\templetes\book_form.html'

from django.db.models import Count

class BookDeleteView(PermissionRequiredMixin,DeleteView):
    model=Book
    success_url=reverse_lazy('books')
    permission_required='LocalLibrary.can_delete_book'
    template_name= r'D:\Django\env\templetes\book_confirm_delete.html'

    def form_valid(self,form):
        
        
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('book-delete',kwargs={'pk':self.object.pk})
            )
    def get_queryset(self):
        return Book.objects.filter(pk=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(pk=self.kwargs['pk']).annotate(instance_count=Count('bookinstance')).values_list('title', 'instance_count')
        return context






