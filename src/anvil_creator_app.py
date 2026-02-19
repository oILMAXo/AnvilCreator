"""
Anvil Creator — Vintage Story Smithing & Clay Forming Recipe Editor
Desktop application using pywebview

Author: Claude (Anthropic) — AI-generated application
Created for: ilmax
Version: 1.0
"""
import webview
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def get_html_path():
    """Get path to the HTML file, works both in dev and bundled mode."""
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'anvil-creator.html')


# Unsaved state tracked in Python to avoid evaluate_js deadlock on close
_has_unsaved = False


class Api:
    """Python API exposed to JavaScript for native file dialogs."""

    def __init__(self, window):
        self.window = window

    def set_unsaved_state(self, state):
        """Called from JS to update unsaved changes flag."""
        global _has_unsaved
        _has_unsaved = bool(state)

    def save_file_dialog(self, default_name, file_type):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        filetypes = [('JSON', '*.json'), ('All files', '*.*')]
        default_ext = '.json'

        path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=filetypes,
            initialfile=default_name,
            title='Сохранить файл'
        )
        root.destroy()
        return path if path else None

    def save_file(self, path, content):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return str(e)

    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        path = filedialog.askopenfilename(
            filetypes=[
                ('JSON files', '*.json'),
                ('Anvil Project (legacy)', '*.anvil'),
                ('All files', '*.*')
            ],
            title='Открыть файл'
        )
        root.destroy()

        if not path:
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {'path': path, 'content': content}
        except Exception as e:
            return {'error': str(e)}


def on_closing():
    """Check Python-side unsaved flag (no evaluate_js = no deadlock)."""
    global _has_unsaved
    if not _has_unsaved:
        return True  # No unsaved changes, close immediately

    # Show confirmation dialog
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    result = messagebox.askyesno(
        'Anvil Creator',
        'Есть несохранённые изменения.\nВыйти без сохранения?\n\n'
        'Unsaved changes will be lost.\nExit without saving?',
        icon='warning'
    )
    root.destroy()
    return result  # True = close, False = cancel


def main():
    html_path = get_html_path()
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        sys.exit(1)

    window = webview.create_window(
        title='Anvil Creator — VS Smithing Recipe Editor',
        url=html_path,
        width=1200,
        height=800,
        min_size=(900, 600),
        resizable=True,
        text_select=False,
        confirm_close=False,
    )

    window.events.closing += on_closing

    api = Api(window)
    window.expose(
        api.set_unsaved_state,
        api.save_file_dialog,
        api.save_file,
        api.open_file_dialog,
    )

    webview.start(debug=False)


if __name__ == '__main__':
    main()
