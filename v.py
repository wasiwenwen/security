# ==========================================================================================================
# ------------------------------------------------初始值設定-------------------------------------------------
import csv
import datetime
import calendar
import random
from scheduling3 import *
# 該月有幾天
day = 0
# 幾個假日
all_sun_sat = 0
# S1/S2的list
S1_list = []
S2_list = []
# 單一地點成員數
member = 4
# 誰在哪天特休
WhoChangeWhichDay1 = [[],[],[],[]]
WhoChangeWhichDay2 = [[],[],[],[]]
offday_permen = [0,0,0,0]
offday_permen2 = [0,0,0,0]
# 匯入匯出檔案
file_in  = 'in(31).csv'
file_out = 'out(31).csv'
# ==========================================================================================================
# ------------------------------------------------讀檔案-----------------------------------------------------
def read8(file):
    # 讀出day/all_sun_sat/一開始的休假狀況
    global day , all_sun_sat , S1_list , S2_list
    fh1 = open(file, 'r', newline = '', encoding = 'utf-8') #newline 參數指定 open()不對換行字元做額外處理
    csv1 = csv.DictReader(fh1) 
    cname1 = csv1.fieldnames #csv1.fieldnames 中為原始檔案第一列中的欄位名稱
    for aline in csv1:
        year = int(aline[cname1[0]])
        month = int(aline[cname1[1]])
        break
    # 該月有幾天
    day = int(calendar.monthrange(year , month)[1])
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
    fh1 = open(file, 'r', newline = '', encoding = 'utf-8') #newline 參數指定 open()不對換行字元做額外處理
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
    return year , month
year , month = read8(file_in)
# ==========================================================================================================
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
# ------------------------------------------------建議休假日-------------------------------------------------
# 先把可以連假的狀況補上（前提是那天都沒有人休假）
for m in range(member):
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
        if cycle>day*member: break
for m in range(member):
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
        if cycle>day*member: break
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 將單日休假人數的日子補上還沒排滿all_sun_sat的人
for sun_sat_nobodyLike in range(s1_allleft_peroneday_list.count(0)):
    for m in range(member):
        if S1_list[m][0] != all_sun_sat:
            for i in range(day):
                if S1_list[m][2][i] == 0 and s1_allleft_peroneday_list[i] == 0 and S1_list[m][0] < all_sun_sat:
                    S1_list[m][2][i] = 1
                    S1_list[m][0]+=1
                    s1_allleft_peroneday_list[i]+=1
for sun_sat_nobodyLike in range(s2_allleft_peroneday_list.count(0)):
    for m in range(member):
        if S2_list[m][0] != all_sun_sat:
            for i in range(day):
                if S2_list[m][2][i] == 0 and s2_allleft_peroneday_list[i] == 0 and S2_list[m][0] < all_sun_sat:
                    S2_list[m][2][i] = 1
                    S2_list[m][0]+=1
                    s2_allleft_peroneday_list[i]+=1
# ------------------------------------------------------------------------------------------------------------------------------------------------
# 如果每天都已經有人休假，但是還有人假還沒修完
s1_everyone_left_num = [int(m[0]) for m in S1_list]
while s1_everyone_left_num.count(all_sun_sat) != member and s1_allleft_peroneday_list.count(0) == 0:
    for m in range(member):
        daylist = [int(i) for i in range(day)]
        random.shuffle(daylist)
        for i in daylist:
            if i == 0 and s1_allleft_peroneday_list[i] == 1 and (S1_list[m][2][i+1] == 1) and (S1_list[m][2][i] == 0)and S1_list[m][0] < all_sun_sat:
                S1_list[m][2][i] = 1
                S1_list[m][0]+=1
                s1_allleft_peroneday_list[i]+=1
                s1_everyone_left_num[m]+=1
            elif i != day-1 and i != 0 and s1_allleft_peroneday_list[i] == 1 and (S1_list[m][2][i+1] == 1 or S1_list[m][2][i-1] == 1) and (S1_list[m][2][i] == 0) and S1_list[m][0] < all_sun_sat:
                S1_list[m][2][i] = 1
                S1_list[m][0]+=1
                s1_allleft_peroneday_list[i]+=1
                s1_everyone_left_num[m]+=1
            elif i == day-1 and s1_allleft_peroneday_list[i] == 1 and (S1_list[m][2][i-1] == 1) and (S1_list[m][2][i] == 0) and S1_list[m][0] < all_sun_sat:
                S1_list[m][2][i] = 1
                S1_list[m][0]+=1
                s1_allleft_peroneday_list[i]+=1
                s1_everyone_left_num[m]+=1
