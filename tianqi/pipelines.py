# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi

class TianqiPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        # 建立连接池，**表示参数对
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool=dbpool)

    def process_item(self, item, spider):
        result = self.dbpool.runInteraction(self.insert, item)
        result.addErrback(self.error)

    def error(self, reason):
        print(reason)


    def insert(self, cursor, item):
        sql = "insert weinan values(%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (item['day'], item['weatherm'], item['weathern'], item['temm'], item['temn'], item['windm'], item['windn']))



