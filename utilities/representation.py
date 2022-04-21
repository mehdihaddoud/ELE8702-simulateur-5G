import matplotlib.pyplot as plt

import seaborn as sns
#sns.set()

def plot_positions(ue_pos:dict, antenna_pos:list):
    """Illustre la position des antennes et des UEs

    Args:
        ue_pos (dict{str:list(tuple)}): Dict des liste de coordonnée des UEs
            selon l'application.
        antenna_pos (list(tuple)): Liste de la position des antennes

    """
    #Zip au format [[x],[y]]
    ues_xy = {}
    for app, values in ue_pos.items():
        ues_xy[app] = list(zip(*values))
    antenna_xy = list(zip(*antenna_pos))

    #Plot
    fig, ax = plt.subplots()
    ue_scatters = []
    apps = []
    for app, values in ues_xy.items():
        ue_scatters.append(ax.scatter(values[0], values[1],  marker = 'x'))
        apps.append(app)
    antenna_scatter = ax.scatter(antenna_xy[0], antenna_xy[1], marker='o')
    plt.legend((*ue_scatters,antenna_scatter),
           (*apps,'Antenna'))


    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Position des UEs et des antennes')

    plt.show()

def plot_pathloss(pathloss_values:list):
    f = plt.figure()
    sns.kdeplot(pathloss_values, shade = True)
    sns.distplot(pathloss_values)
    plt.xlabel('pathloss (dB)')
    plt.title('Histogramme du pathloss')
    plt.show()