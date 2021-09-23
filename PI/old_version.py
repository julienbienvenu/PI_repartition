# author : Quentin Chevalier

import numpy as np
import random
from matching.games import HospitalResident
import csv

# VARIABLES---------------------------------------------
PI_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']  # project names

# nb of group or individual / project, possibility of modularity
Proj_Capacities = [1]*len(PI_names)

# 1,2,3..., can be lower than the number of projects
group_names = [str(i+1) for i in range(len(PI_names))]

# Rank project in pref order
def get_list():

    with open('drive.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data

prefs = get_list()


# ------------------------------------------------------

e = 100
seed = 1
m = 0
num = 1
min = e
m_len = max([len(i) for i in prefs])+1
while m < 2000:
    m = 0
    while m < 2000:
        seed += 1
        m += 1
        random.seed(seed)
        np.random.seed(seed)

        size = len(prefs)
        PI_num = len(PI_names)

        groupe_Name = np.arange(1, size+1)
        groupe_list = [str(groupe_Name[k]) for k in range(len(groupe_Name))]
        group_prefs = {}
        for k in range(size):
            group_prefs[groupe_list[k]] = prefs[k]

        # full random
        rank_users = []
        for k in range(PI_num):
            tempPIn = []
            for i in range(size):
                for j in range(PI_num):
                    if len(prefs[i]) > j and prefs[i][j] == PI_names[k]:
                        tempPIn.append(str(i+1))
            indexes = np.arange(len(tempPIn))
            np.random.shuffle(indexes)
            tempPIn = np.array(tempPIn)
            tempPIn = tempPIn[indexes]
            tempPIn = list(tempPIn)
            rank_users.append(tempPIn)

        project_prefs = {}
        for k in range(PI_num):
            project_prefs[PI_names[k]] = rank_users[k]

        capacities = {}
        for k in range(PI_num):
            capacities[PI_names[k]] = Proj_Capacities[k]

        game = HospitalResident.create_from_dictionaries(
            group_prefs, project_prefs, capacities
        )
        a = game.solve()

        def evaluate(p):
            malheur = 0  # should be low
            v = list(p.values())
            old_v = v.copy()
            for k in range(len(v)):
                if v[k] != []:
                    v[k] = [int(str(v[k][0]))]
            for i in range(len(v)):
                if v[i] == []:
                    for j in range(size):
                        if [j+1] not in v:
                            v[i] = [j+1]
                            break
            n = False
            tab = []
            for k in range(size):
                letter = PI_names[k]
                if len(v[k]) == 0:
                    continue
                groupe = int(v[k][0])-1
                if old_v[k] == []:
                    malheur += m_len*2
                    tab.append([letter, groupe+1, m_len])
                    n = True
                    continue
                for i in range(len(PI_names)):
                    if len(prefs[groupe]) > i and prefs[groupe][i] == letter:
                        tab.append([letter, groupe+1, i+1])
                        malheur += i+1
                        break

            return(malheur, n, tab)

        e, _, res = evaluate(a)
        if min > e:
            min = e
            print('solution ' + str(num))
            num += 1
            for k in res:
                print(k[0], group_names[k[1]-1], "voeux", k[2])
            print("malheur = "+str(e), "\n")
