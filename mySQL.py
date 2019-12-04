from datetime import datetime
import pymysql

def get_num_RTC () :
    now = datetime.now()
   
    return str(now.month) + str(now.day) + str(now.hour)

#Return _id which is calculated by RTC.
def get_mod_RTC () :
    now = datetime.now()

    hour = now.hour
    minute = now.minute
    second = now.second

    retval = 3600 * hour + 60 * minute + second
    retval = retval % 33000
    retval = str(retval / 10)

    return retval

def mySQL(sqltype,tablename,where,value,time):
    # MySQL Connection, Access databse
    db = pymysql.connect(host='localhost', user='sion', password='flytothemoon', db='flytothemoon', charset='utf8', use_unicode=True)

    # Make Cursor from Connection
    cursor = db.cursor()

    # Write SQL Query
    if (sqltype == 'showall') :
        try :
            sql = "select * from "+tablename
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        finally :
            db.close()


    elif (sqltype == 'findvalue') :
        try :
            sql = "select value from "+tablename+" where time='"+time+"' and place='"+where+"' and value='"+value+"'"
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchone()
            #print (rows)
            if (rows == None) :
                retval = 0
                return retval
            elif 1 in rows :
                retval = 1
            else :
                retval = 0
            return retval
        finally :
            db.close()

    elif (sqltype == 'findvalue_rtc_id') :
        try :
            _id = get_mod_RTC ()
            sql = "select value from "+tablename+" where _id='"+_id+"'"
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchone()
            #print (rows)
            if (rows == None) :
                retval = 0
                return retval
            elif 1 in rows :
                retval = 1
            else :
                retval = 0
            return retval
        finally :
            db.close()

    elif (sqltype == 'findvalue_rtc') :
        try :
            rtc = get_num_RTC ()
            sql = "select value from "+tablename+" where time='"+rtc+"' and place='"+tablename+"'"
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchone()
            #print (rows)
            if (rows == None) :
                retval = 0
                return retval
            elif 1 in rows :
                retval = 1
            else :
                retval = 0
            return retval
        finally :
            db.close()

    elif (sqltype == 'findtime_id') :
        try :
            _id = get_mod_RTC ()
            sql = "select * from "+tablename+" where _id='"+_id+"'"
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchone()
            return rows
        finally :
            db.close()

    elif (sqltype == 'insert') :
        try :
            sql = "INSERT INTO "+tablename+" (place) VALUES ('"+where+"')"
            print(sql)
            cursor.execute(sql)
            db.commit()
            return cursor.lastrowid
        finally :
            db.close()

    elif (sqltype == 'insertvalue') :
        try :
            sql = "INSERT INTO "+tablename+" (place,value,time) VALUES ('"+where+"','"+value+"','"+time+"')"
            print(sql)
            cursor.execute(sql)
            db.commit()
            return cursor.lastrowid
        finally :
            db.close()


    elif (sqltype == 'update') :
        print("update")

    elif (sqltype == 'delete') :
        print("delete")

