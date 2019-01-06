import csv
import datetime
import calendar


# ==========================================================================================================
# 初始值設定

# 該月有幾天
day = 0
# 幾個假日
all_sun_sat = 0

# S1/S2的list
S1_list = []
S2_list = []

# ==========================================================================================================
def read8():
    # 讀出day/all_sun_sat/一開始的休假狀況
    global day , all_sun_sat , S1_list , S2_list
    fh1 = open('test.csv', 'r', newline = '', encoding = 'utf-8') #newline 參數指定 open()不對換行字元做額外處理
    csv1 = csv.DictReader(fh1) 
    cname1 = csv1.fieldnames #csv1.fieldnames 中為原始檔案第一列中的欄位名稱
    for aline in csv1:
        year = int(aline[cname1[0]])
        month = int(aline[cname1[1]])
        break
    # 該月有幾天
    day = int(calendar.monthrange(year , month)[1])
    # print(day)
    # 幾個假日
    sunday_to_count     = calendar.SUNDAY
    saturday_to_count   = calendar.SATURDAY
    matrix              = calendar.monthcalendar(year,month)
    num_sundays         = sum(1 for x in matrix if x[sunday_to_count] != 0)
    num_saturdays       = sum(1 for x in matrix if x[saturday_to_count] != 0)
    all_sun_sat         = num_sundays + num_saturdays
    fh1.close()
    # ==========================================================================================================
    # 讀入每個人的休假日狀況
    fh1 = open('test.csv', 'r', newline = '', encoding = 'utf-8') #newline 參數指定 open()不對換行字元做額外處理
    csv1 = csv.DictReader(fh1) 
    cname1 = csv1.fieldnames #csv1.fieldnames 中為原始檔案第一列中的欄位名稱
    S1_list = []
    S2_list = []

    for aline in csv1:
        list=[]
        # group/name/prefer
        list1 = [aline[cname1[i]] for i in range(2,5)]
        # 1~day
        list2 = [int(aline[cname1[i]]) for i in range(5,day+5)]
        # 已填休假天數
        sum1 = sum(list2)
        list.append(sum1)
        list.append(list1)
        list.append(list2)
        if list1[0] =='S1':
            S1_list.append(list)
        elif list1[0] =='S2':
            S2_list.append(list)
    fh1.close()
# ==========================================================================================================
read8()
print(S1_list)
# print(S2_list)
# 依照已填休假日多到少排序
S1_list.sort(reverse=True)
S2_list.sort(reverse=True)
s1_allleft_peroneday_list = []
s2_allleft_peroneday_list = []
# 每天休假人數
for i in range(day):
    s1_allleft_peroneday = 0
    s2_allleft_peroneday = 0
    for m in range(4):
        s1_allleft_peroneday += S1_list[m][2][i]
        s2_allleft_peroneday += S2_list[m][2][i]
    s1_allleft_peroneday_list.append(s1_allleft_peroneday)
    s2_allleft_peroneday_list.append(s2_allleft_peroneday)
# ==========================================================================================================
# 先把可以連假的狀況補上（前提是那天都沒有人休假）
for m in range(4):
    cycle = 0
    while S1_list[m][0] < all_sun_sat:
        for i in range(day):
            if i == 0 and s1_allleft_peroneday_list[i] == 0 and (S1_list[m][2][i+1] == 1) and S1_list[m][0] < all_sun_sat:
                S1_list[m][2][i] = 1
                S1_list[m][0]+=1
                s1_allleft_peroneday_list[i]+=1
            elif i != day-1 and i != 0 and s1_allleft_peroneday_list[i] == 0 and (S1_list[m][2][i+1] == 1 or S1_list[m][2][i-1] == 1)and S1_list[m][0] < all_sun_sat:
                S1_list[m][2][i] = 1
                S1_list[m][0]+=1
                s1_allleft_peroneday_list[i]+=1
            elif i == day-1 and s1_allleft_peroneday_list[i] == 0 and (S1_list[m][2][i-1] == 1)and S1_list[m][0] < all_sun_sat:
                S1_list[m][2][i] = 1
                S1_list[m][0]+=1
                s1_allleft_peroneday_list[i]+=1
        cycle+= 1
        if cycle>day*10:
            break
    cycle = 0
    while S2_list[m][0] < all_sun_sat:
        for i in range(day):
            if i == 0 and s2_allleft_peroneday_list[i] == 0 and (S2_list[m][2][i+1] == 1) and S2_list[m][0] < all_sun_sat:
                S2_list[m][2][i] = 1
                S2_list[m][0]+=1
                s2_allleft_peroneday_list[i]+=1
            elif i != day-1 and i != 0 and s2_allleft_peroneday_list[i] == 0 and (S2_list[m][2][i+1] == 1 or S2_list[m][2][i-1] == 1)and S2_list[m][0] < all_sun_sat:
                S2_list[m][2][i] = 1
                S2_list[m][0]+=1
                s2_allleft_peroneday_list[i]+=1
            elif i == day-1 and s2_allleft_peroneday_list[i] == 0 and (S2_list[m][2][i-1] == 1)and S2_list[m][0] < all_sun_sat:
                S2_list[m][2][i] = 1
                S2_list[m][0]+=1
                s2_allleft_peroneday_list[i]+=1
        cycle+= 1
        if cycle>day*10:
            break
print(s1_allleft_peroneday_list)
# print(s2_allleft_peroneday_list)
print(S1_list)
# print(S2_list)
# ==========================================================================================================
# 將單日休假人數的日子補上還沒排滿all_sun_sat的人
print(s1_allleft_peroneday_list.count(0))
# print(s2_allleft_peroneday_list.count(0))
for sun_sat_nobodyLike in range(s1_allleft_peroneday_list.count(0)):
    for m in range(4):
        if S1_list[m][0] != all_sun_sat:
            for i in range(day):
                if S1_list[m][2][i] == 0 and s1_allleft_peroneday_list[i] == 0 and S1_list[m][0] < all_sun_sat:
                    S1_list[m][2][i] = 1
                    S1_list[m][0]+=1
                    s1_allleft_peroneday_list[i]+=1
for sun_sat_nobodyLike in range(s2_allleft_peroneday_list.count(0)):
    for m in range(4):
        if S2_list[m][0] != all_sun_sat:
            for i in range(day):
                if S2_list[m][2][i] == 0 and s2_allleft_peroneday_list[i] == 0 and S2_list[m][0] < all_sun_sat:
                    S2_list[m][2][i] = 1
                    S2_list[m][0]+=1
                    s2_allleft_peroneday_list[i]+=1
print(s1_allleft_peroneday_list)
print(s2_allleft_peroneday_list)
print(S1_list)
print(S2_list)
# ==========================================================================================================
# 如果每天都已經有人休假，但是還有人假還沒修完
# if s1_allleft_peroneday_list.count(0) > 0:
#     for 


