#!/usr/bin/env python

import urllib
import requests
import re
import time
import datetime
import os
from bs4 import BeautifulSoup
from pyPdf import PdfFileReader
from tabula import read_pdf


# Constants
url = "http://www.police.wa.gov.au/Traffic/Cameras/Camera-locations"
fileName = "locations.pdf"

# Need to convert names to upper to match table format
weekDay = time.strftime( "%A" )
date = time.strftime( "%d" )
monthName = time.strftime( "%B" )
year = time.strftime( "%Y" )

# The same format the dates are in the PDF
currentDate = weekDay.upper() + " " + date + " " + monthName.upper() + " " + year


def readMyLocations( inFile ):

    # Read file into memory then close it
    print "Reading in your locations\n"
    fp = open( inFile )
    fullFile = fp.read()
    fp.close()

    # Seperate the rows into a list and return it
    mySuburbs = fullFile.split( '\n' )
    # Remove the last empty element that comes from the last \n
    mySuburbs.pop()

    print "Your Locations: "
    print mySuburbs, "\n"

    return mySuburbs


# Find newest pdf
def findCurrentPDF():

    print "Finding PDF for current time period"

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

    print "PDF Found!\n"

    return pdfLink


# Download pdf
def downloadPDF( url ):

    print "Downloading PDF"
    urllib.urlretrieve( url, fileName )
    print "Download Complete!\n"


# Delete any temp files
def cleanUp():
    os.remove( fileName )

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

def displayLocations( locations ):
# Print all elements in tuple formatted as:
#
# Suburb
# [ Street Name ]
#
    # First test if there is any values in locations
    if not locations:
        print "No spped cameras relevent to you, your safe!\n"
    else:
        for a, b in locations:
            print a
            print "[ " + b + " ]\n"


def main():

    print "\n"

    downloadPDF( findCurrentPDF() )

    myLocations = readMyLocations( "mySuburbs.txt" )

    locations = findReleventLocations( myLocations )

    displayLocations( locations )

    cleanUp()


if __name__ == '__main__':
    main()
