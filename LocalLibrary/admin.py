from django.contrib import admin
from .models import Author,Genre,Book,BookInstance,Language
# Register your models here.
 
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class AuthorAdmin(admin.ModelAdmin):
    # pass
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death') # list_display will be used for displaying these label as needed
    fields = ['first_name', 'last_name', ('date_of_birth'),('date_of_death')] 
    # exclude=[('date_of_death')] # using this exclude attribute it will not show date_of_death in admin interface!!
admin.site.register(Author,AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# @register decorator exactly the same thing as the admin.site.register()

@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)

class BookInstanceAdmin(admin.ModelAdmin):
    # pass
    list_display=('book','status','borrower','due_back','id')
    list_filter=('status','due_back') # filer add korber jemon ta amra differnet website a dekhi, price,brand filter kora jay
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )