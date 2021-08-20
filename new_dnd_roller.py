import matplotlib.pyplot as plt
from Characters import characters
from attack import Attack, Save, Check
from Stat import Stat

attacks1 = [
	Save(Stat.DEX, 10, '8d6', name='fireball'),
	Attack(1, '1d8+1', name='eblast1',  repeated=1 ),
#	Attack(1, '3d4+1', name='eblast10',  repeated=1 ),
#	Attack(1, '4d4+1', name='eblast12',  repeated=1 ),
#	Attack(10, '1d10+8', name='eblast_bonus_action',  repeated=4 ),
#	Attack(10, '1d10+8', name='eblast_surge',  repeated=4 ),
]
#attacks2 = [
#	Attack(15, '3d8+27', name='whatever busted shit fran made', repeated=4 ),
#	Attack(15, '2d4', name='spell', repeated=3 ),
#	Attack(15, '1d4', name='spell_last', repeated=1 ),
#]

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

def graph_compare(df_list, name_list=None):
	x_axis = df1.index
	plt.title('Comparison of Attack Patterns')

	for i in range(len(df_list)):
		l = name_list[i] if name_list else 'attack pattern {}'.format(i)
		plt.plot(x_axis, df_list[i].sum(axis=1), label=l)

	plt.xlabel("Target Armor Class")
	plt.ylabel("Average Damage per round")
	plt.legend(loc=1, ncol=1)
	plt.show()

if __name__ == '__main__':
	amon = characters[0]
	amon.set_attacks(attacks1)
	df = amon.evaluate_over(Stat.DEX)
	graph_damage_by_attack(df)
