import csv
import datetime
import calendar
import random

# ==========================================================================================================
# 初始值設定

# 該月有幾天
day = 0
# 幾個假日
all_sun_sat = 0

# S1/S2的list
S1_list = []
S2_list = []

# 單一地點成員數
member = 4
# 
file_in  = 'v_in.csv'
file_out = 'v_out.csv'
# ==========================================================================================================
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
# ==========================================================================================================
year , month = read8(file_in)

# print(S1_list)
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
        if cycle>day*member:
            break
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
        if cycle>day*member:
            break
# print(s1_allleft_peroneday_list)
# print(s2_allleft_peroneday_list)
# print(S1_list)
# print(S2_list)
# ==========================================================================================================
# 將單日休假人數的日子補上還沒排滿all_sun_sat的人
# print(s1_allleft_peroneday_list.count(0))
# print(s2_allleft_peroneday_list.count(0))
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
# print(s1_allleft_peroneday_list)
# print(s2_allleft_peroneday_list)
# print(S1_list)
# print(S2_list)
# ==========================================================================================================
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
print(s1_allleft_peroneday_list)
# print(s2_allleft_peroneday_list)
print(S1_list)
# print(S2_list)
# ==========================================================================================================
# 如果大家假都修完，但是還是有某些日子沒人休息
# if s1_allleft_peroneday_list.count(0)>0:
#     need_your_left1 = ['','','','','','']
#     for i in range(day):
#         if s1_allleft_peroneday_list[i] == 0:
#             need_your_left1.append('需特休')
#         else:
#             need_your_left1.append('')
#     print(need_your_left1)
# if s2_allleft_peroneday_list.count(0)>0:
#     need_your_left2 = ['','','','','','']
#     for i in range(day):
#         if s2_allleft_peroneday_list[i] == 0:
#             need_your_left2.append('需特休')
#         else:
#             need_your_left2.append('')
#     print(need_your_left2)
# ==========================================================================================================
# 塞特休
# 判斷連假
while s1_allleft_peroneday_list.count(0) != 0:
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S1_list[0][2] , S1_list[1][2] , S1_list[2][2] , S1_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order + 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order - 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S1_list[m][2][order] == 0 and (S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 1):
                        H_check_list[m].append('P')
                    elif S1_list[m][2][order] == 0 and ((S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 0) or (S1_list[m][2][order + 1] == 0 and S1_list[m][2][order - 1] == 1)):
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member):
                H_check_list[m].append('F')
        order += 1
    print(H_check_list)
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
    # print(nPTm_list)
    nPTm_list.sort(reverse=True)
    print(nPTm_list)
    # 先換一天每人一天
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0:
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s1_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0:
            
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] += -1
            s1_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
    print(S1_list)
    print(s1_allleft_peroneday_list)
    break
while s1_allleft_peroneday_list.count(0) != 0:
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S1_list[0][2] , S1_list[1][2] , S1_list[2][2] , S1_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order + 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S1_list[m][2][order] == 0 and S1_list[m][2][order - 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S1_list[m][2][order] == 0 and (S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 1):
                        H_check_list[m].append('P')
                    elif S1_list[m][2][order] == 0 and ((S1_list[m][2][order + 1] == 1 and S1_list[m][2][order - 1] == 0) or (S1_list[m][2][order + 1] == 0 and S1_list[m][2][order - 1] == 1)):
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member):
                H_check_list[m].append('F')
        order += 1

    for m in range(member):
        sort = nPTm_list[m][3]
        P = H_check_list[sort].count('P')
        T = H_check_list[sort].count('T')
        nPTm_list[m][1] = P
        nPTm_list[m][2] = T
    nPTm_list.sort(reverse=True)
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0:
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s1_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0:
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S1_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s1_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
    if s1_allleft_peroneday_list.count(0) == 0:
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
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order + 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order - 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S2_list[m][2][order] == 0 and (S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 1):
                        H_check_list[m].append('P')
                    elif S2_list[m][2][order] == 0 and ((S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 0) or (S2_list[m][2][order + 1] == 0 and S2_list[m][2][order - 1] == 1)):
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member):
                H_check_list[m].append('F')
        order += 1
    print(H_check_list)
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
    # print(nPTm_list)
    nPTm_list.sort(reverse=True)
    print(nPTm_list)
    # 先換一天每人一天
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0:
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s2_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0:
            
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] += -1
            s2_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
    print(S2_list)
    print(s2_allleft_peroneday_list)
    break
while s2_allleft_peroneday_list.count(0) != 0:
    order = 0
    H_check_list = [[],[],[],[]]
    for m1 , m2 , m3 , m4 in zip(S2_list[0][2] , S2_list[1][2] , S2_list[2][2] , S2_list[3][2]):
        day_schedule = [m1 , m2 , m3 , m4]
        if day_schedule.count(1) == 0:
            for m in range(member):
                if order == 0:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order + 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                elif order == day - 1:
                    if S2_list[m][2][order] == 0 and S2_list[m][2][order - 1] == 1:
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
                else:
                    if S2_list[m][2][order] == 0 and (S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 1):
                        H_check_list[m].append('P')
                    elif S2_list[m][2][order] == 0 and ((S2_list[m][2][order + 1] == 1 and S2_list[m][2][order - 1] == 0) or (S2_list[m][2][order + 1] == 0 and S2_list[m][2][order - 1] == 1)):
                        H_check_list[m].append('T')
                    else: H_check_list[m].append('F')
        else:
            for m in range(member):
                H_check_list[m].append('F')
        order += 1

    for m in range(member):
        sort = nPTm_list[m][3]
        P = H_check_list[sort].count('P')
        T = H_check_list[sort].count('T')
        nPTm_list[m][1] = P
        nPTm_list[m][2] = T
    nPTm_list.sort(reverse=True)
    for sort in range(member):
        changeMen = nPTm_list[sort][3]
        if H_check_list[changeMen].count('P') > 0:
            changeDay = H_check_list[changeMen].index('P')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s2_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'
        elif H_check_list[changeMen].count('T') > 0 and H_check_list[changeMen].count('P') == 0:
            changeDay = H_check_list[changeMen].index('T')
            H_check_list[changeMen][changeDay] = 'F'
            S2_list[changeMen][2][changeDay] = 1
            nPTm_list[sort][0] -= 1
            s2_allleft_peroneday_list[changeDay] = 1
            for m in range(member):
                if m == changeMen:
                    break
                else: H_check_list[m][changeDay] = 'F'

# ==========================================================================================================
# 寫出檔案
with open(file_out, 'w', newline='', encoding = 'utf-8') as csvfile:
     # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)

    # 寫入一列資料
    writer.writerow(['year', 'month', 'group','name','prefer',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])

    # 寫入另外幾列資料
    for m in range(member):
        s1_out = []
        s1_out.append(year)
        s1_out.append(month)
        for i in range(3):
            s1_out.append(S1_list[m][1][i])
        for i in range(day):
            s1_out.append(S1_list[m][2][i])
        writer.writerow(s1_out)
    for m in range(member):
        s2_out = []
        s2_out.append(year)
        s2_out.append(month)
        for i in range(3):
            s2_out.append(S2_list[m][1][i])
        for i in range(day):
            s2_out.append(S2_list[m][2][i])
        writer.writerow(s2_out)
    csvfile.close()
