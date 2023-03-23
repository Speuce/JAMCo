### Steps To Run Load Testing:
- In your database docker container:
  - Enter `psql -U postgres postgres`, then run `ALTER SYSTEM SET max_connections=300;`
- Set `TEST` env var to 1
- In backend database container:
  - `python manage.py dumpdata > db_dump.json`
  - `locust -f tests/performance/locustfile.py -H http://localhost:8000 -u 100 -r 20`, then visit `localhost:8089` and clicking "Start Swarming"
  -  `python manage.py flush` > `yes`
  - `python manage.py loaddata db_dump.json`
  