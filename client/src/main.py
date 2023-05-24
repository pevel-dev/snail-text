import asyncio
import sys
from PyQt6 import QtWidgets
from qasync import QEventLoop

from editor_frontend import Frontend

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Frontend(debug_mode=False)
    window.show()
    # app.exec()
    loop.create_task(window.update_text())
    window.backend.run()
