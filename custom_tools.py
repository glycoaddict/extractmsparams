import re
import tkinter as tk
from tkinter import filedialog as fd
import os



def checkcolumnsandreplace(df):
    # input is a dataframe
    print('checkcolumns, columns = ', df.columns)
    if any(re.match(item, '\r\n') for item in df.columns):
        print('\\r\\n newline detected')
        print('cleaning the columns')
        df.columns = standardizenewline(df.columns)
        return df
    else:
        return df

def standardizenewline(slist):
    newlist = []
    for s in slist:
        newlist.append(str(s).replace('\r\n','\n'))
    return newlist



def opendir(s):
    import subprocess
    s = '\"' + os.path.abspath(s) + '\"'
    s.replace("/", '\"')
    subprocess.Popen('explorer ' + s)


def openfile(t):
    os.startfile(t)


def getfiles(title='Choose files', filetype='.csv'):
    root = tk.Tk()
    root.lift()
    f = fd.askopenfilenames(parent=root, title=title, filetypes=[('',filetype)])
    root.destroy()
    return f


def getfile(title='Choose files', sformat='.csv'):  
    
    
    
    root = tk.Tk()
    root.lift()    
    
    try:
        f = fd.askopenfilename(parent=root, title=title, filetypes=[('', sformat)])
        root.withdraw()
        return f
    except:
        print('error - no file exists')
        return ''
    
    


def getsavefile(title='Choose files', sformat='.csv', initialfile=''):
    root = tk.Tk()
    root.lift()
    try:        
        f = fd.asksaveasfilename(parent=root,
                                  title=title,
                                  filetypes=[('', sformat)],
                                 initialfile=initialfile)
        if len(f)<1:
            root.withdraw()
            root.destroy()
            return ''
        f = os.path.splitext(f)[0] + sformat
        print('file to save as =' , f)
        root.withdraw()
        return f
    except:
        print(title + ': error - no filename chosen')
        return ''
    
    

def getfolder(title='Choose output folder'):
    root = tk.Tk()    
    root.lift()
    try:
        f = fd.askdirectory(title=title)
        root.withdraw()
    except:
        print(title + ': error - no file exists')
        root.withdraw()
        root.destroy()
        return ''
    f = f.replace('/','\\')
    root.destroy()
    return f



class singleinputbox:    
    def __init__(self, text='enter value:', default='0'):
        
        self.root = tk.Tk()
        self.root.configure(background='red')        
        self.root.focus_set()        
        self.text = text
        self.value = ''        
        (self.root).protocol("WM_DELETE_WINDOW", self.on_closing)      
        
        

        tk.Label(self.root, text=text).grid(row=0, column=0)        

        self.e = tk.Entry(self.root)
        self.e.grid(row=0, column=1)        
        self.e.insert(0, default)
        self.e.selection_range(0, 100)
        self.e.focus_set()        
        self.root.attributes("-topmost",True)
        self.root.lift()       

        self.button = tk.Button(self.root, text='Submit', command=self.submit)
#        self.button.configure(background='blue', foreground='blue')
        self.button.grid(row=1)        

        self.root.mainloop()
        

    def submit(self):    
        if len(self.e.get())>0:
            self.value = self.e.get()        
            self.root.withdraw()
#            self.root.destroy()           
            self.root.quit()           
        
        
    def on_closing(self):
        from tkinter import messagebox
        if messagebox.askokcancel("Quit", "Quit and apply current values?"):
            self.submit()
    
    def value(self):
        return self.value        


def get_script_path():
    import sys
    return os.path.dirname(os.path.realpath(sys.argv[0]))

   
