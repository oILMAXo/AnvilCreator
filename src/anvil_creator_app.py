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
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox


def get_base_dir():
    """Get base directory, works both in dev and bundled mode."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_html_path():
    """Get path to the HTML file."""
    return os.path.join(get_base_dir(), 'anvil-creator.html')


def get_icon_path():
    """Get path to the icon file."""
    return os.path.join(get_base_dir(), 'anvil-creator.ico')


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


def set_window_icon(icon_path):
    """Установить иконку окна через Windows API (обход ограничения pywebview)."""
    if sys.platform != 'win32' or not os.path.exists(icon_path):
        return
    try:
        user32 = ctypes.windll.user32
        # Загрузить .ico файл
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x0010
        LR_DEFAULTSIZE = 0x0040
        icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE

        # Большая иконка (32x32) и маленькая (16x16)
        hicon_big = user32.LoadImageW(0, icon_path, IMAGE_ICON, 32, 32, icon_flags)
        hicon_small = user32.LoadImageW(0, icon_path, IMAGE_ICON, 16, 16, icon_flags)

        # Найти окно по заголовку
        hwnd = user32.FindWindowW(None, 'Anvil Creator — VS Smithing Recipe Editor')
        if hwnd:
            WM_SETICON = 0x0080
            ICON_BIG = 1
            ICON_SMALL = 0
            if hicon_big:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)
            if hicon_small:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
    except Exception:
        pass  # Не критично, просто будет дефолтная иконка


def on_shown(window):
    """Вызывается когда окно pywebview отображено."""
    icon_path = get_icon_path()
    set_window_icon(icon_path)


def main():
    html_path = get_html_path()
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        sys.exit(1)

    # Задать AppUserModelID до создания окна
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('AnvilCreator.VS.1')

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
    window.events.shown += lambda: on_shown(window)

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
