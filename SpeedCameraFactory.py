class SpeedCameraFactory:


    def makeCamera( self, string ):

        #If the string contains " and " or " & " then it is a Red Light Camera
        #If the string ends with " #F" then it is a Fixed Camera
        #Otherwise it is a variable camera

        if " and " in string or " & " in string:
            print( "RedLightCamera")
        elif " #F" in string:
            print( "FixedCamera" )
        else:
            print( "Variable Camera" )

