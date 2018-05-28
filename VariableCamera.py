class VariableCamera:

    def __init__( self, suburb, street ):
        
        self.suburb = suburb
        self.street = street


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
        str += ", On " + self.street

        return str