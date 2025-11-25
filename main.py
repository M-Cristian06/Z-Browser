import sys

# PyQt6 GUI components
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QToolBar, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QUrl, QSize

# Browser engine
from PyQt6.QtWebEngineWidgets import QWebEngineView


# MainBrowserWindow
class BrowserMainWindow(QMainWindow):
    def __init__(self):
        """ Initilizes the entire UI and sets up the main components """    
        super().__init__()
        self.setWindowTitle("Z-Net Browser V0.0.1")
        self.resize(QSize(1280, 720))
        self.setWindowIcon(QIcon("src/media/icon.png"))
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.browser_engine()
        self.create_tool_bar()
        self.browser.urlChanged.connect(self.update_url_bar)
# BrowserEngineSetup: Creates and configures the QWebEngineView instance
    def browser_engine(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        self.browser.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.setCentralWidget(self.browser)
    def create_tool_bar(self):
        """ Creates the top toolbar with url bar """
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        #Address bar 
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_from_url_bar)
        toolbar.addWidget(self.url_bar)

    def load_from_url_bar(self):
        """Loads the page typed into the address bar. """
        url_text = self.url_bar.text()
        if not url_text.startswith("http"):
            url_text = "https://" + url_text
        self.browser.setUrl(QUrl(url_text))

    def update_url_bar(self, url):
        """ Updates the address bar when navigation changes """
        self.url_bar.setText(url.toString())
                




app = QApplication(sys.argv)
try:
    with open("src/themes/style.qss", "r") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    print("Style file not found")
    
window = BrowserMainWindow()
window.show()
app.exec()

