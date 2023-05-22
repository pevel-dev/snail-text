import asyncio

from PyQt6.QtWidgets import QMainWindow, QTextEdit, QMenuBar, QFileDialog, \
    QMessageBox

from client.src.editor_backend import EditorBackend


class Frontend(QMainWindow):
    def __init__(self, file_path=None, debug_mode=False):
        super().__init__()

        self.backend = EditorBackend(file_path, debug_mode)
        self.text = str(self.backend.crdt)

        self.setWindowTitle("snail-text")
        self.text_widget = QTextEdit()
        self.text_widget.setPlainText(self.text)

        self.text_widget.textChanged.connect(self.text_change)
        self.setCentralWidget(self.text_widget)
        self.setup_menus()

        self.backend.dataChanged.connect(self.update_text)
        # self.backend.run()

    def text_change(self):
        current_text = self.text_widget.toPlainText()
        self.backend.handle_change_text(current_text, self.text)
        self.text = current_text

    def setup_menus(self):
        menu_bar = QMenuBar(parent=self)

        file_menu = menu_bar.addMenu("&File")

        open_action = file_menu.addAction("&Open")
        open_action.triggered.connect(self.open_file)

        save_action = file_menu.addAction("&Save")
        save_action.triggered.connect(self.save_file)

        self.setMenuBar(menu_bar)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )
        self.backend = EditorBackend(file_path)
        self.text = str(self.backend.crdt)
        self.text_widget.setPlainText(self.text)

    def save_file(self):
        if self.backend.file is None:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Text Files (*.txt);;All Files (*)"
            )
            if file_path:
                self.backend.file = file_path

        try:
            with open(self.backend.file, "w") as f:
                f.write(str(self.backend.crdt))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    async def update_text(self):
        while True:
            if not self.backend.has_changes:
                await asyncio.sleep(0.01)
                continue
            self.text = str(self.backend.crdt)
            self.text_widget.setPlainText(self.text)
            self.backend.has_changes = False
