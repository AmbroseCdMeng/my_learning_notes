from oracleTool import OracleTool
import re
'''
Author:         
Date:           2019年4月25日13:31:19
Description:    IDCard Checked
'''


class IdCardCheck:
    def __init__(self, username, password, tns):
        self.o = OracleTool(username, password, tns)

    # idCardNum 校验码
    def check_id_num(self, num):
        if len(num) != 18:
            return False
        if not num[:-1].isdigit():
            return False

        # 校验码计算规则
        # 前 17 位数字 * 指定系数 --> 求和 --> 与 11 取余
        fact = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        sum = 0
        for i in range(17):
            sum += fact[i] * int(num[i])
        m = sum % 11
        # 余数 0~10 分别对应 10X98765432
        chk = '10X98765432'
        if chk[m] == num[-1]:
            return True
        else:
            return False

    # idCardNum 有效性检验
    def check_id_num_isvalid(self, num):
        reg = "^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
        if re.search(reg, num):
            return True
        return False

    # 开始搜索
    # districtNo 字符串
    # 其他参数为数字
    def start_search(self,
                     districtNo,
                     birth_year=['2019'],
                     birth_month=range(1, 13),
                     birth_day=range(1, 32),
                     sex=[1, 2]):
        # 搜索结果集
        cardlist = []
        # 省市区代码数组(6位)
        districtNoArr = []
        # 生日代码数组(8位)
        birthdayArr = []

        # 填充有效的省市区代码
        if len(districtNo) == 2:
            sql = "select distinct t.districtno from id_card_areabase t where t.provinceno = :districtNo"
            params = {"districtNo": districtNo}
            districtNoArr = self.o.Query(sql, params)
        elif len(districtNo) == 4:
            sql = "select distinct t.districtno from id_card_areabase t where t.cityno = :cityno"
            params = {"cityNo": districtNo}
            districtNoArr = self.o.Query(sql, params)
        elif len(districtNo) == 6:
            sql = "select distinct t.districtno from id_card_areabase t where t.districtno = :districtno"
            params = {"districtno": districtNo}
            districtNoArr = self.o.Query(sql, params)

        # 填充有效的生日代码
        for year in birth_year:
            for month in birth_month:
                for day in birth_day:
                    if month == 2:
                        if day in [31, 30]:
                            continue
                        elif day == 29 and (
                            (int(year) % 4 == 0 and int(year) % 100 != 0) or
                            (int(year) % 400 == 0)):
                            continue
                    if month in [4, 6, 9, 11]:
                        if day in [31]:
                            continue
                    birthdayArr.append((str(year)) + (
                        "0" + str(month) if month < 10 else str(month)) + (
                            "0" + str(day) if day < 10 else str(day)))
        # 穷举 idcardNum
        for districtNo in districtNoArr:
            for birthday in birthdayArr:
                for s in sex:
                    cardlist.extend(self.id_num_list(districtNo[0], birthday, s))
        return cardlist

    # idCardNum 穷举
    # 身份证规则：省市区代码(6) + 生日(8位) + 顺序码(3)【自然顺序(2) + 男奇女偶(1)】+ 校验码(1)
    # 1 男 0 女
    def id_num_list(self, districtNo, birthday, sex):
        # 空数组存储有效的 id_num
        rs = []
        # 性别校验码
        sex_m = [1, 3, 5, 7, 9]
        sex_w = [0, 2, 4, 6, 8]
        # 拼接身份证号码
        id_num_14 = str(districtNo) + str(birthday)
        for i in range(100):
            t_num_16 = ""
            if i < 10:
                t_num_16 = id_num_14 + "0" + str(i)
            else:
                t_num_16 = id_num_14 + str(i)
            for j in (sex_m if sex == 1 else sex_w):
                t_num_17 = t_num_16 + str(j)
                for k in [
                        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X"
                ]:
                    t_num_18 = t_num_17 + k
                    if self.check_id_num(t_num_18) and self.check_id_num_isvalid(
                            t_num_18):
                        rs.append(t_num_18)
        return rs
