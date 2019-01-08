
import random
from collections import Counter
#S1_list[m][2] 是 目前的班表
# A B C
member = 4
S1_list = [[8, ['S1', 'M1', 'A'], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0]], [8, ['S1', 'M2', 'B'], [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], [8, ['S1', 'M3', 'A'], [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]], [8, ['S1', 'M4', 'C'], [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]]]

b_A = ["A", "D"]
b_B = ["A", "B", "D"]
b_C = ["A", "B", "C", "D", "E"]

 

def shift_schedule(S_list, member):
	point = dict()
	for i in range(member): #計點
		point[i] = 0
	schedule = [S_list[m][2] for m in range(member)] #總班表
	prefer_list = [S_list[m][1][2] for m in range(member)] #每個人的喜好
	prefer = dict()
	for i in range(member):
		prefer[i] = prefer_list[i]
	# day_schedule_all = [] #
	# for d in range(len(schedule[0])): 
		# day_schedule_all.append([schedule[m][d] for m in range(member)]) #每天的班表
	
	#先排AC班
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		print(Day)
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
							max1 = length(find_start(Day, schedule[rm], 1), find_end(Day, schedule[rm], 1), schedule[rm])
							change_m = rm
							final_start = start
					#換勝出的人
					schedule[change_m][Day] = "A"
					day_schedule[change_m] = "A"
					replace_work(schedule[change_m], final_start, Day, "A")
					#換另一個人
					schedule[day_schedule.index(0)][Day] = "C"
					replace_work(schedule[day_schedule.index(0)], Day, find_end(Day, schedule[day_schedule.index(0)], 1), "C")
				else:
					for rm in repeat_m:
						locals()['length_after_' + str(rm) ] = length(Day, find_end(Day, schedule[rm]), schedule[rm])
					if 'length_after_' + str(repeat_m[0]) != 'length_after_' + str(repeat_m[1]):
						max1 = -11 #上班日最大值
						change_m = 100 #連續上班日最少的人
						final_end = 10000
						for rm in repeat_m:
							end = find_end(Day, schedule[rm], 1)
							if length(Day, end, schedule[rm]) > max1:
								max1 = length(Day, find_end(Day, schedule[rm], 1), schedule[rm])
								change_m = rm
								final_end = end
					#換勝出的人
					schedule[change_m][Day] = "C"
					day_schedule[change_m] = "C"				
					replace_work(schedule[change_m], Day, final_end, "C")
					#換另一個人
					schedule[day_schedule.index(0)][Day] = "A"
					replace_work(schedule[day_schedule.index(0)],find_start(Day, schedule[day_schedule.index(0)], 1), Day, "A")
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
					end = min(find_end(Day, schedule[M], 1), find_end(Day, schedule[M], "C"), find_end(Day, schedule[M], "A"))
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
	
	#排出整個月的B班，以連續上最多天(不換班)為準則
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		#先判斷那天是否還有空班
		if day_schedule.count(0) == 0: 
			Day += 1
			continue
		elif "B" in day_schedule:
			Day += 1
			continue
		else:
			repeat_m = [p for p, v in enumerate(day_schedule) if v == 0] #找到還沒排班的人
			maxlen = -1
			for m in repeat_m:
				end = min(find_end(Day, schedule[m], 1), find_end(Day, schedule[m], "C"), find_end(Day, schedule[m], "A"))
				len1 = length(Day, end, schedule[m])
				if len1 > maxlen:
					maxlen = len1
					change_m = m
					final_end = end 
			replace_work(schedule[change_m], Day, final_end, "B")
			Day += 1
	
	#當還有人沒有被排班
	cycle = 0
	while cycle <= 11:
		#先塞唯一解
		only_work(schedule) 
		#再按照喜好排班
		replace_by_prefer(schedule, prefer, point)
		cycle += 1
	"""
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		先判斷那天是否剩一天沒填
		if day_schedule.count(0) == 1:
			m = day_schedule.index(0)
			if "A" not in day_schedule:
				schedule[m][Day] = "A"
			elif "C" not in day_schedule:
				schedule[m][Day] = "C"
			Day += 1
		else: Day += 1
	"""
	#考量偏好，填完剩下的班表
	"""
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		times = Counter(day_schedule)
		if times[0] == 2:
			notyet_m = [p for p, v in enumerate(day_schedule) if v == 0] #找到那天還沒排班的人
			if prefer[notyet_m[0]] =! prefer[notyet_m[1]]:# 如果兩個人的喜好不重複
				for m in notyet_m:
					replace1 = prefer[m] #第一個人的喜好
					if replace1 == "A":
						schedule[notyet_m[0]][Day] = replace1
						replace_work(schedule[notyet_m[0]],  find_start(Day, schedule[notyet_m[0]]), end, "A")
					elif replace1 == "C":
						schedule[notyet_m[0]][Day] = replace1
						replace_work(schedule[notyet_m[0]], Day, find_end(Day, schedule[notyet_m[0]]), "C")		
			else: #如果兩人喜好重複
				random.shuffle(notyet_m)
				m_one, m_two = notyet_m[0], notyet_m[1]
				point[m_one] += 1
				replace1 = prefer[m_one] #第一個人的喜好
				if replace1 == "A": #如果第一個人的喜好是"A"
					schedule[m_one][Day] = "A"
					replace_work(schedule[m_one],  find_start(Day, schedule[m_one]), end, "A")
					replace2 == "C" #第二個人就得填C
					schedule[m_two][Day] = replace2
					replace_work(schedule[m_two], Day, find_end(Day, schedule[m_two]), "C")
				elif replace1 == "C": #如果第一個人的喜好是"C"
					schedule[m_one][Day] = "C"
					replace_work(schedule[m_one], Day, find_end(Day, schedule[m_two]), "C")
					replace2 == "A" #第二個人就得填A
					replace_work(schedule[m_two],  find_start(Day, schedule[m_two]), end, "A")
		else:
			Day += 1
		"""
	#最後輸出
	print(point)
	for i in range(member):
		S_list[i][2] = schedule[i]
	return S_list

			
