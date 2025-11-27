#module/tab_module.py

# PyQt6 GUI components
from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QTabBar
from PyQt6.QtCore import QUrl

# Browser engine
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

# Modules Import 
from module.safe_module import SafeWebPage # Safe page module import 


class tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.profile = QWebEngineProfile("PersistentProfile")
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.tabs()
    def tabs(self, url="https://www.google.com"):
        add_tab_bar_widget = QWidget()
        self.addTab(add_tab_bar_widget, "+")
        self.tabBar().setTabButton(0, QTabBar.ButtonPosition.LeftSide, None)
        self.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.tabCloseRequested.connect(self.close_tab)
        first_tab_widget = QWidget()
        layout = QVBoxLayout()
        first_tab_widget.setLayout(layout)
        first_tab_browser = QWebEngineView()
        first_tab_browser.setPage(SafeWebPage(self.profile, parent=first_tab_browser))
        first_tab_browser.load(QUrl(url))
        layout.addWidget(first_tab_browser)
        self.addTab(first_tab_widget, "New Tab")
        self.currentChanged.connect(self.add_tabs)
        first_tab_browser.titleChanged.connect(lambda title: self.setTabText(self.indexOf(first_tab_widget), title))
     

    def add_tabs(self, index, url="https://www.google.com"):

        new_tab_widget = QWidget()
        layout = QVBoxLayout()
        new_tab_widget.setLayout(layout)
        new_browser = QWebEngineView()
        
        new_browser.setPage(SafeWebPage(self.profile, parent=new_browser))  
        new_browser.load(QUrl(url))
        layout.addWidget(new_browser)
        if index == 0:
            self.addTab(new_tab_widget, "New Tab")
            self.setCurrentIndex(self.count() - 1)
        new_browser.titleChanged.connect(lambda title, tab_index=self.indexOf(new_tab_widget): self.setTabText(tab_index, title))
   
        
    def currentWidgetBrowser(self):
        widget = self.currentWidget()
        if widget and widget.layout():
            for i in range(widget.layout().count()):
                item = widget.layout().itemAt(i).widget()
                if isinstance(item, QWebEngineView):
                    return item
        return None
 
        
    def closeEvent(self, event):
        for i in range(self.count()):
            widget = self.widget(i)
            if widget and widget.layout():
                for j in range(widget.layout().count()):
                    item = widget.layout().itemAt(j).widget()
                    if isinstance(item, QWebEngineView):
                        item.page().deleteLater()
                        item.deleteLater()
        event.accept()            
        
    def close_tab(self, index):
        if index == 0: # don't close "+" tab
            return
        
        widget = self.widget(index)
        if widget and widget.layout():
            for i in range(widget.layout().count()):
                item = widget.layout().itemAt(i).widget()
                if isinstance(item, QWebEngineView):
                    item.page().deleteLater()
                    item.deleteLater()
            self.removeTab(index)
        
 