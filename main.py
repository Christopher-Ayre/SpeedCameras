import urllib
import requests
import re
import time
from bs4 import BeautifulSoup
from pyPdf import PdfFileReader
from tabula import read_pdf

# Constants
url = "http://www.police.wa.gov.au/Traffic/Cameras/Camera-locations"
fileName = "locations.pdf"

# Need to convert names to upper to match table format
weekDay = ( time.strftime( "%A" ).upper() )
date = time.strftime( "%d" )
monthName = ( time.strftime( "%B" ).upper() )
year = time.strftime( "%Y" )

# The same format the dates are in the PDF
currentDate = weekDay + " " + date + " " + monthName + " " + year


# Find newest pdf
def findCurrentPDF():

    print "Finding PDF for current time period"

    # First PDF link appears to be the latest, potentially upgrade later.

    sourceCode = requests.get( url )
    sourceCode = sourceCode.text
    htmlCode = BeautifulSoup( sourceCode, 'html.parser' )

    # Select the first link that has "media" in the url, get that links url
    firstLink = htmlCode.select_one( "a[href*=media]" ).get( "href" )

    # Concatenate strings to get final link url
    pdfLink = "http://www.police.wa.gov.au" + firstLink

    print "PDF Found!\n"

    return pdfLink


# Download pdf
def downloadPDF( url ):

    # TODO: 
    # Change file name/path
    # Delete file after use

    print "Downloading PDF"
    urllib.urlretrieve( url, fileName )
    print "Download Complete!\n"


# Parse PDF
def findReleventTable():
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
        


# Find loactions near me ( possible file input? )
def findReleventLocations( releventSuburbs ):
    # Grab the table that corresponds with today
    table = findReleventTable()

    # TODO: Romove next line after development
    #print table

    suburbsOne = table[1]
    suburbsTwo = table[3]
    streetsOne = table[0]
    streetsTwo = table[2]

    # Empty tuple to hold Suburb and street names
    locations = []

    # Iterate through first list
    # Try to join lists again later
    pos = 0
    for ii in suburbsOne: 
        if ii in releventSuburbs:
            locations.append((ii,streetsOne[pos]))
        pos = pos + 1

    # Iterate through second list
    pos = 0
    for ii in suburbsTwo: 
        if ii in releventSuburbs:
            locations.append((ii,streetsTwo[pos]))
        pos = pos + 1


    return locations




# Display relevent speed cameras


print "\n"

downloadPDF( findCurrentPDF() )

myLocations = ['Maddington','Kenwick','Bentley']

locations = findReleventLocations( myLocations )

# Print all elements in tuple formatted as:
#
# Suburb
# [ Street Name ]
#

for a, b in locations:
    print a
    print "[ " + b + " ]\n"
