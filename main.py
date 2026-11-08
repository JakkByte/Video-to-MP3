import os
import sys
import subprocess
import threading
import queue
import json
import webbrowser
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

APP_NAME = "Video to MP3 | JakkByte"
BG = "#17111F"
CARD = "#21192B"
BORDER = "#483557"
TEXT = "#F8F5FC"
MUTED = "#B7A6C7"
PURPLE = "#A78BFA"
GREEN = "#A3E635"
RED = "#FF6B79"
EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".flv", ".mpeg", ".mpg", ".m4v", ".3gp"}


TRANSLATIONS = {'en': {'queue': 'CONVERSION QUEUE',
        'files': '{n} files',
        'video': 'VIDEO FILE',
        'status': 'STATUS',
        'add': '+  ADD VIDEOS',
        'remove': 'REMOVE SELECTED',
        'convert': 'CONVERT TO MP3',
        'ready': 'Ready. Add videos to begin.',
        'select': 'Select video files',
        'supported': 'Supported video files',
        'all': 'All files',
        'waiting': 'Waiting',
        'running': 'Converting...',
        'completed': 'Completed',
        'failed': 'Failed',
        'skipped': 'Skipped',
        'added': 'Added {n} video(s). Ready to convert.',
        'none_added': 'No new supported videos were added.',
        'removed': 'Selected videos removed from the queue.',
        'nothing': 'Add videos or remove completed items to start again.',
        'progress': 'Converting {n} of {total}: {name}',
        'starting': 'Converting 0 of {total} videos...',
        'converted': 'Converted: {name}',
        'exists': 'Skipped: {name} (MP3 already exists)',
        'error': 'Failed: {name} — {detail}',
        'fatal': 'FFmpeg unavailable: {detail}',
        'finished': 'Finished: {ok} converted, {fail} failed, {skip} skipped.',
        'footer': 'VIDEO TO MP3  •  DEVELOPED BY JAKKBYTE',
        'about': 'ABOUT / LICENSES',
        'about_title': 'ABOUT / LICENSES',
        'third_party': 'Third-party software',
        'about_description': 'This app uses FFmpeg to convert video audio to MP3.',
        'ffmpeg_license': 'FFmpeg is licensed under LGPLv3 or later.',
        'license_files': 'View license files',
        'ffmpeg_site': 'FFmpeg website',
        'close': 'Close',
        'license_missing': 'License files were not found in this build.'},
 'pt': {'queue': 'FILA DE CONVERSÃO',
        'files': '{n} arquivos',
        'video': 'ARQUIVO DE VÍDEO',
        'status': 'STATUS',
        'add': '+  ADICIONAR VÍDEOS',
        'remove': 'REMOVER SELECIONADOS',
        'convert': 'CONVERTER PARA MP3',
        'ready': 'Pronto. Adicione vídeos para começar.',
        'select': 'Selecionar arquivos de vídeo',
        'supported': 'Vídeos compatíveis',
        'all': 'Todos os arquivos',
        'waiting': 'Aguardando',
        'running': 'Convertendo...',
        'completed': 'Concluído',
        'failed': 'Falhou',
        'skipped': 'Ignorado',
        'added': '{n} vídeo(s) adicionado(s). Pronto para converter.',
        'none_added': 'Nenhum vídeo novo compatível foi adicionado.',
        'removed': 'Vídeos selecionados removidos da fila.',
        'nothing': 'Adicione vídeos ou remova os concluídos para converter novamente.',
        'progress': 'Convertendo {n} de {total}: {name}',
        'starting': 'Convertendo 0 de {total} vídeos...',
        'converted': 'Convertido: {name}',
        'exists': 'Ignorado: {name} (o MP3 já existe)',
        'error': 'Falha: {name} — {detail}',
        'fatal': 'FFmpeg indisponível: {detail}',
        'finished': 'Finalizado: {ok} convertidos, {fail} falhas, {skip} ignorados.',
        'footer': 'VIDEO TO MP3  •  DESENVOLVIDO POR JAKKBYTE',
        'about': 'SOBRE / LICENÇAS',
        'about_title': 'SOBRE / LICENÇAS',
        'third_party': 'Software de terceiros',
        'about_description': 'Este aplicativo utiliza o FFmpeg para converter áudio de vídeos em MP3.',
        'ffmpeg_license': 'O FFmpeg é licenciado sob LGPLv3 ou posterior.',
        'license_files': 'Ver arquivos de licença',
        'ffmpeg_site': 'Site do FFmpeg',
        'close': 'Fechar',
        'license_missing': 'Arquivos de licença não encontrados nesta versão.'},
 'es': {'queue': 'COLA DE CONVERSIÓN',
        'files': '{n} archivos',
        'video': 'ARCHIVO DE VIDEO',
        'status': 'ESTADO',
        'add': '+  AÑADIR VIDEOS',
        'remove': 'QUITAR SELECCIONADOS',
        'convert': 'CONVERTIR A MP3',
        'ready': 'Listo. Añade videos para comenzar.',
        'select': 'Seleccionar archivos de video',
        'supported': 'Videos compatibles',
        'all': 'Todos los archivos',
        'waiting': 'En espera',
        'running': 'Convirtiendo...',
        'completed': 'Completado',
        'failed': 'Fallido',
        'skipped': 'Omitido',
        'added': 'Se añadieron {n} video(s). Listo para convertir.',
        'none_added': 'No se añadieron videos nuevos compatibles.',
        'removed': 'Videos seleccionados eliminados de la cola.',
        'nothing': 'Añade videos o elimina los completados para repetir.',
        'progress': 'Convirtiendo {n} de {total}: {name}',
        'starting': 'Convirtiendo 0 de {total} videos...',
        'converted': 'Convertido: {name}',
        'exists': 'Omitido: {name} (el MP3 ya existe)',
        'error': 'Error: {name} — {detail}',
        'fatal': 'FFmpeg no disponible: {detail}',
        'finished': 'Finalizado: {ok} convertidos, {fail} fallidos, {skip} omitidos.',
        'footer': 'VIDEO TO MP3  •  DESARROLLADO POR JAKKBYTE',
        'about': 'ACERCA DE / LICENCIAS',
        'about_title': 'ACERCA DE / LICENCIAS',
        'third_party': 'Software de terceros',
        'about_description': 'Esta aplicación utiliza FFmpeg para convertir audio de videos a MP3.',
        'ffmpeg_license': 'FFmpeg se distribuye bajo LGPLv3 o posterior.',
        'license_files': 'Ver archivos de licencia',
        'ffmpeg_site': 'Sitio web de FFmpeg',
        'close': 'Cerrar',
        'license_missing': 'No se encontraron los archivos de licencia.'},
 'fr': {'queue': 'FILE DE CONVERSION',
        'files': '{n} fichiers',
        'video': 'FICHIER VIDÉO',
        'status': 'STATUT',
        'add': '+  AJOUTER DES VIDÉOS',
        'remove': 'RETIRER LA SÉLECTION',
        'convert': 'CONVERTIR EN MP3',
        'ready': 'Prêt. Ajoutez des vidéos pour commencer.',
        'select': 'Sélectionner des vidéos',
        'supported': 'Vidéos compatibles',
        'all': 'Tous les fichiers',
        'waiting': 'En attente',
        'running': 'Conversion...',
        'completed': 'Terminé',
        'failed': 'Échec',
        'skipped': 'Ignoré',
        'added': '{n} vidéo(s) ajoutée(s). Prêt à convertir.',
        'none_added': 'Aucune nouvelle vidéo compatible ajoutée.',
        'removed': 'Vidéos sélectionnées retirées de la liste.',
        'nothing': 'Ajoutez des vidéos ou retirez les fichiers terminés.',
        'progress': 'Conversion {n} sur {total} : {name}',
        'starting': 'Conversion de 0 sur {total} vidéos...',
        'converted': 'Converti : {name}',
        'exists': 'Ignoré : {name} (le MP3 existe déjà)',
        'error': 'Échec : {name} — {detail}',
        'fatal': 'FFmpeg indisponible : {detail}',
        'finished': 'Terminé : {ok} convertis, {fail} échecs, {skip} ignorés.',
        'footer': 'VIDEO TO MP3  •  DÉVELOPPÉ PAR JAKKBYTE',
        'about': 'À PROPOS / LICENCES',
        'about_title': 'À PROPOS / LICENCES',
        'third_party': 'Logiciels tiers',
        'about_description': "Cette application utilise FFmpeg pour convertir l'audio des vidéos en MP3.",
        'ffmpeg_license': 'FFmpeg est distribué sous LGPLv3 ou ultérieure.',
        'license_files': 'Voir les fichiers de licence',
        'ffmpeg_site': 'Site de FFmpeg',
        'close': 'Fermer',
        'license_missing': 'Fichiers de licence introuvables.'},
 'de': {'queue': 'KONVERTIERUNGSLISTE',
        'files': '{n} Dateien',
        'video': 'VIDEODATEI',
        'status': 'STATUS',
        'add': '+  VIDEOS HINZUFÜGEN',
        'remove': 'AUSWAHL ENTFERNEN',
        'convert': 'IN MP3 UMWANDELN',
        'ready': 'Bereit. Videos hinzufügen, um zu starten.',
        'select': 'Videodateien auswählen',
        'supported': 'Unterstützte Videos',
        'all': 'Alle Dateien',
        'waiting': 'Wartend',
        'running': 'Konvertierung...',
        'completed': 'Abgeschlossen',
        'failed': 'Fehlgeschlagen',
        'skipped': 'Übersprungen',
        'added': '{n} Video(s) hinzugefügt. Bereit.',
        'none_added': 'Keine neuen unterstützten Videos hinzugefügt.',
        'removed': 'Ausgewählte Videos entfernt.',
        'nothing': 'Videos hinzufügen oder fertige Einträge entfernen.',
        'progress': 'Konvertiere {n} von {total}: {name}',
        'starting': 'Konvertiere 0 von {total} Videos...',
        'converted': 'Konvertiert: {name}',
        'exists': 'Übersprungen: {name} (MP3 existiert bereits)',
        'error': 'Fehler: {name} — {detail}',
        'fatal': 'FFmpeg nicht verfügbar: {detail}',
        'finished': 'Fertig: {ok} konvertiert, {fail} Fehler, {skip} übersprungen.',
        'footer': 'VIDEO TO MP3  •  ENTWICKELT VON JAKKBYTE',
        'about': 'INFO / LIZENZEN',
        'about_title': 'INFO / LIZENZEN',
        'third_party': 'Software von Drittanbietern',
        'about_description': 'Diese App verwendet FFmpeg, um Video-Audio in MP3 umzuwandeln.',
        'ffmpeg_license': 'FFmpeg steht unter LGPLv3 oder neuer.',
        'license_files': 'Lizenzdateien anzeigen',
        'ffmpeg_site': 'FFmpeg-Website',
        'close': 'Schließen',
        'license_missing': 'Lizenzdateien wurden nicht gefunden.'}}
