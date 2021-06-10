STAT_BONUS_DEFAULT =	{
									'STR':0,
									'DEX':0,
									'CON':0,
									'INT':0,
									'WIS':0,
									'CHA':0
								}

def __prof(level):
	return 2 + (level-1)//4


class Character():
	def __init__(self,name, hp, ac, level=1, stat_bonuses=STAT_BONUS_DEFAULT.copy()):
		self.name = name
		self.prof_bonus = 0
		self.prof= {} # Holds str of skills profficient in
		self.stat_bonuses = stat_bonuses
		self.hp = hp
		self.ac = ac

characters = [
	Character('Amon', 135, 23),
	Character('Giaus', 94, 20),
	Character('Knack', 157, 20),
	Character('Shvari', 126, 18),
	Character('Solin', 132, 22)
]