def find_end(day, one_schedule, stop):
	slice = one_schedule[day:]
	if stop in slice: end = slice.index(stop)
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
		
def replace_work(one_schedule, day, end, replace_d):
	one_schedule[day: end] = replace_d * len(one_schedule[day: end])
	

def only_work(schedule):
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		#先判斷那天是否剩一天沒填
		if day_schedule.count(0) == 1:
			m = day_schedule.index(0)
			if "A" not in day_schedule:
				schedule[m][Day] = "A"
				# start = max(find_start(Day, schedule[m], 1), find_start(Day, schedule[m], "A"), find_start(Day, schedule[m], "B"), find_start(Day, schedule[m], "C"))
				# replace_work(schedule[m], start, Day, "A")
			else:
				schedule[m][Day] = "C"
				# end = min(find_end(Day, schedule[m], 1), find_end(Day, schedule[m], "A"), find_end(Day, schedule[m], "B"), find_end(Day, schedule[m], "C"))
				# replace_work(schedule[m], Day, end, "C")
			Day += 1
		else: Day += 1

def replace_by_prefer(schedule, prefer, point):
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		times = Counter(day_schedule)
		if times[0] == 2:
			notyet_m = [p for p, v in enumerate(day_schedule) if v == 0] #找到那天還沒排班的人
			if prefer[notyet_m[0]] != prefer[notyet_m[1]]:# 如果兩個人的喜好不重複
				for m in notyet_m:
					replace1 = prefer[m] #第一個人的喜好
					if replace1 == "A":
						# schedule[m][Day] = replace1
						start = max(find_start(Day, schedule[m], 1), find_start(Day, schedule[m], "A"),find_start(Day, schedule[m], "B"), find_start(Day, schedule[m], "C"))
						replace_work(schedule[m], start, Day, "A")
					elif replace1 == "C":
						# schedule[m][Day] = "C"
						end = min(find_end(Day, schedule[m], 1), find_end(Day, schedule[m], "A"), find_end(Day, schedule[m], "C"),find_end(Day, schedule[m], "B"))
						replace_work(schedule[m], Day, end, "C")
				
			else: #如果兩人喜好重複
				#先比點數
				if point[notyet_m[0]] > point[notyet_m[1]]: 
					m_one, m_two = notyet_m[1], notyet_m[0]
				elif point[notyet_m[0]] < point[notyet_m[1]]:
					m_one, m_two = notyet_m[0], notyet_m[1]
				else:
					random.shuffle(notyet_m)
					m_one, m_two = notyet_m[0], notyet_m[1]
				point[m_one] += 1 #m_one可以排到自己喜歡的班
				replace1 = prefer[m_one] #第一個人的喜好
				if replace1 == "A": #如果第一個人的喜好是"A"
					# schedule[m_one][Day] = "A"
					start = max(find_start(Day, schedule[m_one], 1),find_start(Day, schedule[m_one], "A"), find_start(Day, schedule[m_one], "B"), find_start(Day, schedule[m_one], "C"))
					replace_work(schedule[m_one], start, Day, "A")
					replace2 = "C" #第二個人就得填C
					# schedule[m_two][Day] = replace2
					end = min(find_end(Day, schedule[m_two], 1), find_end(Day, schedule[m_two], "A"), find_end(Day, schedule[m_two], "B"))
					replace_work(schedule[m_two], Day, end, "C")
				elif replace1 == "C": #如果第一個人的喜好是"C"
					# schedule[m_one][Day] = "C"
					end = min(find_end(Day, schedule[m_one], 1),find_end(Day, schedule[m_one], "C"), find_end(Day, schedule[m_one], "A"), find_end(Day, schedule[m_one], "B"))
					replace_work(schedule[m_one], Day, end,"C")
					
					replace2 = "A" #第二個人就得填A
					# schedule[m_two][Day] = "A"
					start = max(find_start(Day, schedule[m_two], 1), find_start(Day, schedule[m_two], "A"),find_start(Day, schedule[m_two], "B"), find_start(Day, schedule[m_two], "C"))
					replace_work(schedule[m_two], start, Day, "A")
			Day += 1
			break
		else: Day += 1	

print(shift_schedule(S1_list, member))
print(len(S1_list[0][2]))
#塞天數的問題