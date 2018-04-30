import psycopg2

class reportingTool():

    def __init__(self, dbname):
        self.db = dbname

    def runQuery(self, query):
        db = psycopg2.connect(dbname=self.db)
        curs = db.cursor()
        curs.execute(query)
        returned_vals = curs.fetchall()
        db.close()
        return returned_vals

    def mostPopularArticles(self):
        popularArtclesQuery = '''
                    SELECT articles.title, subq.num
                    FROM   (SELECT path, count(path) as num
                            FROM log 
                            WHERE path != '/'
                            GROUP BY path
                            ORDER BY num DESC
                            LIMIT 3) as subq, articles
                    WHERE subq.path LIKE '%/article/' || articles.slug
                    ORDER BY subq.num DESC
                    '''

        returned_vals = self.runQuery(popularArtclesQuery)

        print('\n\nThe Top three most popular Articles are:\n')
        for val in returned_vals:
            print('{0} -- {1} views'.format(val[0], val[1]))

    def mostPopularAuthors(self):

        popularAuthorsQuery = '''
                SELECT authors.name, sum(subq.count) as subqcount
                FROM   (SELECT articles.slug, articles.author, count(log.path)
                        FROM articles, log
                        WHERE log.path LIKE '%/article/' || articles.slug
                        GROUP BY articles.slug, articles.author) as subq, authors
                WHERE subq.author = authors.id
                GROUP BY authors.name
                ORDER BY subqcount desc            
                '''

        returned_vals = self.runQuery(popularAuthorsQuery)

        print('\n\nThe Most Popular Authors ranked by page views:\n')
        for val in returned_vals:
            print('{0} -- {1} article views'.format(val[0], val[1]))

    def daysAboveFailLimit(self):

        aboveFailureQuery = '''
                WITH total as  (select time::date as absdate, count(*) as totalcount
                                from log
                                group by time::date)
                Select total.absdate,  (select count(*) 
                                        from log
                                        where status != '200 OK'
                                        and time::date = total.absdate)::numeric
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
            print('{0} -- {1:.2f}% errors'.format(val[0].strftime("%B %d, %Y"), val[1]))


report = reportingTool('news')

report.mostPopularArticles()
report.mostPopularAuthors()
report.daysAboveFailLimit()