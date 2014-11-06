import Tkinter as tk
import os

root = tk.Tk()
root.title("Gaussian Curve Fitting")
root.geometry("768x600")

welcome = tk.Label(root, text='This program fit Gaussian distribution on chi plot data and return the height of peak found.')
welcome.pack()

def getFilePath(filePath):
    if os.path.isfile(filePath):
        return filePath
    elif not os.path.exists(filePath):
        return '0' # the file path does not exist
    elif os.path.isdir(filePath):
        return '1' # is a directory
    
    
fileinfo = tk.Label(root, text='Input file path:')
filepath = tk.Entry(root)

fileinfo.pack()
filepath.pack()

def showentry(event):
    file_path = filepath.get()
    checkpath = getFilePath(file_path)
    rightPath = False
    if checkpath == '0':
        print 'The file path does not exist. Please enter again'
    elif checkpath == '1':
        print 'Directory found. Please continue with input.'
    else:
        print 'file found: ' + file_path
  
filepath.bind('<Return>', showentry)
# invoke event loop
root.mainloop()
