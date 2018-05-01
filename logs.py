#!/usr/bin/env python

import psycopg2


class reportingTool():
    '''
    Initialize the ReportingTool class.

    Params:
    dbname(string) - name of database to be connected to when running queries
    '''
    def __init__(self, dbname):
        self.db = dbname

    def runQuery(self, query):
        '''
        Method to eliminate code duplication.
        Connects to DB and runs query passed to it as param.
        Returns the result of the query passed to it.

        Params:
        query(string) - SQL query to be excuted against dbname
        '''
        db = psycopg2.connect(dbname=self.db)
        curs = db.cursor()
        curs.execute(query)
        returned_vals = curs.fetchall()
        db.close()
        return returned_vals

    def mostPopularArticles(self):
        '''
        Returns the top 3 most popular articles from db, and their viewcount
        '''

        popularArtclesQuery = '''
                    SELECT articles.title, count(log.path) as num
                    FROM log, articles
                    WHERE log.path LIKE '/article/' || articles.slug
                    GROUP BY articles.title
                    ORDER BY num DESC
                    LIMIT 3
                    '''

        returned_vals = self.runQuery(popularArtclesQuery)

        print('\n\nThe Top three most popular Articles are:\n')
        for val in returned_vals:
            print('{0} -- {1} views'.format(val[0], val[1]))

    def mostPopularAuthors(self):
        '''
        Returns authors with the most article views
        ordered by most popular author
        '''

        popularAuthorsQuery = '''
                SELECT authors.name, sum(subq.count) as subqcount
                FROM   (SELECT articles.slug, articles.author, count(log.path)
                        FROM articles, log
                        WHERE log.path LIKE '/article/' || articles.slug
                        GROUP BY articles.slug, articles.author) as subq,
                            authors
                WHERE subq.author = authors.id
                GROUP BY authors.name
                ORDER BY subqcount desc
                '''

        returned_vals = self.runQuery(popularAuthorsQuery)

        print('\n\nThe Most Popular Authors ranked by page views:\n')
        for val in returned_vals:
            print('{0} -- {1} article views'.format(val[0], val[1]))

    def daysAboveFailLimit(self):
        '''
        Returns days which had a high than 1% HTTP failure response rate
        '''
        aboveFailureQuery = '''
                WITH total as  (select time::date as absdate, count(*)
                                    as totalcount
                                from log
                                group by time::date)
                Select total.absdate,  (select count(*)
                                        from log
                                        where status != '200 OK'
                                        and time::date =
                                            total.absdate)::numeric
                                        / count(*) * 100
                from log, total
                where log.time::date = total.absdate
                group by total.absdate
                having ((select count(*)
                        from log
                        where status != '200 OK'
                        and time::date = total.absdate)::numeric
                        / count(*) * 100) > 1.0
                '''

        returned_vals = self.runQuery(aboveFailureQuery)

        print('\n\nDays with a higher than 1% failure rate:\n')

        for val in returned_vals:
            print('{0} -- {1:.2f}% errors'.format(val[0].strftime("%B %d, %Y"),
                                                  val[1]))


report = reportingTool('news')

report.mostPopularArticles()
report.mostPopularAuthors()
report.daysAboveFailLimit()