def cnames():
    return {
            'aliceblue': '#F0F8FF',
            'antiquewhite': '#FAEBD7',
            'aqua': '#00FFFF',
            'aquamarine': '#7FFFD4',
            'azure': '#F0FFFF',
            'beige': '#F5F5DC',
            'bisque': '#FFE4C4',
            'black': '#000000',
            'blanchedalmond': '#FFEBCD',
            'blue': '#0000FF',
            'blueviolet': '#8A2BE2',
            'brown': '#A52A2A',
            'burlywood': '#DEB887',
            'cadetblue': '#5F9EA0',
            'chartreuse': '#7FFF00',
            'chocolate': '#D2691E',
            'coral': '#FF7F50',
            'cornflowerblue': '#6495ED',
            'cornsilk': '#FFF8DC',
            'crimson': '#DC143C',
            'cyan': '#00FFFF',
            'darkblue': '#00008B',
            'darkcyan': '#008B8B',
            'darkgoldenrod': '#B8860B',
            'darkgray': '#A9A9A9',
            'darkgreen': '#006400',
            'darkkhaki': '#BDB76B',
            'darkmagenta': '#8B008B',
            'darkolivegreen': '#556B2F',
            'darkorange': '#FF8C00',
            'darkorchid': '#9932CC',
            'darkred': '#8B0000',
            'darksalmon': '#E9967A',
            'darkseagreen': '#8FBC8F',
            'darkslateblue': '#483D8B',
            'darkslategray': '#2F4F4F',
            'darkturquoise': '#00CED1',
            'darkviolet': '#9400D3',
            'deeppink': '#FF1493',
            'deepskyblue': '#00BFFF',
            'dimgray': '#696969',
            'dodgerblue': '#1E90FF',
            'firebrick': '#B22222',
            'floralwhite': '#FFFAF0',
            'forestgreen': '#228B22',
            'fuchsia': '#FF00FF',
            'gainsboro': '#DCDCDC',
            'ghostwhite': '#F8F8FF',
            'gold': '#FFD700',
            'goldenrod': '#DAA520',
            'gray': '#808080',
            'green': '#008000',
            'greenyellow': '#ADFF2F',
            'honeydew': '#F0FFF0',
            'hotpink': '#FF69B4',
            'indianred': '#CD5C5C',
            'indigo': '#4B0082',
            'ivory': '#FFFFF0',
            'khaki': '#F0E68C',
            'lavender': '#E6E6FA',
            'lavenderblush': '#FFF0F5',
            'lawngreen': '#7CFC00',
            'lemonchiffon': '#FFFACD',
            'lightblue': '#ADD8E6',
            'lightcoral': '#F08080',
            'lightcyan': '#E0FFFF',
            'lightgoldenrodyellow': '#FAFAD2',
            'lightgreen': '#90EE90',
            'lightgray': '#D3D3D3',
            'lightpink': '#FFB6C1',
            'lightsalmon': '#FFA07A',
            'lightseagreen': '#20B2AA',
            'lightskyblue': '#87CEFA',
            'lightslategray': '#778899',
            'lightsteelblue': '#B0C4DE',
            'lightyellow': '#FFFFE0',
            'lime': '#00FF00',
            'limegreen': '#32CD32',
            'linen': '#FAF0E6',
            'magenta': '#FF00FF',
            'maroon': '#800000',
            'mediumaquamarine': '#66CDAA',
            'mediumblue': '#0000CD',
            'mediumorchid': '#BA55D3',
            'mediumpurple': '#9370DB',
            'mediumseagreen': '#3CB371',
            'mediumslateblue': '#7B68EE',
            'mediumspringgreen': '#00FA9A',
            'mediumturquoise': '#48D1CC',
            'mediumvioletred': '#C71585',
            'midnightblue': '#191970',
            'mintcream': '#F5FFFA',
            'mistyrose': '#FFE4E1',
            'moccasin': '#FFE4B5',
            'navajowhite': '#FFDEAD',
            'navy': '#000080',
            'oldlace': '#FDF5E6',
            'olive': '#808000',
            'olivedrab': '#6B8E23',
            'orange': '#FFA500',
            'orangered': '#FF4500',
            'orchid': '#DA70D6',
            'palegoldenrod': '#EEE8AA',
            'palegreen': '#98FB98',
            'paleturquoise': '#AFEEEE',
            'palevioletred': '#DB7093',
            'papayawhip': '#FFEFD5',
            'peachpuff': '#FFDAB9',
            'peru': '#CD853F',
            'pink': '#FFC0CB',
            'plum': '#DDA0DD',
            'powderblue': '#B0E0E6',
            'purple': '#800080',
            'red': '#FF0000',
            'rosybrown': '#BC8F8F',
            'royalblue': '#4169E1',
            'saddlebrown': '#8B4513',
            'salmon': '#FA8072',
            'sandybrown': '#FAA460',
            'seagreen': '#2E8B57',
            'seashell': '#FFF5EE',
            'sienna': '#A0522D',
            'silver': '#C0C0C0',
            'skyblue': '#87CEEB',
            'slateblue': '#6A5ACD',
            'slategray': '#708090',
            'snow': '#FFFAFA',
            'springgreen': '#00FF7F',
            'steelblue': '#4682B4',
            'tan': '#D2B48C',
            'teal': '#008080',
            'thistle': '#D8BFD8',
            'tomato': '#FF6347',
            'turquoise': '#40E0D0',
            'violet': '#EE82EE',
            'wheat': '#F5DEB3',
            'white': '#FFFFFF',
            'whitesmoke': '#F5F5F5',
            'yellow': '#FFFF00',
            'yellowgreen': '#9ACD32'}
    
    
def islistempty(file_list):    
    if len(file_list) < 1:
        print('Error. list length is zero. no files inputted.')
        return True
    

# This is the file uploader class
class fileup():
    
    
    def __init__(self, textprompt='Please choose file.', filetype='csv'):
        self.filename = ''
        self.filedata = ''  
        self.bytefile=None
        self.filetype=filetype
        print(textprompt)
        self.sidethreadbrowse()
     
    
    def sidethreadbrowse(self):   
        import threading
        import fileupload
        from ipywidgets import widgets
        from IPython.display import display
        
        ## Begin initialisation of buttons
        uploader = fileupload.FileUploadWidget()
        uploader.observe(self._handle_upload, names='data')
        display(uploader)
    
    
    def _handle_upload(self, change):        
        # This creates a new file object in memory and copies
        # the uploaded file onto it.
        w = change['owner']
        with open(w.filename, 'wb') as f:
            f.write(w.data)
            
        # Give feedback on the file uploaded
        # restrict the output to only the first 2^10 characters.
        print('Uploaded `{}` ({:.2f} kB)'.format(
            w.filename, len(w.data) / 2**10)) 
        self.filename=w.filename
        self.readfile(w.data)
                
    
    def readfile(self, data):
        import pandas as pd
        import io
        df=None        
        bytefile = io.BytesIO(data)
        
        if self.filetype == 'csv':
            try:                
                df = pd.read_csv(bytefile)
            except:
                raise ValueError('ERROR, the file "{}" is not a recognised format ({}).'.format(f.filename, f.filetype))
                
        elif self.filetype == 'excel':
            try:                
                df = pd.read_excel(bytefile)
            except:
                raise ValueError('ERROR, the file "{}" is not a recognised format ({}).'.format(f.filename, f.filetype))
        
        self.df = df
        self.bytefile = bytefile
        
        return

    
    
    
def reload(moduletoreload):    
    import importlib
    importlib.reload(moduletoreload)
