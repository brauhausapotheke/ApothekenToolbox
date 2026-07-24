import customtkinter as ctk
from tkinter import filedialog

from apotheken_toolbox.update_service import aktualisieren


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ApothekenToolbox")
        self.geometry("900x450")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        titel = ctk.CTkLabel(
            self,
            text="🏥 ApothekenToolbox",
            font=("Arial", 28, "bold")
        )
        titel.pack(pady=(20, 25))

        # ------------------------------
        # Ornamentum
        # ------------------------------

        ctk.CTkLabel(
            self,
            text="Ornamentum-Datei",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=25)

        frame1 = ctk.CTkFrame(self, fg_color="transparent")
        frame1.pack(fill="x", padx=20, pady=(5, 20))

        self.ods_entry = ctk.CTkEntry(frame1)
        self.ods_entry.pack(side="left", expand=True, fill="x", padx=(5, 10))

        ctk.CTkButton(
            frame1,
            text="Durchsuchen",
            width=140,
            command=self.waehle_ods
        ).pack(side="right")

        # ------------------------------
        # CSV
        # ------------------------------

        ctk.CTkLabel(
            self,
            text="AVS-CSV",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", padx=25)

        frame2 = ctk.CTkFrame(self, fg_color="transparent")
        frame2.pack(fill="x", padx=20, pady=(5, 20))

        self.csv_entry = ctk.CTkEntry(frame2)
        self.csv_entry.pack(side="left", expand=True, fill="x", padx=(5, 10))

        ctk.CTkButton(
            frame2,
            text="Durchsuchen",
            width=140,
            command=self.waehle_csv
        ).pack(side="right")

        # ------------------------------
        # Status
        # ------------------------------

        self.status = ctk.CTkLabel(
            self,
            text="Status: Bereit",
            font=("Arial", 14)
        )
        self.status.pack(pady=(20, 5))

        self.progress = ctk.CTkProgressBar(self, width=700)
        self.progress.pack()
        self.progress.set(0)

        self.start_button = ctk.CTkButton(
            self,
            text="Preise aktualisieren",
            width=220,
            height=40,
            state="disabled",
            command=self.preise_aktualisieren
        )
        self.start_button.pack(pady=25)

    # ------------------------------------------------

    def waehle_ods(self):

        datei = filedialog.askopenfilename(
            title="Ornamentum auswählen",
            filetypes=[("ODS-Dateien", "*.ods")]
        )

        if datei:
            self.ods_entry.delete(0, "end")
            self.ods_entry.insert(0, datei)
            self.pruefe_start()

    # ------------------------------------------------

    def waehle_csv(self):

        datei = filedialog.askopenfilename(
            title="AVS-CSV auswählen",
            filetypes=[("CSV-Dateien", "*.csv")]
        )

        if datei:
            self.csv_entry.delete(0, "end")
            self.csv_entry.insert(0, datei)
            self.pruefe_start()

    # ------------------------------------------------

    def pruefe_start(self):

        if self.ods_entry.get() and self.csv_entry.get():
            self.start_button.configure(state="normal")
            self.status.configure(text="Status: Bereit zum Aktualisieren")
        else:
            self.start_button.configure(state="disabled")
            self.status.configure(text="Status: Bereit")

    # ------------------------------------------------

    def preise_aktualisieren(self):

        ods_datei = self.ods_entry.get()
        csv_datei = self.csv_entry.get()

        self.status.configure(text="Status: Starte...")
        self.progress.set(0.2)

        aktualisieren(ods_datei, csv_datei)


def start_gui():

    app = App()
    app.mainloop()