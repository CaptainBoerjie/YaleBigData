from multiprocessing import Pool, TimeoutError
import pymysql

def dothis(x):
    id = x
    db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM historic WHERE his_id = %s;",(id))
    entries = cursor.fetchone()
    for entry in entries:
        print("ID: {} - entry".format(entry))
    print("{}: finished".format(id))
    db.close()
    return 0

if __name__ == "__main__":

    db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
    cursor = db.cursor()
    cursor.execute("SELECT his_id FROM historic;")
    ids = cursor.fetchall()
    db.close()

    sendargs = []
    for id in ids:
        sendargs.append(id[0])
    pool = Pool(processes = 4)
    while 1:
        res = pool.map(dothis,sendargs)
        try:
            print(res.get(timeout=25))
        except TimeoutError:
            print("Timeout Error")

    db.close()

