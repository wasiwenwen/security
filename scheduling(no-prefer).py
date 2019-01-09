#用目前排到的所有班計分
import random
from collections import Counter


def shift_schedule(S_list, member):
	point = dict()
	for i in range(member): #計點
		point[i] = 0
	schedule = [S_list[m][2] for m in range(member)] #總班表
	prefer_list = [S_list[m][1][2] for m in range(member)] #每個人的喜好
	prefer = dict()
	for i in range(member):
		prefer[i] = prefer_list[i]
	#先排AC班
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
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
					schedule[change_m][Day] = "A"
					day_schedule[change_m] = "A"		
					replace_work(schedule[change_m], final_start, Day, "A")

					schedule[day_schedule.index(0)][Day] = "C"
					end = find_end(Day, schedule[day_schedule.index(0)], 1)
					replace_work(schedule[day_schedule.index(0)], Day, end, "C")
					
				else: #A前面相等，看C
					for rm in repeat_m:
						locals()['length_after_' + str(rm)] = length(Day, find_end(Day, schedule[rm]), schedule[rm])
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
						schedule[change_m][Day] = "C"
						day_schedule[change_m] = "C"	
						replace_work(schedule[change_m], Day, final_end, "C")
					
						schedule[day_schedule.index(0)][Day] = "A"
						start = find_start(Day, schedule[day_schedule.index(0)], 1)
						replace_work(schedule[day_schedule.index(0)], start, Day, "A")
					
					else: #如果都相等
						random.shuffle(repeat_m) #隨機抽
						for rm in repeat_m:
							change_m = rm
							schedule[change_m][Day] = "A"
							day_schedule[change_m] = "A"		
							replace_work(schedule[change_m], final_start, Day, "A")
							
							schedule[day_schedule.index(0)][Day] = "C"
							end = find_end(Day, schedule[day_schedule.index(0)], 1)
							replace_work(schedule[day_schedule.index(0)], Day, end, "C")

			elif times[0] == 1:
				if times["C"] == 1:
					change_m = day_schedule.index(0)
					# day_schedule[change_m] = "A"
					schedule[change_m][Day] = "A"
					start = max(find_start(Day, schedule[change_m], 1), find_start(Day, schedule[change_m], "C"), find_start(Day, schedule[change_m], "A"))
					replace_work(schedule[change_m], start, Day, "A")
					
				elif times["A"] == 1:
					change_m = day_schedule.index(0)
					# day_schedule[change_m] = "C"
					schedule[change_m][Day] = "C"
					end = min(find_end(Day, schedule[change_m], 1), find_end(Day, schedule[change_m], "C"), find_end(Day, schedule[change_m], "A"))
					replace_work(schedule[change_m], Day, end, "C")
		Day += 1
	
	
	#排出整個月的B班，以連續上最多天(不換班)為準則
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		#如果那天還有空班且沒有B班
		if (0 in day_schedule) and ("B" not in day_schedule):
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
	
	# 當還有人沒有被排班
	not_done = True
	# for i in range(10):
	while not_done:
		not_done = False
		# 先排三缺一的限定班
		only_work(schedule)
		# 再按照喜好排班
		not_done = replace_by_prefer(schedule, prefer, point, not_done)
	# 最後輸出
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
	check_only = True
	while check_only:
		check_only = False
		Day = 0
		for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
			day_schedule = [m1, m2, m3, m4]
			#先判斷那天是否剩一天沒填
			if day_schedule.count(0) == 1:
				m = day_schedule.index(0)
				if "A" not in day_schedule:
					schedule[m][Day] = "A"
					start = max(find_start(Day, schedule[m], 1), find_start(Day, schedule[m], "A"), find_start(Day, schedule[m], "B"), find_start(Day, schedule[m], "C"))
					replace_work(schedule[m], start, Day, "A")
				elif "C" not in day_schedule:
					schedule[m][Day] = "C"
					end = min(find_end(Day, schedule[m], 1), find_end(Day, schedule[m], "A"), find_end(Day, schedule[m], "B"), find_end(Day, schedule[m], "C"))
					replace_work(schedule[m], Day, end, "C")
				check_only = True #如果有三缺一，就要重頭再檢查一次
			Day += 1
			

def replace_by_prefer(schedule, prefer, point, check_done):
	Day = 0
	for m1, m2, m3, m4 in zip(schedule[0], schedule[1], schedule[2], schedule[3]):
		day_schedule = [m1, m2, m3, m4]
		times = Counter(day_schedule)
		if times[0] == 2:
			notyet_m = [p for p, v in enumerate(day_schedule) if v == 0] #找到那天還沒排班的人
			"""
			if prefer[notyet_m[0]] != prefer[notyet_m[1]]:# 如果兩個人的喜好不重複
				for m in notyet_m:
					replace1 = prefer[m] #第一個人的喜好
					if replace1 == "A":
						# schedule[m][Day] = replace1
						start = max(find_start(Day, schedule[m], 1), find_start(Day, schedule[m], "A"),find_start(Day, schedule[m], "B"), find_start(Day, schedule[m], "C"))
						replace_work(schedule[m], start, Day, "A")
						# if prefer[m] == "A": point[m] += (len(schedule[m][start: Day]) + 1)
					elif replace1 == "C":
						# schedule[m][Day] = "C"
						end = min(find_end(Day, schedule[m], 1), find_end(Day, schedule[m], "A"), find_end(Day, schedule[m], "C"),find_end(Day, schedule[m], "B"))
						replace_work(schedule[m], Day, end, "C")
						# if prefer[m] == "C": point[m] += (len(schedule[m][Day: end]))
			"""
			# else: #如果兩人喜好重複
				#先比點數
				# prefer1 = prefer[notyet_m[0]]

				# if schedule[notyet_m[0]].count(prefer1) > schedule[notyet_m[1]].count(prefer1):
					# m_one, m_two = notyet_m[1], notyet_m[0]
				# elif schedule[notyet_m[0]].count(prefer1) < schedule[notyet_m[1]].count(prefer1):
					# m_one, m_two = notyet_m[0], notyet_m[1]
				# else:
			prefer1 = random.choice(["A","C"])
			# random.shuffle(notyet_m)
			m_one, m_two = notyet_m[0], notyet_m[1]
			replace1 = prefer1
			# replace1 = prefer[m_one] #第一個人的喜好
			if replace1 == "A": #如果第一個人的喜好是"A"
				# schedule[m_one][Day] = "A"
				start = max(find_start(Day, schedule[m_one], 1), find_start(Day, schedule[m_one], "A"), find_start(Day, schedule[m_one], "B"), find_start(Day, schedule[m_one], "C"))
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
			check_done = True
			break
		Day += 1
	return check_done
	