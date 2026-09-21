import tkinter as tk
from tkinter import ttk, messagebox
 
from linked_list import LinkedList
from interface import Interface
 
 
class App(tk.Tk):
    def __init__(self):
        # Crea la ventana principal, la lista enlazada vacía y construye la interfaz.
        super().__init__()
        self.title("Simple Lists Workshop - To-do list")
        self.geometry("820x560")
        self.minsize(700, 480)
        self.tasks = LinkedList()
        self._build_ui()
 
    # ---------------- Interface ----------------
    def _build_ui(self):
        # Arma todos los elementos visuales: entrada, botones, lista, dibujo y estado.
        form = ttk.Frame(self, padding=10)
        form.pack(fill="x")
 
        ttk.Label(form, text="Task:").grid(row=0, column=0, sticky="w")
        self.entry = ttk.Entry(form, width=40)
        self.entry.grid(row=0, column=1, sticky="we", padx=6)
        self.entry.bind("<Return>", lambda event: self.add_last())
 
        ttk.Label(form, text="Position:").grid(row=1, column=0, sticky="w", pady=6)
        self.position = tk.IntVar(value=0)
        ttk.Spinbox(form, from_=0, to=999, width=5,
                    textvariable=self.position).grid(row=1, column=1, sticky="w", padx=6)
 
        buttons = ttk.Frame(form)
        buttons.grid(row=2, column=0, columnspan=2, sticky="w", pady=4)
        for label, command in [
            ("Add first", self.add_first),
            ("Add last", self.add_last),
            ("Insert at position", self.insert_at),
            ("Complete / Reopen", self.toggle_completed),
            ("Delete", self.remove_selected),
        ]:
            ttk.Button(buttons, text=label, command=command).pack(side="left", padx=3)
        form.columnconfigure(1, weight=1)
 
        ttk.Label(self, text="Tasks (list traversal):", padding=(10, 0)).pack(anchor="w")
        body = ttk.Frame(self, padding=(10, 4))
        body.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(body, height=8, font=("Segoe UI", 11),
                                  activestyle="none", selectmode="browse")
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(body, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)
 
        ttk.Label(self, text="Linked list structure:", padding=(10, 0)).pack(anchor="w")
        self.node_canvas = Interface(self)
        self.node_canvas.pack(fill="x", padx=10, pady=4)
 
        self.status = ttk.Label(self, anchor="w", padding=(10, 4))
        self.status.pack(fill="x")
        self.refresh()
 
    # ---------------- Helpers ----------------
    def _get_text(self):
        # Lee el texto escrito; si está vacío muestra un aviso y devuelve None.
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Missing task", "Please type a task first.")
            return None
        return text
 
    def _get_selected_index(self):
        # Devuelve la posición de la tarea elegida en la lista; si no hay ninguna, avisa.
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Select a task", "Please choose a task from the list.")
            return None
        return selection[0]
 
    def _on_select(self, _event):
        # Al elegir una tarea, copia su posición en el campo "Position".
        selection = self.listbox.curselection()
        if selection:
            self.position.set(selection[0])
 
    def _clear_and_refresh(self):
        # Limpia el campo de texto y actualiza la pantalla.
        self.entry.delete(0, "end")
        self.refresh()
 
    # ---------------- Actions (buttons) ----------------
    def add_first(self):
        # Botón "Add first": agrega la tarea escrita al inicio de la lista.
        text = self._get_text()
        if text:
            self.tasks.add_first(text)
            self._clear_and_refresh()
 
    def add_last(self):
        # Botón "Add last": agrega la tarea escrita al final de la lista.
        text = self._get_text()
        if text:
            self.tasks.add_last(text)
            self._clear_and_refresh()
 
    def insert_at(self):
        # Botón "Insert at position": inserta la tarea en la posición indicada.
        text = self._get_text()
        if not text:
            return
        try:
            self.tasks.insert_at(self.position.get(), text)
        except (IndexError, tk.TclError):
            messagebox.showerror("Invalid position",
                                 f"Use a value between 0 and {self.tasks.size}.")
            return
        self._clear_and_refresh()
 
    def remove_selected(self):
        # Botón "Delete": elimina la tarea seleccionada.
        index = self._get_selected_index()
        if index is not None:
            self.tasks.remove_at(index)
            self.refresh()
 
    def toggle_completed(self):
        # Botón "Complete / Reopen": cambia el estado de la tarea seleccionada.
        index = self._get_selected_index()
        if index is not None:
            self.tasks.toggle_completed(index)
            self.refresh(selected=index)
 
    # ---------------- Refresh ----------------
    def refresh(self, selected=None):
        # Redibuja la lista de texto, el dibujo de nodos y los contadores.
        nodes = self.tasks.traverse()
 
        self.listbox.delete(0, "end")
        for i, node in enumerate(nodes):
            mark = "[x]" if node.completed else "[ ]"
            self.listbox.insert("end", f"{i}.  {mark}  {node.task}")
            if node.completed:
                self.listbox.itemconfig(i, fg="#7a8794")
        if selected is not None and selected < len(nodes):
            self.listbox.selection_set(selected)
 
        self.node_canvas.draw(nodes)
 
        pending = sum(1 for node in nodes if not node.completed)
        self.status.config(
            text=f"Total: {self.tasks.size}   |   Pending: {pending}"
                 f"   |   Completed: {self.tasks.size - pending}")
