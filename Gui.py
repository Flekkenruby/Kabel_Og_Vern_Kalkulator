import customtkinter as ctk
import threading
from kabel import main
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self._after_id = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)

    def schedule(self, _event):
        self._after_id = self.widget.after(400, self.show)

    def show(self):
        if self.tooltip:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip = ctk.CTkToplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.configure(fg_color="#010101")
        self.tooltip.wm_attributes("-transparentcolor", "#010101")
        self.tooltip.geometry(f"+{x}+{y}")
        ctk.CTkLabel(self.tooltip, text=self.text, fg_color="#5C5B5B", corner_radius=6).pack(padx=0, pady=0)

    def hide(self, event):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None



        
class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("Kabel og vern kalkulator")
        self.update()
        self.state('zoomed')        
        self.bind("<Escape>", lambda e: self.destroy())

        #columns

        Column_1 = ctk.CTkFrame(self, fg_color="#333232", width=200)
        Column_1.pack(side="left", anchor="nw", padx=20, pady=20)

        Column_2 = ctk.CTkFrame(self, fg_color="#333232", width=200)
        Column_2.pack(side="left", anchor="nw", padx=20, pady=20)

        Column_3 = ctk.CTkFrame(self, fg_color="#333232", width=250)
        Column_3.pack(side="left", anchor="nw", padx=20, pady=20)

        ctk.CTkLabel(Column_3, text="Resultater", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="nw", padx=20, pady=10)
        self.res_Ib      = ctk.CTkLabel(Column_3, text="Belastningsstrøm (Ib): -")
        self.res_Ib.pack(anchor="nw", padx=20, pady=5)
        self.res_sikring = ctk.CTkLabel(Column_3, text="Sikring: -")
        self.res_sikring.pack(anchor="nw", padx=20, pady=5)
        self.res_kar     = ctk.CTkLabel(Column_3, text="Karakteristikk: -")
        self.res_kar.pack(anchor="nw", padx=20, pady=5)
        self.res_kabel   = ctk.CTkLabel(Column_3, text="Kabelstørrelse: -")
        self.res_kabel.pack(anchor="nw", padx=20, pady=5)
        self.res_Iz      = ctk.CTkLabel(Column_3, text="Tillatt strøm (Iz): -")
        self.res_Iz.pack(anchor="nw", padx=20, pady=5)
        self.res_DeltaU  = ctk.CTkLabel(Column_3, text="Spenningsfall (ΔU): -")
        self.res_DeltaU.pack(anchor="nw", padx=20, pady=5)
        self.res_deltaU  = ctk.CTkLabel(Column_3, text="Spenningsfall (Δu): -")
        self.res_deltaU.pack(anchor="nw", padx=20, pady=5)
        self.res_DeltaP  = ctk.CTkLabel(Column_3, text="Effekttap (ΔP): -")
        self.res_DeltaP.pack(anchor="nw", padx=20, pady=5)
        self.res_deltaP  = ctk.CTkLabel(Column_3, text="Effekttap (Δp): -")
        self.res_deltaP.pack(anchor="nw", padx=20, pady=5)

        self.ctk_label_1 = ctk.CTkLabel(Column_1, text="Motordata", font=ctk.CTkFont(size=24, weight="bold"))
        self.ctk_label_1.pack(anchor="nw", padx=20, pady=10)

        self.Pa_entry = ctk.CTkEntry(Column_1, placeholder_text="Watt (P)", width=150)
        self.Pa_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.Pa_entry, "Avgitt effekt (P) i watt")

        self.U_entry = ctk.CTkEntry(Column_1, placeholder_text="Volt (U)", width=150)
        self.U_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.U_entry, "Spenning (U) i volt")

        self.Cos_entry = ctk.CTkEntry(Column_1, placeholder_text="Cos φ", width=150)
        self.Cos_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.Cos_entry, "Effektfaktor (Cos φ)")

        self.effi_entry = ctk.CTkEntry(Column_1, placeholder_text="Virkningsgrad (0-1)", width=150)
        self.effi_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.effi_entry, "Faktoren mellom avgitt og tilført effekt (0-1)")

        self.SI_entry = ctk.CTkEntry(Column_1, placeholder_text="Startstrømsfaktor (SI)", width=150)
        self.SI_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.SI_entry, "Faktoren mellom startstrøm og nominal strøm (SI)")

        self.temp_entry = ctk.CTkEntry(Column_1, placeholder_text="Temperatur (°C)", width=150)
        self.temp_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.temp_entry, "Omgivelsestemperatur (°C)")

        self.ctk_label_2 = ctk.CTkLabel(Column_2, text="Kabeldata", font=ctk.CTkFont(size=24, weight="bold"))
        self.ctk_label_2.pack(anchor="nw", padx=20, pady=10)

        self.Leder_temp_entry = ctk.CTkEntry(Column_2, placeholder_text="Leder temperatur (°C)", width=150)
        self.Leder_temp_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.Leder_temp_entry, "Temperatur på lederene (°C)")

        self.forlegning_entry = ctk.CTkOptionMenu(Column_2, values=["Forlegningsmetode","A1", "A2", "B1", "B2", "C", "E"], width=150)
        self.forlegning_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.forlegning_entry, "A1: Isolerte ledere forlagt i instalasjonsrør i en termisk isolert vegg\nA2: Flerlederkabel forlagt i instalasjonsrør i en termisk isolert vegg\nB1: Isolerte ledere forlagt i instalasjonsrør på vegg\nB2: Flerlederkabel forlagt i instalasjonsrør på vegg\nC: En eller flerlederkabel montert på vegg\nE: Flerlederkabel forlagt i luft")

        self.isolasjon_entry = ctk.CTkOptionMenu(Column_2, values=["Isolasjonstype","PVC", "PEX"], width=150)
        self.isolasjon_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.isolasjon_entry, "Type isolasjon brukt i kabelen\nPVC: Max 70°C\nPEX: Max 90°C")

        self.calble_length_entry = ctk.CTkEntry(Column_2, placeholder_text="Kabel lengde (m)", width=150)
        self.calble_length_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.calble_length_entry, "Lengden på kabelen i meter")

        self.cable_drop_entry = ctk.CTkEntry(Column_2, placeholder_text="Maks spenningsfall (%)", width=150)
        self.cable_drop_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.cable_drop_entry, "Maksimalt tillatt spenningsfall i prosent")

        self.power_loss_entry = ctk.CTkEntry(Column_2, placeholder_text="Maks effekttap (%)", width=150)
        self.power_loss_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.power_loss_entry, "Maksimalt tillatt effekttap i prosent")

        self.calble_group_entry = ctk.CTkEntry(Column_2, placeholder_text="Antall kabler i gruppe", width=150)
        self.calble_group_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.calble_group_entry, "Antall kabler som ligger i samme gruppe")
        
        self.roof_entry = ctk.CTkCheckBox(Column_2, text="Ligger kabelen direkte under et tak?")
        self.roof_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.roof_entry, "Kryss av hvis kabelen ligger direkte under et tak")

        self.cable_gap_entry = ctk.CTkCheckBox(Column_2, text="Er det mellomrom mellom kablene?")
        self.cable_gap_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.cable_gap_entry, "Kryss av hvis det er en kabeltykkelse mellom kablene")

        self.cable_bro_entry = ctk.CTkCheckBox(Column_2, text="Ligger kabelen på en kabelbro?")
        self.cable_bro_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.cable_bro_entry, "Kryss av hvis kabelen ligger på en kabelbro")

        self.cable_bridge_type_entry = ctk.CTkOptionMenu(Column_2, values=["Bro type","Uperforert", "Perforert", "Stige"], width=150)
        self.cable_bridge_type_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.cable_bridge_type_entry, "Type kabelbro")

        self.cable_bridge_stack_entry = ctk.CTkEntry(Column_2, placeholder_text="Antall broer stablet", width=150)
        self.cable_bridge_stack_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.cable_bridge_stack_entry, "Antall kabelbroer stablet oppå hverandre")

        self.cable_bridge_orientation_entry = ctk.CTkOptionMenu(Column_2, values=["Bro orientering","Horisontal", "Vertikal"], width=150)
        self.cable_bridge_orientation_entry.pack(anchor="nw", padx=20, pady=10)
        Tooltip(self.cable_bridge_orientation_entry, "Orientering på kabelbroen")

        self.Writing_checkbox = ctk.CTkCheckBox(Column_3, text="Skriv ut i Word")
        self.Writing_checkbox.pack(anchor="nw", padx=20, pady=10)

        self.calculate_button = ctk.CTkButton(Column_3, text="Beregn", command=self.calculate)
        self.calculate_button.pack(pady=20)

    def calculate(self):
        def flt(entry, default): return float(entry.get()) if entry.get() else default
        def integer(entry, default): return int(entry.get()) if entry.get() else default

        distanse_tak = "J" if self.roof_entry.get() else "N"
        distanse_kabel = "J" if self.cable_gap_entry.get() else "N"
        kabelbro = "J" if self.cable_bro_entry.get() else "N"
        word_export = bool(self.Writing_checkbox.get())

        args = (
            flt(self.Pa_entry, 0), flt(self.U_entry, 0), flt(self.Cos_entry, 0),
            flt(self.effi_entry, 1), flt(self.SI_entry, 1), self.forlegning_entry.get(),
            flt(self.temp_entry, 0) if self.temp_entry.get() else "N/A", flt(self.Leder_temp_entry, 20), self.isolasjon_entry.get(),
            integer(self.calble_group_entry, 1), flt(self.calble_length_entry, 0),
            kabelbro, integer(self.cable_bridge_stack_entry, 1),
            self.cable_bridge_type_entry.get(), self.cable_bridge_orientation_entry.get(),
            distanse_kabel, distanse_tak,
            flt(self.cable_drop_entry, 5), flt(self.power_loss_entry, 5),
        )

        def run():
            result = main(*args, word_export=word_export)
            if result:
                self.after(0, lambda: self.update_results(result))

        threading.Thread(target=run, daemon=True).start()

    def update_results(self, result):
        self.res_Ib.configure(text=f"Belastningsstrøm (Ib): {result['Ib']} A")
        self.res_sikring.configure(text=f"Sikring: {result['Sikring']} A")
        self.res_kar.configure(text=f"Karakteristikk: {result['Karakteristikk']}")
        self.res_kabel.configure(text=f"Kabelstørrelse: {result['Kabel']} mm²")
        self.res_Iz.configure(text=f"Tillatt strøm (Iz): {result['Iz']} A")
        self.res_DeltaU.configure(text=f"Spenningsfall (ΔU): {result['DeltaU']} V")
        self.res_deltaU.configure(text=f"Spenningsfall (Δu): {result['deltaU']} %")
        self.res_DeltaP.configure(text=f"Effekttap (ΔP): {result['DeltaP']} W")
        self.res_deltaP.configure(text=f"Effekttap (Δp): {result['deltaP']} %")



app = App()
app.mainloop()