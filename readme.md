### a simple python script to emulate the DB connection crash

When the process holds the row lock crashes without commit or closing the connection how doe MySQL detect that and release the row lock ?

I had though there maybe existed some kind time out until MySQL detects that, so I wrote this simple python script to test it. But to my surprise I find the second process grabs the lock immediately after the first process returns, i.e. no time out from I have observed. But how does MySQL detect the lost connection and release the row lock immediately ?



#### Use `SELECT … FOR UPDATE` to test the row lock behavior

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

in the second termial `./crash_test.py` to select and update. I found when the 1st termial return, the second terminal will continue immediately.

BTW, `innodb_lock_wait_timeout` is easy to triggered if just `sleep(90)`



#### What I observered contradicts the answers

But what I see so far is that if the first process gets the row lock exits without commit & close the connection, the second process will immediately get the lock and continue to update the record. I don't see any wait_timeout invloved. 

What I obseve is that:

1. If the first process gets the lock `commit`, the second process will get the lock immediately
2. If the first process gets the lock just return without`commit & close`, the second process will get the lock immediately too.



This seems to **contradict** the answers in [MySQL rollback on transaction with lost/disconnected connection](https://stackoverflow.com/questions/9936699/mysql-rollback-on-transaction-with-lost-disconnected-connection)

So the question now is **HOW** MySQL does that ?

