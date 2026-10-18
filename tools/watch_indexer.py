#!/usr/bin/env python3
"""watch_indexer.py - Vigila cambios en ~/joko-lab/ y re-indexa automaticamente"""
import os, time, subprocess, threading, logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = os.path.expanduser("~/joko-lab")
INDEXER = os.path.join(WATCH_DIR, "tools", "indexer.py")
VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")
COOLDOWN = 15  # segundos de espera tras el ultimo cambio

logging.basicConfig(level=logging.INFO, format="[watch] %(message)s")
log = logging.getLogger(__name__)

class JokoLabHandler(FileSystemEventHandler):
    def __init__(self):
        self.timer = None

    def on_modified(self, event):
        self._handle(event)

    def on_created(self, event):
        self._handle(event)

    def on_deleted(self, event):
        self._handle(event)

    def _handle(self, event):
        if event.is_directory:
            return
        # Vigilar .md (docs) y .yaml/.yml (Knowledge Objects). Fix 2-ago-2026:
        # antes solo .md → curar un KO (ej: DEC-001.yaml) no disparaba re-indexado.
        if not (event.src_path.endswith(".md")
                or event.src_path.endswith(".yaml")
                or event.src_path.endswith(".yml")):
            return
        if ".lancedb" in event.src_path or ".git" in event.src_path:
            return
        # Fix 03-sep-2026 (opcion b del usuario): ignorar 04-operations/backlogs/.
        # El backlog se modifica a todas horas (entradas de sesiones, backups
        # .BACKUP.*) y disparaba reindexados constantes. El cron horario
        # (rag-reindex-catchup) indexa igualmente su contenido 1x/hora.
        if "/04-operations/backlogs/" in event.src_path:
            return

        # Reiniciar timer de cooldown
        if self.timer and self.timer.is_alive():
            self.timer.cancel()

        self.timer = threading.Timer(COOLDOWN, self._run_indexer)
        self.timer.daemon = True
        self.timer.start()

    def _run_indexer(self):
        log.info("Re-indexando tras cambios en archivos .md/.yaml/.yml...")
        try:
            result = subprocess.run(
                [VENV_PYTHON, INDEXER],
                capture_output=True, text=True, timeout=1800
            )
        except subprocess.TimeoutExpired:
            log.error("Indexacion abortada: supero los 1800s de timeout")
            return
        if result.returncode == 0:
            # Extraer numero de registros de la salida
            for line in result.stdout.split("\n"):
                if "registros" in line:
                    log.info(f"Indexacion completada: {line.strip()}")
                    break
        else:
            log.error(f"Error en indexacion: {result.stderr[:200]}")

def main():
    log.info(f"Vigilando {WATCH_DIR} (cooldown: {COOLDOWN}s)")
    log.info(f"Indexador: {INDEXER}")

    event_handler = JokoLabHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
