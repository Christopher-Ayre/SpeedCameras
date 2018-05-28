class RedLightCamera:

    def __init__( self, suburb, streetOne, streetTwo ):
        
        self.suburb = suburb
        self.streetOne = streetOne
        self.streetTwo = streetTwo


    # Check if this camera is in given suburb
    def inSuburb( self, suburb ):
        
        inSuburb = False
        
        # Ignore case when checking, user may have input wrong
        if suburb.lower() == self.suburb.lower():
            inSuburb = True

        return inSuburb

    
    # Give a well formated output string
    def getDisplayString( self ):
        
        str = "Camera in " + self.suburb
        str += ", On the corner of " + self.streetOne + " and " + self.streetTwo

        return str