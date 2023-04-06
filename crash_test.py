#! /usr/bin/env python3
# coding:utf-8
import mysql.connector
from mysql.connector import errorcode
import time
import argparse
import os
from dotenv import load_dotenv


class DBCheck:
    def __init__(self):
        load_dotenv('.env.local')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASS')
        self.host = os.getenv('DB_HOST')
        self.dbname = os.getenv('DB_NAME')
        self.crash = 0
        self.cnx = None

    def select_update(self):
        try:
            self.cnx = mysql.connector.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               database=self.dbname)
            if self.cnx.is_connected():
                db_Info = self.cnx.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                print(f"Is autocommit {self.cnx.autocommit}")
            else:
                print('Failed to connect the DB')
                return

            cursor = self.cnx.cursor()
            print("Before updating a record, select first")
            print(
                f"Are we in_transaction before select?: {self.cnx.in_transaction}")
            # autocommit is disabled by default and the first SQL statement will implicitly begin a transaction.
            sql_select_query = """select * from users where id = 1 for update"""
            cursor.execute(sql_select_query)
            print(
                f"Are we in_transaction after select?: {self.cnx.in_transaction}")
            record = cursor.fetchone()
            print(f"select result: {record}")

            # Update single record now
            sql_update_query = """Update users set username = 'qiulang' where id = 1"""
            cursor.execute(sql_update_query)
            print('I am about to sleep for 30 seconds')
            time.sleep(30)
            # 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
            # If sleep 90 second, it will definitely trigger innodb_lock_wait_timeout
            if self.crash == 1:
                print('Kill own process without calling self.cnx.close()')
                os.kill(os.getpid(), 9)
            else:
                print('OK let us continue to run instead of crashing')
            self.cnx.commit()
            print(
                f"Are we in_transaction after commit?: {self.cnx.in_transaction}")
            print("Record Updated successfully ")

            print("After updating record, select again")
            cursor.execute(sql_select_query)
            record = cursor.fetchone()
            print(record)

        except mysql.connector.Error as err:
            if err.errno == errorcode.CR_CONN_HOST_ERROR or err.errno == errorcode.CR_UNKNOWN_HOST:
                print(f"Failed to connect to database {self.host}")
            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("The user name or password is incorrect")
            else:
                print(err)
            exit(1)
        finally:
            if self.crash == 1:
                print(
                    f"Are we in_transaction without commit and close?: {self.cnx.in_transaction}")
                return
            if self.cnx != None and self.cnx.is_connected():
                print(
                    f"Are we in_transaction before close?: {self.cnx.in_transaction}")
                cursor.close()
                self.cnx.close()


if __name__ == '__main__':
    test = DBCheck()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--crash", default=0, type=int,
                        help="Whether to exit before commit")
    test.crash = parser.parse_args().crash
    test.select_update()
    print(f"Are we in_transaction before return?: {test.cnx.in_transaction}")
