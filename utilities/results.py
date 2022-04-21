
"""Module de résultats

Utilitaire pour gérer les résultats, incluant une 
classe AppResults.

"""

class AppResults():
    """Conteneur de résultats d'applications

    Classe utilisé pour enregistrer les résultats de 
    chaque application

    Attibuts:
        app_name (str): Nom de l'application
        n_ra_attempt (int): Nombre de rentatives de connexion
        n_collision (int): Nombre de collisions (1 collision par UE 
            ayant colisionné)
        pk_generated (int): Nombre de paquets générés. Un paquet est considéré
            généré quand il est prêt à être envoyé.
        cummul_ra_time (int): Temps cumulatif, en millisecondes, que les UEs de 
            l'application on passé en tentative de connexion (en considérant les
            backoff et les tentatives multiples)
        n_ra_time (int): Nombre de connexion complétés
        

    """
    def __init__(self, app_name):
        self.app_name = app_name
        self.n_rach_attempt = 0
        self.n_collision = 0
        self.pk_generated = 0
        self.cummul_ra_time = 0
        self.n_ra_time = 0
        self.cummul_waiting_time = 0
        self.n_waiting_time = 0
        self.cummul_trans_time = 0
        self.n_trans_time = 0

    # def __add__(self,results):
    #     new_results = AppResults(self.app_name)
    #     new_results.n_rach_attempt = self.n_rach_attempt \
    #                                + results.n_rach_attempt
    #     new_results.n_collision = self.n_collision \
    #                             + results.n_collision
    #     new_results.pk_generated = self.pk_generated \
    #                              + results.pk_generated
    #     new_results.cummul_ra_time = self.cummul_ra_time \
    #                              + results.cummul_ra_time
    #     new_results.n_ra_time = self.n_ra_time \
    #                              + results.n_ra_time
    #     new_results.cummul_waiting_time = self.cummul_waiting_time \
    #                              + results.cummul_waiting_time
    #     new_results.n_waiting_time = self.n_waiting_time \
    #                              + results.n_waiting_time
    #     new_results.cummul_trans_time = self.cummul_trans_time \
    #                              + results.cummul_trans_time
    #     new_results.n_trans_time = self.n_trans_time \
    #                              + results.n_trans_time
    #     return(new_results)


    def add(self,results):

        self.n_rach_attempt = self.n_rach_attempt + results.n_rach_attempt
        self.n_collision = self.n_collision + results.n_collision
        self.pk_generated = self.pk_generated + results.pk_generated
        self.cummul_ra_time = self.cummul_ra_time + results.cummul_ra_time
        self.n_ra_time = self.n_ra_time + results.n_ra_time
        self.cummul_waiting_time = self.cummul_waiting_time + results.cummul_waiting_time
        self.n_waiting_time = self.n_waiting_time + results.n_waiting_time
        self.cummul_trans_time = self.cummul_trans_time + results.cummul_trans_time
        self.n_trans_time = self.n_trans_time + results.n_trans_time
        
    def add_RA_time(self, ra_time:int):
        """Enregistre le temps d'accès aléatoire

        """
        self.cummul_ra_time += ra_time
        self.n_ra_time += 1


    def increment_pkt(self,N):
        self.pk_generated +=N


    def add_waiting_time(self, waiting_time:int):
        """Enregistre le temps d'attente d'un paquet

        Le temps d'attente est défini comme étant le temps
        entre le moment où un paquet est prêt à être envoyé 
        (RRC Connected) et le moment de la transmission.

        """
        self.cummul_waiting_time += waiting_time
        self.n_waiting_time += 1

    def add_trans_time(self, trans_time:int):
        """Enregistre le temps de transmission

        Le temps de transmission est défini par le temps 
        entre la transmission du premier et dernier bit
        du paquet.

        """
        self.cummul_trans_time += trans_time
        self.n_trans_time += 1


    def print_results(self):
        """Affiche les résultats

        """
        print('**********Results**********')
        print('App: {}'.format(self.app_name))
        print('Nombre de tentatives de connexion: {}'.format(self.n_rach_attempt))
        print('Nombre de collisions: {}'.format(self.n_collision))
        print('NNombre de paquets générés: {}'.format(self.pk_generated))
        print('Nombre de paquets transmis: {}'.format(self.n_trans_time))
        print('Temps moyen de connexion aléatoire: {}'.format(self.cummul_ra_time/self.n_ra_time))
        print("Temps d'attente moyen: {}".format(self.cummul_waiting_time/self.n_waiting_time))
        print('Temps de transmisison moyen: {}'.format(self.cummul_trans_time/self.n_trans_time))
        print('***************************')
