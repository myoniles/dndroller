import re

rgx = r"(\d+)d(\d+)\s*([+|-]\s*\d*)?"
pattern = re.compile(rgx)
def string_to_roll(strint):
	m = pattern.match(strint)
	nums =  [0 if g==None else int(g) for g in m.groups()]
	return tuple(nums)

class Attack():
	def __init__(self, to_hit_bonus, damage_on_hit, name='', elven_acc=False, repeated=1):
		self.hit_bonus = to_hit_bonus
		self.repeated = repeated

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

	def give_dis(self):
		if self.adv:
			self.adv = False
			return
		self.dis = True

	def roll_damage(self):
		n_rolls = 1 + (self.adv ^ self.dis) + ((self.adv ^ self.dis) & self.adv) * self.elven_acc
		rolls = [random.randint(1,20) + self.hit_bonus for r in range(n_rolls)]
		roll = rolls[0]
		if self.adv ^ self.dis:
			roll = max(rolls) if self.adv else min(rolls)

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

