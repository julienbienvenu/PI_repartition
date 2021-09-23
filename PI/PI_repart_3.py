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
        maximun envisagé : 2846

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

    saving_model = model + [objective_val]

    with open("resul_pi_2.csv", "a") as f: #open with append mode
      
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(saving_model)

def func_objective(model):

    objective_expr = np.nanmean(model)**3/np.nanstd(model) #average^3/ecart-type

    return objective_expr 

def choix_n_meilleurs(liste_choix, nb_choix):

    choix = []
    for i in range(len(liste_choix)):
        choix_groupe = []
        for j in range(len(liste_choix[0])):
            
            if liste_choix[i][j] >= (19 - nb_choix + 1) :

                choix_groupe.append([liste_choix[i][j],j])

        
        choix.append(choix_groupe)

    return choix

def simplification(choix):

    maximun = [0,0,17,0,18,17,18,18,19,0,19,0,18,0,0,17,0,12,13]
    choix_opti = []
    cpt = 1

    for i in range(19):

        if maximun[i] != 0:
            test = 0
            for j in range(nb_choix): 

                if choix[i][j][0] == maximun[i] and test == 0:                                   
                    choix_opti.append([choix[i][j]])
                    test = 1

        else :

            choix_opti.append(choix[i])

    return choix_opti

def affectation_aleatoire(multi):
    actual_result = 2750 #minimun acceptable

    deja_util = [0 for _ in range(19)]

    model = [-1 for i in range(19)]
    model_value = [-1 for i in range(19)]
    test = True

    for i in range(19):
        if (len(choix_opti[i])==1):
            
            model[i] = choix_opti[i][0][1] + 1
            model_value[i] = choix_opti[i][0][0]
            deja_util[choix_opti[i][0][1]] = 1

    for i in range(19):

        if model[i] == -1:

            x = random.randint(0,nb_choix - 1)
            
            selec = choix[i][x][1]
            selec_place = x
            cpt = 0
                    
            while (deja_util[selec] != 0 and cpt<nb_choix - 1):

                selec = choix[i][(x+cpt)%nb_choix][1]
                selec_place = (x+cpt)%nb_choix
                cpt+=1

            if (cpt<nb_choix - 1):
                
                deja_util[selec] = 1
                model[i]=selec + 1
                model_value[i] = choix[i][selec_place][0] #note du PI

            else :
                
                return False

    if test :
        #Calcul du modèle (notes PI)
        result = func_objective(model_value)
        
        #Enregistrement si bon modèle (numéro PI)
        if result > actual_result :
            
            save(model, result)
            print('New instance :', result)

        
            
def affectation_valeurs(model, prefs):

    model_values = []

    for i in range(len(model)):
        model_values.append(prefs[i][model[i]])

    return model_values

nb_choix = 8
liste_choix = get_list()
choix = choix_n_meilleurs(liste_choix, nb_choix)
choix_opti = simplification(choix)



for _ in range(100):

    liste_choix = get_list()
    choix = choix_n_meilleurs(liste_choix, nb_choix)
  
    lock = Lock()
    multi = [0 for _ in range(20000000)]
    
    with Pool(16) as p:
    
            r = list(tqdm.tqdm(p.imap(affectation_aleatoire, multi), total=len(multi)))
