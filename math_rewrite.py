from Characters import Chracter

def prob_hit_n(n):
	assert(n <= 20)
	return 1/20

def prob_hit_adv(n):
	assert(n <= 20)
	return (2*n-1) / 20**2

def prob_hit_elven(n):
	assert(n <= 20)
	return 1 + 3*n*(n - 1)/20**3

def get_avg_roll(num_die, hit_die):
	# 1/n (1 + 2 + 3 + ...n-1 +  n )
	# = 1/n ( ( n + 1 ) + (n-1 + 2) + ... )
	# = (n/2 * (n + 1) ) / n
	# = (n+1) / 2
	return num_die * (hit_die + 1 )/2

def effective_roll(attacker, defender):
	# attacker: Character
	# defender Character
	effective_ac = defender.ac - attacker.