s2_everyone_left_num = [int(m[0]) for m in S2_list]
while s2_everyone_left_num.count(all_sun_sat) != member and s2_allleft_peroneday_list.count(0) == 0:
    for m in range(member):
        daylist = [int(i) for i in range(day)]
        random.shuffle(daylist)
        for i in daylist:
            if i == 0 and s2_allleft_peroneday_list[i] == 1 and (S2_list[m][2][i+1] == 1) and (S2_list[m][2][i] == 0)and S2_list[m][0] < all_sun_sat:
                S2_list[m][2][i] = 1
                S2_list[m][0]+=1
                s2_allleft_peroneday_list[i]+=1
                s2_everyone_left_num[m]+=1
            elif i != day-1 and i != 0 and s2_allleft_peroneday_list[i] == 1 and (S2_list[m][2][i+1] == 1 or S2_list[m][2][i-1] == 1) and (S2_list[m][2][i] == 0) and S2_list[m][0] < all_sun_sat:
                S2_list[m][2][i] = 1
                S2_list[m][0]+=1
                s2_allleft_peroneday_list[i]+=1
                s2_everyone_left_num[m]+=1
            elif i == day-1 and s2_allleft_peroneday_list[i] == 1 and (S2_list[m][2][i-1] == 1) and (S2_list[m][2][i] == 0) and S2_list[m][0] < all_sun_sat:
                S2_list[m][2][i] = 1
                S2_list[m][0]+=1
                s2_allleft_peroneday_list[i]+=1
                s2_everyone_left_num[m]+=1
