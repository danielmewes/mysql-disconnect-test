### a simple python script to emulate the DB connction crash 

To check how long will the second thread/process wait if the first one crashes, please refer to the following 2 discussions

[MySQL rollback on transaction with lost/disconnected connection](https://stackoverflow.com/questions/9936699/mysql-rollback-on-transaction-with-lost-disconnected-connection)

[When a thread/process crashes on acquired DB locks, how does DB detects that and releases the lock?](https://dba.stackexchange.com/questions/292592/when-a-thread-process-crashes-on-acquired-db-locks-how-does-db-detects-that-and)



Host MySQL on https://www.freemysqlhosting.net/, create a table like following

```sql
mysql> select * from users;
+----+-------------+
| id | username    |
+----+-------------+
|  1 | john doe    |
|  2 | jane doe    |
|  3 | alice jones |
|  4 | lisa romero |
+----+-------------+
```



Using https://pypi.org/project/mysql-connector-python/ as mysql driver.



Open 2 terminals, in the first terminal run `./crash_test.py -c 1`  return without calling `close()` to emulate the crash

in the second termial `./crash_test.py` to select and update. I found when the 1st termial return, the second terminal will continue immediately 

