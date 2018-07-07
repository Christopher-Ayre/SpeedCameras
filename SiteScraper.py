#Used to scrape the WA police website for Fixed and RedLight camera locations

import requests
from bs4 import BeautifulSoup

class SiteScraper:

    def __init__( self, ui ):
        
        self.url = "http://www.police.wa.gov.au/Traffic/Cameras/Camera-locations"
        self.ui = ui

    
    def returnLocations( self ):

        website = self.getSite()
        

    def getSite( self ):

        self.ui.log( self, "Getting Website Code" )

        sourceCode = requests.get( self.url )
        sourceCode = sourceCode.text
        htmlCode = BeautifulSoup( sourceCode, 'html.parser' )

        return htmlCode