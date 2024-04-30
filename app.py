import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Controls(QWidget):
    play_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    reset_signal = pyqtSignal()
    upload_video_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.create_layout()

    def create_layout(self):
        # Overall layout
        main_layout = QVBoxLayout(self)  

        # upload button at the top-right
        self.upload_button = QPushButton('Upload', self)
        self.upload_button.setFixedSize(90, 35) 
        upload_layout = QHBoxLayout()
        upload_layout.addStretch()  # Add stretch to push the button to the right
        upload_layout.addWidget(self.upload_button)
        upload_layout.setContentsMargins(0, 0, 0, 0)  # Left, Top, Right, Bottom margins
        upload_layout.setSpacing(0)
        # Add upload layout to the main layout
        main_layout.addLayout(upload_layout)

        # A spacer item to provide padding below the upload button if needed
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # central buttons layout
        control_layout = QHBoxLayout()
        self.play_button = QPushButton('Play', self)
        self.pause_button = QPushButton('Pause', self)
        self.reset_button = QPushButton('Reset', self)
        
        self.play_button.setFixedSize(200, 50)
        self.pause_button.setFixedSize(200, 50)
        self.reset_button.setFixedSize(200, 50)
        
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.reset_button)
        control_layout.setSpacing(10)  # Space between buttons

        # add some space before the main controls
        main_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # add the central control layout to the main layout
        main_layout.addLayout(control_layout)
        
        main_layout.addSpacing(15)
        
        # connect signals
        self.play_button.clicked.connect(self.play_signal.emit)
        self.pause_button.clicked.connect(self.pause_signal.emit)
        self.reset_button.clicked.connect(self.reset_signal.emit)
        self.upload_button.clicked.connect(self.upload_video_signal.emit)
        
class VideoPlayer(QVideoWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self)  
        self.setStyleSheet("background-color: black;")

    def load_video(self, url):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        
    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def reset(self):
        self.media_player.setPosition(0)
        self.media_player.play()
        
    def resizeEvent(self, event):
        # maintain a 16:9 aspect ratio
        new_width = event.size().width()
        new_height = int(new_width * 9 / 16)
        self.resize(new_width, new_height)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_interface()
  
    def initialize_interface(self):
        self.setWindowTitle("Video Matcher")
        screen = QApplication.primaryScreen().geometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addStretch(1) 
        
        video_layout = QHBoxLayout()
        self.query_screen = VideoPlayer()
        self.match_screen = VideoPlayer()
        
        self.query_screen.setMinimumSize(640, 480)
        self.match_screen.setMinimumSize(640, 480)
        
        self.query_screen.media_player.mediaStatusChanged.connect(self.handle_media_status_change)
        self.match_screen.media_player.mediaStatusChanged.connect(self.handle_media_status_change)
        
        video_layout.addWidget(self.query_screen, 1)
        video_layout.addWidget(self.match_screen, 1)

        main_layout.addLayout(video_layout)

        self.controls = Controls()
        main_layout.addStretch(1) 
        
        main_layout.addWidget(self.controls)
        # connect signals to the corresponding slots of video players
        self.controls.play_signal.connect(self.query_screen.play)
        self.controls.pause_signal.connect(self.query_screen.pause)
        self.controls.reset_signal.connect(self.query_screen.reset)
        self.controls.upload_video_signal.connect(self.upload_video)
        
    def handle_media_status_change(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.controls.play_button.setEnabled(True)
            self.controls.pause_button.setEnabled(True)
            self.controls.reset_button.setEnabled(True)
        elif status in [QMediaPlayer.NoMedia, QMediaPlayer.EndOfMedia]:
            self.controls.play_button.setEnabled(False)
            self.controls.pause_button.setEnabled(False)
            self.controls.reset_button.setEnabled(False)
            
    def upload_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4)")
        if file_name:
            self.query_screen.load_video(file_name)
            self.match_screen.load_video(file_name)
            self.query_screen.play()  # Automatically play the video after loading 
        
def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
