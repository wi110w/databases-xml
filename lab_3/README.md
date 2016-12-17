## About lab
Lab #3 project for course "Databases. XML". Subject area: library.
## Goals
* Add caching module to Lab #2 using `redis-py`
* Prepare test data (about 50-100K documents)
* Implement caching using `redis-py`
* Measure time for responses with cache hit and cache miss

##Usage
Use `./manage.py runserver` to search data and measure time

##Results
Amount of data: 80 000
Redis version: 3.2.5

|key|miss|hit|
|:---|:---|:---|
|Librarian: 'Travis'|0.2506537437438965|0.07793831825256348|
|Reader: 'Monica'|0.28309059143066406|0.06664919853210449|