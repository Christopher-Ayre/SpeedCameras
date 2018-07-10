class CameraController:

    def __init__( self, ui, camFetcher, factory ):
        self.ui = ui
        self.camFetcher = camFetcher
        self.factory = factory
        self.locations = None
        self.cameras = []


    def run( self ):
    #TESTING
        self.loadCamLocations()
        self.buildCameras()



    #Load or reload camera locations
    def loadCamLocations( self ):

        #TODO: also get cameras that arn't stored in pdf. i.e. Fixed and RedLight 
        self.locations = self.camFetcher.getLocations()


    def buildCameras( self ):
        if self.locations:
            for cam in self.locations:
                cam = self.factory.makeCamera( cam[0], cam[1] )

                #Not null
                if cam:
                    self.cameras.append( cam )