import sys
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# Para gráficos (reemplazo de JFreeChart)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Para exportar a Excel (reemplazo de Apache POI)
import openpyxl
from openpyxl.styles import Font

# Add the project root so this file can also be run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Classes.clsDog import ClsDog
from Classes.clsCat import ClsCat
from Controller.ctlPet import ctlPet
from Model.modelDog import ModelDog
from Model.modelCat import ModelCat


class FrmPet(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Pet Manager")
        self.geometry("1060x420")
        self.resizable(False, False)

        # Controlador y listas
        self.ctl_pet = ctlPet(ModelDog(), ModelCat())
        self.dog_object_list = []
        self.cat_object_list = []

        # Inicialización de la interfaz gráfica
        self._init_components()

        # Cargar datos iniciales
        self.dog_object_list = self.ctl_pet.list_pet("Dog")
        self.fill_dog_jlist()
        self.cat_object_list = self.ctl_pet.list_pet("Cat")
        self.fill_cat_jlist()
        self.fill_jlist()

        # Refrescar reportes
        self.refresh_report_by_health_status()
        self.refresh_dog_report()
        self.refresh_cat_report()

    def _init_components(self):
        # Título principal
        lbl_title = tk.Label(self, text="Pet Manager", font=("Tahoma", 18, "bold"))
        lbl_title.pack(pady=5)

        # Contenedor de pestañas (JTabbedPane)
        self.tabbed_pane = ttk.Notebook(self)
        self.tabbed_pane.pack(fill="both", expand=True, padx=10, pady=5)

        # 1. Pestaña: Pet List
        self.tab_pet_list = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.tab_pet_list, text="Pet List")
        self.pet_listbox = tk.Listbox(self.tab_pet_list)
        self.pet_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # 2. Pestaña: Dog Manager
        self.tab_dog_manager = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.tab_dog_manager, text="Dog Manager")
        self._setup_dog_manager_ui()

        # 3. Pestaña: Cat Manager
        self.tab_cat_manager = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.tab_cat_manager, text="Cat Manager")
        self._setup_cat_manager_ui()

        # 4. Pestaña: Dog List
        self.tab_dog_list = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.tab_dog_list, text="Dog List")
        self.dog_listbox = tk.Listbox(self.tab_dog_list)
        self.dog_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # 5. Pestaña: Cat List
        self.tab_cat_list = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.tab_cat_list, text="Cat List")
        self.cat_listbox = tk.Listbox(self.tab_cat_list)
        self.cat_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # 6. Pestañas para reportes con gráficos
        self.jp_report_by_health_status = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.jp_report_by_health_status, text="Report By Health Status")

        self.jp_dog_report = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.jp_dog_report, text="Dog Report")

        self.jp_cat_report = ttk.Frame(self.tabbed_pane)
        self.tabbed_pane.add(self.jp_cat_report, text="Cat Report")

        # Botones inferiores de exportación y reinicio
        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(pady=10)

        btn_export_pet = ttk.Button(frame_buttons, text="Export Pet List", command=self.btn_exportar_pet_list_action_performed)
        btn_export_pet.grid(row=0, column=0, padx=10)

        btn_export_dog = ttk.Button(frame_buttons, text="Export Dog List", command=self.btn_exportar_dog_list_action_performed)
        btn_export_dog.grid(row=0, column=1, padx=10)

        btn_export_cat = ttk.Button(frame_buttons, text="Export Cat List", command=self.btn_exportar_cat_list_action_performed)
        btn_export_cat.grid(row=0, column=2, padx=10)

        btn_restart = ttk.Button(frame_buttons, text="Restart", command=self.btn_restart_action_performed)
        btn_restart.grid(row=0, column=3, padx=10)

    def _setup_dog_manager_ui(self):
        f = self.tab_dog_manager
        
        ttk.Label(f, text="Code").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_code_dog = ttk.Entry(f)
        self.txt_code_dog.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(f, text="Name").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.txt_name_dog = ttk.Entry(f)
        self.txt_name_dog.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(f, text="Born year").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_born_year_dog = ttk.Entry(f)
        self.txt_born_year_dog.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(f, text="Color").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.txt_color_dog = ttk.Entry(f)
        self.txt_color_dog.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(f, text="Health Status").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.cb_health_status_dog = ttk.Combobox(f, values=["Sick", "Healthy", "In Surgery"], state="readonly")
        self.cb_health_status_dog.current(0)
        self.cb_health_status_dog.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(f, text="Breed").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.cb_breed_dog = ttk.Combobox(f, values=["Criollo", "Schnauzer", "German shepherd", "Pincher"], state="readonly")
        self.cb_breed_dog.current(0)
        self.cb_breed_dog.grid(row=2, column=3, padx=5, pady=5)

        self.cb_pedigree_var = tk.BooleanVar()
        self.cb_pedigree = ttk.Checkbutton(f, text="Pedigree", variable=self.cb_pedigree_var)
        self.cb_pedigree.grid(row=2, column=4, padx=5, pady=5)

        ttk.Label(f, text="petId").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.txt_pet_id = ttk.Entry(f, state="readonly")
        self.txt_pet_id.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(f, text="dogId").grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.txt_dog_id = ttk.Entry(f, state="readonly")
        self.txt_dog_id.grid(row=3, column=3, padx=5, pady=5)

        btn_frame = ttk.Frame(f)
        btn_frame.grid(row=4, column=0, columnspan=5, pady=15)

        ttk.Button(btn_frame, text="Save", command=self.btn_crear_dog_action_performed).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Search", command=self.btn_buscar_dog_action_performed).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.btn_editar_dog_action_performed).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.btn_eliminar_dog_action_performed).pack(side="left", padx=5)

    def _setup_cat_manager_ui(self):
        f = self.tab_cat_manager

        ttk.Label(f, text="Code").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_code_cat = ttk.Entry(f)
        self.txt_code_cat.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(f, text="Name").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.txt_name_cat = ttk.Entry(f)
        self.txt_name_cat.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(f, text="Born year").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_born_year_cat = ttk.Entry(f)
        self.txt_born_year_cat.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(f, text="Color").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.txt_color_cat = ttk.Entry(f)
        self.txt_color_cat.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(f, text="Health Status").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.cb_health_status_cat = ttk.Combobox(f, values=["Sick", "Healthy", "In Surgery"], state="readonly")
        self.cb_health_status_cat.current(0)
        self.cb_health_status_cat.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(f, text="Breed").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.cb_breed_cat = ttk.Combobox(f, values=["Birman", "British", "Bombay", "Abyssinian"], state="readonly")
        self.cb_breed_cat.current(0)
        self.cb_breed_cat.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(f, text="petId2").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.txt_pet_id_2 = ttk.Entry(f, state="readonly")
        self.txt_pet_id_2.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(f, text="catId").grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.txt_cat_id = ttk.Entry(f, state="readonly")
        self.txt_cat_id.grid(row=3, column=3, padx=5, pady=5)

        btn_frame = ttk.Frame(f)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=15)

        ttk.Button(btn_frame, text="Save", command=self.btn_crear_cat_action_performed).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Search", command=self.btn_buscar_cat_action_performed).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.btn_editar_cat_action_performed).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.btn_eliminar_cat_action_performed).pack(side="left", padx=5)

    # --- REPORTES Y GRÁFICOS ---
    def refresh_report_by_health_status(self):
        report = self.ctl_pet.list_pet_by_health_status()
        labels = [record.get_health_status() for record in report]
        values = [record.get_amount_of_pets_by_health_status() for record in report]

        # Limpiar contenedor previo
        for widget in self.jp_report_by_health_status.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        if values:
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        else:
            ax.text(0.5, 0.5, "No pets registered", ha="center", va="center")
        ax.set_title("Pets Classification By health status")

        canvas = FigureCanvasTkAgg(fig, master=self.jp_report_by_health_status)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_dog_report(self):
        report = self.ctl_pet.list_dog_by_health_status()
        categories = [record.get_health_status() for record in report]
        values = [record.get_amount_of_pets_by_health_status() for record in report]

        for widget in self.jp_dog_report.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(categories, values, color='skyblue')
        ax.set_title("Dogs Classification By health status")
        ax.set_xlabel("Health Status")
        ax.set_ylabel("Amount of Dogs")

        canvas = FigureCanvasTkAgg(fig, master=self.jp_dog_report)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_cat_report(self):
        report = self.ctl_pet.list_cat_by_health_status()
        categories = [record.get_health_status() for record in report]
        values = [record.get_amount_of_pets_by_health_status() for record in report]

        for widget in self.jp_cat_report.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(categories, values, color='lightgreen')
        ax.set_title("Cats Classification By health status")
        ax.set_xlabel("Amount Of Cats")
        ax.set_ylabel("Health Status")

        canvas = FigureCanvasTkAgg(fig, master=self.jp_cat_report)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- CRUD PERROS ---
    def btn_crear_dog_action_performed(self):
        try:
            code = self.txt_code_dog.get().strip()
            name = self.txt_name_dog.get().strip()
            color = self.txt_color_dog.get().strip()
            born_year = int(self.txt_born_year_dog.get().strip())
            breed = self.cb_breed_dog.get()
            health_status = self.cb_health_status_dog.get()
            pedigree = self.cb_pedigree_var.get()

            if not code or not name or not color:
                messagebox.showwarning("Warning", "Fill all fields")
            else:
                dog = ClsDog(dog_id=0, breed=breed, pedigree=pedigree, pet_id=0,
                             code=code, name=name, born_year=born_year, color=color, health_status=health_status)
                if not self.ctl_pet.create_pet(dog):
                    messagebox.showerror("Error", "Could not save the dog. Check that its code is unique.")
                    return
                self.dog_object_list = self.ctl_pet.list_pet("Dog")
                self.fill_dog_jlist()
                self.fill_jlist()
                self.clear_dog_fields()
                messagebox.showinfo("Info", "The record has been saved")
                self.refresh_report_by_health_status()
                self.refresh_dog_report()
        except ValueError:
            messagebox.showerror("Error", "Please add a valid born year")

    def btn_buscar_dog_action_performed(self):
        code = self.txt_code_dog.get().strip()
        dog = self.ctl_pet.search_pet(code, "Dog")
        if not dog:
            messagebox.showwarning("Info", "Code not found")
        else:
            self._set_entry_text(self.txt_pet_id, str(dog.get_pet_id()))
            self._set_entry_text(self.txt_dog_id, str(dog.get_dog_id()))
            self.txt_name_dog.delete(0, tk.END)
            self.txt_name_dog.insert(0, dog.get_name())
            self.txt_color_dog.delete(0, tk.END)
            self.txt_color_dog.insert(0, dog.get_color())
            self.txt_born_year_dog.delete(0, tk.END)
            self.txt_born_year_dog.insert(0, str(dog.get_born_year()))
            self.cb_health_status_dog.set(dog.get_health_status())
            self.cb_breed_dog.set(dog.get_breed())
            self.cb_pedigree_var.set(dog.is_pedigree())

    def btn_editar_dog_action_performed(self):
        try:
            code = self.txt_code_dog.get().strip()
            name = self.txt_name_dog.get().strip()
            color = self.txt_color_dog.get().strip()
            born_year = int(self.txt_born_year_dog.get().strip())
            breed = self.cb_breed_dog.get()
            health_status = self.cb_health_status_dog.get()
            pedigree = self.cb_pedigree_var.get()
            pet_id = int(self.txt_pet_id.get())
            dog_id = int(self.txt_dog_id.get())

            dog = ClsDog(dog_id=dog_id, breed=breed, pedigree=pedigree, pet_id=pet_id,
                         code=code, name=name, born_year=born_year, color=color, health_status=health_status)
            response = self.ctl_pet.edit_pet(dog)
            if response:
                self.dog_object_list = self.ctl_pet.list_pet("Dog")
                self.fill_dog_jlist()
                self.fill_jlist()
                self.clear_dog_fields()
                messagebox.showinfo("Info", "Record updated")
                self.refresh_report_by_health_status()
                self.refresh_dog_report()
            else:
                messagebox.showerror("Error", "Error updating the record")
        except Exception:
            messagebox.showwarning("Warning", "You have to search the record to update")

    def btn_eliminar_dog_action_performed(self):
        pet_id = self.txt_pet_id.get().strip()
        dog_id = self.txt_dog_id.get().strip()
        if not pet_id or not dog_id:
            messagebox.showwarning("Warning", "You have not searched a dog yet")
        else:
            try:
                dog = ClsDog(pet_id=int(pet_id), dog_id=int(dog_id))
                removed = self.ctl_pet.delete_pet(dog)
                if removed:
                    self.dog_object_list = self.ctl_pet.list_pet("Dog")
                    self.fill_dog_jlist()
                    self.fill_jlist()
                    self.clear_dog_fields()
                    messagebox.showinfo("Info", "The dog has been deleted successfully!")
                    self.refresh_report_by_health_status()
                    self.refresh_dog_report()
                else:
                    messagebox.showerror("Error", "An error has occurred during the dog deletion.")
            except Exception:
                messagebox.showerror("Error", "Please, search a dog (by code) that you want to delete and try again...")

    # --- CRUD GATOS ---
    def btn_crear_cat_action_performed(self):
        try:
            code = self.txt_code_cat.get().strip()
            name = self.txt_name_cat.get().strip()
            color = self.txt_color_cat.get().strip()
            born_year = int(self.txt_born_year_cat.get().strip())
            breed = self.cb_breed_cat.get()
            health_status = self.cb_health_status_cat.get()

            if not code or not name or not color:
                messagebox.showwarning("Warning", "Fill all fields")
            else:
                cat = ClsCat(cat_id=0, breed=breed, pet_id=0, code=code, name=name,
                             born_year=born_year, color=color, health_status=health_status)
                if not self.ctl_pet.create_pet(cat):
                    messagebox.showerror("Error", "Could not save the cat. Check that its code is unique.")
                    return
                self.cat_object_list = self.ctl_pet.list_pet("Cat")
                self.fill_cat_jlist()
                self.fill_jlist()
                self.clear_cat_fields()
                messagebox.showinfo("Info", "The record has been saved")
                self.refresh_report_by_health_status()
                self.refresh_cat_report()
        except ValueError:
            messagebox.showerror("Error", "Please add a valid born year")

    def btn_buscar_cat_action_performed(self):
        code = self.txt_code_cat.get().strip()
        cat = self.ctl_pet.search_pet(code, "Cat")
        if not cat:
            messagebox.showwarning("Info", "Code not found")
        else:
            self._set_entry_text(self.txt_pet_id_2, str(cat.get_pet_id()))
            self._set_entry_text(self.txt_cat_id, str(cat.get_cat_id()))
            self.txt_name_cat.delete(0, tk.END)
            self.txt_name_cat.insert(0, cat.get_name())
            self.txt_color_cat.delete(0, tk.END)
            self.txt_color_cat.insert(0, cat.get_color())
            self.txt_born_year_cat.delete(0, tk.END)
            self.txt_born_year_cat.insert(0, str(cat.get_born_year()))
            self.cb_health_status_cat.set(cat.get_health_status())
            self.cb_breed_cat.set(cat.get_breed())

    def btn_editar_cat_action_performed(self):
        try:
            code = self.txt_code_cat.get().strip()
            name = self.txt_name_cat.get().strip()
            color = self.txt_color_cat.get().strip()
            born_year = int(self.txt_born_year_cat.get().strip())
            breed = self.cb_breed_cat.get()
            health_status = self.cb_health_status_cat.get()
            pet_id = int(self.txt_pet_id_2.get())
            cat_id = int(self.txt_cat_id.get())

            cat = ClsCat(cat_id=cat_id, breed=breed, pet_id=pet_id, code=code, name=name,
                         born_year=born_year, color=color, health_status=health_status)
            response = self.ctl_pet.edit_pet(cat)
            if response:
                self.cat_object_list = self.ctl_pet.list_pet("Cat")
                self.fill_cat_jlist()
                self.fill_jlist()
                self.clear_cat_fields()
                messagebox.showinfo("Info", "Record updated")
                self.refresh_report_by_health_status()
                self.refresh_cat_report()
            else:
                messagebox.showerror("Error", "Error updating the record")
        except Exception:
            messagebox.showwarning("Warning", "You have to search the record to update")

    def btn_eliminar_cat_action_performed(self):
        pet_id = self.txt_pet_id_2.get().strip()
        cat_id = self.txt_cat_id.get().strip()
        if not pet_id or not cat_id:
            messagebox.showwarning("Warning", "You have not searched a cat yet")
        else:
            try:
                cat = ClsCat(pet_id=int(pet_id), cat_id=int(cat_id))
                removed = self.ctl_pet.delete_pet(cat)
                if removed:
                    self.cat_object_list = self.ctl_pet.list_pet("Cat")
                    self.fill_cat_jlist()
                    self.fill_jlist()
                    self.clear_cat_fields()
                    messagebox.showinfo("Info", "The cat has been deleted successfully!")
                    self.refresh_report_by_health_status()
                    self.refresh_cat_report()
                else:
                    messagebox.showerror("Error", "An error has occurred during the cat deletion.")
            except Exception:
                messagebox.showerror("Error", "Please, search a cat (by code) that you want to delete and try again...")

    # --- EXPORTAR A EXCEL (openpyxl) ---
    def btn_exportar_pet_list_action_performed(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Pets"

        headers = ["AnimalType", "Code", "Name", "Color", "Health Status", "Breed", "Pedigree"]
        ws.append(headers)

        # Aplicar negrita a los encabezados
        for cell in ws[1]:
            cell.font = Font(bold=True)

        for dog in self.dog_object_list:
            pedigree_str = "Yes" if dog.is_pedigree() else "No"
            ws.append([dog.get_animal_type(), dog.get_code(), dog.get_name(),
                       dog.get_color(), dog.get_health_status(), dog.get_breed(), pedigree_str])

        for cat in self.cat_object_list:
            ws.append([cat.get_animal_type(), cat.get_code(), cat.get_name(),
                       cat.get_color(), cat.get_health_status(), cat.get_breed(), ""])

        dt_str = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
        file_name = f"pet_list_report_date_{dt_str}-time.xlsx"
        wb.save(file_name)
        messagebox.showinfo("Info", "The file has been exported successfully")

    def btn_exportar_dog_list_action_performed(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Dogs"

        headers = ["AnimalType", "Code", "Name", "Color", "Health Status", "Breed", "Pedigree"]
        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for dog in self.dog_object_list:
            pedigree_str = "Yes" if dog.is_pedigree() else "No"
            ws.append([dog.get_animal_type(), dog.get_code(), dog.get_name(),
                       dog.get_color(), dog.get_health_status(), dog.get_breed(), pedigree_str])

        dt_str = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
        file_name = f"dog_list_report_date_{dt_str}-time.xlsx"
        wb.save(file_name)
        messagebox.showinfo("Info", "The file has been exported successfully")

    def btn_exportar_cat_list_action_performed(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Cats"

        headers = ["AnimalType", "Code", "Name", "Color", "Health Status", "Breed"]
        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for cat in self.cat_object_list:
            ws.append([cat.get_animal_type(), cat.get_code(), cat.get_name(),
                       cat.get_color(), cat.get_health_status(), cat.get_breed()])

        dt_str = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
        file_name = f"cat_list_report_date_{dt_str}-time.xlsx"
        wb.save(file_name)
        messagebox.showinfo("Info", "The file has been exported successfully")

    def btn_restart_action_performed(self):
        self.destroy()
        app = FrmPet()
        app.mainloop()

    # --- MÉTODOS AUXILIARES Y LISTAS ---
    def clear_dog_fields(self):
        self.txt_code_dog.delete(0, tk.END)
        self.txt_name_dog.delete(0, tk.END)
        self.txt_color_dog.delete(0, tk.END)
        self.txt_born_year_dog.delete(0, tk.END)
        self._set_entry_text(self.txt_pet_id, "")
        self._set_entry_text(self.txt_dog_id, "")
        self.cb_breed_dog.current(0)
        self.cb_health_status_dog.current(0)
        self.cb_pedigree_var.set(False)

    def clear_cat_fields(self):
        self.txt_code_cat.delete(0, tk.END)
        self.txt_name_cat.delete(0, tk.END)
        self.txt_color_cat.delete(0, tk.END)
        self.txt_born_year_cat.delete(0, tk.END)
        self._set_entry_text(self.txt_pet_id_2, "")
        self._set_entry_text(self.txt_cat_id, "")
        self.cb_breed_cat.current(0)
        self.cb_health_status_cat.current(0)

    def fill_jlist(self):
        self.pet_listbox.delete(0, tk.END)
        for dog in self.dog_object_list:
            data = f"{dog.get_name()} - {dog.get_code()} - {dog.get_animal_type()}"
            self.pet_listbox.insert(tk.END, data)
        for cat in self.cat_object_list:
            data = f"{cat.get_name()} - {cat.get_code()} - {cat.get_animal_type()}"
            self.pet_listbox.insert(tk.END, data)

    def fill_dog_jlist(self):
        self.dog_listbox.delete(0, tk.END)
        for dog in self.dog_object_list:
            data = f"{dog.get_name()} - {dog.get_code()} - {dog.get_animal_type()}"
            self.dog_listbox.insert(tk.END, data)

    def fill_cat_jlist(self):
        self.cat_listbox.delete(0, tk.END)
        for cat in self.cat_object_list:
            data = f"{cat.get_name()} - {cat.get_code()} - {cat.get_animal_type()}"
            self.cat_listbox.insert(tk.END, data)

    def _set_entry_text(self, entry_widget, text):
        entry_widget.config(state="normal")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text)
        entry_widget.config(state="readonly")


if __name__ == "__main__":
    app = FrmPet()
    app.mainloop()