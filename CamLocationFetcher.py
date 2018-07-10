#Used to implement design patterns on the different methods of getting camera locations.

class CamLocationFetcher:

    def __init__( self, pdfDown ):
        self.pdfDown = pdfDown

    def getLocations( self ):

        #TODO: also get cameras that arn't stored in pdf. i.e. Fixed and RedLight 
        locations = self.pdfDown.returnLocations()

        return locations