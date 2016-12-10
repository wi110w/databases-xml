from datetime import time, datetime
from operator import itemgetter
from pymongo import MongoClient
from django.utils import timezone
from bson.code import Code
from faker import Faker
from random import randint

mongoclient = MongoClient(host='localhost', port=27017)
db = mongoclient.library
fake = Faker()

serial = ['Yes', 'No']
is_author = ['Yes', 'No']
titles = []
for i in range(10):
    title = fake.sentence(nb_words=randint(1, 4))
    titles.append(title.rstrip('.'))

genres = []
for i in range(5):
    genres.append(fake.word())


def fill_books():
    for i in range(20):
        db.books.insert({"title": titles[randint(0, 9)],
                         "genre": genres[randint(0, 4)],
                         "author": fake.name(),
                         "publication_date": fake.date_time_this_decade(),
                         "serial": serial[randint(0, 1)]})


def fill_librarians():
    for i in range(20):
        db.librarians.insert({"name": fake.first_name(),
                              "surname": fake.last_name(),
                              "usertype": 'Librarian',
                              "registration_date": fake.date_time_this_decade()})


def fill_readers():
    for i in range(20):
        db.readers.insert({"name": fake.first_name(),
                           "surname": fake.last_name(),
                           "usertype": 'Reader',
                           "registration_date": fake.date_time_this_decade(),
                           "books_offered": randint(1, 5),
                           "is_author": is_author[randint(0, 1)]})


def fill_journal():
    db.journal.remove({})
    books = get_books()
    readers = get_readers()
    librarians = get_librarians()
    for i in range(100):
        book = get_book_by_title(books[randint(0, 19)][0])
        reader_name = readers[randint(0, 19)][0].split()
        reader = get_reader_by_name(reader_name[0])
        lib_name = librarians[randint(0, 19)][0].split()
        librarian = get_librarian_by_name(lib_name[0])
        db.journal.insert({
            "number": randint(1, 1000),
            "title": 'Record',
            "dump_date": fake.date_time_this_decade(),
            "reader": reader,
            "book": book,
            "librarian": librarian,
            "issue_date": fake.date_time_this_decade(),
            "repayment_date": fake.date_time_this_decade(),
            "real_repayment_date": fake.date_time_this_decade()
        })


def fill_database():
    if db.books.count() == 0 and db.readers.count() == 0 and \
                    db.librarians.count() == 0:
        fill_books()
        fill_readers()
        fill_librarians()
        fill_journal()


def get_journal():
    return db.journal.find()


def get_books():
    books = []
    for book in db.books.find():
        books.append((book['_id'], book['title']))
    return books


def get_readers():
    readers = []
    for reader in db.readers.find():
        readers.append((reader['_id'],
                        reader['name'] + ' ' + reader['surname']))
    return readers


def get_librarians():
    librarians = []
    for librarian in db.librarians.find():
        librarians.append((librarian['_id'],
                        librarian['name'] + ' ' + librarian['surname']))
    return librarians


def get_book_by_title(book_title):
    return db.books.find_one({"title": book_title})


def get_record_by_number(number):
    return db.journal.find_one({"number": int(number)})


def get_reader_by_name(name):
    return db.readers.find_one({"name": name})


def get_librarian_by_name(name):
    return db.librarians.find_one({"name": name})


def delete_record(number):
    db.journal.remove({"number": int(number)})


def reset():
    db.journal.remove({})
    db.readers.remove({})
    db.librarians.remove({})
    db.books.remove({})


def edit_record(number, title, book_title, reader_name, librarian_name, issue_date, repay_date, real_repay_date):
    record = get_record_by_number(number)
    reader = get_reader_by_name(reader_name)
    librarian = get_librarian_by_name(librarian_name)
    book = get_book_by_title(book_title)
    db.journal.update(
        record,
        {
            "$set":
                {
                    "title": title,
                    "book": book,
                    "reader": reader,
                    "librarian": librarian,
                    "issue_date": issue_date,
                    "repayment_date": repay_date,
                    "real_repayment_date": real_repay_date
                }
        }
    )


def add_record(title, book_title, reader_name, librarian_name, issue_date, repay_date, real_repay_date):
    journal = sort_by_number()
    reader_name = reader_name.split()
    reader = get_reader_by_name(reader_name[0])
    librarian_name = librarian_name.split()
    librarian = get_librarian_by_name(librarian_name[0])
    book = get_book_by_title(book_title)
    today = timezone.now()
    db.journal.insert_one(
        {
            'number': int(journal[0]['number']) + 1,
            'title': title,
            'dump_date': today,
            'reader': reader,
            'librarian': librarian,
            'book': book,
            'issue_date': datetime.combine(issue_date, time.min),
            'repayment_date': datetime.combine(repay_date, time.min),
            'real_repayment_date': datetime.combine(real_repay_date, time.min)
        }
    )


def sort_by_dump_date():
    journal = db.journal.aggregate([{
        "$sort": {
            "dump_date": -1
        }
    }])

    return journal


def sort_by_number():
    sorted_journal = []
    journal = db.journal.aggregate([{
        "$sort": {
            "number": -1
        },
    }])

    for record in journal:
        sorted_journal.append({'title': record['title'], 'number': record['number']})

    return sorted_journal


def get_lent_books():
    mapper = Code(
        "function() {"
        "   emit(this.book.title, 1);"
        "}"
    )
    reducer = Code(
        "function(key, values) {"
        "   return Array.sum(values);"
        "}"
    )
    populated_books = []
    books = db.journal.map_reduce(mapper, reducer, "populated_books")
    for book in books.find():
        populated_books.append({'title': book['_id'], 'taken': int(book['value'])})
    return populated_books


def get_journal_by_book_and_year(year):
    records = []
    journal = db.journal.aggregate([
        {"$project":
             {"year": {"$year": "$issue_date"},
              "book": {"title": 1}
              }
         },
        {"$match":
             {"year": year}
         },
        {"$group":
             {"_id": "$book.title", "records": {"$sum": 1}}
         }
    ])

    for record in journal:
        records.append({'book_title': record['_id'], 'amount': record['records']})

    return records


def get_top_librarians():
    mapper = Code("""
                  function() {
                      var key = this.librarian._id;
                      var value = {
                                       full_name: this.librarian.name + ' ' + this.librarian.surname,
                                       reader_id: this.reader._id,
                                       count: 1
                                   };
                      emit(key, value);
                  }""")

    reducer = Code("""
                   function(key, values){
                     var reduced_values = { full_name: values[0].full_name, reader_id: null, count: 1 };
                     for(var i = 1; i < values.length; i++) {
                           var flag = false;
                           for(var j = 0; j < i; j++) {
                                if(values[j].reader_id.equals(values[i].reader_id)) {
                                    flag = true;
                                    break;
                                }
                           }
                           if(flag){
                                continue;
                                }
                           reduced_values.count += values[i].count;
                     }
                       return reduced_values;
                   }""")

    top_libs = []
    librarians = db.journal.map_reduce(mapper, reducer, "top_libs")
    for lib in librarians.find():
        top_libs.append({'full_name': lib['value']['full_name'],
                         'readers_served': int(lib['value']['count'])})
    top_libs = sorted(top_libs, key=itemgetter('readers_served'), reverse=True)
    return top_libs