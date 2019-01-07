"""
1.雙休
	1先抓兩天休假，前面比較多天的都塞進A
	2另一格往後都填完C
2.塞B

"""
import random
from collections import Counter
#S1_list[m][2] 是 目前的班表
# A B C
member = 4
S1_list = [[8, ['S1', 'M1', 'A'], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0]], [8, ['S1', 'M2', 'B'], [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], [8, ['S1', 'M3', 'A'], [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]], [8, ['S1', 'M4', 'C'], [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]]]

b_A = ["A", "D"]
b_B = ["A", "B", "D"]
b_C = ["A", "B", "C", "D", "E"]

point = dict()
for i in range(member):
	point[i] = 0

def shift_schedule(S_list, member):
	schedule = [S_list[m][2] for m in range(member)] #總班表
	prefer = [S_list[m][1][2] for m in range(member)] #每個人的喜好
	# day_schedule_all = [] #
	# for d in range(len(schedule[0])): 
		# day_schedule_all.append([schedule[m][d] for m in range(member)]) #每天的班表
	
	#先排AC班
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
	# for day_schedule in day_schedule_all:
		times = Counter(day_schedule)
		if times[1] == 2:
			if times[0] == 2:
				repeat_m = [p for p, v in enumerate(day_schedule) if v == 0] #找到那天要上班的人
				for rm in repeat_m:
					locals()['length_before_' + str(rm) ] = length(find_start(Day, schedule[rm], 1), Day, schedule[rm])
				if 'length_before_' + str(repeat_m[0]) != 'length_before_' + str(repeat_m[1]):
					max1 = -11 #上班日最大值
					change_m = 100 #連續上班日最少的人
					final_start = 10000
					for rm in repeat_m:
						start = find_start(Day, schedule[rm], 1)
						if length(start, Day, schedule[rm]) > max1:
							max1 = length(find_start(Day, schedule[rm], 1), find_end(Day, schedule[rm]), schedule[rm])
							change_m = rm
							final_start = start
					schedule[change_m][Day] = "A"
					day_schedule[change_m] = "A"
					replace_work(schedule[change_m], final_start, Day, "A")
					# print(change_m, day_schedule.index(0))
					schedule[day_schedule.index(0)][Day] = "C"
					replace_work(schedule[day_schedule.index(0)], Day, find_end(Day, schedule[day_schedule.index(0)]), "C")
				else:
					for rm in repeat_m:
						locals()['length_after_' + str(rm) ] = length(Day, find_end(Day, schedule[rm]), schedule[rm])
					if 'length_after_' + str(repeat_m[0]) != 'length_after_' + str(repeat_m[1]):
						max1 = -11 #上班日最大值
						change_m = 100 #連續上班日最少的人
						final_end = 10000
						for rm in repeat_m:
							end = find_end(Day, schedule[rm])
							if length(Day, end, schedule[rm]) > max1:
								max1 = length(Day, find_end(Day, schedule[rm]), schedule[rm])
								change_m = rm
								final_end = end
					schedule[change_m][Day] = "C"
					day_schedule[change_m] = "C"				
					replace_work(schedule[change_m], Day, final_end, "C")
					schedule[day_schedule.index(0)][Day] = "A"
					replace_work(schedule[day_schedule.index(0)],find_start(Day, schedule[day_schedule.index(0)], 1), end, "A")
			if times[0] == 1:
				if times["C"] == 1:
					M = day_schedule.index(0)
					day_schedule[M] = "A"
					schedule[M][Day] = "A"
					# print(find_start(Day, schedule[M], 1), find_start(Day, schedule[M], "C"), find_start(Day, schedule[M], "A"))
					start = max(find_start(Day, schedule[M], 1), find_start(Day, schedule[M], "C"), find_start(Day, schedule[M], "A"))
					replace_work(schedule[M], start, Day, "A")
				elif times["A"] == 1:
					M = day_schedule.index(0)
					day_schedule[M] = "C"
					schedule[M][Day] = "C"
					end = min(find_end(Day, schedule[M], 0), find_end(Day, schedule[M], "C"), find_end(Day, schedule[M], "A"))
					replace_work(schedule[M], Day, end, "C")

		Day += 1
	#再挑出必須特休的日子
	"""
	cycle = 0
	while True:
		Day = 0
		H_check_list = [[],[],[],[]]
		for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
			day_schedule = [m1, m2, m3, m4]
			#如果當天沒人休假
			if day_schedule.count(1) == 0:
				for m in range(member):
					if Day == 0:
						if schedule[m][Day] == 0 and schedule[m][Day + 1] == 1:
							H_check_list[m].append("T")
						else: H_check_list[m].append("F")
					elif Day == len(schedule[0]) - 1:
						if schedule[m][Day] == 0 and schedule[m][Day - 1] == 1:
							H_check_list[m].append("T")
						else: H_check_list[m].append("F")
					else:
						if schedule[m][Day] == 0 and schedule[m][Day + 1] == 1 and schedule[m][Day - 1] == 1:
							H_check_list[m].append("P")
						elif schedule[m][Day] == 0 and ((schedule[m][Day + 1] == 1 and schedule[m][Day - 1] == 0) or (schedule[m][Day + 1] == 0 and schedule[m][Day - 1] == 1)):
							H_check_list[m].append("T")
						else: 
							H_check_list[m].append("F")
			else:
				for m in range(member):
					H_check_list[m].append("F")
			Day += 1
			cycle += 1
		T_list = []
		P_list = []
		for m in range(member):
			T_list.append(H_check_list[m].count("T"))
			P_list.append(H_check_list[m].count("P"))
		
		
		if cycle >= 1:
			break
		"""	
	
	#判斷B班
	for day in range(len(schedule[0])):
		for 
	
	
	
	
	
	
	
	
	
	
	
	for i in range(m):
		S_list[i][2] = schedule[i]
	return S_list

			
def find_end(day, one_schedule):
	slice = one_schedule[day:]
	if 1 in slice: end = slice.index(1)
	else: end = len(one_schedule)
	return (end + day)

def find_start(day, one_schedule, stop): #one_schedule是要數的人的班表
	slice = one_schedule[:day]
	if stop in slice: start = dict(map(reversed, enumerate(slice)))[stop] + 1
	else: start = 0
	return start 

def length(start, end, one_schedule):
	length_w = len(one_schedule[start :end])
	return length_w
	
def add(day, holiday, one_schedule, replace_d): #如果是零，就替代掉後面的部分
	if holiday == 0:
		end = find_end(day, one_schedule) + day
		one_schedule[day: end] = replace_d * len(one_schedule[day: end])
		
def replace_work(one_schedule, day, end, replace_d):
	one_schedule[day: end] = replace_d * len(one_schedule[day: end])

	
# print(shift_schedule(S1_list, m))

#同一天要有ABC 
#轉換次數
#