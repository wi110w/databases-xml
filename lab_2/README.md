## About lab
Lab #2 project for course "Databases. XML". Subject area: library.
## Goals
* Rewrite lab #2 from the previous semester to use MongoDB schema instead MySQL
* Implement CRUD using `pymongo`
* Use aggregate() and map/reduce framework

## Aggregate() usage
* Sort by dump_date and number(separately)
```js
db.journal.aggregate([{
        "$sort": {
            "dump_date": -1
        }
    }])
    

db.journal.aggregate([{
        "$sort": {
            "number": -1
        },
    }])
```

* Get amount of records for each book that was lent at defined year
```js
db.journal.aggregate([
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
```

## Map/Reduce usage
* Get amount of readers that each librarian has served
```js
mapper = Code(
              "function() {"
              "    var key = this.librarian._id;"
              "    var value = {"
              "                     full_name: this.librarian.name + ' ' + this.librarian.surname,"
              "                     reader_id: this.reader._id,"
              "                     count: 1"
              "                 };"
              "    emit(key, value);"
              "}")

reducer = Code(
               "function(key, values){"
               "  var reduced_values = { full_name: values[0].full_name, reader_id: null, count: 1 };"
               "  for(var i = 1; i < values.length; i++) {"
               "        var flag = false;"
               "        for(var j = 0; j < i; j++) {"
               "             if(values[j].reader_id.equals(values[i].reader_id)) {"
               "                 flag = true;"
               "                 break;"
               "             }"
               "        }"
               "        if(flag){"
               "             continue;"
               "             }"
               "        reduced_values.count += values[i].count;"
               "  }"
               "    return reduced_values;"
               "}")
```

* Get amount of lent books
```js
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
```

## Usage
* run `./manage.py runserver` to launch server and see the website.
