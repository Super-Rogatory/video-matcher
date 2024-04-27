from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

class Controls(QWidget):
    '''
        Signals are notifications emitted by widgets when something happens. That something can be any number of things, 
        from pressing a button, to the text of an input box changing, to the text of the window changing.
    '''
    play_signal = pyqtSignal(int)
    pause_signal = pyqtSignal(int)
    reset_button = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.create_layout()
    
        
    def create_layout(self):
        # use state variable to maintain access to buttons
        layout = QHBoxLayout(self)
        # create buttons
        self.play_button = QPushButton('Play', self)
        self.pause_button = QPushButton('Pause', self)
        self.reset_button = QPushButton('Reset', self)
        
        self.play_button.setFixedSize(200, 50)  
        self.pause_button.setFixedSize(200, 50)  
        self.reset_button.setFixedSize(200, 50) 
        
        # add to layout - organized horizontally - 
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.reset_button)
        
        
        