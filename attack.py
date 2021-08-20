import re
import util
from Stat import Stat

def calc_attack_at_ac(attack, effective_ac):
	acc = 0
	hit_func = util.prob_hit_n

	acc += sum([ hit_func(n) * attack.exp_dmg for n in range(effective_hit, 20)])
	acc += attack.crit_dmg()
	return acc

class Move():
	def __init__(self, damage_on_hit, challenge, name='', repeated=1):
		print(damage_on_hit, challenge)
		self.repeated = repeated

		# Kept for notekeeping
		self.challenge_attribute = challenge

		dice_nums = util.string_to_roll(damage_on_hit)
		self.on_hit_n, self.on_hit_die, self.on_hit_flat = dice_nums
		self.name = name

	def _calc_dmg(self):
		# this is just a wrapper
		# It calculates damage regardless of AC or challenge
		# Use this in conjunction with prob_hit to determine damage against a specific AC
		return util.get_avg_roll(self.on_hit_n, self.on_hit_die) + self.on_hit_flat

	def calc_dmg(self, target):
		# override in children
		assert(False)

class Attack(Move):
	def __init__(self, to_hit_bonus, damage_on_hit, name = '', repeated=1):
		super().__init__(damage_on_hit, Stat.AC, name=name, repeated=repeated)
		self.hit_bonus = to_hit_bonus
		self.adv = False
		self.dis = False
		self._adv_hit_func = util.prob_hit_adv
		self._dis_hit_func = util.prob_hit_dis

	def update(self):
		self.hit_func = util.prob_hit_n
		if self.adv and self.dis:
			self.adv, self.dis = (False, False)
		if self.adv and not self.dis:
			self.hit_func = self._adv_hit_func
		elif not self.adv and self.dis:
			self.hit_func = self._dis_hit_func

	def give_adv(self):
		if self.dis:
			self.dis = False
			return
		self.adv = True

	def give_dis(self):
		if self.adv:
			self.adv = False
			return
		self.dis = True

	def calc_dmg(self, target):
		self.update()
		acc = 0

		effective_challenge = max(target.stat_block[Stat.AC] - self.hit_bonus, 0)
		acc += sum([ self._calc_dmg() * self.hit_func(n) for n in range(effective_challenge+1, 20)])

		# Natural 20
		if target.stat_block[Stat.AC] < 20 + self.hit_bonus:
			acc += self.hit_func(20) * (2*(util.get_avg_roll(self.on_hit_n, self.on_hit_die)) + self.on_hit_flat)
		return acc

class Check(Move):
	def __init__(self,skill, DC, damage_on_hit, name='', repeated=1):
		super().__init__(damage_on_hit, skill, name=name, repeated=repeated)
		self.DC=0

	def calc_dmg(self, target):
		acc = 0
		acc += self._calc_dmg() * (self.DC - target.get_bonus(self.challenge_attribute, False))/20
		return acc

class Save(Move):
	def __init__(self, stat ,DC, damage_on_hit, name='', repeated=1):
		super().__init__(damage_on_hit, stat, name=name, repeated=repeated)
		self.DC=DC

	def calc_dmg(self, target):
		#TODO
		acc = 0
		acc += self._calc_dmg() * (self.DC - target.get_bonus(self.challenge_attribute, True))/20
		return acc
