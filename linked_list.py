from node import Node
 
 
class LinkedList:
    def __init__(self):
        # Crea una lista vacía: sin primer nodo y con tamaño 0.
        self.head = None
        self.size = 0
 
    def is_empty(self):
        # Dice si la lista no tiene ninguna tarea (True o False).
        return self.head is None
 
    def add_first(self, task):
        # Agrega una tarea al principio: el nuevo nodo apunta a la antigua cabeza.
        new_node = Node(task)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
 
    def add_last(self, task):
        # Agrega una tarea al final: recorre la lista hasta el último nodo y lo enlaza.
        new_node = Node(task)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
 
    def insert_at(self, position, task):
        # Inserta una tarea en una posición (0 = inicio). Da error si la posición no existe.
        if position < 0 or position > self.size:
            raise IndexError("Position out of range")
        if position == 0:
            self.add_first(task)
            return
        previous = self.head
        for _ in range(position - 1):
            previous = previous.next
        new_node = Node(task)
        new_node.next = previous.next
        previous.next = new_node
        self.size += 1
 
    def remove_at(self, position):
        # Elimina la tarea de una posición saltándola: el nodo anterior apunta al siguiente.
        if position < 0 or position >= self.size:
            raise IndexError("Position out of range")
        if position == 0:
            self.head = self.head.next
        else:
            previous = self.head
            for _ in range(position - 1):
                previous = previous.next
            previous.next = previous.next.next
        self.size -= 1
 
    def toggle_completed(self, position):
        # Marca la tarea como completada, o la vuelve a abrir si ya estaba completada.
        current = self.head
        for _ in range(position):
            current = current.next
        current.completed = not current.completed
 
    def traverse(self):
        # Recorre toda la lista de principio a fin y devuelve los nodos en orden.
        nodes = []
        current = self.head
        while current is not None:
            nodes.append(current)
            current = current.next
        return nodes
