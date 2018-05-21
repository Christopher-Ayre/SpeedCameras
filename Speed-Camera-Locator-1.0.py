#!/usr/bin/env python

try:
    #Python2
    from Tkinter import *
except ImportError:
    #Python3
    from tkinter import *

from speedCamera import *

top = Tk()

def updateSuburbs():

    suburbList = E.get().split(',')
    if not suburbList[-1]:
        suburbList.pop()
    
    f = open( 'history', 'w' )

    for i in suburbList:
        f.write( i + "\n" )

    f.close()

# Code to do shit
def findCameras():

    updateSuburbs()

    downloadPDF( findCurrentPDF() )
    
    myLocations = E.get().split(",")

    cameraLocations = findReleventLocations( myLocations )

    # Open acess to the text field
    text.configure( state = 'normal' )
    text.delete(1.0, END)

    if not cameraLocations:
        text.insert( END, "No Relevent Speed Cameras!" )
    else:
        for a, b in cameraLocations:            
            text.insert( END, a + "\n" )
            text.insert( END, "[ " + b + " ]\n\n" )

    # Close acess        
    text.configure( state = 'disabled' )

    cleanUp()

    

def close_window():
    # System.exit() 
    # Mark would be proud
    top.destroy()

def getPrevious():

    previous = ""

    try:
        fp = open( 'history' )
        fullFile = fp.read()
        fp.close()

        # Seperate the rows into a list 
        loist = fullFile.split( '\n' )
        # Remove the last empty element that comes from the last \n
        loist.pop()

        # Concatenate into single string
        for i in loist:
            previous += i + ","
        
    except IOError:
        previous = ""

    return previous
    

# Label 1
label = Label( top, text = "Suburbs:" )
label.grid( row = 0, column = 0 )

# Entry ( 1 Row TextBox )
E = Entry( width = 50 )
E.insert(END, getPrevious() )
E.grid( row=1, column=0, columnspan=8, ipadx=5, ipady=2 )



# Label 2
label2 = Label( top, text = "\nCameras:" )
label2.grid( row = 2, column = 0 )

# TextBox ( MultiLine )
text = Text( top, state = 'disabled' )
text.grid( row = 3, column = 0, columnspan=8 )


# Button one
B = Button( text = "FIND", command = findCameras )
B.grid( row=4, column=0, ipadx=40, ipady=8 )

# Button two
B2 = Button( text = "EXIT", command = close_window )
B2.grid( row=4, column=7, ipadx=40, ipady=8 )



top.resizable( width = False, height = False )
top.title("Speed Camera Locator 1.0")
top.mainloop()
