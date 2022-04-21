"""Input file

Inputs are format as dict.

"""

INPUT_DICT1={
    'nb_antennas':16, 
    'antenna_height':10,
    'apps':{
        'Streaming 4K': {
            'nb_ues':40,
            # Accès
            'gen_distribution': {
                'type': 'exponential', #interval [a,b]
                'scale' : 200
                #'b':100 #ms
            },
            'len_distribution': {
                'type': 'uniform',
                'a': 320000,
                'b': 480000
            },
            'fraction_connected':0.5
        },
        'Contrôles de drone': {
            'nb_ues':40,
            # Accès
            'gen_distribution': {
                'type': 'uniform',
                'a': 30 ,#ms (scale = mean = 1/lambda)
                'b' : 40
            },
            'len_distribution': {
                'type': 'uniform',
                'a': 95,
                'b' : 105
            },
            'fraction_connected':0.5,
        },
        'Détection automobile' :{
            'nb_ues': 1000,
            # Accès
            'gen_distribution': {
                'type': 'uniform',
                'a': 700,  # ms (scale = mean = 1/lambda)
                'b' : 1300
            },
            'len_distribution': {
                'type': 'uniform',
                'a': 95,
                'b' : 105
            },
            'fraction_connected': 0.5,
        }
    },
    'ue_height': 1.5,
    'map_size': 5, #km^2
    'scenario': 'UMi',
    'frequency': 28, #GHz
    'antenna_gain': 35,
    # Accès
    'rach_table_path': 'data/rachFrameStructure_FR2_TDD.csv',
    'simulation_time': 10, #secondes
    'inactivity_timer': 50,
    'scs': 60, #kHz
    'ra_parameters': {
        'RA_length_idle':50, #ms
        'RA_length_innactive': 20 #ms
    },
    'max_inactive_ues': 10, #par antenne
    'backoff_time': 100,
    'prach_config_index': 5,
    'number_of_preambles': 54,
    # Ordonnancement
    'scheduling_table': 1,
    'rcv_power_to_cqi':{
        'min': -90, #Puissance correspondant à la valeur minimale de CQI
        'max': -50   #Puissance correspondant à la valeur maximale de CQI
    },
    'cqi_table_path': 'data/CQI_table_1.csv',
    'bandwith_to_RB_table': 'data/NR_bandwidth_SCS_to_RB_FR2.csv',
    'bandwidth': 100, #MHz
    'tbs_overhead': 16,
    'fraction_available_RB': 0.2,
    'grant_delay': 1
}

INPUT_DICT2={
    'nb_antennas':16, #must be a square of an int
    'antenna_height':35,
    'apps': {
        'Streaming 4K': {
            'nb_ues': 40,
            # Accès
            'gen_distribution': {
                'type': 'exponential',  # interval [a,b]
                'scale': 200
                # 'b':100 #ms
            },
            'len_distribution': {
                'type': 'uniform',
                'a': 320000,
                'b': 480000
            },
            'fraction_connected': 0.5
        },
        'Contrôles de drone': {
            'nb_ues': 40,
            # Accès
            'gen_distribution': {
                'type': 'uniform',
                'a': 30,  # ms (scale = mean = 1/lambda)
                'b': 40
            },
            'len_distribution': {
                'type': 'uniform',
                'a': 95,
                'b': 105
            },
            'fraction_connected': 0.5,
        },
        'Détection automobile': {
            'nb_ues': 1000,
            # Accès
            'gen_distribution': {
                'type': 'uniform',
                'a': 700,  # ms (scale = mean = 1/lambda)
                'b': 1300
            },
            'len_distribution': {
                'type': 'uniform',
                'a': 95,
                'b': 105
            },
            'fraction_connected': 0.5,
        }
    },
    'ue_height': 1.5,
    'map_size': 12, #km^2
    'scenario': 'RMa',
    'frequency': 0.9, #GHz
    'antenna_gain': 45,
    # Accès
    'rach_table_path': 'data/rachFrameStructure_FR1_FDD.csv',
    'simulation_time': 10, #secondes
    'inactivity_timer': 50,
    'scs': 15, #kHz
    'ra_parameters': {
        'RA_length_idle':50, #ms
        'RA_length_innactive': 20 #ms
    },
    'max_inactive_ues': 10, #par antenne
    'backoff_time': 100,
    'prach_config_index': 22,
    'number_of_preambles': 54,
    # Ordonnancement
    'scheduling_table': 1,
    'rcv_power_to_cqi':{
        'min': -100, #Puissance correspondant à la valeur minimale de CQI
        'max': -60   #Puissance correspondant à la valeur maximale de CQI
    },
    'cqi_table_path': 'data/CQI_table_2.csv',
    'bandwith_to_RB_table': 'data/NR_bandwidth_SCS_to_RB_FR1.csv',
    'bandwidth': 30, #MHz,
    'tbs_overhead': 16,
    'fraction_available_RB': 0.2,
    'grant_delay': 1
}