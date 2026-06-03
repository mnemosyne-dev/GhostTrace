import sys

from PyQt6.QtWidgets import QApplication
from ui.dashboard import GhostTraceDashboard



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = GhostTraceDashboard()
    window.show()

    sys.exit(app.exec())