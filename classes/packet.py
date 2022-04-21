
"""Module de paquets

Module définissant la classe Packet.

"""

class Packet:

    """Classe Packet

    Cette classe décrit un paquet d'information pouvant être échangé
    entre appareils. Principalement utilisée pour enregistrer de 
    l'information.

    Attributs:
        generation_time_ms(int): Temps (en ms) auquel le paquet est 
            considéré comme prêt à être envoyé
        size(int): Taille du paquet en bits
        remaining_size(int): Taille de la partie du paquet pas encore
            transmisse
        ue_id(int): ID du UE associé
        start_waiting_time(int): Temps auquel le paquet a commencé à 
            attendre (connecté et prêt à être transmis)(en ms)
        start_trans_time(int): Temps de la transmission du premier bit (en ms)
        end_trans_time(int): Temps de la transmission du dernier bit (en ms)

    """
    def __init__(self, generation_subframe: int, size: int, ue_id) -> None:
        self.generation_subframe = generation_subframe
        self.size = size
        self.remaining_size = size
        self.ue_id = ue_id
        self.available_ressources = True
        self.start_waiting_time = -1
        self.start_trans_time = -1
        self.end_trans_time = -1

    def get_waiting_time(self):
        return self.start_trans_time - self.start_waiting_time

    def get_trans_time(self):
        return self.end_trans_time - self.start_trans_time

    def __repr__(self):
        return 'UE:{};gen_time:{};swaiting:{};strans{}'.format(
            self.ue_id, self.generation_subframe, 
            self.start_waiting_time, self.start_trans_time)