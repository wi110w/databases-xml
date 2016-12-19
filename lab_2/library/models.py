from datetime import time, datetime
from operator import itemgetter
from pymongo import MongoClient
from django.utils import timezone
from bson.code import Code
from bson.objectid import ObjectId
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
        db.books.insert_one({"title": titles[randint(0, 9)],
                             "genre": genres[randint(0, 4)],
                             "author": fake.name(),
                             "publication_date": fake.date_time_this_decade(),
                             "serial": serial[randint(0, 1)]})


def fill_librarians():
    for i in range(20):
        db.librarians.insert_one({"name": fake.first_name(),
                                  "surname": fake.last_name(),
                                  "usertype": 'Librarian',
                                  "registration_date": fake.date_time_this_decade()})


def fill_readers():
    for i in range(20):
        db.readers.insert_one({"name": fake.first_name(),
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
        book = get_book_by_id(books[randint(0, 19)][0])
        reader = get_reader_by_id(readers[randint(0, 19)][0])
        librarian = get_librarian_by_id(librarians[randint(0, 19)][0])
        db.journal.insert_one({
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


def get_book_by_id(book_id):
    return db.books.find_one({"_id": book_id})


def get_record_by_number(number):
    return db.journal.find_one({"number": int(number)})


def get_reader_by_id(reader_id):
    return db.readers.find_one({"_id": reader_id})


def get_librarian_by_id(lib_id):
    return db.librarians.find_one({"_id": lib_id})


def delete_record(number):
    db.journal.delete_one({"number": int(number)})


def reset():
    db.journal.drop()
    db.readers.drop()
    db.librarians.drop()
    db.books.drop()


def edit_record(number, title, book_id, reader_id, librarian_id, issue_date, repay_date, real_repay_date):
    reader = get_reader_by_id(ObjectId(reader_id))
    librarian = get_librarian_by_id(ObjectId(librarian_id))
    book = get_book_by_id(ObjectId(book_id))
    db.journal.update_one(
        {'number': int(number)},
        {
            "$set":
                {
                    "title": title,
                    "book": book,
                    "reader": reader,
                    "librarian": librarian,
                    "issue_date": datetime.combine(issue_date, time.min),
                    "repayment_date": datetime.combine(repay_date, time.min),
                    "real_repayment_date": datetime.combine(real_repay_date, time.min)
                }
        }
    )


def add_record(title, book_id, reader_id, librarian_id, issue_date, repay_date, real_repay_date):
    journal = sort_by_number()
    reader = get_reader_by_id(ObjectId(reader_id))
    librarian = get_librarian_by_id(ObjectId(librarian_id))
    book = get_book_by_id(ObjectId(book_id))
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
                     var reduced_values = values[0];
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