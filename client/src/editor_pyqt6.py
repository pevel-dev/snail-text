import argparse
import sys

from PyQt6.QtGui import QKeySequence

from editor_backend import EditorBackend
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, \
    QMessageBox, QMenuBar


class MainWindow(QMainWindow):
    def __init__(self, init_file_path=None):
        self.backend = EditorBackend(init_file_path)
        self.text = str(self.backend.crdt)
        super().__init__()

        self.setWindowTitle("My App")
        self.text_widget = QTextEdit()
        self.text_widget.setPlainText(self.text)

        self.text_widget.textChanged.connect(self.text_change)
        self.setCentralWidget(self.text_widget)
        self.setup_menus()

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
        file_path, _ = QFileDialog.getOpenFileName \
            (self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        self.backend = EditorBackend(file_path)
        self.text = str(self.backend.crdt)
        self.text_widget.setPlainText(self.text)

    def save_file(self):
        if self.backend.file is None:
            file_path, _ = QFileDialog.getSaveFileName\
                (self, "Save File", "","Text Files (*.txt);;All Files (*)")
            if file_path:
                self.backend.file = file_path

        try:
            with open(self.backend.file, "w") as f:
                f.write(str(self.backend.crdt))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def main():
    parser = argparse.ArgumentParser(
        prog="Snail Text Editor",
        description="Edits text at very low speeds",
        epilog="Licensed under the BEERWARE license.",
    )
    parser.add_argument("-f", "--file", default="")
    args = parser.parse_args()

    file = args.file if args.file != "" else None

    app = QApplication(sys.argv)

    window = MainWindow(file)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
