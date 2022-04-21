from functools import total_ordering
from numpy.lib.shape_base import apply_over_axes
from classes.antenna import Antenna
from classes.scheduler import Scheduler
from classes.ue import UE, UEStatus
from input import INPUT_DICT2 as INPUT_DICT
from utilities.representation import plot_pathloss, plot_positions
from utilities.file_io import read_csv_index_table
from utilities.results import AppResults
from utilities.stochastic import gen_packets
import utilities.position as pos


import numpy as np
from operator import itemgetter
from scipy.stats import lognorm, uniform
from utilities.position import equidistant_coords, random_coord, get_distance

"""Main module

"""

app1 = 'Streaming 4K'

app2 = "Contrôles de drone"

app3 = "Détection automobile"

if __name__ == '__main__':
    ################ Module 1 ################
    

    ################ Module 2 ################

    # Sauf la bloucle appelant les méthodes "update"
    ################ Module 1 ################

    #Ajouter le main du module 1 en excluant les graphs

    #On fixe le germe (seed) pour obtenir des résultats reproductibles
    np.random.seed(1234)
    #Initialization des attributs de classe
    UE.init_ue_class()
    Antenna.init_antenna_class()

    #Création des UEs

    pos_antennas = pos.equidistant_coords(INPUT_DICT['nb_antennas'], INPUT_DICT['map_size'])

    pos_app1 = pos.random_coord(INPUT_DICT['apps'][app1]['nb_ues'], INPUT_DICT['map_size'])

    pos_app2 = pos.random_coord(INPUT_DICT['apps'][app2]['nb_ues'], INPUT_DICT['map_size'])

    pos_app3 = pos.random_coord(INPUT_DICT['apps'][app3]['nb_ues'], INPUT_DICT['map_size'])

    pos_ue = {app1 : pos_app1 , app2 : pos_app2, app3 : pos_app3}

    ues_app1 = []


    for index in range(len(pos_app1)):
        ues_app1.append(UE(app1,pos_app1[index],INPUT_DICT['ue_height']))

    #print(f"Number of users app1 : {len(ues_app1)}")

    ues_app2 = []

    for index in range(len(pos_app2)):
        ues_app2.append(UE(app2,pos_app2[index],INPUT_DICT['ue_height']))

    ues_app3 = []

    for index in range(len(pos_app3)):
        ues_app3.append(UE(app3,pos_app3[index],INPUT_DICT['ue_height']))


    #print(f"Number of users app1 : {len(ues_app2)}")

    users = ues_app1 + ues_app2 + ues_app3

    #Création des antennes
    #TODO

    antennas= []

    for index in range(len(pos_antennas)):
        antennas.append(Antenna(pos_antennas[index],INPUT_DICT['scenario'],INPUT_DICT['frequency'],INPUT_DICT['antenna_height']))
    #print(f"Number of antennas is : {len(antennas)}")


    pathloss_list = []
    distances_list = []

    number_of_connections = 0

    for i in range(len(users)) :
        lowest_pathloss = 10000 #very high
        for j in range(len(antennas)) :
            distance = pos.get_distance(users[i].get_coord(),antennas[j].get_coord())
            users[i].set_propagation(distance,INPUT_DICT['scenario'])
            antennas[j].calculate_pathloss(users[i],distance)
            calculated_pathloss = users[i].get_pathloss()
            if (calculated_pathloss <= lowest_pathloss):
                lowest_pathloss = calculated_pathloss
                best_antenna = j
                best_distance = distance
                propagation = users[i].get_propagation()
        antennas[best_antenna].add_ue(users[i])
        users[i].set_pathloss(lowest_pathloss)
        users[i].force_propagation(propagation)
        number_of_connections += 1
        pathloss_list.append(users[i].get_pathloss())
        distances_list.append(best_distance)
        #print(f"User with id : {users[i].get_id()} has propagation {users[i].get_propagation()} and is connected with antenna {antennas[best_antenna].get_id()}(distance : {antennas[best_antenna].get_user_distance(users[i].get_id())} and pathloss = {users[i].get_pathloss()})")


    #print(f"Le nombre de connection est {number_of_connections} pour {len(users)} utilisateurs")

    #print(f"Le nombre de pathloss et le nombre de distance sont respectivement {len(pathloss_list)} et {len(distances_list)} pour {len(users)} utilisateurs")
    ues = users

    ues_dict = {}

    for element in ues :
        ues_dict[element.id] = element

    ################ Module 2 ################
    # Il n'y a pas de modifications nécessaire à effectuer
    # dans le main. Les modifications à effectuer sont dans
    # antennes et ue.

    #Read PRACH Tables
    rach_table = read_csv_index_table(INPUT_DICT['rach_table_path'])

    #Fetch access_info
    access_info = {name:INPUT_DICT[name] for name in (
        'inactivity_timer',
        'scs',
        'ra_parameters',
        'backoff_time',
        'number_of_preambles',
        'max_inactive_ues')
    }

    access_info['rach_structure'] = rach_table[
        INPUT_DICT['prach_config_index']]

    rach_structure = access_info['rach_structure']

    sim_time = 1000

    #print("Rach structure is {} and its type is {}: ".format(rach_structure,type(rach_structure)))

    # rach_structure = access_info['rach_structure']
    #
    # print("*******")
    # print(rach_structure[0])
    # print("*******")

    UE.add_access_info(access_info)

    #Create results per app
    app_results = {}
    for app_name in INPUT_DICT['apps']:
        app_results[app_name] = AppResults(app_name)

    #Generate random number for fraction decision
    rand_num = uniform.rvs(size=len(ues))
    for i, ue in enumerate(ues):
        #Generate packets
        ue.add_packet_list(gen_packets(INPUT_DICT['simulation_time']*sim_time,
            INPUT_DICT['apps'][ue.app_name]['gen_distribution'],
            INPUT_DICT['apps'][ue.app_name]['len_distribution']))
        #Manage initial connection
        if rand_num[i] <= INPUT_DICT['apps'][ue.app_name][
            'fraction_connected']:
            ue.status = UEStatus.RRC_CONNECTED
            ue._previous_status = UEStatus.RRC_IDLE
            #print("UE {} has status {}".format(ue.id,ue.status))
        else:
            ue.status = UEStatus.RRC_IDLE
            #print("UE {} has status {}".format(ue.id, ue.status))
        #Assign results objects

    
    ################ Module 3 ################
    #TODO: À intégrer dans votre code
    # Considère une liste contenant tous les ues (nommée ue) 
    # et un dictionnaire contenant les antennes avec l'ID comme clé (nommé antennas).

    # Ajouter l'information de CQI au UEs
    UE.add_cqi_info(INPUT_DICT['rcv_power_to_cqi']) #initialise un attribut cls

    for ue in ues:
        #Initialisation du CQI
        ue.initialize_CQI() #chaque ue à son propre cqi

    #Lecture du CQI and des tables de largeurs de bandes
    cqi_table = read_csv_index_table(INPUT_DICT['cqi_table_path'])
    bandwith_to_RB_table = read_csv_index_table(INPUT_DICT['bandwith_to_RB_table'])
    # Initialisation de l'ordonnaceur
    Scheduler.init_scheduler_class(INPUT_DICT['tbs_overhead'] , #int
        cqi_table, bandwith_to_RB_table, INPUT_DICT['bandwidth'], #bandwidth is int
        INPUT_DICT['fraction_available_RB'], INPUT_DICT['scs'],
        INPUT_DICT['grant_delay'] )

    for element in antennas:
        element.init_scheduler()

    ##########################################
    


    # #Boucle d'update (Comme au module 2)
    # for time_ms in range(INPUT_DICT['simulation_time']*1000):
    #     for antenna in antennas.values():
    #         antenna.update(time_ms)
    #

    #Update loop
    for time_ms in range(INPUT_DICT['simulation_time']*sim_time):
        #Go through all antennas to update
        for element in antennas:
            element.update(rach_structure, time_ms)

    for element in ues :
        app_results[element.app_name].add(element.results)

    # tot_results = AppResults('all')
    # for results in app_results.values():
    #     tot_results = tot_results + results
    #     results.print_results()
    # tot_results.print_results()

    # #tot_results = AppResults('all')
    # for results in app_results.values():
    #     #tot_results = tot_results + results
    #     results.print_results()
    #tot_results.print_results()

    if INPUT_DICT['rach_table_path'] ==  'data/rachFrameStructure_FR2_TDD.csv' :

        print("Mode : FR2")

    else:

        print("Mode : FR1")

    all = AppResults('all')

    nb_result = 0

    if ues_app1 != [] :
        app_results[app1].print_results()
        all.add(app_results[app1])
        nb_result += 1

    if ues_app2 != []:
        app_results[app2].print_results()
        all.add(app_results[app2])
        nb_result += 1

    if ues_app3 != [] :
        app_results[app3].print_results()
        all.add(app_results[app3])
        nb_result += 1

    if nb_result >= 2 :
        all.print_results()

