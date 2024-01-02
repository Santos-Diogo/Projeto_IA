import Grafo
import Entregas as ent

graph_dict = {
    ('Vila Nova de Famalicão',): [('Gavião', 27), ('Antas', 22), ('Calendário', 27), ('Mouquim', 34), ('Louro', 40), ('Brufe', 30)],
    ('Antas',): [('Calendário', 39), ('Esmeriz', 26), ('Vale', 52)],
    ('Calendário',): [('Brufe', 16)],
    ('Gavião', ): [('Vale', 35), ('Mouquim', 30), ('Antas', 50)],
    ('Brufe', ): [('Louro', 34), ('Outiz', 25)],
    ('Outiz', ): [('Vilarinho', 52), ('Louro', 27)],
    ('Mouquim', ): [('Louro', 16)],
    ('Esmeriz', ): [],
    ('Vale', ): [],
    ('Louro', ): [],
    ('Vilarinho', ): []
}

graph_pos_dict = {
    'Vila Nova de Famalicão': {'pos': (0, 0), 'connections': [('Gavião', 27), ('Antas', 22), ('Calendário', 27), ('Mouquim', 34), ('Louro', 40), ('Brufe', 30)]},
    'Antas': {'pos' : (0.9, -1.2), 'connections' : [('Calendário', 39), ('Esmeriz', 26), ('Vale', 52)]},
    'Calendário': {'pos' : (-1, -1.466), 'connections' : [('Brufe', 16)]},
    'Gavião': {'pos' : (1.052, 1.736), 'connections' : [('Vale', 35), ('Mouquim', 30), ('Antas', 50)]},
    'Brufe': {'pos' : (-1.396, -0.1), 'connections' : [('Louro', 34), ('Outiz', 25)]},
    'Outiz': {'pos' : (-2.92, 0.954), 'connections' : [('Vilarinho', 52), ('Louro', 27)]},
    'Mouquim': {'pos' : (-0.447, 2.46), 'connections' : [('Louro', 16)]},
    'Esmeriz': {'pos' : (0.469, -3.559), 'connections' : []},
    'Vale': {'pos' : (3.322, 1.123), 'connections' : []},
    'Louro': {'pos' : (-1.383, 2.4), 'connections' : []},
    'Vilarinho': {'pos' : (-2.839, -2.616), 'connections' : []}
}


G = Grafo(graph_dict, graph_pos_dict)

entregas = ent.populate_entregas('Dataset/Entregas.csv')



