#main.py

import sys

# PyQt6 GUI components
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QUrl

# Browser engine
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile


# Modules import 
from module.tabs_module import tab # Tabs module import

# MainBrowserWindow
class BrowserMainWindow(QMainWindow):
    def __init__(self):
        """ Initilizes the entire UI and sets up the main components """    
        super().__init__()
        self.setWindowTitle("Z-Net Browser V0.0.2")
        self.resize(QSize(1280, 720))
        self.setWindowIcon(QIcon("src/media/icon.png"))
        self.tab = tab()
        self.setCentralWidget(self.tab)
        self.create_tool_bar()
        self.tab.currentChanged.connect(self.on_tab_changed)
        self.on_tab_changed(self.tab.currentIndex())
    

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
        current_browser = self.tab.currentWidgetBrowser()
        if current_browser:
            current_browser.setUrl(QUrl(url_text))

    def update_url_bar(self, url):
        """ Updates the address bar when navigation changes """
        self.url_bar.setText(url.toString())
                
    def on_tab_changed(self, index):
        browser = self.tab.currentWidgetBrowser()
        if browser:
            try:
                browser.urlChanged.disconnect()
            except TypeError:
                pass
            browser.urlChanged.connect(self.update_url_bar)
            self.update_url_bar(browser.url())


app = QApplication(sys.argv)

#load/read style file 
try:
    with open("src/themes/style.qss", "r") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    print("Style file not found")
    
window = BrowserMainWindow()
window.show()
app.exec()