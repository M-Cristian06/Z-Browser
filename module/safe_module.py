import sys
#PyQt6 Import 
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QUrl


class SafeWebPage(QWebEnginePage):
    def featurePermissionRequested(self, url, feature):
        if feature.name == 'Notifications' or feature.name == 'Camera' or feature.name == 'Microphone':
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.Deny)
        reply = QMessageBox.question(
        None, 
        "Permission Storage",
        f"Site {url.host()} wants access to LocalStorage. \n Do You want do give access?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
        if reply == QMessageBox.StandardButton.Yes:
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.Grant)
        else:
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.Deny)