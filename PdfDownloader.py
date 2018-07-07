#TODO: 
# Change from finding relevent cameras to just formatting all cameras into a tuple of strings
# Change all output to logging


import urllib.request
import requests
import re
import time
import datetime
import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from tabula import read_pdf

class PdfDownloader:

    def __init__( self, ui ):

        self.url = "http://www.police.wa.gov.au/Traffic/Cameras/Camera-locations"
        self.fileName = "locations.pdf"

        # Need to convert names to upper to match table format
        weekDay = time.strftime( "%A" )
        date = time.strftime( "%d" )
        monthName = time.strftime( "%B" )
        year = time.strftime( "%Y" )

        # The same format the dates are in the PDF
        self.currentDate = weekDay.upper() + " " + date + " " + monthName.upper() + " " + year
        
        #Used for logging
        self.ui = ui

    def returnLocations(self):

        self.downloadPDF( self.findCurrentPDF() )

        self.locations = self.findAllLocations()

        self.cleanUp( self.fileName, self.locations )

        return self.locations

    def findCurrentPDF(self):

        self.ui.log( self, "Finding PDF for current time period" )

        # Find today
        today = datetime.date.today()

        # Find the start of the week, this is how they identify their camera pdfs
        startOfWeek = today - datetime.timedelta( days = today.weekday() )

        startOfWeekString = startOfWeek.strftime('%d%m%Y')

        sourceCode = requests.get( self.url )
        sourceCode = sourceCode.text
        htmlCode = BeautifulSoup( sourceCode, 'html.parser' )

        # Get a list of all the media links
        linkList = htmlCode.select( "a[href*=media]" ) #.get( "href" )

        # Iterate through list and find this weeks link
        for i in linkList:
            if startOfWeekString in i.get("href"):
                firstLink = i.get("href")

        # Concatenate strings to get final link url
        pdfLink = "http://www.police.wa.gov.au" + firstLink

        self.ui.log( self, "PDF Found!" )

        return pdfLink


    def downloadPDF( self, url ):

        self.ui.log( self, "Downloading PDF" )

        urllib.request.urlretrieve( url, self.fileName )

        self.ui.log( self, "Download Complete!" )



    # Parse PDF
    def findAllLocations(self):
        # Consider what to do near midnight

        self.ui.log( self, "Finding all today's cameras" )

        table = read_pdf( self.fileName, multiple_tables = True, pages = "all" )

        locationTable = "Error!"

        # Loop through table and find the one corresponding to todays date
        for ii in table:
            if ii[0][0] == self.currentDate:
                locationTable = ii

        self.ui.log( self, "All cameras found!" )

        self.ui.log( self, "Parsing tables" )

        suburbsOne = locationTable[1]
        suburbsTwo = locationTable[3]
        streetsOne = locationTable[0]
        streetsTwo = locationTable[2]

        print( suburbsOne + "\n\n" )
        print( suburbsTwo + "\n\n" )
        print( streetsOne + "\n\n" )
        print( streetsTwo + "\n\n" )

        # Empty tuple to hold Suburb and street names
        locations = []

        # Iterate through first list
        # Try to join lists again later
        pos = 0
        for ii in suburbsOne:
            locations.append((ii,streetsOne[pos]))
            pos = pos + 1

        # Iterate through second list
        pos = 0
        for ii in suburbsTwo:
            locations.append((ii,streetsTwo[pos]))
            pos = pos + 1

        print( locations )
        return locations

    # Delete any temp files
    def cleanUp(self, fileName, locations ):

        self.ui.log( self, "Removed file: " + fileName )

        for ii in locations:
            if (ii[0] != ii[0]) or ( ii == ('Suburb', 'Street Name') ):
                print( ii[0])
                locations.remove(ii)

        os.remove( fileName )
