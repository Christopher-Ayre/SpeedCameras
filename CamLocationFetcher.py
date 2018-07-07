#Used to implement design patterns on the different methods of getting camera locations.

class CamLocationFetcher:

    def getLocations( self, pdfDown ):

        #TODO: also get cameras that arn't stored in pdf. i.e. Fixed and RedLight 
        locations = pdfDown.returnLocations()

        return locations