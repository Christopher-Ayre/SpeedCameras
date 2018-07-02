#TODO: 
# Change from finding relevent cameras to just formatting all cameras into a tuple of strings
# Change all output to logging


import time
import datetime
import os
from bs4 import BeautifulSoup
from pyPdf import PdfFileReader
from tabula import read_pdf

class PdfDownloader:

    def __init__( self ):

        self.url = "http://www.police.wa.gov.au/Traffic/Cameras/Camera-locations"
        self.fileName = "locations.pdf"

        # Need to convert names to upper to match table format
        weekDay = time.strftime( "%A" )
        date = time.strftime( "%d" )
        monthName = time.strftime( "%B" )
        year = time.strftime( "%Y" )

        # The same format the dates are in the PDF
        self.currentDate = weekDay.upper() + " " + date + " " + monthName.upper() + " " + year

    def returnLoacations(self):

        downloadPDF( findCurrentPDF() )


        locations = findReleventLocations( myLocations )

        displayLocations( locations )

        cleanUp()

    def findCurrentPDF(self):

        # Find today
        today = datetime.date.today()

        # Find the start of the week, this is how they identify their camera pdfs
        startOfWeek = today - datetime.timedelta( days = today.weekday() )

        startOfWeekString = startOfWeek.strftime('%d%m%Y')

        sourceCode = requests.get( url )
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

        return pdfLink


    def downloadPDF( self, url ):

        print "Downloading PDF"
        urllib.urlretrieve( url, fileName )
        print "Download Complete!\n"



    # Parse PDF
    def findReleventTable(self):
        # Consider what to do near midnight

        print "Finding all today's cameras\n"
        table = read_pdf( fileName, multiple_tables = True, pages = "all" )

        locations = "Error!"

        # Loop through table and find the one corresponding to todays date
        for ii in table:
            if ii[0][0] == currentDate:
                locations = ii

        # Newlines to remove errors from view
        print "\n" * 50
        print "All cameras found!\n"

        return locations

    # Delete any temp files
    def cleanUp(self):
        os.remove( fileName )