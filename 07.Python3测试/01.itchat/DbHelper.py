'''
2019年1月30日16:54:22

    Oracle -- DbHelper

'''

import cx_Oracle

HOST = 'localhost'
USERNAME = 'scott'
PASSWORD = 'scott'
PORT = '1521'
SERVICE_NANE = 'orcl.168.92.1'


class DbHelper:

    # init
    def __init__(self):
        self.host = HOST
        self.username = USERNAME
        self.password = PASSWORD
        self.port = PORT
        self.service_name = SERVICE_NANE
        self.conn = None
        self.oracle_conn()

    # get oracle connection
    def oracle_conn(self):
        if not self.conn:
            try:
                conn_str = self.username + "/" + self.password + "@" + self.host + ":" + self.port + "/" + self.service_name
                # print(conn_str)
                self.conn = cx_Oracle.connect(conn_str)
            except Exception as e:
                print(e)
        else:
            pass

    # close oracle connection
    def __del__(self):
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
            except Exception as e:
                print(e)

    # get cursor
    def newCursor(self):
        try:
            cursor = self.conn.cursor()
            if cursor:
                return cursor
            else:
                print('get cursor failed')
                return None
        except Exception as e:
            print(e)
            return None

    # close cursor
    def delCursor(self, cursor):
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(e)

    # sql checked
    def sqlChecked(self, sql):
        flag = True
        sql = sql.upper()
        sql_ele = sql.strip().split()

        # update or delete
        # update tablename set col_name = col_value where 1 = 1
        # delete col_name from tablename where 1 = 1
        if len(sql_ele) < 4:
            flag = False
        elif sql_ele[0] in ['UPDATE', 'DELETE']:
            if 'WHERE' not in sql_ele:
                flag = False
        return flag

    # Query
    def Query(self, sql, params={}, n_start=0, n_count=1):
        data = []
        # get cursor
        cursor = self.newCursor()
        if not cursor:
            return data
        cursor.execute(sql, params)
        if (n_start == 0 and n_count == 1):
            data.append(cursor.fetchone())
        else:
            data = cursor.fetchall()
            if n_count == -1:
                data.extend(data[n_start:])
            else:
                data.extend(data[n_start:n_start + n_count])
        # close cursor
        self.delCursor(cursor)
        return data

    # Insert Update Delete
    def Execute(self, sql, params = {}):
        data = None
        # get cursor
        cursor = self.newCursor()
        if not cursor:
            return data
        # check sql
        if not self.sqlChecked(sql):
            return data
        # execute
        try:
            data = cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            # close cursor
            self.delCursor(cursor)
        return data


if __name__ == "__main__":
    o = DbHelper()

    # queryParams = {'MSG_ID': '100002'}
    # sql = "SELECT * FROM ITCHAT_MSGINFO T WHERE T.MSG_ID = :MSG_ID"
    # o.oracle_query(sql, queryParams)

    # queryParams = ('100002',)     # 按照位置传参需要写成元组形式 即使只有一个参数
    # sql - "SELECT T.* FROM ITCHAT_MSGINFO T WHERE T.MSG_ID = :1"
    # o.oracle_query(sql, queryParams)

    # test -- insert
    insertParams = {'MSG_ID':'TEST001', 'FR_USERNAME': 'MENG', 'TO_USERNAME': 'CD'}
    sql = "INSERT INTO ITCHAT_MSGINFO (MSG_ID, FR_USERNAME, TO_USERNAME) VALUES (:MSG_ID, :FR_USERNAME, :TO_USERNAME)"
    o.Execute(sql, insertParams)
