from tkinter import Tk, Entry, Menu, SEL_FIRST, SEL_LAST, INSERT, END


class ClipboardFeatures:
    def __init__(self, entry: Entry, window: Tk) -> None:
        self.window = window

        # Create entry widget
        self.entry = Entry(window)

        # Create context menu
        self.entry = entry
        self.context_menu = Menu(entry, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)

        # Globally bind 'undo-hotkey' (Ctrl-Z)
        entry.bind('<Control-z>', self.undo_text)

        # Globally bind context menu
        entry.bind('<Button-3>', self.show_context_menu)

        # Bind click event to focus and highlight the entire entry
        entry.bind("<FocusIn>", lambda event: self.on_click(entry, event))

    def copy_text(self) -> None:
        self.entry.clipboard_clear()
        self.entry.clipboard_append(self.entry.selection_get())
        self.entry.update()

    def cut_text(self) -> None:
        self.copy_text()
        self.entry.delete(SEL_FIRST, SEL_LAST)

    def paste_text(self) -> None:
        self.entry.insert(INSERT, self.entry.clipboard_get())

    def undo_text(self, event) -> None:
        self.context_menu.post(event.x_root, event.y_root)

    def show_context_menu(self, event) -> None:
        self.context_menu.post(event.x_root, event.y_root)

    def on_click(self, entry, event) -> None:
        self.entry.focus_set()
        self.entry.select_range(0, END)
