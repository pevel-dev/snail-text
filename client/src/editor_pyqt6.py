import sys

from editor_backend import EditorBackend
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        self.backend = EditorBackend()
        self.text = ""
        super().__init__()

        self.setWindowTitle("My App")
        self.text_widget = QTextEdit()
        self.text_widget.textChanged.connect(self.text_change)
        self.setCentralWidget(self.text_widget)

    def text_change(self):
        current_text = self.text_widget.toPlainText()
        self.backend.handle_change_text(current_text, self.text)
        self.text = current_text


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
