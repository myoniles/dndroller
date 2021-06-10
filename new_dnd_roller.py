import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import pandas
from Characters import characters

EPOCH = 10000
SAME_POOL = True

def str_or_int(strint):
	if type(strint) == str and 'd' in strint:
		strint = strint.split('d')

rgx = r"(\d+)d(\d+)\s*([+|-]\s*\d*)?"
pattern = re.compile(rgx)
def string_to_roll(strint):
	m = pattern.match(strint)
	print(m.groups())
	nums =  [0 if g==None else int(g) for g in m.groups()]
	return tuple(nums)

class Attack():
	def __init__(self, to_hit_bonus, damage_on_hit, name='', elven_acc=False, repeated=1):
		self.hit_bonus = to_hit_bonus
		self.repeated = repeated

		#self.on_hit_n, self.on_hit_die = damage_on_hit.split('d')
		#self.on_hit_n, self.on_hit_die = int(self.on_hit_n), int(self.on_hit_die)

		dice_nums = string_to_roll(damage_on_hit)
		self.on_hit_n, self.on_hit_die, self.on_hit_flat = dice_nums


		self.elven_acc = elven_acc
		self.adv = False
		self.dis = False
		self.name = name

	def give_adv(self):
		if self.dis:
			self.dis = False
			return
		self.adv = True

	def give_adv(self):
		if self.adv:
			self.adv = False
			return
		self.dis = True

	def roll_damage(self):
		n_rolls = 1 + (self.adv ^ self.dis) + ((self.adv ^ self.dis) & self.adv) * self.elven_acc
		rolls = [random.randint(1,20) + self.hit_bonus for r in range(n_rolls)]
		roll = rolls[0]
		if self.adv ^ self.dis:
			roll = max(rolls) if adv else min(rolls)

		dmg = sum([random.randint(1, self.on_hit_die) + self.on_hit_flat for n in range(self.on_hit_n)])
		dmg *= self.repeated
		if roll == 20 + self.hit_bonus:
			roll = 'N'
			dmg *= 2
		elif roll <= 1 + self.hit_bonus:
			roll = -1
			dmg = 0
		return (roll, dmg)

def roll_attacks(attacks, ac):
	acc = 0
	for attack in attacks:
		roll, dmg = attack.roll_damage()
		if roll == 'N' or roll > ac:
			acc += dmg
	return acc


attacks = [
	Attack(5, '4d8+27', name='test', repeated=7),
]

def generate_pools(attacks, num):
	acc = {}
	for attack in attacks:
		acc[attack.name] = [ attack.roll_damage() for n in range(num)]
	return acc

def mean(ac, pool):
	acc = 0
	for p in pool:
		acc += p[1] if (p[0] == 'N' or p[0] > ac) else 0
	return acc / len(pool)

def graph_damage_by_attack(df):
	x_axis = df.index
	fig, ax = plt.subplots(1,2)
	ax[0].set_title('Total Damage')
	ax[1].set_title('Damage by attack')
	ax[0].plot(x_axis, df.sum(axis=1), label='total dpt')
	for col in df:
		ax[1].plot(x_axis, df[col], label=col)
	plt.xlabel("Target Armor Class")
	plt.ylabel("Average Damage per round")
	plt.legend(loc=1, ncol=1)
	plt.show()

def graph_rounds_to_kill(df, characters):
	plt.title('Rounds to Kill')
	labels = []
	rounds = []
	s =df.sum(axis=1)
	for char in characters:
		labels.append(char.name)
		rounds.append(char.hp / s[char.ac])
	ypos = np.arange(len(labels))

	plt.bar(ypos, rounds)
	plt.xticks(ypos, labels)
	plt.ylabel("Rounds to Kill")
	plt.show()

if __name__ == '__main__':
	pools = generate_pools(attacks, EPOCH)
	linspace = list(range(18, 28))
	df = pandas.DataFrame(columns=[attack.name for attack in attacks], index=linspace)
	for ac in linspace:
		for attack in attacks:
			acc = 0
			p = pools[attack.name]
			df[attack.name][ac] = mean(ac, p)
	graph_damage_by_attack(df)
	graph_rounds_to_kill(df, characters)
