from RedLightCamera import RedLightCamera
from FixedCamera import FixedCamera
from VariableCamera import VariableCamera

class SpeedCameraFactory:

    

    def makeCamera( self, suburb, location ):

        #If the string contains " and " or " & " then it is a Red Light Camera
        #If the string ends with " #F" then it is a Fixed Camera
        #Otherwise it is a variable camera


        if ( 'Suburb' not in suburb ):

            if " and " in location or " & " in location:

                #Couldn't get a regex to split at both
                streets = location.split( " and " )

                if len( streets ) < 2:
                    streets = location.split( " & " )

                return RedLightCamera( suburb, streets[0], streets[1] )

            elif " #F" in location:

                #remove added ending
                location = location[:-3]

                return FixedCamera( suburb, location )
            else:
                
                return VariableCamera( suburb, location )

        return None