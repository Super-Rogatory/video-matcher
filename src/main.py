# ENTRY POINT
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from ui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
    
# may or may not need, if executed directly run main(), else if imported use auxiliary function
if __name__ == "__main__":
    main()