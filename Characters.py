import attack
from enum import Enum

class Stat(Enum):
	STR = enum.auto()
	DEX = enum.auto()
	CON = enum.auto()
	INT = enum.auto()
	WIS = enum.auto()
	CHA = enum.auto()
	AC = enum.auto()

class Character():
	#TODO separate the character into two comonents: Stat block and attacks?

	def __init__(self,name, hp, ac, level=1):
		self.name = name
		self.prof_bonus = 0
		self.prof= {} # Holds str of skills profficient in
		self.hp = hp
		self.ac = ac
		# TODO
		self.str = 0
		self.dex = 0
		self.con = 0
		self.int = 0
		self.wis = 0
		self.cha = 0

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

	def get_attacks(self):
		return self._attacks.copy()


	def get_bonus(self, attr, save=True):
		acc = 0
		if save and attr in self.prof:
			acc += self.prof_bonus
		acc += util.bonus_from_attribute(self.stat_block[attr])
		return acc

characters = [
	Character('Amon', 135, 23),
	Character('Giaus', 94, 20),
	Character('Knack', 157, 20),
	Character('Shvari', 126, 18),
	Character('Solin', 132, 22)
]

Giaus = characters[1]
Giaus.register_attack(Attack())
