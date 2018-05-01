# Logs Analysis
Reporting tool for online article click rates

## Dependencies
* Python 2.7+
* PostgreSQL 9.5.12
* PsycoPG2


## Installation and running
There are 2 branches in this project, with identical logs.py files - but different purposes.

* *Master* Branch - **does NOT** contain newsdata.sql required for running. This branch is for Udacity Project where db is not hosted locally
* *database-included* Branch - **does** contain newsdata.sql database, pushed to git LFS. This branch is for all other usage. 

If Using the database-included branch, follow these steps to get up and running

* Fork & clone the database-included branch. 
* Open up bash / terminal and navigate to the same directory you cloned the repo
* run the following command to initialize the newsdata DB in PostgresQL
```
psql -d news -f newsdata.sql
```
* To run the logs- execute the following command in the same terminal window
```
python logs.py
```

Running the logs.py file will run the following three queries automatically, and output them to the console.

1) Find the three most popular articles, and their view count - ordered by most popular article
2) Rank the most popular authors based on article view count
3) Find days in the month where the HTTP response failure rate exceeded 1%
