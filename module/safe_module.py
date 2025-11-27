
#PyQt6 Import 
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWebEngineCore import QWebEnginePage


class SafeWebPage(QWebEnginePage):
    def featurePermissionRequested(self, url, feature):
       if feature in (
            QWebEnginePage.Feature.Notifications,
            QWebEnginePage.Feature.MediaAudioCapture,
            QWebEnginePage.Feature.MediaVideoCapture     
        ):
            self.setFeaturePermission(
                url, 
                feature, 
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser
            )
    