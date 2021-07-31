import attack
from Stat import Stat
import pandas as pd
import random
import util

class Character():
	#TODO separate the character into two comonents: Stat block and attacks?

	def __init__(self,name, hp, ac, level=1, elven_acc=False, crit_min = 20):
		self.name = name
		self.prof_bonus = 0
		self.prof= {} # Holds str of skills profficient in
		self.hp = hp
		self.ac = ac
		# TODO
		stat_block = [(s, 10) for s in list(Stat)]
		self.stat_block = dict(stat_block)
		self.crit_min = min(20, crit_min)
		self.elven_acc = elven_acc

		self._attacks = []

	def to_kill_target(self, defender):
		acc = 0
		for attack in self.attacks:
			acc += attack.calc

	def set_attacks(self, attacks):
		self._attacks = attacks.copy()
		if self.elven_acc:
			for a in attacks:
				a._adv_hit_func = prob_hit_elven
				a.update()

	def set_stat(self, stat_type, value):
		self.stat_block[stat_type] = value

	def get_attacks(self):
		return self._attacks.copy()


	def get_bonus(self, attr, save=True):
		acc = 0
		if save and attr in self.prof:
			acc += self.prof_bonus
		acc += util.bonus_from_attribute(self.stat_block[attr])
		return acc

	def register_attack(self, attack):
		self._attacks.append(attack)

	def generate_df(self, linspace, targets=None):
		if not targets:
			targets = [ Character('dummy_'+str(i) , random.randint(1,100), 10) for i in linspace ]
			for i in range(len(targets)):
				targets[i].set_stat(Stat.DEX, 2*i)
				print(targets[i].stat_block[Stat.DEX])
		df = pd.DataFrame(columns=[attack.name for attack in self._attacks], index=linspace)
		for target in targets:
			for a in self._attacks:
				df[a.name][target.get_bonus(Stat.DEX)] = a.calc_dmg(target)
		return df


characters = [
	Character('Amon', 135, 23),
	Character('Giaus', 94, 20),
	Character('Knack', 157, 20),
	Character('Shvari', 126, 18),
	Character('Solin', 132, 22)
]

Giaus = characters[1]
