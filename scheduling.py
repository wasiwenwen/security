import random
from collections import Counter
#S1_list[m][2] 是 目前的班表
# A B C
m = 4
# S1_list = [[8, ['S1', 'M1', 'A'], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0]], [8, ['S1', 'M2', 'B'], [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], [8, ['S1', 'M3', 'A'], [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]], [8, ['S1', 'M4', 'C'], [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]]]

b_A = ["A", "D"]
b_B = ["A", "B", "D"]
b_C = ["A", "B", "C", "D", "E"]

count = dict()
for i in range(m):
	count[i] = 0

def shift_schedule(S_list, member):
	schedule = [S_list[m][2] for m in range(member)] #每個人的班表
	prefer = [S_list[m][1][2] for m in range(member)] #每個人的喜好
	# for d in range(len(schedule[0])): 
		# day_schedule = [schedule[m][d] for m in range(member)] #每天的出席狀況
	for one_day in range(len(schedule[0])): #一天一天看
		p1 = 0
		for one_schedule in schedule: #一個一個人看
			#先把所有人填滿到下一個休假
			add(one_day, one_schedule[one_day], one_schedule, prefer[p1])
			p1 += 1 #換下一個人
		day_schedule = [schedule[m][one_day] for m in range(member)]
		times = Counter(day_schedule)
		if (times["A"] >= 1 and times["B"] >=1 and times["C"] >= 1) and (times[1] < 2):
			continue
		elif times[1] == 2:
			if times["A"] == 2:
				repeat_m = [p for p, v in enumerate(day_schedule) if v == "A"]
				random.shuffle(repeat_m)
				for rm in repeat_m:
					schedule[rm][one_day] = "C"
					end = find_end(one_day, schedule[rm])
					replace_work(schedule[rm], one_day, end, "C")
					count[rm] += 1
					break
					
			if times["C"] == 2:
				repeat_m = [p for p, v in enumerate(day_schedule) if v == "C"]
				random.shuffle(repeat_m)	
				for rm in repeat_m:
					if schedule[rm][one_day - 1] in b_A:
						schedule[rm][one_day] = "A"
						start = find_start(one_day, schedule[rm])
						replace_work(schedule[rm], start, one_day, "A")
						count[rm] += 1
						break
		else:
			repeat_w = times.most_common(1)[0][0] #出現最多的
			if times["A"] == 0: add_w = "A"
			elif times["B"] == 0: add_w = "B"
			elif times["C"] == 0: add_w = "C"
			repeat_m = [p for p, v in enumerate(day_schedule) if v == repeat_w]
			
			max = 0 #上班日最小值
			least_m = 100 #連續上班日最少的人
			final_end = 10000
			for rm in repeat_m:
				end = find_end(one_day, schedule[rm])
				if len(schedule[rm][one_day: one_day + end]) > max:
					max = len(schedule[rm][one_day: one_day + end])
					least_m = rm
					final_end = end
			replace_work(schedule[least_m], one_day, final_end, add_w)

	for i in range(m):
		S_list[i][2] = schedule[i]
	return S_list
			
def find_end(day, one_schedule):
	slice = one_schedule[day:]
	if 1 in slice: end = slice.index(1)
	else: end = len(one_schedule)
	return end

def find_start(day, one_schedule): #one_schedule是要移動的人的班表
	slice = one_schedule[:day]
	if 1 in slice: start = dict(map(reversed, enumerate(slice)))[1]
	else: start = len(one_schedule)
	return start
	
def add(day, holiday, one_schedule, replace_d): #如果是零，就替代掉後面的部分
	if holiday == 0:
		end = find_end(day, one_schedule)
		one_schedule[day: day + end] = replace_d * len(one_schedule[day: day + end])
		
def replace_work(one_schedule, day, end, replace_d):
	one_schedule[day: day + end] = replace_d * len(one_schedule[day: day + end])
	
# print(shift_schedule(S1_list, m))

#同一天要有ABC 
#轉換次數
#