from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import add_record as db_add_record, edit_record as db_edit_record, \
    delete_record as db_delete_record
from .models import *
from .forms import AddEditForm, SearchYearForm, SearchNameForm
from time import time


def index(request):
    fill_database()
    journal = get_journal()
    paginator = Paginator(journal, 10)
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    context = {'pages': pages}

    return render(request, 'library_redis/index.html', context)


def detail(request, record_num):
    record = get_record_by_number(record_num)
    context = {'record': record}

    return render(request, 'library_redis/detail.html', context)


def detail_reader(request, reader_id):
    reader = get_reader_by_id(reader_id)
    context = {'reader': reader}

    return render(request, 'library_redis/reader_info.html', context)


def detail_librarian(request, lib_id):
    librarian = get_librarian_by_id(lib_id)
    context = {'lib': librarian}

    return render(request, 'library_redis/librarian_info.html', context)


def detail_book(request, book_id):
    book = get_book_by_id(book_id)
    context = {'book': book}

    return render(request, 'library_redis/book_info.html', context)


def delete_record(request, record_num):
    db_delete_record(record_num)
    return redirect('library_redis:index')


def add_record(request):
    if request.method == 'POST':
        form = AddEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            reader = form.cleaned_data['reader']
            librarian = form.cleaned_data['librarian']
            book = form.cleaned_data['book']
            issue_date = form.cleaned_data['issue_date']
            repay_date = form.cleaned_data['repay_date']
            real_repay_date = form.cleaned_data['real_repay_date']
            db_add_record(title, book, reader, librarian, issue_date, repay_date, real_repay_date)
            return redirect('library_redis:index')
    else:
        form = AddEditForm()
    context = {'form': form}

    return render(request, 'library_redis/new.html', context)


def edit_record(request, record_num):
    if request.method == 'POST':
        form = AddEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            reader = form.cleaned_data['reader']
            librarian = form.cleaned_data['librarian']
            book = form.cleaned_data['book']
            issue_date = form.cleaned_data['issue_date']
            repay_date = form.cleaned_data['repay_date']
            real_repay_date = form.cleaned_data['real_repay_date']
            db_edit_record(record_num, title, book, reader, librarian, issue_date, repay_date, real_repay_date)
            return redirect('library_redis:detail', record_num=record_num)
    else:
        record = get_record_by_number(record_num)
        form = AddEditForm(initial=
                           {'title': record['title'],
                            'reader': record['reader']['_id'],
                            'librarian': record['librarian']['_id'],
                            'book': record['book'],
                            'issue_date': record['issue_date'],
                            'repay_date': record['repayment_date'],
                            'real_repay_date': record['real_repayment_date']})

    context = {'form': form, 'record': record}

    return render(request, 'library_redis/edit.html', context)


def reset_data(request):
    reset()
    return redirect('library_redis:index')


def sort_data(request):
    sorted_journal = sort_by_dump_date()
    paginator = Paginator(sorted_journal, 10)
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    context = {'pages': pages}
    return render(request, 'library_redis/sort.html', context)


def statistics(request):
    records = []
    books = get_lent_books()
    top_libs = get_top_librarians()
    if request.GET:
        form = SearchYearForm(request.GET)
        if form.is_valid():
            year = form.cleaned_data['year']
            records = get_journal_by_book_and_year(year)
    else:
        form = SearchYearForm()
    context = {'books': books, 'records': records, 'form': form, 'top_libs': top_libs}
    return render(request, 'library_redis/statistics.html', context)


def search(request):
    records = []
    if request.GET:
        form = SearchNameForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            print(cached(name))
            start = time()
            records = search_records_by_lib(name)
            if records is None:
                records = search_records_by_reader(name)
            time_result = time() - start
            print("load time: " + str(time_result))
    else:
        form = SearchNameForm()
    paginator = Paginator(records, 10)
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    context = {'form': form, 'pages': pages, 'request': request}
    return render(request, 'library_redis/search.html', context)