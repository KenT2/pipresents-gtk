import os,sys
import configparser
#from pp_utils import Monitor
from pp_displaymanager import DisplayManager
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk

class pp_kbddriver(object):
    
    # printing key ranges of keycode
    # limited to the Extended ASCII ranges which have the code 0-255
    printing_ranges=[[32,126],[128,255]]

    # CLASS VARIABLES  (pp_gpiodriver.)
    driver_active=False
    title=''

    config=None

    def __init__(self):
        self.mon=Monitor()
        self.dm=DisplayManager()

    def init(self,filename,filepath,widget,pp_dir,pp_home,pp_profile,callback=None):

        # instantiate arguments
        self.widget=widget
        self.filename=filename
        self.filepath=filepath
        self.callback=callback
        pp_kbddriver.driver_active = False
        # print filename,filepath
        # read .cfg file.
        reason,message=self._read(self.filename,self.filepath)
        if reason =='error':
            return 'error',message
            
        if self.config.has_section('DRIVER') is False:
            return 'error','No DRIVER section in '+self.filepath
        
        #read information from DRIVER section
        pp_kbddriver.title=self.config.get('DRIVER','title')
        self.bind_printing = self.config.get('DRIVER','bind-printing')

        # and make the keymap
        self.make_keymap()
        
        self.dm.register_kbdriver(self.on_key_pressed)

        pp_kbddriver.driver_active = True
        return 'normal', pp_kbddriver.title + 'Initialised'

    def start (self):
        return

    # allow track plugins (or anyting else) to access analog input values
    def get_input(self,channel):
            return False, None


    def terminate(self):
        pp_kbddriver.driver_active = False
        return

    def is_active(self):
        return pp_kbddriver.driver_active

    def handle_output_event(self,name,param_type,param_values,req_time):
        return 'normal',pp_kbddriver.title+' has no output methods'


    def make_keymap(self):
        # specific keys
        self.specific_key_map=dict()
        for option in self.config.items('keys'):
            condition=option[0]
            condition=condition.replace('<','')
            condition=condition.replace('>','')
            symbolic_name=option[1]
            self.specific_key_map[condition]=symbolic_name
        #print (self.specific_key_map)


    def on_key_pressed(self,keycode,win):
        keyname=Gdk.keyval_name(keycode)
        #print (keyname,keycode)
        #match with specific key
        matched,sname=self.match_specific(keycode)
        if matched:
            #print ('specific',keycode,matched,sname)
            self.callback(sname,pp_kbddriver.title)
            return
        matched,sname=self.match_printing(keycode)
        if matched:
            self.callback(sname,pp_kbddriver.title)
            return            
        
    def match_specific(self,keycode):
        keyname=Gdk.keyval_name(keycode)
        #print ('match',keyname, self.specific_key_map)
        if keyname in self.specific_key_map:
            return True,self.specific_key_map[keyname]
        return False,None

    def match_printing(self,keycode):
        for an_range in pp_kbddriver.printing_ranges:
            #print (keycode,an_range[0],an_range[1])
            if an_range[0] <= keycode <= an_range[1]:
                sname='pp-key-'+Gdk.keyval_name(keycode)
                return True,sname
        return False,None



    # read the key bindings from keys.cfg
    def _read(self,filename,filepath):
        if os.path.exists(filepath):
            self.config = configparser.ConfigParser(inline_comment_prefixes = (';',))
            self.config.optionxform = str
            
            self.config.read(filepath)
            return 'normal',filename+' read'
        else:
            return 'error',filename+' not found at: '+filepath

# dummy debug monitor
class Monitor(object):
    
    def err(self,inst,message):
        print ('ERROR: ',message)

    def log(self,inst,message):
        print ('LOG: ',message)

    def warn(self,inst,message):
        print ('WARN: ',message)

class Display(object):
    
    def __init__(self):
        self.mon=Monitor()
    
    def init(self):
        self.options={'fullscreen':False}
        app = Gtk.Application()
        app.connect('activate', self.on_activate)
        app.run(None)       
        
    def on_activate(self,app):
        # set up the displays and create a canvas for each display
        self.dm=DisplayManager()
        self.pp_dir=sys.path[0]
        status,message,self.root=self.dm.init(app,self.options,self.end,self.pp_dir,True)
        if status !='normal':
            print ('Error',message)

        self.kb=pp_kbddriver()
        self.kb.init('keys.cfg','/home/pp/pipresents/pp_io_config/keys.cfg',None,'','','',callback=self.kb_event)
    
    def kb_event(self,sname,title,win):
        print ('symbolic',sname,title,win)
    
    def end(self,win):
        win.close()
        print ('end')


            


if __name__ == '__main__':


    disp=Display()
    disp.init()
    #pp=PiPresents()
    




   
