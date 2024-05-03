import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog, QSpacerItem, QSizePolicy, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QFont
import find_frame
import audiofingerprint
import find_similar_video
import datetime

# utility conversion function
def format_time_hh_mm_ss_ms(ms):
    # divmod is division and modulus haha cool little function here -> returns tuple (result of division, remainder of division)
    seconds, milliseconds = divmod(ms, 1000)
    if milliseconds >= 500:
        seconds += 1  # Round up if milliseconds are 500 or more
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# remove the _modifiedmp4
def sanitize_name(full_path):
    base_name = os.path.basename(full_path) # extract file name from full path
    pos = base_name.find('_modified') # remove _modified portion
    if pos != -1:
        return base_name[:pos].capitalize()  # return everything before "_modified"
    return base_name.capitalize()

class Controls(QWidget):
    play_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    reset_signal = pyqtSignal()
    upload_video_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.create_layout()

    def create_layout(self):
        # overall layout container
        main_layout = QVBoxLayout(self)  

        # upload button at the top-right
        self.upload_button = QPushButton('Upload', self)
        self.upload_button.setFixedSize(90, 35) 
        upload_layout = QHBoxLayout()
        upload_layout.addStretch()  # add stretch to push the button to the right
        upload_layout.addWidget(self.upload_button)
        upload_layout.setContentsMargins(0, 0, 0, 0)  # 0 margin default
        upload_layout.setSpacing(0)
        # add upload layout to the main layout
        main_layout.addLayout(upload_layout)

        # provide padding below the upload button if needed
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
    def __init__(self, screen_type):
        super().__init__()
        self.screen_type = screen_type  
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self)
        font = QFont("Segoe UI", 12)
        # initialize label for displaying text
        self.label = QLabel(self.screen_type, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel { color: white; background-color: black; }")
        self.label.resize(self.size())
        self.label.raise_()
        self.label.show()
        self.setStyleSheet("background-color: black;")

    def set_message(self, message):
        self.label.setText(message)
        self.label.update() 
        self.label.show()
        
    def load_video(self, url):
        # /home/super-rogatory/simplevideomatcher/Queries/video5_1_modified.mp4 Example <- Fine
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        self.label.show()
        
    def play(self):
        self.label.hide()
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
        self.label.resize(self.size())
            
    def play_from_frame(self, frame_index):
        # calculate frame position in milliseconds
        frame_time_ms = int((frame_index / 30) * 1000)  # 30 fps
        self.media_player.setPosition(frame_time_ms)
        self.media_player.play()
        self.label.hide()
    
    def play_from_start(self):
        # calculate frame position in milliseconds
        self.media_player.setPosition(0)
        self.media_player.play()
        self.label.hide()
        
        
        
# worker is a unit of work to be put on "background" thread - processing allows execution without "Not responding..." hangup
class Worker(QObject):
    finished = pyqtSignal(int, float)  
    error = pyqtSignal(str)

    def __init__(self, query_video_path, original_video_path):
        super().__init__()
        self.query_video_path = query_video_path
        self.original_video_path = original_video_path

    def run(self):
        try:
            # clean up temporary files <- from original find_frame.py
            audiofingerprint.remove_temporary_files('original_audio.wav', 'query_audio.wav')
            
            # audio extraction <- from original find_frame.py
            audiofingerprint.extract_audio(self.query_video_path, 'query_audio.wav')
            audiofingerprint.extract_audio(self.original_video_path, 'original_audio.wav')

            # audio fingerprint comparison to find offset <- from original find_frame.py
            offset_seconds = audiofingerprint.find_offset('original_audio.wav', 'query_audio.wav', 10)

            # frame matching based on audio offset
            frame_match_index = find_frame.process_videos(self.original_video_path, self.query_video_path, offset_seconds)
            
            # this emission should get handled by our worker thread to set class attributes
            self.finished.emit(frame_match_index, offset_seconds)

            # clean up temporary files
            audiofingerprint.remove_temporary_files('original_audio.wav', 'query_audio.wav')
        except Exception as e:
            self.error.emit(str(e))
                   
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_interface()
        self.frame_match_index = 0
        self.offset_seconds = 0
        self.videos_ready = False  # Tracks if both videos are loaded
        self.query_video_name = ""
        
    def initialize_interface(self):
        # interface work - nothing notable here creating UI, screens, screen size, adding controls, connecting controls to handlers
        self.setWindowTitle("Video Matcher")
        screen = QApplication.primaryScreen().geometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addStretch(1) 
        
        video_layout = QHBoxLayout()
        self.query_screen = VideoPlayer("Query")
        self.match_screen = VideoPlayer("Match")
        
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
        self.controls.play_signal.connect(self.match_screen.play)
        self.controls.pause_signal.connect(self.match_screen.pause)
        self.controls.reset_signal.connect(self.match_screen.reset)
        self.controls.upload_video_signal.connect(self.upload_video)
                
    def handle_media_status_change(self, status):
        # check if both videos are loaded
        if (self.query_screen.media_player.mediaStatus() == QMediaPlayer.LoadedMedia and
            self.match_screen.media_player.mediaStatus() == QMediaPlayer.LoadedMedia):
            self.videos_ready = True
        else:
            self.videos_ready = False

    def upload_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4)")
        if file_name:
            # disable controls immediately after a file is selected
            self.controls.play_button.setEnabled(False)
            self.controls.pause_button.setEnabled(False)
            self.controls.reset_button.setEnabled(False)

            original_video_filename = find_similar_video.find_similar_video(file_name, './preprocessing.json')
            self.query_video_name = sanitize_name(file_name) # setup query video name - OUTPUT VARIABLE
            original_video_path = os.path.join(os.path.abspath("video/"), original_video_filename)

            self.query_screen.load_video(file_name)
            self.match_screen.load_video(original_video_path)

            # set "Looking for a match..." message
            self.query_screen.set_message("Looking for a match...")
            self.match_screen.set_message("Looking for a match...")
            self.videos_ready = False
            
            # setup the thread and worker
            self.thread = QThread()
            self.worker = Worker(file_name, original_video_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_processing_finished)
            self.worker.error.connect(self.handle_error)

            # cleanup and thread management
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

    def on_processing_finished(self, frame_match_index, offset_seconds):
        # emits captured on complete of processing, keep an eye out for emits shot by Worker class
        self.frame_match_index = frame_match_index # setup frame match index - also works as an OUTPUT VARIABLE
        self.offset_seconds = offset_seconds # capture offset seconds, works as an OUTPUT VARIABLE 
        if self.videos_ready:
            # Enable buttons only after both videos are loaded and processing is complete
            self.update_info_display()
            self.controls.play_button.setEnabled(True)
            self.controls.pause_button.setEnabled(True)
            self.controls.reset_button.setEnabled(True)
        QTimer.singleShot(1000, self.start_videos)

    def update_info_display(self):
        # convert times to readable format
        offset_ms = self.offset_seconds * 1000
        offset_time_str = format_time_hh_mm_ss_ms(offset_ms)
        duration_ms = self.query_screen.media_player.duration()  # <- already in ms
        duration_str = format_time_hh_mm_ss_ms(duration_ms)
        
        info_text = (f"RESULTS\n-------------------------------------------! \nFile: {self.query_video_name} | Start Time: {offset_time_str} | "
                     f"Duration: {duration_str} | Frame Index: {self.frame_match_index}\n-------------------------------------------")
        print(info_text)
        
    def handle_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def start_videos(self):
        # Assuming we now have frame_match_index properly set
        self.query_screen.play_from_start()
        self.match_screen.play_from_frame(self.frame_match_index)      
     
def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
