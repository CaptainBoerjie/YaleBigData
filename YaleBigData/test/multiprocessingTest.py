from multiprocessing import Pool
import pymysql

def dothis(x,cursor):
    print("{}: finished".format(x))
    cursor.execute("SELECT * FROM historic WHERE his_id = %s;",(x))
    entry = cursor.fetchone()
    print(entry)

if __name__ == "__main__":

    db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
    cursor = db.cursor()
    cursor.execute("SELECT his_id FROM historic;")
    ids = cursor.fetchall()

    sendargs = []
    for id in ids:
        sendargs.append((id[0],cursor))
        
    with Pool(4) as p:
        print(p.map(dothis,sendargs))

    db.close()