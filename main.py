
import urllib
import requests
import re
from bs4 import BeautifulSoup

# Global for now, will we need more than one file?
url = "http://www.police.wa.gov.au/Traffic/Cameras/Camera-locations"
fileName = "locations.pdf"


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

    print "PDF Found!"

    return pdfLink


# Download pdf
def downloadPDF( url ):

    print "Downloading PDF"
    urllib.urlretrieve( url, fileName )
    print "Download Complete!"


# Parse PDF



# Find loactions near me ( possible user input )
# Display relevent speed cameras

downloadPDF( findCurrentPDF() )
