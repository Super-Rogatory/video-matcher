from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl

class VideoPlayer(QVideoWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer(None)
        self.video_widget = QVideoWidget()

    def load_video(self, url):
        self.media_player.setSource(QUrl.fromLocalFile(url))
        self.media_player.setVideoOutput(self.video_widget)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    # def reset(self):
    #     self.player.setPosition(0)  # Reset to the start
    #     self.player.pause()


# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider
# from PyQt6.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt6.QtMultimediaWidgets import QVideoWidget
# from PyQt6.QtCore import QUrl, Qt


# class VideoPlayer(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Video Player")
#         self.setGeometry(100, 100, 1024, 768)

#         self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
#         self.video_widget = QVideoWidget()

#         self.start_button = QPushButton("Start")
#         self.start_button.clicked.connect(self.start_video)

#         self.pause_button = QPushButton("Pause")
#         self.pause_button.clicked.connect(self.pause_video)

#         self.stop_button = QPushButton("Stop")
#         self.stop_button.clicked.connect(self.stop_video)

#         self.slider = QSlider(Qt.Orientation.Horizontal)
#         self.slider.sliderMoved.connect(self.set_position)

#         self.media_player.setVideoOutput(self.video_widget)
#         self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("Video.mp4")))
#         self.media_player.positionChanged.connect(self.position_changed)
#         self.media_player.durationChanged.connect(self.duration_changed)

#         layout = QVBoxLayout()
#         layout.addWidget(self.video_widget)
#         layout.addWidget(self.start_button)
#         layout.addWidget(self.pause_button)
#         layout.addWidget(self.stop_button)
#         layout.addWidget(self.slider)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#     def start_video(self):
#         self.media_player.play()

#     def pause_video(self):
#         self.media_player.pause()

#     def stop_video(self):
#         self.media_player.stop()

#     def set_position(self, position):
#         self.media_player.setPosition(position)

#     def position_changed(self, position):
#         self.slider.setValue(position)

#     def duration_changed(self, duration):
#         self.slider.setRange(0, duration)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     video_player = VideoPlayer()
#     video_player.show()
#     sys.exit(app.exec())
