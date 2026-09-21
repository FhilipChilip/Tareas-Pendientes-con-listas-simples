class Node:
    def __init__(self, task):
        # Crea un nodo con una tarea. Empieza a completar sin apuntar a otro nodo.
        self.task = task         
        self.completed = False   
        self.next = None          
