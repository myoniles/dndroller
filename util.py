import math
import re

rgx = r"(\d+)d(\d+)\s*([+|-]\s*\d*)?"
pattern = re.compile(rgx)

def string_to_roll(strint):
	m = pattern.match(strint)
	nums =  [0 if g==None else int(g) for g in m.groups()]
	return tuple(nums)

def prob_hit_n(n):
	assert(n <= 20)
	return 1/20

def prob_hit_adv(n):
	assert(n <= 20)
	return (2*n-1) / 20**2

def prob_hit_dis(n):
	assert(n <= 20)
	return

def prob_hit_elven(n):
	assert(n <= 20)
	return 1 + 3*n*(n - 1)/20**3

def get_avg_roll(num_die, hit_die):
	# 1/n (1 + 2 + 3 + ...n-1 +  n )
	# = 1/n ( ( n + 1 ) + (n-1 + 2) + ... )
	# = (n/2 * (n + 1) ) / n
	# = (n+1) / 2
	return num_die * ( hit_die + 1 )/2

def __prof(level):
	return 2 + (level-1)//4

def bonus_from_attribute(stat):
	return math.floor((stat - 10) / 2.0)
