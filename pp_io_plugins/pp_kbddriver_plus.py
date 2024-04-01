#enhanced keyboard driver
import copy
import os,sys
import configparser
from pp_displaymanager import DisplayManager
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk

class pp_kbddriver_plus(object):
    
    # keyvodes of alphaanumeric key ranges
    # 0-9, a-z, A-Z
    an_ranges=[[32,126],[128,255]]

    # match list items

    DIRECTION = 0         # in/out
    MODE= 1               # for input the match mode any-character,specific-character,any-line,specific-line
    MATCH = 2             # for input the character/string to match (no EOL)
    NAME=3                # symbolic name for input and output
    
    TEMPLATE=['','','',''] 

# CLASS VARIABLES  (pp_kbddriver_plus.)
    driver_active=False
    title=''          # used for error reporting and logging
    inputs={}

    # executed by main program and by each object using the driver
    def __init__(self):
        self.dm=DisplayManager()

     # executed once from main program   
    def init(self,filename,filepath,widget,pp_dir,pp_home,pp_profile,event_callback=None):
        
        # instantiate arguments
        self.widget=widget
        self.filename=filename
        self.filepath=filepath
        self.event_callback=event_callback

        pp_kbddriver_plus.driver_active = False

        # read pp_kbddriver_plus.cfg file.
        reason,message=self._read(self.filename,self.filepath)
        if reason =='error':
            return 'error',message
        if self.config.has_section('DRIVER') is False:
            return 'error','No DRIVER section in '+self.filepath
        
        # all the below are used by another instance of pp_kbddriver_plus so must reference class variables
        # read information from DRIVER section
        pp_kbddriver_plus.title=self.config.get('DRIVER','title')
        pp_kbddriver_plus.bind_printing = self.config.get('DRIVER','bind-printing')
        
        # construct the match list from the config file
        pp_kbddriver_plus.in_names=[]
        pp_kbddriver_plus.out_names=[]
        for section in self.config.sections():
            if section == 'DRIVER':
                continue
            entry=copy.deepcopy(pp_kbddriver_plus.TEMPLATE)
            entry[pp_kbddriver_plus.NAME]=self.config.get(section,'name')
            entry[pp_kbddriver_plus.DIRECTION]=self.config.get(section,'direction')
            if entry[pp_kbddriver_plus.DIRECTION] =='none':
                continue
            elif entry[pp_kbddriver_plus.DIRECTION] == 'in':
                entry[pp_kbddriver_plus.MODE]=self.config.get(section,'mode')
                if entry[pp_kbddriver_plus.MODE] in ('specific-character','specific-line'):
                    entry[pp_kbddriver_plus.MATCH]=self.config.get(section,'match')
                pp_kbddriver_plus.in_names.append(copy.deepcopy(entry))
            else:
                return 'error',pp_kbddriver_plus.title + ' direction not in or out'
        #print (pp_kbddriver_plus.in_names)
        
        self.dm.register_kbdriver(self.on_key_pressed)       
        # all ok so indicate the driver is active
        pp_kbddriver_plus.driver_active=True

        # init must return two arguments
        return 'normal',pp_kbddriver_plus.title + ' active'


    def start(self):
        # init input buffers
        pp_kbddriver_plus.inputs['current-character']=''
        pp_kbddriver_plus.inputs['current-line']=''
        pp_kbddriver_plus.inputs['previous-line']=''


    def on_key_pressed(self,keycode,win):
        if pp_kbddriver_plus.driver_active is True:
            keyname=Gdk.keyval_name(keycode)
            #print ('\nReceived',keyname,keycode)
            enter = True if keyname=='Return' else False
            if keyname in ('Delete','Backspace'):
                delete=True
            else:
                delete=False
            # determine and decode printing characters
            match,dummy=self.match_printing(keycode)
            if match:
                character=chr(Gdk.keyval_to_unicode(keycode))
            else:
                character=None
                #print ('not a printing character')
            #print ('after filter', character,enter,delete)

            # shuffle and empty the buffer
            if enter is True:
                pp_kbddriver_plus.inputs['previous-line'] = pp_kbddriver_plus.inputs['current-line']
                pp_kbddriver_plus.inputs['current-line']=''
                pp_kbddriver_plus.inputs['current-character']=''
                # do match of line
                #print ('Return Detected')
                matched,sname = self.match_specific_line(pp_kbddriver_plus.inputs['previous-line'])
                if matched:
                    #print ('Matched specific line',keyname,pp_kbddriver_plus.inputs['previous-line'])
                    self.event_callback(sname,pp_kbddriver_plus.title)
                    return   

                matched,sname = self.match_any_line(pp_kbddriver_plus.inputs['previous-line'])
                if matched:
                    #print ('Matched any line',keyname,pp_kbddriver_plus.inputs['previous-line'])
                    self.event_callback(sname,pp_kbddriver_plus.title)
                    return
                    
                #return may also match with specific character
                matched,sname=self.match_specific_char(keyname)
                if matched:
                    #print ('Return may also be specific char',keyname,sname)
                    self.event_callback(sname,pp_kbddriver_plus.title)
                    return           
            else:
                # a character other than Return has been received
                if character!=None:
                    #printing character so store it
                    pp_kbddriver_plus.inputs['current-character']=character
                    pp_kbddriver_plus.inputs['current-line']+=character
                
                matched,sname=self.match_specific_char(keyname)
                if matched:
                    #print ('matched specific char ',keyname,sname)
                    self.event_callback(sname,pp_kbddriver_plus.title)
                    return
                    
                if pp_kbddriver_plus.bind_printing =='yes':
                    matched,sname=self.match_printing(keycode)
                    if matched:
                        #print ('matched bind printing',keyname,sname)
                        self.event_callback(sname,pp_kbddriver_plus.title)
                    return   
                      
                matched,sname=self.match_any_char(keyname)
                if matched:
                    #print ('matched any char',keyname,sname)
                    self.event_callback(sname,pp_kbddriver_plus.title)
                    return
                                                                                                    

    def match_any_char(self,keyname):
        #print ('matching any char',keyname)
        for entry in pp_kbddriver_plus.in_names:
            if entry[pp_kbddriver_plus.MODE] == 'any-character':
                return True,entry[pp_kbddriver_plus.NAME]
        return False,None


    def match_specific_char(self,keyname):
        #print ('matching specific char',keyname)
        for entry in pp_kbddriver_plus.in_names:
            if entry[pp_kbddriver_plus.MODE] == 'specific-character' and entry[pp_kbddriver_plus.MATCH]==keyname:
                return True,entry[pp_kbddriver_plus.NAME] 
        return False,None

    def match_printing(self,keycode):
        #print ('matching printing character',keycode)
        keyname=Gdk.keyval_name(keycode)
        for an_range in pp_kbddriver_plus.an_ranges:
            #print (keycode,an_range[0],an_range[1])
            if an_range[0] <= keycode <= an_range[1]:
                sname='pp-key-'+Gdk.keyval_name(keycode)
                return True,sname
        return False,None                
                    

    def match_specific_line(self,line):
        #print ('matching specific line',line)
        
        for entry in pp_kbddriver_plus.in_names:
            #print (entry[pp_kbddriver_plus.MODE],entry[pp_kbddriver_plus.MATCH],line)
            if entry[pp_kbddriver_plus.MODE] == 'specific-line' and line == entry[pp_kbddriver_plus.MATCH]:
                return True,entry[pp_kbddriver_plus.NAME]
        return False,''

    def match_any_line(self,line):
        #print ('matching any line',line)
        
        for entry in pp_kbddriver_plus.in_names:
            #print (entry[pp_kbddriver_plus.MODE],entry[pp_kbddriver_plus.MATCH],line)
            if entry[pp_kbddriver_plus.MODE] == 'any-line':
                return True,entry[pp_kbddriver_plus.NAME]
        return False,''


    # allow track plugins (or anything else) to access analog input values
    def get_input(self,key):
        if key in pp_kbddriver_plus.inputs:
            return True, pp_kbddriver_plus.inputs[key]
        else:
            return False, None


    # allow querying of driver state
    def is_active(self):
        return pp_kbddriver_plus.driver_active


    # called by main program only. Called when PP is closed down               
    def terminate(self):
            pp_kbddriver_plus.driver_active = False



# ************************************************
# output interface method
# this can be called from many objects so needs to operate on class variables
# ************************************************                            
    # execute an output event

    def handle_output_event(self,name,param_type,param_values,req_time):
        return 'normal','no output methods'



# ***********************************
# reading .cfg file
# ************************************

    def _read(self,filename,filepath):
        if os.path.exists(filepath):
            self.config = configparser.ConfigParser(inline_comment_prefixes = (';',))
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

        self.kb=pp_kbddriver_plus()
        self.kb.init('keys_plus.cfg','/home/pp/pipresents-gtk/pp_resources/pp_templates/keys_plus.cfg',None,'','','',event_callback=self.kb_event)
        self.kb.start()
#       init(self,filename,filepath,widget,pp_dir,pp_home,pp_profile,event_callback=None):
    
    def kb_event(self,sname,title):
        print ('CALBACK symbolic',sname,title)
    
    def end(self,win):
        win.close()
        print ('end')


            


if __name__ == '__main__':
    disp=Display()
    disp.init()

    




   
