import argparse
import asyncio
import sys
from PyQt6 import QtWidgets
from qasync import QEventLoop

from editor_frontend import Frontend

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="snail-text",
        description="Slowest text editor on the planet"
    )
    parser.add_argument('server_address')
    args = parser.parse_args()

    server = args.server_address

    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Frontend(debug_mode=False, server_address=server)
    window.show()
    # app.exec()
    loop.create_task(window.update_text())
    window.backend.run()
