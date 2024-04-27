from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QGuiApplication
from .controls import Controls
from .videoplayer import VideoPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_interface()

    def initialize_interface(self):
        self.setWindowTitle("Video Matcher")  # Window title
        
        # Set up main layout
        screen = QGuiApplication.primaryScreen().geometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.resize(width, height)
        
        # Create vertical layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Adding top vertical spacing
        vertical_spacing = int(height * 0.15)
        main_layout.insertSpacing(0, vertical_spacing)

        # Horizontal layout for the video players
        video_layout = QHBoxLayout()

        # Creating two media players
        self.query_screen = VideoPlayer() 
        self.match_screen = VideoPlayer()

        # Set minimum sizes for video players
        self.query_screen.setMinimumSize(640, 480)
        self.match_screen.setMinimumSize(640, 480)

        # Add video players to the layout with equal stretch factors
        video_layout.addWidget(self.query_screen, 1)  # Stretch factor of 1
        video_layout.addWidget(self.match_screen, 1)  # Stretch factor of 1

        main_layout.addLayout(video_layout)

        # Adding bottom vertical spacing
        main_layout.insertSpacing(main_layout.count(), 50)

        # Add controls to the window
        self.controls = Controls()
        main_layout.addWidget(self.controls)


        