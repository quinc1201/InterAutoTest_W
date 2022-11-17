#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 1、导入pymsql包
import pymysql
from utils.LogUtil import my_log


class Mysql():
    def __init__(self, host, user, passwd, database, charset='utf8', port=3306):
        self.log = my_log()
        # 2、链接database
        try:
            self.conn = pymysql.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database,
                charset=charset,
                port=port
            )
            # 3、获取执行sql的光标对象，以字典的形式返回数据：cursor=pymysql.cursors.DictCursor
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            print('-------------数据库链接失败----------------\n{}'.format(e))
            raise

    def fetchone(self, sql):
        """
        查询单条记录
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self, sql):
        """
        查询多条记录
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        """
        执行
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.log.error('Mysql执行失败')
            self.log.error(e)
            return False
        return True

    def __del__(self):
        # 关闭光标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭链接对象
        if self.conn is not None:
            self.conn.close()


if __name__ == '__main__':
    mysql = Mysql(
        '192.168.204.128',
        'quincy',
        'quincy1201',
        'movie_cat',
    )
    res = mysql.fetchall("select * from user")
    print(res)

    sql = "update user set nickname='quincy123' where login_name='quincy'"
    mysql.exec(sql)

"""
# 4、执行sql
sql = "select * from user"
cursor.execute(sql)
res = cursor.fetchall()
print(res)
# 5、关闭对象
cursor.close()
conn.close()
"""