LANG_NAMES = {'en':'English', 'pt':'Português (Brasil)', 'es':'Español', 'fr':'Français', 'de':'Deutsch'}


def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("720x780")
        self.root.minsize(660, 700)
        self.root.configure(bg=BG)
        self.config_path = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "JakkByte", "VideoToMP3", "settings.json")
        self.lang = "en"
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                saved = json.load(f).get("language", "en")
                if saved in TRANSLATIONS:
                    self.lang = saved
        except (OSError, ValueError, TypeError, AttributeError):
            pass
        self.items = []
        self.busy = False
        self.messages = queue.Queue()
        self.completed = 0
        self.failed = 0
        self.current = 0
        self.total_in_batch = 0
        self.build_ui()
        self.root.after(100, self.poll_messages)
        try:
            icon = resource_path("icon.ico")
            if os.path.isfile(icon):
                self.root.iconbitmap(icon)
        except tk.TclError:
            pass

    def t(self, key, **kwargs):
        return TRANSLATIONS[self.lang][key].format(**kwargs)

    def change_language(self, display):
        self.lang = next((code for code, name in LANG_NAMES.items() if name == display), "en")
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"language": self.lang}, f)
        except OSError:
            pass
        self.refresh_language()

    def refresh_language(self):
        self.queue_label.config(text=self.t("queue"))
        self.count_label.config(text=self.t("files", n=len(self.items)))
        self.tree.heading("filename", text=self.t("video"))
        self.tree.heading("status", text=self.t("status"))
        self.add_btn.config(text=self.t("add"))
        self.remove_btn.config(text=self.t("remove"))
        self.convert_btn.config(text=self.t("convert"))
        self.footer.config(text=self.t("footer"))
        self.about_btn.config(text=self.t("about"))
        status_keys = {"Waiting": "waiting", "Running": "running", "Converting...": "running",
                       "Completed": "completed", "Failed": "failed", "Skipped": "skipped"}
        for entry in self.items:
            key = status_keys.get(entry["status"], "waiting")
            self.tree.set(entry["id"], "status", self.t(key))
        if not self.busy:
            self.set_status(self.t("ready"))

    def build_ui(self):
        # Square, compact layout: dark JakkByte styling and clean spacing.
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=22, pady=(17, 12))

        header = tk.Frame(outer, bg=BG)
        header.pack(fill="x", pady=(0, 7))
        tk.Label(header, text="VIDEO TO MP3", font=("Segoe UI", 24, "bold"),
                 bg=BG, fg=TEXT).pack()
        tk.Label(header, text="JAKKBYTE  /  INDIE SOFTWARE", font=("Segoe UI", 9),
                 bg=BG, fg=PURPLE).pack(pady=(2, 0))
        langrow = tk.Frame(outer, bg=BG)
        langrow.pack(fill="x", pady=(2, 0))
        self.language_choice = ttk.Combobox(langrow, state="readonly", width=19,
                                            values=list(LANG_NAMES.values()), font=("Segoe UI", 9))
        self.language_choice.set(LANG_NAMES[self.lang])
        self.language_choice.pack(side="right")
        self.about_btn = tk.Button(
            langrow, text=self.t("about"), command=self.show_about,
            bg=BG, fg=PURPLE, activebackground=BG, activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 9),
            padx=6, pady=3
        )
        self.about_btn.pack(side="left")
        self.language_choice.bind("<<ComboboxSelected>>",
                                  lambda event: self.change_language(self.language_choice.get()))
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=(8, 10))

        panel = tk.Frame(outer, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        panel_header = tk.Frame(panel, bg=CARD)
        panel_header.pack(fill="x", padx=15, pady=(13, 9))
        self.queue_label = tk.Label(panel_header, text=self.t("queue"), font=("Segoe UI", 10, "bold"),
                                    fg=TEXT, bg=CARD)
        self.queue_label.pack(side="left")
        self.count_label = tk.Label(panel_header, text=self.t("files", n=0), font=("Segoe UI", 9),
                                    fg=PURPLE, bg=CARD)
        self.count_label.pack(side="right")

        list_frame = tk.Frame(panel, bg=CARD)
        list_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.tree = ttk.Treeview(list_frame, columns=("filename", "status"),
                                 show="headings", selectmode="extended", height=9)
        self.tree.heading("filename", text=self.t("video"))
        self.tree.heading("status", text=self.t("status"))
        self.tree.column("filename", width=440, minwidth=200, anchor="w", stretch=True)
        self.tree.column("status", width=145, minwidth=115, anchor="center", stretch=False)
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        buttons = tk.Frame(outer, bg=BG)
        buttons.pack(fill="x", pady=(13, 9))
        self.add_btn = self.button(buttons, self.t("add"), self.add_files, PURPLE, BG)
        self.add_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.remove_btn = self.button(buttons, self.t("remove"), self.remove_selected,
                                      "#392B4A", TEXT)
        self.remove_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.convert_btn = self.button(outer, self.t("convert"), self.start_conversion,
                                       GREEN, "#101010")
        self.convert_btn.pack(fill="x", pady=(0, 12))

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Jakk.Horizontal.TProgressbar", troughcolor="#352942",
                        background=GREEN, bordercolor="#352942",
                        lightcolor=GREEN, darkcolor=GREEN, thickness=9)
        style.configure("Treeview", background=CARD, fieldbackground=CARD,
                        foreground=TEXT, rowheight=30, borderwidth=0,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#342640",
                        foreground=TEXT, font=("Segoe UI", 9, "bold"),
                        relief="flat", padding=(8, 8))
        style.map("Treeview", background=[("selected", "#594276")],
                  foreground=[("selected", TEXT)])
        self.progress = ttk.Progressbar(outer, style="Jakk.Horizontal.TProgressbar",
                                         mode="determinate", maximum=100)
        self.progress.pack(fill="x")

        self.status = tk.Label(outer, text=self.t("ready"),
                               font=("Segoe UI", 9), fg=MUTED, bg=BG,
                               anchor="w", justify="left")
        self.status.bind("<Configure>", lambda event: self.status.config(wraplength=max(250, event.width - 8)))
        self.status.pack(fill="x", pady=(10, 8))
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=(0, 9))
        self.footer = tk.Label(outer, text=self.t("footer"),
                               font=("Segoe UI", 8), fg=PURPLE, bg=BG)
        self.footer.pack()

    def show_about(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("about_title"))
        dialog.geometry("520x390")
        dialog.resizable(False, False)
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()

        content = tk.Frame(dialog, bg=BG, padx=24, pady=20)
        content.pack(fill="both", expand=True)
        tk.Label(content, text="VIDEO TO MP3", font=("Segoe UI", 19, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(content, text="JAKKBYTE  •  v1.0.0",
                 font=("Segoe UI", 10), bg=BG, fg=PURPLE).pack(anchor="w", pady=(2, 16))
        tk.Label(content, text=self.t("third_party"),
                 font=("Segoe UI", 11, "bold"), bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(content, text=self.t("about_description"),
                 font=("Segoe UI", 10), bg=BG, fg=MUTED,
                 justify="left", wraplength=460).pack(anchor="w", pady=(8, 5))
        tk.Label(content, text=self.t("ffmpeg_license"),
                 font=("Segoe UI", 10), bg=BG, fg=MUTED).pack(anchor="w")

        links = tk.Frame(content, bg=BG)
        links.pack(anchor="w", pady=(17, 8))
        tk.Button(links, text=self.t("license_files"), command=self.open_licenses,
                  bg=CARD, fg=PURPLE, activebackground=CARD,
                  activeforeground=TEXT, relief="flat", cursor="hand2",
                  font=("Segoe UI", 9), padx=12, pady=7).pack(side="left")
        tk.Button(links, text=self.t("ffmpeg_site"),
                  command=lambda: webbrowser.open("https://ffmpeg.org/"),
                  bg=CARD, fg=PURPLE, activebackground=CARD,
                  activeforeground=TEXT, relief="flat", cursor="hand2",
                  font=("Segoe UI", 9), padx=12, pady=7).pack(side="left", padx=(9, 0))
        tk.Button(content, text=self.t("close"), command=dialog.destroy,
                  bg=GREEN, fg="#101010", relief="flat", cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=18, pady=7).pack(anchor="e", side="bottom")

    def open_licenses(self):
        folder = resource_path("licenses")
        if os.path.isdir(folder):
            if os.name == "nt":
                os.startfile(folder)
            else:
                webbrowser.open(Path(folder).as_uri())
        else:
            from tkinter import messagebox
            messagebox.showwarning(self.t("about_title"), self.t("license_missing"),
                                   parent=self.root)

    def button(self, parent, text, command, bg, fg):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg, activebackground=bg,
                         activeforeground=fg, font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                         cursor="hand2", pady=9, disabledforeground="#8B8292")

    def set_status(self, text, color=MUTED):
        self.status.config(text=text, fg=color)

    def add_files(self):
        if self.busy:
            return
        patterns = " ".join("*" + e for e in sorted(EXTENSIONS))
        paths = filedialog.askopenfilenames(title=self.t("select"), filetypes=[(self.t("supported"), patterns), (self.t("all"), "*.*")])
        known = {entry["path"].casefold() for entry in self.items}
        added = 0
        for raw in paths:
            path = os.path.abspath(raw)
            if Path(path).suffix.lower() not in EXTENSIONS or not os.path.isfile(path) or path.casefold() in known:
                continue
            item_id = self.tree.insert("", "end", values=(os.path.basename(path), self.t("waiting")))
            self.items.append({"path": path, "id": item_id, "status": "Waiting"})
            known.add(path.casefold())
            added += 1
        self.count_label.config(text=self.t("files", n=len(self.items)))
        if added:
            self.set_status(self.t("added", n=added), PURPLE)
        elif paths:
            self.set_status(self.t("none_added"), RED)

    def remove_selected(self):
        if self.busy:
            return
        selected = set(self.tree.selection())
        for item_id in selected:
            self.tree.delete(item_id)
        self.items = [entry for entry in self.items if entry["id"] not in selected]
        self.count_label.config(text=self.t("files", n=len(self.items)))
        self.set_status(self.t("removed"))

    def start_conversion(self):
        if self.busy:
            return
        pending = [entry for entry in self.items if entry["status"] in ("Waiting", "Failed", "Skipped")]
        if not pending:
            self.set_status(self.t("nothing"), PURPLE)
            return
        self.busy = True
        self.completed = 0
        self.failed = 0
        self.current = 0
        self.total_in_batch = len(pending)
        self.progress["value"] = 0
        self.add_btn.config(state="disabled")
        self.remove_btn.config(state="disabled")
        self.convert_btn.config(state="disabled")
        self.set_status(self.t("starting", total=len(pending)), PURPLE)
        threading.Thread(target=self.convert_worker, args=(pending,), daemon=True).start()

    def convert_worker(self, pending):
        try:
            ffmpeg = resource_path("ffmpeg.exe")
            if not os.path.isfile(ffmpeg):
                raise FileNotFoundError("FFmpeg executable not found: " + ffmpeg)
        except Exception as exc:
            self.messages.put(("fatal", str(exc), len(pending)))
            return
        for number, entry in enumerate(pending, start=1):
            self.messages.put(("running", entry["id"], number, len(pending)))
            source = entry["path"]
            output = os.path.splitext(source)[0] + ".mp3"
            if os.path.exists(output):
                self.messages.put(("result", entry["id"], "Skipped", "MP3 already exists; original was not overwritten.", number, len(pending)))
                continue
            command = [ffmpeg, "-nostdin", "-n", "-hide_banner", "-loglevel", "error", "-i", source,
                       "-map", "0:a:0", "-vn", "-codec:a", "libmp3lame", "-q:a", "2", output]
            conversion_started = False
            try:
                conversion_started = True
                options = {"capture_output": True, "text": True, "errors": "replace", "check": True}
                if os.name == "nt":
                    options["creationflags"] = subprocess.CREATE_NO_WINDOW
                subprocess.run(command, **options)
                self.messages.put(("result", entry["id"], "Completed", output, number, len(pending)))
            except Exception as exc:
                if isinstance(exc, subprocess.CalledProcessError):
                    detail = (exc.stderr or str(exc)).strip().splitlines()
                    error = detail[-1] if detail else "FFmpeg failed."
                else:
                    error = str(exc)
                # Remove a partial output generated by a failed conversion only.
                try:
                    if conversion_started and os.path.exists(output):
                        os.remove(output)
                except OSError:
                    pass
                self.messages.put(("result", entry["id"], "Failed", error, number, len(pending)))
        self.messages.put(("finished", len(pending)))

    def poll_messages(self):
        try:
            while True:
                message = self.messages.get_nowait()
                kind = message[0]
                if kind == "running":
                    _, item_id, number, total = message
                    self.tree.set(item_id, "status", self.t("running"))
                    self.set_status(self.t("progress", n=number, total=total, name=self.tree.set(item_id, "filename")), PURPLE)
                elif kind == "result":
                    _, item_id, result, detail, number, total = message
                    self.tree.set(item_id, "status", self.t(result.lower()))
                    for entry in self.items:
                        if entry["id"] == item_id:
                            entry["status"] = result
                            break
                    if result == "Completed":
                        self.completed += 1
                        self.set_status(self.t("converted", name=os.path.basename(detail)), GREEN)
                    elif result == "Skipped":
                        self.set_status(self.t("exists", name=self.tree.set(item_id, "filename")), PURPLE)
                    else:
                        self.failed += 1
                        self.set_status(self.t("error", name=self.tree.set(item_id, "filename"), detail=detail[:130]), RED)
                    self.progress["value"] = number / total * 100
                elif kind == "fatal":
                    _, detail, total = message
                    self.failed = total
                    self.busy = False
                    self.add_btn.config(state="normal")
                    self.remove_btn.config(state="normal")
                    self.convert_btn.config(state="normal")
                    self.set_status(self.t("fatal", detail=detail[:160]), RED)
                elif kind == "finished":
                    self.finish()
        except queue.Empty:
            pass
        self.root.after(100, self.poll_messages)

    def finish(self):
        self.busy = False
        self.add_btn.config(state="normal")
        self.remove_btn.config(state="normal")
        self.convert_btn.config(state="normal")
        skipped = max(0, self.total_in_batch - self.completed - self.failed)
        color = GREEN if not self.failed else RED
        self.set_status(self.t("finished", ok=self.completed, fail=self.failed, skip=skipped), color)


if __name__ == "__main__":
    window = tk.Tk()
    ConverterApp(window)
    window.mainloop()
