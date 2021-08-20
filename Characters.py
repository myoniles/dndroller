import attack
from Stat import Stat
import pandas as pd
import random
import util

class Character():
	#TODO separate the character into two comonents: Stat block and attacks?
	# Nah I think its better if attacks act as a list of components.
	# Don't complicate the code base too much

	# Then Again I have more or less done that already
	# If a class is data and its associated functionality, why do I want to have just the data elsewhere?

	def __init__(self,name, hp, level=1, elven_acc=False, crit_min = 20):
		self.name = name
		self.prof_bonus = 0
		self.prof= {} # Holds str of skills profficient in
		self.hp = hp
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

	def evaluate_over(self, stat, linspace=list(range(0,21,2))):
		# Generate one dummy then update throughout
		# even with garbage collector it is cleaner
		dummy_stat = dict([(s, 10) for s in list(Stat)])
		dummy = Character('dummy', float('inf'))
		dummy.stat_block = dummy_stat
		df = pd.DataFrame(columns=[attack.name for attack in self._attacks], index=linspace)
		for challenge in linspace:
			dummy_stat[stat] = challenge
			# no need to update dummy because it already has the reference to the list
			for a in self._attacks:
				df[a.name][challenge] = a.calc_dmg(dummy)
		return df


characters = [
	Character('Amon', 135),
	Character('Giaus', 94),
	Character('Knack', 157),
	Character('Shvari', 126),
	Character('Solin', 132)
]
