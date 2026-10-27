import json
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "tasks.json"


def load_tasks():
    """Read tasks from the JSON file; return an empty list if missing or broken."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [t for t in data if isinstance(t, dict) and "title" in t]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    """Write all tasks to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except OSError as err:
        messagebox.showerror("Save failed", str(err))


class TodoApp:
    def __init__(self, root):
        self.tasks = load_tasks()
        root.title("To-Do List Application")
        root.geometry("440x480")

        self.entry = tk.Entry(root, font=("Calibri", 13))
        self.entry.pack(fill="x", padx=12, pady=(12, 6))
        self.entry.bind("<Return>", lambda e: self.add_task())

        bar = tk.Frame(root)
        bar.pack(pady=4)
        for text, cmd in [("Add", self.add_task), ("Done / Undo", self.toggle_task),
                          ("Delete", self.delete_task), ("Clear Done", self.clear_done)]:
            tk.Button(bar, text=text, command=cmd, width=11).pack(side="left", padx=3)

        self.listbox = tk.Listbox(root, font=("Calibri", 13), activestyle="none")
        self.listbox.pack(fill="both", expand=True, padx=12, pady=8)
        self.status = tk.Label(root, anchor="w")
        self.status.pack(fill="x", padx=12, pady=(0, 8))
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for t in self.tasks:
            self.listbox.insert(tk.END, ("[x] " if t["done"] else "[ ] ") + t["title"])
            if t["done"]:
                self.listbox.itemconfig(tk.END, fg="gray")
        done = sum(1 for t in self.tasks if t["done"])
        self.status.config(text=f"{len(self.tasks)} tasks, {done} done")
        save_tasks(self.tasks)

    def selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Select a task", "Please click a task first.")
            return None
        return sel[0]

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            messagebox.showwarning("Empty task", "Please type a task first.")
            return
        self.tasks.append({"title": title, "done": False})
        self.entry.delete(0, tk.END)
        self.refresh()

    def toggle_task(self):
        i = self.selected()
        if i is not None:
            self.tasks[i]["done"] = not self.tasks[i]["done"]
            self.refresh()

    def delete_task(self):
        i = self.selected()
        if i is not None:
            del self.tasks[i]
            self.refresh()

    def clear_done(self):
        self.tasks = [t for t in self.tasks if not t["done"]]
        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()
