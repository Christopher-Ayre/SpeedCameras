from time import gmtime, strftime

class UI:

    def log( self, object, message ):
        print( self.getTime() + " : " + self.getObjectName( object ) + " : " + message )


    def getTime(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def getObjectName( self, object ):
        return object.__class__.__name__