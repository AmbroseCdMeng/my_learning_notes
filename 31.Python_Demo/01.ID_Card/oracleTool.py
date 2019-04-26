import cx_Oracle

'''
Author:         
Date:           2019年4月25日14:21:54
Description:    Oracle Tools
'''


class OracleTool:

    # 初始化 Oracle 连接
    def __init__(self, username, password, tns):
        self._username = username
        self._password = password
        self._tns = tns
        self._conn = None
        self._reOpenConn()

    # 重新打开连接
    def _reOpenConn(self):
        if not self._conn:
            self._conn = cx_Oracle.connect(
                self._username, self._password, self._tns)
        else:
            pass

    # 关闭连接
    def _closeConn(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    # 创建新游标
    def _newCursor(self):
        cur = self._conn.cursor()
        if cur:
            return cur
        else:
            print("Error: CreateNewCursorFailed")
            return None

    # 删除游标
    def _delCursor(self, cur):
        if cur:
            cur.close()

    # Query 参数为字典
    def Query(self, sql, params, startIndex=0, number=-1):
        data = []
        cur = self._newCursor()
        if not cur:
            return data
        # cur.execute(sql)
        cur.prepare(sql)
        cur.execute(None, params)
        if startIndex == 0 and number == 1:
            data.append(cur.fetchone())
        else:
            t_data = cur.fetchall()
            if number == -1:
                data.extend(t_data[startIndex:])
            else:
                data.extend(t_data[startIndex:startIndex + number])
        self._delCursor(cur)
        return data

    # Updata Delete Insert  参数为字典
    def Exec(self, sql, params):
        try:
            data = None
            cur = self._newCursor()
            if not cur:
                return data
            data = cur.execute(sql, params)
            self._delCursor(cur)
            return data
        except Exception:
            self._conn.rollback()
        else:
            self._conn.commit()
        finally:
            self._conn.close()

    # Update Delete Insert -- Many  参数为字典列表

    def Execmany(self, sql, params):
        try:
            data = None
            cur = self._newCursor()
            if not cur:
                return data
            data = cur.executemany(sql, params)
            self._delCursor(cur)
            return data
        except Exception:
            self._conn.rollback()
        else:
            self._conn.commit()
        finally:
            self._conn.close()

    # 导出结果文件
    def Export(self, sql, params, filename, colfg='||'):
        data = self.Query(sql, params)
        if data:
            with open('filename', 'a') as f:
                str_result = ""
                for row in data:
                    str_result += str(row) + colfg
                    str_result += '\n'
                f.write(str_result)
