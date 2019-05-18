
from oracleTool import OracleTool
from idcard import IdCardCheck

class Test:

    def test_conn(username, password, tns):
        o = OracleTool(username, password, tns)
        sql = " SELECT T.*, T.ROWID FROM EMP T WHERE T.EMPNO = :EMPNO"
        result = o.Query('SELECT T.*, T.ROWID FROM EMP T', {})
        print(result)
        # o.Export(sql, {"EMPNO": "7369"}, "test_data")


    def test_id_card_search(username, password, tns):
        idcard = IdCardCheck(username, password, tns)

        # 搜索参数
        districtNo = "622826"
        birth_year = ['1995']
        birth_month = [10]
        birth_day = [26]
        sex = [1]

        return idcard.start_search(districtNo, birth_year, birth_month, birth_day, sex)


    if __name__ == "__main__":
        tns = """
        (DESCRIPTION =
            (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
            (CONNECT_DATA =
            (SERVER = DEDICATED)
            (SERVICE_NAME = orcl.168.92.1)
            )
        )
        """
        username = "scott"
        password = "scott"

        # test_conn(username, password, tns)

        result = test_id_card_search(username, password, tns)
        if result:
            print('共计搜索到 %s 条数据'%(len(result)))
            with open('filename', 'a') as f:
                str_res = ""
                for row in result:
                    str_res += str(row) + " || "
                    str_res += "\n"
                f.write(str_res)
        else:
            print('共计搜索到 %s 条数据'%(0))

        
