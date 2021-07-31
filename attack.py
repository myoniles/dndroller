import re
import util
from Stat import Stat

def calc_attack_at_ac(attack, effective_ac):
	acc = 0
	hit_func = util.prob_hit_n

	acc += sum([ hit_func(n) * attack.exp_dmg for n in range(effective_hit, 20)])
	acc += attack.crit_dmg()
	return acc

class Attack():
	def __init__(self, to_hit_bonus, damage_on_hit, challenge=Stat.AC, name='', repeated=1, save=True):
		self.hit_bonus = to_hit_bonus
		self.DC=0
		if challenge != Stat.AC:
			self.DC = to_hit_bonus
		self.repeated = repeated

		self.challenge_attribute = challenge
		self.challenge_save = save

		dice_nums = util.string_to_roll(damage_on_hit)
		self.on_hit_n, self.on_hit_die, self.on_hit_flat = dice_nums

		self.adv = False
		self.dis = False
		self._adv_hit_func = util.prob_hit_adv
		self._dis_hit_func = util.prob_hit_dis
		self.name = name

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

	def _calc_dmg(self):
		#this is just a wrapper
		# It calculates damage regardless of AC or challenge
		# Use this in conjunction with prob_hit to determine damage against a specific AC
		self.update()
		return util.get_avg_roll(self.on_hit_n, self.on_hit_die) + self.on_hit_flat

	def calc_dmg(self, target):
		self.update()
		acc = 0
		if self.challenge_attribute == Stat.AC:
			effective_challenge = max(target.ac - self.hit_bonus, 0)
			acc += sum([ self._calc_dmg() * self.hit_func(n) for n in range(effective_challenge+1, 20)])
			# Natural 20
			if target.ac < 20 + self.hit_bonus:
				acc += self.hit_func(20) * (2*(util.get_avg_roll(self.on_hit_n, self.on_hit_die)) + self.on_hit_flat)
		else:
			acc += self._calc_dmg() * (self.DC - target.get_bonus(self.challenge_attribute, self.challenge_save))/20
		return acc
