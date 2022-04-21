
from classes.packet import Packet

"""Module d'ordonnancement

Module définissant la classe Scheduler. Les objets Scheduler sont 
assignés à une antenne afin de gérer la transmission des paquets.

"""

class Scheduler:
    """Classe Scheduler

    Classe utilisée pour ordonnancer la transmission et paquets
    et gérer les ressources

    Attributs:
        remaining_rbs(int): Nombre de Ressource Block non assignés
            pour le slot courant.
        waiting_queue(list): liste de paquets attendant être transmis
        scheduled_packets(dict): Dictionnaire de paquets associé à leur 
            temps de fin de transmission.
        ues(dict(int:UE)): Dictionnaire des UEs associés à laquelle 
        appartient le schduler, associé par l'identifiant des UEs. 

    """

    def __init__(self, ues):
        self.remaining_rbs = 0
        self.waiting_queue = []
        self.scheduled_packets = {}
        self.ues = ues
        self.file_attente = []
        self.transmitted = 0

    @classmethod
    def init_scheduler_class(cls, tbs_overhead, cqi_efficiency_table, 
        bandwith_to_RB_table, used_bandwidth, fraction_available_RB, 
        used_scs, grant_delay):
        """Initialise les paramètre de classe de l'ordonnanceur

        Args:
            tbs_overhead (int): Symbole d'"overhead" des RBs
            cqi_efficiency_table (dict): Dictionnaire de l'efficacité des 
                CQI associé à l'index (1 à 15)
            bandwith_to_RB_table (dict): Dictionnaire des RBs par slot, 
                associé pas SCS. Pour chaque SCS, une liste est associée, 
                pour laquelle chque index représente une largeur de bande 
                différente. La clé "SCS" est associée à la liste des 
                largeurs de bande possibles. 
            used_bandwidth(int): Largeur de bande sélection en MHz
            fraction_available_RB(float): Fraction des RBs disponible 
                pour la transmission
            used_scs(int): Distance entre les porteuse en kHzsélectionné (SCS)
            grant_delay(int): Délais en millisecondes entre le temps ou un UE 
                est prêt, et le temps auquel il peut transmettre.

        """
        bandwidth_SCS_to_n_prb_table = {}
        bandwidth_values = [int(bandwidth_str[:-3]) for bandwidth_str 
            in bandwith_to_RB_table['SCS']]
        for scs, value in bandwith_to_RB_table.items():
            if type(scs) == str:
                continue
            for i, bandwidth in enumerate(bandwidth_values):
                if fraction_available_RB >= 0 and fraction_available_RB <= 1:
                    if type(value[i]) == int:
                        bandwidth_SCS_to_n_prb_table[
                            (bandwidth, scs)] = (
                            round(value[i] * fraction_available_RB))
                        if bandwidth_SCS_to_n_prb_table[
                            (bandwidth, scs)] < 1:
                            bandwidth_SCS_to_n_prb_table[
                                (bandwidth, scs)] = 1 
                else:
                    raise ValueError
        cls.n_usable_subchannels = bandwidth_SCS_to_n_prb_table[(used_bandwidth, used_scs)]

        cls.tbs_overhead = tbs_overhead
        cls.cqi_efficiency_table = cqi_efficiency_table
        cls.scs = used_scs
        cls.slots_per_ms = int(cls.scs /15)
        cls.grant_delay = grant_delay
    
    def compute_n_subchannels(self, packet_size: int,
        max_subchannels: int, cqi) -> int:
        """ Détermine le nombre minimal de sous porteuses nécessaire 
        pour transmettre le paquet et les ressources utilisé pour 
        y parvenir. S'il n'y a pas assez de ressource pour tout 
        transmettre, retourne la quatité d'information qui a pu être
        transmise.

        Args:
            packet_size (int): Taille du paquet
            max_subchannels (int): Nombre de sous porteuses disponible
                pour la transmission de paquets

        Returns:
                (Nombre de sous porteurses utilisées, information transmisse)
        """

        for n_subchannels in range(1, max_subchannels):
        # Verify if the transmission delay will be the same with one less subchannel
            covered_memory = self.get_TBS(cqi)*n_subchannels
            if packet_size <= covered_memory:
                return (n_subchannels, covered_memory)

        return (max_subchannels, self.get_TBS(cqi)*max_subchannels)

    def get_TBS(self, cqi):
        """ Détermine le TBS

        Args:
            cqi(int): Indice de qualité du canal(CQI)

        Returns:
            int: Nombre de bit qu'un RB peut transmettre

        """
        if self.tbs_overhead >= 168:
            raise ValueError('TBS Overhead should be smaller than 168'
                            + 'to transmit data.')
        return self.cqi_efficiency_table[cqi]*min(
            156, 168-self.tbs_overhead)

    def schedule(self, time_ms, packets : list):
        """Méthode d'ordonnacement de paquets

        Méthode utilisée pour ordonnancer les paquets. Coordonne les 
        autre méthodes de la classe Scheduler.

        Args:
            time_ms(int): Temps simulé depuis le début de la simulation
                en ms.
            packets(list): Liste des paquets à ordonnancer
        """
        transmitted_packets = []

        waiting_time = []

        trans_time = []

        for item in packets:
            if item not in self.waiting_queue:
                self.waiting_queue.append(item)
            if item.start_waiting_time == -1:
                item.start_waiting_time = item.generation_subframe


        #TODO: À compléter
        # Ajouter les paquets dans la file d'attente


        # Pour chaque slot dans une ms
        for slot in range(self.slots_per_ms):

            # Déterminer le slot de transmission (courant + grant)

            for packet in self.waiting_queue :
                if packet.available_ressources :
                    if packet.start_trans_time == -1 :
                        packet.start_trans_time = packet.start_waiting_time + self.grant_delay

                    waiting_time.append(packet.get_waiting_time())

                    self.ues[packet.ue_id].results.add_waiting_time(packet.get_waiting_time())

                    n_subchannels = self.compute_n_subchannels(packet.size, self.n_usable_subchannels, self.ues[packet.ue_id].cqi)

                    if packet.size <= n_subchannels[1]:
                        self.remaining_rbs = self.n_usable_subchannels - n_subchannels[0] #catch pas
                        packet.remaining_size = 0 #existe pas
                        if self.waiting_queue[0].remaining_size == 0 :
                            if packet not in transmitted_packets :
                                packet.end_trans_time = time_ms
                                trans_time.append(packet.get_trans_time())
                                self.ues[packet.ue_id].results.add_trans_time(packet.get_trans_time())
                                transmitted_packets.append(packet)
                                del self.waiting_queue[0]
                                self.scheduled_packets[str(packet.end_trans_time)] = packet
                    else :
                        self.remaining_rbs = 0
                        packet.remaining_size = packet.size - n_subchannels[1]
                        packet.available_ressources = False

                else :

                    subchannels_left = self.compute_n_subchannels(packet.remaining_size, self.n_usable_subchannels, self.ues[packet.ue_id].cqi)

                    if packet.remaining_size <= subchannels_left[1]:
                        packet.available_ressources = True
                        packet.remaining_size = 0
                        self.remaining_rbs = self.n_usable_subchannels - subchannels_left[0]
                        if self.waiting_queue[0].remaining_size == 0 :
                            packet.end_trans_time = time_ms
                            trans_time.append(packet)
                            self.ues[packet.ue_id].results.add_trans_time(packet.get_trans_time())
                            transmitted_packets.append(packet)
                            del self.waiting_queue[0]
                            self.scheduled_packets[str(packet.end_trans_time)] = packet

                    else :

                        self.remaining_rbs = 0

                        packet.remaining_size = packet.remaining_size - round(subchannels_left[1])
                # Retourne les paquets qui ont fini d'être transmis
        return (waiting_time, trans_time, transmitted_packets)

            # Trouve le nombre de ressources disponibles

            # Place des paquets jusqu'à ce qu'il n'y ait plus de ressources


