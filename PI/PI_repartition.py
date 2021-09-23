'''
Algo pour répartition des PI :

    Principe de fonctionnement :
        Attribution aléatoire d'un PI par groupe
        Voir si ce modèle est bon
        Enregistrer si c'est un bon modèle

    Fonction objectif :
        Moyenne PI³/ecart-type
        maximun : infinite (tous à 19 c'est pas possible)
        moyenne 15, ecart-type 1 : 3375

    Objectif : maximiser la fonction objectif

    Prévu : 50000*8 tests (voir plus si on est motivés)

    Voili voilou
'''

import numpy as np
import csv
import random
import sys
from multiprocessing import Process, Lock, Pool
import tqdm
import os

# Init choices

def get_list():

    with open('drive.csv', newline='') as f:
        my_list = [list(map(int,rec)) for rec in csv.reader(f, delimiter=',')]


    return my_list

def save(model, objective_val):

    model_bis = [i+1 for i in model]
    saving_model = model_bis + [objective_val]

    with open("resul_pi.csv", "a") as f: #open with append mode
      
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(saving_model)

def func_objective(model):

    objective_expr = np.nanmean(model)**3/np.nanstd(model) #average^3/ecart-type

    return objective_expr 

def affectation_valeurs(model, prefs):

    model_values = []

    for i in range(len(model)):
        model_values.append(prefs[i][model[i]])

    return model_values

def test_repartition(multi):

    actual_result = 0
    model = [i for i in range(0,19)]

    for _ in range(2000000):

        #Affectation aléatoire d'un modèle (numéro de PI)
        random.shuffle(model)

        #Pondération par le choix du PI (note attribué à ce PI)
        model_values = affectation_valeurs(model, prefs)

        #Calcul du modèle (notes PI)
        result = func_objective(model_values)

        #Enregistrement si bon modèle (numéro PI)
        if result > actual_result:
            actual_result = result
            save(model, result)

prefs = get_list()

sys.stdout = open(os.devnull, 'w')

if __name__ == '__main__':
    lock = Lock()
    multi = [0 for _ in range(8)]   
    
    with Pool(8) as p:
	
     		r = list(tqdm.tqdm(p.imap(test_repartition, multi), total=len(multi)))