S1_list.sort()
S2_list.sort()
# ==========================================================================================================
# -------------------------------------------------建議特休--------------------------------------------------
# 判斷連假
while s1_allleft_peroneday_list.count(0) != 0:
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S1_list[0][2] , S1_list[1][2] , S1_list[2][2] , S1_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order + 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order - 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S1_list[m][2][order] == 0 and (S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 1): H_check_list[m].append('P')
                    elif S1_list[m][2][order] == 0 and ((S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 0) or (S1_list[m][2][order + 1] == 0 and S1_list[m][2][order - 1] == 1)): H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member): H_check_list[m].append('F')
        order += 1
    nPTm_list = []
    for m in range(member):
        PTone_list = []
        P = H_check_list[m].count('P')
        T = H_check_list[m].count('T')
        PTone_list.append(0)
        PTone_list.append(P)
        PTone_list.append(T)
        PTone_list.append(m)
        nPTm_list.append(PTone_list)
    nPTm_list.sort(reverse=True)
    # 先換一天每人一天
    WhoChangeWhichDay1 = [[],[],[],[]]
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0:
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s1_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay1[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen:break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0:
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] += -1
            s1_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay1[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen:break
                else: H_check_list[m][changeDay] = 'F'
    break
cycle = 0
while s1_allleft_peroneday_list.count(0) != 0:
    cycle += 1
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S1_list[0][2] , S1_list[1][2] , S1_list[2][2] , S1_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order + 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order - 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S1_list[m][2][order] == 0 and (S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 1): H_check_list[m].append('P')
                    elif S1_list[m][2][order] == 0 and ((S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 0) or (S1_list[m][2][order + 1] == 0 and S1_list[m][2][order - 1] == 1)): H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member): H_check_list[m].append('F')
        order += 1
    offday_permen = [len(WhoChangeWhichDay1[0]),len(WhoChangeWhichDay1[1]),len(WhoChangeWhichDay1[2]),len(WhoChangeWhichDay1[3])]
    for m in range(member):
        sort = nPTm_list[m][3]
        P = H_check_list[sort].count('P')
        T = H_check_list[sort].count('T')
        nPTm_list[m][1] = P
        nPTm_list[m][2] = T
    nPTm_list.sort(reverse=True)
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0 and len(WhoChangeWhichDay1[sort]) < min(offday_permen):
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s1_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay1[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen: break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0 and len(WhoChangeWhichDay1[sort]) < min(offday_permen):
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s1_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay1[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen: break
                else: H_check_list[m][changeDay] = 'F'
    if s1_allleft_peroneday_list.count(0) == 0 : 
        break
    if cycle > 5: #讓特休平均分佈
        while offday_permen[0] != offday_permen[1] and offday_permen[1] != offday_permen[2] and offday_permen[2] != offday_permen[3] or s1_allleft_peroneday_list.count(0) != 0:
            for d in range(day):
                if s1_allleft_peroneday_list[d] == 0:
                    changeMen = offday_permen.index(min(offday_permen))
                    changeDay = d
                    H_check_list[changeMen][changeDay] = 'F'
                    S1_list[changeMen][2][changeDay] = 1
                    for sort in range(member):
                        if changeMen == nPTm_list[sort][3]:
                            nPTm_list[sort][0] -= 1
                            break
                    s1_allleft_peroneday_list[changeDay] = 1
                    WhoChangeWhichDay1[changeMen].append(changeDay)
                    offday_permen[changeMen] +=1
                    for m in range(member):
                        if m == changeMen: break
                        else: H_check_list[m][changeDay] = 'F'
        break
# --------s2
while s2_allleft_peroneday_list.count(0) != 0:
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S2_list[0][2] , S2_list[1][2] , S2_list[2][2] , S2_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order + 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order - 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S2_list[m][2][order] == 0 and (S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 1): H_check_list[m].append('P')
                    elif S2_list[m][2][order] == 0 and ((S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 0) or (S2_list[m][2][order + 1] == 0 and S2_list[m][2][order - 1] == 1)): H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member): H_check_list[m].append('F')
        order += 1
    # 第一次做就好
    nPTm_list = []
    for m in range(member):
        PTone_list = []
        P = H_check_list[m].count('P')
        T = H_check_list[m].count('T')
        PTone_list.append(0)
        PTone_list.append(P)
        PTone_list.append(T)
        PTone_list.append(m)
        nPTm_list.append(PTone_list)
    nPTm_list.sort(reverse=True)
    # 先換一天每人一天
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0:
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s2_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay2[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen:break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0:
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] += -1
            s2_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay2[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen:break
                else: H_check_list[m][changeDay] = 'F'
    break
cycle = 0
while s2_allleft_peroneday_list.count(0) != 0:
    cycle += 1
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S2_list[0][2] , S2_list[1][2] , S2_list[2][2] , S2_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order + 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order - 1] == 1: H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S2_list[m][2][order] == 0 and (S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 1): H_check_list[m].append('P')
                    elif S2_list[m][2][order] == 0 and ((S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 0) or (S2_list[m][2][order + 1] == 0 and S2_list[m][2][order - 1] == 1)): H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member): H_check_list[m].append('F')
        order += 1
    offday_permen2 = [len(WhoChangeWhichDay2[0]),len(WhoChangeWhichDay2[1]),len(WhoChangeWhichDay2[2]),len(WhoChangeWhichDay2[3])]
    for m in range(member):
        sort = nPTm_list[m][3]
        P = H_check_list[sort].count('P')
        T = H_check_list[sort].count('T')
        nPTm_list[m][1] = P
        nPTm_list[m][2] = T
    nPTm_list.sort(reverse=True)
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0 and len(WhoChangeWhichDay2[sort]) < min(offday_permen2):
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s2_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay2[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen: break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0 and len(WhoChangeWhichDay2[sort]) < min(offday_permen2):
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s2_allleft_peroneday_list[changeDay] = 1
            WhoChangeWhichDay2[changeMen].append(changeDay)
            for m in range(member):
                if m == changeMen: break
                else: H_check_list[m][changeDay] = 'F'
    if s2_allleft_peroneday_list.count(0) == 0 : 
        break
    if cycle > 5: #讓特休平均分佈
        while offday_permen2[0] != offday_permen2[1] and offday_permen2[1] != offday_permen2[2] and offday_permen2[2] != offday_permen2[3] or s2_allleft_peroneday_list.count(0) != 0:
            for d in range(day):
                if s2_allleft_peroneday_list[d] == 0:
                    changeMen = offday_permen2.index(min(offday_permen2))
                    changeDay = d
                    H_check_list[changeMen][changeDay] = 'F'
                    S2_list[changeMen][2][changeDay] = 1
                    for sort in range(member):
                        if changeMen == nPTm_list[sort][3]:
                            nPTm_list[sort][0] -= 1
                            break
                    s2_allleft_peroneday_list[changeDay] = 1
                    WhoChangeWhichDay2[changeMen].append(changeDay)
                    offday_permen2[changeMen] +=1
                    for m in range(member):
                        if m == changeMen: break
                        else: H_check_list[m][changeDay] = 'F'
        break
# ==========================================================================================================

# ----------------------------------------------建議班別-----------------------------------------------------
S1_list = shift_schedule(S1_list, member)
S2_list = shift_schedule(S2_list, member)
# ==========================================================================================================
# ---------------------------------轉換成可以理解的班別代號-----------------------------------------------------
def shiftName(Slist, WhoChangeWhichDay):
    Day = 0
    for m1 , m2 , m3 , m4 in zip(Slist[0][2],Slist[1][2],Slist[2][2],Slist[3][2]):
        day_schedule = [m1,m2,m3,m4]
        if 'B' not in day_schedule and 'A'in day_schedule and'C' in day_schedule:
            Slist[day_schedule.index('A')][2][Day] = 'D'
            Slist[day_schedule.index('C')][2][Day] = 'E'
        Day+=1
    for i in range(day):
        for m in range(member):
            if Slist[m][2][i] == 1 and i not in WhoChangeWhichDay[m]: Slist[m][2][i] = 'L'
            elif Slist[m][2][i] == 1 and i in WhoChangeWhichDay[m]: Slist[m][2][i] = 'AL'
shiftName(S1_list,WhoChangeWhichDay1)
shiftName(S2_list,WhoChangeWhichDay2)
# ==========================================================================================================
# ----------------------------------------------寫出檔案-----------------------------------------------------
with open(file_out, 'w', newline='', encoding = 'utf-8') as csvfile:
     # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow(['year', 'month', 'group','name','prefer',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,'A','B','C','D','E','PR','L','AL','WH','OH'])
    # 寫入另外幾列資料
    for m in range(member):
        A = 0
        B = 0
        C = 0
        D = 0
        E = 0
        PR = 0
        AL = 0
        s1_out = []
        s1_out.append(year)
        s1_out.append(month)
        for i in range(3):s1_out.append(S1_list[m][1][i])
        for i in range(day):s1_out.append(S1_list[m][2][i])
        if day < 31:
            for i in range(31-day):
                s1_out.append('-')
        if 'A' in S1_list[m][2]: A = S1_list[m][2].count('A')
        if 'B' in S1_list[m][2]: B = S1_list[m][2].count('B')
        if 'C' in S1_list[m][2]: C = S1_list[m][2].count('C')
        if 'D' in S1_list[m][2]: D = S1_list[m][2].count('D')
        if 'E' in S1_list[m][2]: E = S1_list[m][2].count('E')
        s1_out.append(A)
        s1_out.append(B)
        s1_out.append(C)
        s1_out.append(D)
        s1_out.append(E)
        if S1_list[m][1][2] == 'A':PR = A+D
        else:PR = C+E
        s1_out.append(PR)
        if 'L' in S1_list[m][2]: L = S1_list[m][2].count('L')
        if 'AL' in S1_list[m][2]: AL = S1_list[m][2].count('AL')
        s1_out.append(L)
        s1_out.append(AL)
        WH = (A+B+C)*8 + (D+E)*12
        OH = (D+E)*4
        s1_out.append(WH)
        s1_out.append(OH)
        writer.writerow(s1_out)

    for m in range(member):
        A = 0
        B = 0
        C = 0
        D = 0
        E = 0
        PR = 0
        AL = 0
        s2_out = []
        s2_out.append(year)
        s2_out.append(month)
        for i in range(3):s2_out.append(S2_list[m][1][i])
        for i in range(day):s2_out.append(S2_list[m][2][i])
        if day < 31:
            for i in range(31-day):
                s2_out.append('-')
        if 'A' in S2_list[m][2]: A = S2_list[m][2].count('A')
        if 'B' in S2_list[m][2]: B = S2_list[m][2].count('B')
        if 'C' in S2_list[m][2]: C = S2_list[m][2].count('C')
        if 'D' in S2_list[m][2]: D = S2_list[m][2].count('D')
        if 'E' in S2_list[m][2]: E = S2_list[m][2].count('E')
        s2_out.append(A)
        s2_out.append(B)
        s2_out.append(C)
        s2_out.append(D)
        s2_out.append(E)
        if S2_list[m][1][2] == 'A':PR = A+D
        else:PR = C+E
        s2_out.append(PR)
        if 'L' in S2_list[m][2]: L = S2_list[m][2].count('L')
        if 'AL' in S2_list[m][2]: AL = S2_list[m][2].count('AL')
        s2_out.append(L)
        s2_out.append(AL)
        WH = (A+B+C)*8 + (D+E)*12
        OH = (D+E)*4
        s2_out.append(WH)
        s2_out.append(OH)
        writer.writerow(s2_out)
    csvfile.close()
