# ENTRY POINT
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from ui.mainwindow import MainWindow

# Personal Notes
# QApplication holds the Qt event loop, one instance required, application sits in event loop until action is taken ie.) .exec_()
# similar to the event loop of Node.js w/ async await, events are added to a queue, from queue events go to event handlers and go back to loop awaiting more events

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
    
# may or may not need, if executed directly run main(), else if imported use auxiliary function
if __name__ == "__main__":
    main()