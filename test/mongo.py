from faker import Faker
from pymongo import MongoClient
from random import randint
from bson.code import Code

client = MongoClient(host='localhost', port=27017)
db = client.college
fake = Faker()

disciplines = ['Geography', 'Maths', 'Physics', 'Biology', 'French', 'Deutch', 'Literature', 'History']
students = []
for i in range(5):
    students.append(fake.last_name())


def fill_journal():
    db.journal.remove({})
    for i in range(30):
        db.journal.insert({
            'surname': students[randint(0, 4)],
            'discipline': disciplines[randint(0, len(disciplines) - 1)],
            'date': fake.date_time_this_month(),
            'mark': randint(1, 5)
        })


def get_best_students():
    best_students = db.journal.aggregate([
        {"$group": {"_id": "$surname", "avg_mark": {"$avg": "$mark"}}},
        {"$match": {"avg_mark": 5}}
    ])

    for student in best_students:
        print(student['_id'] + " - " + str(student['avg_mark']))


def get_low_disciplines():
    low_disciplines = db.journal.distinct("discipline", {"mark": {"$lte": 2}})
    if low_disciplines.count == 0:
        print("No low marks on disciplines")
    else:
        for discipline in low_disciplines:
            print(discipline)


def get_avg_students_per_day():
    mapper = Code("""
                function() {
                    this.date.setHours(0);
                    this.date.setMinutes(0);
                    this.date.setSeconds(0);
                    var key = { surname: this.surname, date: this.date };
                    var value = this.mark;
                    emit(key, value);
                }
    """)
    reducer = Code("""
                function(key, values) {
                    return Array.avg(values);
                }
    """)

    students = db.journal.map_reduce(mapper, reducer, "students")

    for student in students.find():
        print(student['_id']['surname'] + " - " + student['_id']['date'].strftime("%Y-%m-%d")
              + " - " + str(student['value']))


fill_journal()
get_best_students()
get_low_disciplines()
get_avg_students_per_day()