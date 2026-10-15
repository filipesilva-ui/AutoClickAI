"""
AutoClick AI — protótipo de demonstração
Requisitos: Python 3.10+ e, para cliques reais, pyautogui
Instalação opcional: python -m pip install pyautogui

Por segurança, o modo SIMULAÇÃO fica ativado por padrão.
No modo simulação, o programa apenas registra o que faria.
Desmarque "Modo simulação" para permitir cliques reais.
Use apenas em aplicativos e páginas onde você tem autorização.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

try:
    import pyautogui
except ImportError:
    pyautogui = None


class AutoClickDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClick AI | Automação Inteligente")
        self.root.geometry("540x500")
        self.root.minsize(500, 470)
        self.root.configure(bg="#101827")

        self.running = False
        self.stop_event = threading.Event()
        self.click_count = 0

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TLabel", background="#101827", foreground="#e5e7eb",
                        font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TCheckbutton", background="#101827", foreground="#e5e7eb",
                        font=("Segoe UI", 10))
        style.configure("TLabelframe", background="#101827", foreground="#93c5fd")
        style.configure("TLabelframe.Label", background="#101827",
                        foreground="#93c5fd", font=("Segoe UI", 10, "bold"))

        tk.Label(root, text="AUTOCLICK AI", bg="#101827", fg="#60a5fa",
                 font=("Segoe UI", 22, "bold")).pack(pady=(18, 2))
        tk.Label(root, text="Automação de interface • Protótipo de demonstração",
                 bg="#101827", fg="#9ca3af", font=("Segoe UI", 9)).pack(pady=(0, 14))

        settings = ttk.LabelFrame(root, text="Parâmetros de execução", padding=14)
        settings.pack(fill="x", padx=22, pady=5)

        row1 = ttk.Frame(settings)
        row1.pack(fill="x", pady=5)
        ttk.Label(row1, text="Coordenada X:").pack(side="left")
        self.x_var = tk.StringVar(value="500")
        ttk.Entry(row1, textvariable=self.x_var, width=8).pack(side="left", padx=(8, 22))
        ttk.Label(row1, text="Coordenada Y:").pack(side="left")
        self.y_var = tk.StringVar(value="400")
        ttk.Entry(row1, textvariable=self.y_var, width=8).pack(side="left", padx=8)

        row2 = ttk.Frame(settings)
        row2.pack(fill="x", pady=5)
        ttk.Label(row2, text="Intervalo (segundos):").pack(side="left")
        self.interval_var = tk.StringVar(value="2")
        ttk.Entry(row2, textvariable=self.interval_var, width=8).pack(side="left", padx=8)
        ttk.Label(row2, text="Número de cliques (0 = contínuo):").pack(side="left", padx=(8, 0))
        self.limit_var = tk.StringVar(value="5")
        ttk.Entry(row2, textvariable=self.limit_var, width=7).pack(side="left", padx=8)

        self.simulation_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings, text="Modo simulação (não clica de verdade)",
                        variable=self.simulation_var).pack(anchor="w", pady=(10, 2))

        status_box = tk.Frame(root, bg="#172235", padx=14, pady=12)
        status_box.pack(fill="x", padx=22, pady=12)
        tk.Label(status_box, text="STATUS DO SISTEMA", bg="#172235", fg="#9ca3af",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.status_var = tk.StringVar(value="Pronto para iniciar")
        tk.Label(status_box, textvariable=self.status_var, bg="#172235", fg="#34d399",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(4, 6))
        self.counter_var = tk.StringVar(value="Execuções: 0")
        tk.Label(status_box, textvariable=self.counter_var, bg="#172235", fg="#e5e7eb",
                 font=("Segoe UI", 11)).pack(anchor="w")

        buttons = tk.Frame(root, bg="#101827")
        buttons.pack(pady=3)
        self.start_btn = ttk.Button(buttons, text="▶  INICIAR", command=self.start)
        self.start_btn.pack(side="left", padx=7)
        self.stop_btn = ttk.Button(buttons, text="■  PARAR", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=7)
        ttk.Button(buttons, text="Zerar contador", command=self.reset).pack(side="left", padx=7)

        self.log = tk.Text(root, height=7, bg="#0b1220", fg="#cbd5e1",
                           insertbackground="white", relief="flat",
                           font=("Consolas", 9), state="disabled")
        self.log.pack(fill="both", expand=True, padx=22, pady=(8, 16))
        self.write_log("Sistema inicializado. Modo simulação ativado por padrão.")
        self.write_log("Defina X/Y, intervalo e quantidade; depois clique em INICIAR.")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def write_log(self, text):
        timestamp = time.strftime("%H:%M:%S")
        self.log.configure(state="normal")
        self.log.insert("end", f"[{timestamp}] {text}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self):
        if self.running:
            return
        try:
            x = int(self.x_var.get())
            y = int(self.y_var.get())
            interval = float(self.interval_var.get())
            limit = int(self.limit_var.get())
            if x < 0 or y < 0 or interval < 0.2 or limit < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Parâmetros inválidos",
                                 "Informe X/Y inteiros não negativos, intervalo >= 0,2 s e quantidade >= 0.")
            return

        if not self.simulation_var.get():
            if pyautogui is None:
                messagebox.showerror("Dependência ausente",
                                     "Para cliques reais, instale PyAutoGUI:\npython -m pip install pyautogui")
                return
            if not messagebox.askyesno("Confirmar cliques reais",
                    f"O programa clicará em X={x}, Y={y} a cada {interval}s.\n"
                    "Confirme que a posição está correta e que você tem autorização. Continuar?"):
                return

        self.running = True
        self.stop_event.clear()
        self.click_count = 0
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        mode = "SIMULAÇÃO" if self.simulation_var.get() else "CLIQUE REAL"
        self.status_var.set(f"Executando — {mode}")
        self.write_log(f"Início: modo={mode}, posição=({x}, {y}), intervalo={interval}s, limite={limit or 'contínuo'}.")
        threading.Thread(target=self.worker, args=(x, y, interval, limit,
                          self.simulation_var.get()), daemon=True).start()

    def worker(self, x, y, interval, limit, simulation):
        while not self.stop_event.is_set():
            if limit and self.click_count >= limit:
                break
            if not simulation:
                try:
                    pyautogui.click(x=x, y=y)
                except Exception as exc:
                    self.root.after(0, self.write_log, f"Erro no clique: {exc}")
                    break
            self.click_count += 1
            message = (f"[simulado] Clique #{self.click_count} em ({x}, {y})"
                       if simulation else f"Clique #{self.click_count} em ({x}, {y})")
            self.root.after(0, self.write_log, message)
            self.root.after(0, self.counter_var.set, f"Execuções: {self.click_count}")
            if self.stop_event.wait(interval):
                break
        self.root.after(0, self.finish)

    def finish(self):
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_var.set("Execução finalizada")
        self.write_log("Execução encerrada.")

    def stop(self):
        self.stop_event.set()
        self.status_var.set("Solicitando parada...")
        self.write_log("Comando de parada recebido.")

    def reset(self):
        if self.running:
            messagebox.showinfo("Automação em execução", "Pare a execução antes de zerar o contador.")
            return
        self.click_count = 0
        self.counter_var.set("Execuções: 0")
        self.write_log("Contador zerado.")

    def on_close(self):
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    app_root = tk.Tk()
    app = AutoClickDemo(app_root)
    app_root.mainloop()
