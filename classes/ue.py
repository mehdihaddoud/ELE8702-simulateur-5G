
from enum import Enum, auto
from random import randint, choice
from scipy.stats import lognorm
from utilities import results
from math import exp
from random import random
from math import ceil
"""Module de UE

Module définissant la classe UE, qui représente l'appareil d'un usager.

"""

class UE:
    """Classe UE

    Classe définissant les informations et les fonctionnalités
    d'un UE.

    Args:
        app_name (str): Nom de l'application
        coord (tuple(float,float)): Coordoner du UE (x,y)
        height (float): Hauteur du UE
        is_LOS (bool): Indique si la ligne de vu (LOS) du UE est obstrué 
            (par rapport à l'antenne)
        pathloss (float): Pathloss en dB entre l'antenne et le UE
        recv_power (float): Puissance reçue en dBm

    """
    ################ Module 1 ################
    def __init__(self,
                 app_name:str,
                 coord:tuple,
                 height:float) -> None:
        self.app_name = app_name
        self.coord = coord
        self.height = height

        self.is_LOS = True
        self.pathloss = float('inf')
        self.inactivity_counter = 0
        self.recv_power = -float('inf')
        self._previous_status = UEStatus.RRC_IDLE
        self.id = UE.id_counter
        self.preamble_selected = []
        self.backoff_time = -1
        self.results = results.AppResults(self.app_name)
        self.is_connecting_time = -1 # Dès que ça finit -> connecté
        UE.id_counter += 1

    def __repr__(self):
        return 'App:{};Coord:{}'.format(self.app_name, self.coord)

    @classmethod
    def init_ue_class(cls):
        cls.id_counter = 0

    #To complete with module 1 implementation

    ################ Module 2 ################

    def increment_inactivity_counter(self):
        self.inactivity_counter += 1
    def reset_inactivity_counter(self):
        self.inactivity_counter = 0
    def get_inactivity_counter(self):
        return self.inactivity_counter
    def increment_pkt(self, size):
            self.results.increment_pkt(size)

    def set_propagation(self, distance, scenario):

        if scenario == 'UMi':

            if distance <= 18:

                self.is_LOS = True

            else:

                prob = 18 / distance + exp(-distance / 36) * (1 - 18 / distance)

                self.is_LOS = random() < prob

        else:  ##RMa

            if distance <= 10:

                self.is_LOS = True

            else:

                prob = exp(- (distance - 10) / 1000)

                self.is_LOS = random() < prob

    def force_propagation(self, propagation):
        if propagation is 'LOS':
            self.is_LOS = True
        else:
            self.is_LOS = False

    def get_propagation(self):

        if self.is_LOS:
            return 'LOS'
        else:
            return 'NLOS'

    def get_height(self):
        return self.height

    def set_pathloss(self, value):
        self.pathloss = value

    def get_pathloss(self):
        return self.pathloss

    def get_coord(self):
        return self.coord

    def get_id(self):
        return self.id

    def get_app(self):
        return self.app_name


    ################ Module 2 ################
    @classmethod
    def add_access_info(cls, access_info):
        """Initialise les attributs d'accès des UEs"""
        cls.inactivity_timer = access_info['inactivity_timer']
        cls.scs = access_info['scs']
        cls.ra_parameters = access_info['ra_parameters']
        cls.backoff_time = access_info['backoff_time']
        cls.number_of_preambles = access_info['number_of_preambles']
        cls.max_inactive_ues = access_info['max_inactive_ues']
        cls.rach_structure = access_info['rach_structure']

    def is_valid_preamble_subframe(self,
                                   rach_structure: list,
                                   subframe: int) -> bool:
        # print("UE {} needs to connect at time : {}".format(self.id, subframe))
        if int(subframe / 10) % int(rach_structure[1]) == int(rach_structure[2]):
            # valid frame
            if self.scs == 60:
                for slot_number in rach_structure[3].split(","):
                    if subframe == ceil(int(slot_number) / 4):
                        #print("UE {} has a valid subframe!".format(self.id))
                        return True
                return False
            elif self.scs == 15:
                for slot_number in rach_structure[3].split(","):
                    if subframe == int(slot_number):  # 15 khz
                        #print("UE {} has a valid subframe!".format(self.id))
                        return True
                return False
            else:
                return False
        else:
            return False

        # if time_lapse (int(subframe/10)) % x == y, valid frame, then check subframee
        # if true check the subframe

        # if not return false
    def add_packet_list(self, packet_list):
        """Ajoute une liste d'information permettant de générer des paquets

        Les informations de paquets sont un tuple indiquant le temps
        de génération et la longeur du paquet en bits. Le prochain
        paquet à envoyer est enregistré dans _next_paquet, les autres
        dans paquet_info.

        """
        self.increment_pkt(len(packet_list))

        self.packet_info = packet_list
        # print("UE {} has been given a packet!".format(self.id))
        if packet_list:
            self._next_packet = packet_list.pop(0)
        else:
            self._next_packet = None



    def get_valid_slot(self):
        return self.rach_structure[3].split(',')


    def _compute_connection_time(self, ra_parameters: dict) -> int:
        """Méthode permettant de déterminer le temps de connexion

        Cette méthode retourne le temps qu'un UE nécessite afin de
        passe du mode RRC_IDLE ou RRC_INACTIVE au mode RRC_CONNECTED

        Args:
            ra_parameters (dict): dictionnaire des paramètre d'entré

        Returns:
            int: Temps de connexion (ms).
        """
        if self._previous_status == UEStatus.RRC_IDLE:
            connection_time = ra_parameters['RA_length_idle']
        elif self._previous_status == UEStatus.RRC_INACTIVE:
            connection_time = ra_parameters['RA_length_innactive']
        else:
            #print('Previous state: {}'.format(self._previous_status))
            raise ValueError('Previous state should be either idle or inactive')
        return connection_time

    """Tentative de connexion à un UE idle

          Cette méthode sélectionnne un préabule and et regarde s'il peut
          être à time_ms. S'il peut être envoyé, il change à l'état 
          connecting et détermine le temps de fin du RA et et incrémente 
          le nombre de rach attempt dans les résultats.

          Args:
              time_ms (int): Temps simulé depuis le début de la 
                  simulation (ms)
          va appeler is_valid
          si valid on le met a connecting

          et select_preamble
          """

    def connect(self, rach_structure: list, time_ms: int):

        # TODO
        # valid_slot = self.rach_structure[3].split(',')
        #
        # if self.is_valid_preamble_subframe(self.rach_structure,time_ms):
        if self.is_valid_preamble_subframe(rach_structure, time_ms):
            # self._select_preamble() pourquoi?

            # RA_time = self._compute_connection_time(self.ra_parameters)
            # self.results.add_RA_time(RA_time)
            # self.results.n_rach_attempt += 1
            self.preamble_selected = self._select_preamble(self.get_valid_slot())
            return True
        else:
            return False

    # Peut transmettre des paquets

    def _select_preamble(self, valid_slots) -> int:

        """Sélectionne un préambule valide

             Sélectionne un format de préambule aléatoirement parmis
             l'ensemble de préambule possible.

             Args:
                 valid_slots (list): List d'entier représentant les
                     slots de transmission valides.

             Return:
                 (int,int,int): Trois index représentant respectivement
                     le préambule, la modulation temporel et le slot.
             """
        # TODO
        numberTimeDomainPrachOccasions = self.rach_structure[6]
        preamble_index = randint(0, self.number_of_preambles - 1)
        time_mod_index = randint(0, numberTimeDomainPrachOccasions - 1)
        slot_index = valid_slots[randint(0, len(valid_slots) - 1)]
        return (preamble_index, time_mod_index, slot_index)

    def _send_packet(self):
        """Transmet le prochain packet à l'antenne

        """
        packet = self._next_packet
        # print("UE {} just sent a packet!".format(self.id))
        if self.packet_info:
            self._next_packet = self.packet_info.pop(0)
        else:
            # self._next_packet = (float('inf'),0)
            self._next_packet = None
        return packet

    def set_disconnected(self, nb_ues_inactive) -> int:
        """Effectue la déconnexion d'un UE

        Permet au UE de passer du mode CONNECTED au mode
        IDLE ou INACTIVE dépendemment du nombre du UE
        inactive déjà connecté
        """

        # le nombre d'inactive
        if self.status == UEStatus.RRC_CONNECTED:
            if nb_ues_inactive <= self.max_inactive_ues:
                self.status = UEStatus.RRC_INACTIVE
                self._previous_status = UEStatus.RRC_CONNECTED
                #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))

                return nb_ues_inactive + 1
            else:
                self.status = UEStatus.RRC_IDLE
                self._previous_status = UEStatus.RRC_CONNECTED
                #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))
                return nb_ues_inactive
        elif self.status == UEStatus.RRC_INACTIVE:
            self.increment_inactivity_counter()
            if self.get_inactivity_counter() > self.inactivity_timer:
                self.status = UEStatus.RRC_IDLE
                self._previous_status = UEStatus.RRC_INACTIVE
                #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))
                self.reset_inactivity_counter()
                return nb_ues_inactive - 1
            else:
                return nb_ues_inactive
        else:
            return nb_ues_inactive

        # TODO

    def update(self, rach_structure: list, time_ms: int, nb_ues_inactive: int) -> list:
        """Met à jour le UE à time_ms

        Gère les fontionnaliés temporelle du UE. À appeler
        à chaque milliseconde. Gère principalement les états
        du UE.

        Args:
            time_ms (int): Temps simulé depuis le début de la
                simulation (ms)


        """

        # Si le UE est connecté, envoie un paquet ou revient enmode IDLE/INACTIVE
        if self.status == UEStatus.RRC_CONNECTED:
            # S'il y a un paquet à transmettre -> transmet le paquet
            if self._next_packet:
                #print("UE {} needs to send the packet : {}".format(self.id, self._next_packet))
                return [self._send_packet(), nb_ues_inactive]
            else:
                return [False, self.set_disconnected(nb_ues_inactive)]


        # Le UE est en mode IDLE ou INACTIVE mais nécessite une connection
        elif self.status == UEStatus.RRC_IDLE:
            if self._next_packet:
                # print("UE {} needs to send the packet : {}".format(self.id, self._next_packet))
                if self.connect(rach_structure, time_ms):
                    self.status = UEStatus.CONNECTING  # tente de se connecter
                    # CHOISIR UN CONNECTING TIME PLUS GROS QUE CELUI DU INACTIVE
                    self._previous_status = UEStatus.RRC_IDLE

                    RA_time = self._compute_connection_time(self.ra_parameters)
                    self.results.add_RA_time(RA_time)
                    self.results.n_rach_attempt += 1

                    self.is_connecting_time = RA_time

                    #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))


            return [False, nb_ues_inactive]


        elif self.status == UEStatus.CONNECTING:

            if self.backoff_time > 0:

                self.backoff_time -= 1

            elif self.backoff_time == 0:

                # refaire un rach attempt

                self.backoff_time = - 1

                self.status = UEStatus.RRC_IDLE

                self._previous_status = UEStatus.CONNECTING

                #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))

            elif self.is_connecting_time > 0:

                self.is_connecting_time -= 1

            elif self.is_connecting_time == 0:

                self.is_connecting_time = -1

                self.status = UEStatus.RRC_CONNECTED

                self._previous_status = UEStatus.CONNECTING

                #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))

                # Collision -> Attend un temps de backoff avant de se reconnecter
                # Si le UE est en train de se connecter, vérifier s'il a terminé sa procédure de connexion
                # Pas de collision -> se connecte
                # self.status = UEStatus.RRC_CONNECTED
            return [False, nb_ues_inactive]

        elif self.status == UEStatus.RRC_INACTIVE:  # CAS INACTIVE

            if self._next_packet:  # si il y a un paquet à envoyer, on se mets en mode connecting
                # print("UE {} needs to send the packet : {}".format(self.id,self._next_packet))
                self.reset_inactivity_counter()

                self.status = UEStatus.CONNECTING

                self._previous_status = UEStatus.RRC_INACTIVE

                RA_time = self._compute_connection_time(self.ra_parameters)

                self.results.add_RA_time(RA_time)

                self.results.n_rach_attempt += 1

                #print("UE {} has changed status to {} from {}".format(self.id, self.status, self._previous_status))

                self.is_connecting_time = RA_time

                return [False, nb_ues_inactive - 1]  # le paquet n'est plus en mode inactive

            else:

                return [False, self.set_disconnected(nb_ues_inactive)]  # on rentre dans set_disconnected pour vérifier si on a pas dépasser le temps d'inactivité

    ################ Module 3 ################
    #TODO: À intégrer à votre code

    @classmethod
    def add_cqi_info(cls, rcv_power_to_cqi):
        cls.rcv_power_to_cqi = rcv_power_to_cqi

    def initialize_CQI(self):
        """Assigne un index de qualité de cannel (CQI) aux UEs

        """
        #Association self.recv_power à index
        if self.recv_power < self.rcv_power_to_cqi['min']:
            self.cqi = 1
        elif self.recv_power > self.rcv_power_to_cqi['max']:
            self.cqi = 15
        else:
            pwr_interval = self.rcv_power_to_cqi['max'] - self.rcv_power_to_cqi['min']
            step = pwr_interval/14
            self.cqi = round((self.recv_power-self.rcv_power_to_cqi['min'])/step +1)
    ###########################################

class UEStatus(Enum):
    #État de connexion possible pour les UEs
    RRC_CONNECTED = auto()  # Peut transmettre des paquets
    CONNECTING = auto()     # Est en train de performer un RACH attempt
    RRC_IDLE = auto()       # Déconnecté, ne peut pas transmettre de paquets
    RRC_INACTIVE = auto()       # Comme idle, mais se reconnecte plus rapidement
