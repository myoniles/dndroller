import pandas as pd
import random
import numpy as np

EPOCH = 10000
SAME_POOL = True

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

def roll_attacks(attacks, ac):
	acc = 0
	for attack in attacks:
		roll, dmg = attack.roll_damage()
		if roll == 'N' or roll > ac:
			acc += dmg
	return acc

def legacy_main():
	linspace = list(range(18, 28))
	df1 = pandas.DataFrame(columns=[attack.name for attack in attacks1], index=linspace)
	df2 = pandas.DataFrame(columns=[attack.name for attack in attacks2], index=linspace)
	for ac in linspace:
		for attack in attacks1:
			acc = 0
			p = pools1[attack.name]
			df1[attack.name][ac] = mean(ac, p)
		for attack in attacks2:
			acc = 0
			p = pools2[attack.name]
			df2[attack.name][ac] = mean(ac, p)
	graph_damage_by_attack(df1)
