from CamLocationFetcher import CamLocationFetcher
from PdfDownloader import PdfDownloader
from SpeedCameraFactory import SpeedCameraFactory
from CameraController import CameraController
from UI import UI


#Dependancy Injection
ui = UI()
downloader = CamLocationFetcher( PdfDownloader( ui ) )
factory = SpeedCameraFactory()
controller = CameraController( ui, downloader, factory )

controller.run()