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

