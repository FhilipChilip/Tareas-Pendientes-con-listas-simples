import tkinter as tk
from tkinter import ttk
 
 
class Interface(ttk.Frame):
    NODE_WIDTH = 130
    NODE_HEIGHT = 54
    GAP = 44
 
    def __init__(self, parent):
        # Crea el lienzo donde se dibujan los nodos, con barra de desplazamiento horizontal.
        super().__init__(parent)
        self.canvas = tk.Canvas(self, height=110, bg="#f5f8fc",
                                highlightthickness=1, highlightbackground="#c9d3e0")
        self.canvas.pack(fill="x")
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        scroll_x.pack(fill="x")
        self.canvas.config(xscrollcommand=scroll_x.set)
 
    def draw(self, nodes):
        # Borra el dibujo anterior y dibuja cada nodo con su flecha hacia el siguiente.
        c = self.canvas
        c.delete("all")
        w, h, gap = self.NODE_WIDTH, self.NODE_HEIGHT, self.GAP
        y = 30
 
        c.create_text(8, 12, anchor="w", text="head", fill="#1d2b64",
                      font=("Segoe UI", 9, "bold"))
        if not nodes:
            c.create_text(60, y + h / 2, anchor="w", text="None (empty list)",
                          fill="#7a8794", font=("Segoe UI", 10))
            c.config(scrollregion=(0, 0, 300, 110))
            return
 
        x = 10
        for node in nodes:
            self._draw_node(node, x, y)
            arrow_start = x + w
            if node.next is not None:
                c.create_line(arrow_start - 15, y + h / 2, arrow_start + gap, y + h / 2,
                              arrow="last", fill="#1d2b64", width=2)
            else:
                c.create_line(arrow_start - 15, y + h / 2, arrow_start + 10, y + h / 2,
                              fill="#1d2b64", width=2)
                c.create_text(arrow_start + 14, y + h / 2, anchor="w", text="None",
                              fill="#7a8794", font=("Segoe UI", 10, "italic"))
            x += w + gap
        c.config(scrollregion=(0, 0, x + 60, 110))
 
    def _draw_node(self, node, x, y):
        # Dibuja una sola caja: a la izquierda la tarea, a la derecha el punto de la referencia.
        c = self.canvas
        w, h = self.NODE_WIDTH, self.NODE_HEIGHT
        color = "#d8f0e0" if node.completed else "#ffffff"
        c.create_rectangle(x, y, x + w, y + h, fill=color, outline="#1d2b64", width=2)
        c.create_line(x + w - 30, y, x + w - 30, y + h, fill="#1d2b64")
        text = node.task if len(node.task) <= 12 else node.task[:11] + "…"
        c.create_text(x + (w - 30) / 2, y + h / 2, text=text, font=("Segoe UI", 10))
        c.create_oval(x + w - 19, y + h / 2 - 4, x + w - 11, y + h / 2 + 4,
                      fill="#1d2b64")
