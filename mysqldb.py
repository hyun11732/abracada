import mysql.connector as con
import pandas as pd
import pymongo as pm

class DB:
    def __init__(self):
        self.mydb = con.connect(
            host="localhost",
            user="root",
            passwd="abracada",
            #auth_plugin='mysql_native_password',
            database="mydb"
        )
        self.limit = str(100)

    def set_limit(self, limit):
        self.limit = str(limit)

    def search_article_by_id(self, article_id):
        cur = self.mydb.cursor()
        query = "select * from articles Where id = " + str(article_id)
        result = pd.read_sql(query, self.mydb)
        print(result)
        return result

    def search_article_by_author(self, author_name):
        cur = self.mydb.cursor()
        query = "insert into author_history value ('" + author_name + "')"
        print(query)
        cur.execute(query)
        self.mydb.commit()
        query = "select * from articles Where name = '" + author_name + "' limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        print(result)
        return result

    def search_article_by_university(self, university) :
        cur = self.mydb.cursor()
        query = "select * from articles where affiliation like '%" + university + "%' limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def search_article_by_title(self, title) :
        cur = self.mydb.cursor()
        query = "select * from articles where pub_title like '%" + title + "%' limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def search_article_by_year(self, year) :
        cur = self.mydb.cursor()
        query = "select * from articles where pub_year = " + str(year) + " limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def search_article_by_journal(self, journal) :
        cur = self.mydb.cursor()
        query = "insert into journal_history value ('" + journal + "')"
        print(query)
        cur.execute(query)
        self.mydb.commit()
        query = "select * from articles where journal = '" + journal + "' limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def search_by_field(self, field) :
        cur = self.mydb.cursor()
        query = "select *  from articles a natural join journal_list j where  j.field like '%" +field + "%' limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def find_journal_ranking(self, rank):
        cur = self.mydb.cursor()
        query = "select * from journal_rankings where ranking = " + str(rank) + " limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def search_article_by_university_ranking(self, rank1, rank2):
        cur = self.mydb.cursor()
        query = "select a.*, u.world_rank from university u, articles a where a.affiliation = u.institution and "+\
                str(rank1) +" <= world_rank and world_rank <= " + str(rank2) + " limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def article_order_by_citedby(self, ascend = True):
        cur = self.mydb.cursor()
        if ascend :
            query = "select * from articles order by citedby" + " limit " + self.limit
        else :
            query = "select * from articles order by citedby desc" + " limit " + self.limit
        result = pd.read_sql(query, self.mydb)
        return result

    def insert_article(self, author, affiliation, citedby, pub_title, pub_year, pub_url, journal):
        cur = self.mydb.cursor()
        query = "insert into articles(name, affiliation, citedby, pub_title, pub_year, pub_url, journal) values ('" + \
                author + "' , '"  + affiliation + "' , "  + str(citedby) + ", '" + pub_title + "' , " +\
                str(pub_year)+ " , '"  + pub_url + "' , '" + journal + "');"
        try :
            cur.execute(query)
            self.mydb.commit()
            return True
        except :
            return False

    def delete_article_by_id(self, id):
        cur = self.mydb.cursor()
        query = "delete from articles where id =" + str(id) + ";"
        try :
            cur.execute(query)
            self.mydb.commit()
            return True
        except :
            return False

    def delete_article_by_title(self, title):
        cur = self.mydb.cursor()
        query = "delete from articles where pub_title = '" + title + "' ;"
        try :
            cur.execute(query)
            self.mydb.commit()
            return True
        except :
            return False

    def update_article_on_citedby(self, id, num) :
        cur = self.mydb.cursor()
        query = "update articles set citedby = citedby +" +  str(num) + " where id = " + str(id)
        try :
            cur.execute(query)
            self.mydb.commit()
            return True
        except :
            return False

    def update_article_on_puburl(self, id, pub_url) :
        cur = self.mydb.cursor()
        query = "update articles set pub_url = '" + pub_url + "' where id = " + str(id)
        try :
            cur.execute(query)
            self.mydb.commit()
            return True
        except :
            return False

    def update_article_on_journal(self, id, journal):
        cur = self.mydb.cursor()
        query = "update articles set journal = '" + journal + "' where id = " + str(id)
        try:
            cur.execute(query)
            self.mydb.commit()
            return True
        except:
            return False

    def show_rank_author(self):
        cur = self.mydb.cursor()
        query = "select author from author_view order by a_view desc limit 3;"
        cur.execute(query)
        author = cur.fetchall()
        result = list()
        for i in author :
            result.append(i[0])
        return result

    def show_rank_journal(self) :
        print("DSAFdasf")
        cur = self.mydb.cursor()
        query2 = "select journal from journal_view order by j_view desc limit 3"
        cur.execute(query2)
        journal = cur.fetchall()
        result = list()
        for i in journal :
            print(i)
            result.append(i[0])
        print(result)
        return result

if __name__ == "__main__" :
    db = DB()
    #db.insert_article("a", "d", 10, "title1", 1920, "", "bytime")
    #db.search_article_by_id(10)
    #db.update_article_on_journal(500011, "pysics")
    db.show_rank_journal()