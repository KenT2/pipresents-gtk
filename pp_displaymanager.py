#! /usr/bin/env python3

import os
import sys
import subprocess
import copy
import configparser

from pp_utils import Monitor,find_pi_model
from pp_gtkutils import CSS
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk

class DisplayManager(object):

    debug = True
    #x11
    x11_display_map = {'NODISPLAY':'NOOP-1','DSI0':'DSI-1','HDMI0':'HDMI-1','DSI1':'DSI-2','HDMI1':'HDMI-2'}
    x11_display_reverse_map = {'NOOP-1':'NODISPLAY','DSI-1':'DSI0','HDMI-1':'HDMI0','DSI-2':'DSI0','HDMI-2':'HDMI1' } 
    
    #wayland
    wayland_display_map = {'NODISPLAY':'NOOP-1','DSI0':'DSI-1','HDMI0':'HDMI-A-1','DSI1':'DSI-2','HDMI1':'HDMI-A-2'}
    wayland_display_reverse_map = {'NOOP-1':'NODISPLAY','DSI-1':'DSI0','HDMI-A-1':'HDMI0','DSI-2':'DSI0','HDMI-A-2':'HDMI1' } 
    
    # Class Variables
    
    dev_is_fullscreen = False
    options=None
    numdisplays=0
    displays=[]        # list of dispay board names detected
    
    window_obj=dict()    #gtk top level window for the monitor 

    monitor_wl_name=dict() # wayland name for the monitor
    monitor_obj=dict()   #gtk monitor
    monitor_width = {}
    monitor_height = {}
    monitor_x = {}
    monitor_y = {}
    
    display_overlaps=False
    
    canvas_obj=dict()    #gtk Fixed, equivalent to Tknite canvas    
    canvas_width=dict()
    canvas_height=dict()

    #FROM CONFIG
    # dimensions modified by fake in pp_display.cfg, used to create borders
    fake_display_width={}    
    fake_display_height={}
    
    # dimensions of the window in non-fullscreen mode (as modified by non-full window width/height in pp_display.cfg)
    window_width=dict()
    window_height=dict()
    
    
    #called by all classes using DisplayManager
    def __init__(self):
        self.mon=Monitor()
        self.css=CSS()
        return

# ***********************************************
# Methods used by the rest of Pi Presents
# ************************************************


    def is_display_connected(self,display_name):
        if display_name not in DisplayManager.display_map:
            return 'error','Display Name not known: '+ display_name,-1
        if display_name not in DisplayManager.displays:
            return 'error','Display not connected: '+ display_name,-1
        return 'normal','',display_name
        
    def get_develop_display():
        return self.develop_id
        
    def get_canvas_obj(self,display):
        return DisplayManager.canvas_obj[display]

    def get_window_obj(self,display):
        return DisplayManager.window_obj[display]  
        
    def get_monitor_obj(self,display):
        return DisplayManager.window_obj[display] 
              
    def get_canvas_dimensions(self,display):
        return DisplayManager.canvas_width[display],DisplayManager.canvas_height[display]
        
    def get_fake_display_dimensions(self,display):
        return DisplayManager.fake_display_width[display],DisplayManager.fake_display_height[display]

    def get_real_display_dimensions(self,display):
        return DisplayManager.monitor_width[display],DisplayManager.monitor_height[display]

    def does_display_overlap(self):
        return DisplayManager.display_overlaps
        
    def register_kbdriver(self,driver_obj):
        DisplayManager.kbdriver=driver_obj


# ***********************************************
# Initialize displays at start
# ************************************************

    # called by pipresents.py  only when PP starts
    def init(self,app,options,close_callback,pp_dir,debug):
        
        self.backlight=None
        
        dm=os.environ['XDG_SESSION_TYPE']
        if dm=='wayland':
            DisplayManager.display_map = DisplayManager.wayland_display_map
            DisplayManager.display_reverse_map = DisplayManager.wayland_display_reverse_map
        elif dm=='x11':
            DisplayManager.display_map = DisplayManager.x11_display_map
            DisplayManager.display_reverse_map = DisplayManager.x11_display_reverse_map
        else:
            return 'error','unknown display manager: '+dm,None
            
        DisplayManager.options=options
        self.close_callback=close_callback
        DisplayManager.debug=debug
        self.pp_dir=pp_dir
        self.backlight=None
        # read display.cfg
        self.read_config(pp_dir)

        # find connected displays from gtk and get their parameters            
        status,message=self.find_gtk_displays()
        if status=='error':
            return status,message,None
            
        self.test_overlaps()

        # compute display_width, display_height accounting for --screensize option
        status,message=self.do_fake_display()
        if status=='error':
            return status,message,None            
            
        # Have now got all the required information

        # setup backlight for touchscreen if connected
        status,message=self.init_backlight()
        if status=='error':
            return status,message,None
                    
        # set up Gtk windows
        status,message,parent_window=self.init_canvas(options,app)
        if status=='error':
            return status,message,None
        else:
            return status,message,parent_window

    def terminate(self):
        self.terminate_backlight()
        
    def close_windows(self,app):
        for display in DisplayManager.displays:
            #print ('closing',display)
            win=DisplayManager.window_obj[display]
            app.remove_window(win)

    def find_gtk_displays(self):
        display = Gdk.Display.get_default()
        #print ('Display name: ',display.get_name())
        monitors=display.get_monitors()
        
        #display manger - detect monitors and set up canvases
        DisplayManager.num_displays=0
        for m in monitors:
            connector=m.get_connector()

            if connector not in DisplayManager.display_reverse_map:
                return 'error','monitor not known: '+connector
            monitor_board_name=DisplayManager.display_reverse_map[connector]
            #print (connector,monitor_board_name)
            DisplayManager.displays.append(monitor_board_name)
            DisplayManager.num_displays+=1            
            DisplayManager.monitor_wl_name[monitor_board_name]=connector
            DisplayManager.monitor_obj[monitor_board_name]=m
            geometry = m.get_geometry()
            DisplayManager.monitor_x[monitor_board_name] = geometry.x
            DisplayManager.monitor_y[monitor_board_name] = geometry.y
            DisplayManager.monitor_width[monitor_board_name]=geometry.width
            DisplayManager.monitor_height[monitor_board_name]=geometry.height
        self.print_gtk()
        return 'normal',''

    def test_overlaps(self):
        DisplayManager.display_overlaps= False
        if DisplayManager.num_displays==3:
            self.test_overlap(0,2)
            self.test_overlap(1,2)
            self.test_overlap(0,1)
        if DisplayManager.num_displays==2:
            self.test_overlap(0,1)   


    def test_overlap(self,i1,i2):
        overlap=False
        id0=DisplayManager.displays[i1]
        id1=DisplayManager.displays[i2]
        if  DisplayManager.monitor_x[id0] == DisplayManager.monitor_x[id1]\
            and DisplayManager.monitor_y[id0] == DisplayManager.monitor_y[id1]:
            overlap=True    
            DisplayManager.display_overlaps=True
        return
            
    
 
    def do_fake_display(self):

        for did in DisplayManager.displays:
            reason,message,fake_width,fake_height=self.get_fake_dimensions(did)
            if reason =='error':
                return 'error',message
            if reason == 'null':
                DisplayManager.fake_display_width[did]=DisplayManager.monitor_width[did]
                DisplayManager.fake_display_height[did]=DisplayManager.monitor_height[did]  
            else:
                DisplayManager.fake_display_width[did] = fake_width
                DisplayManager.fake_display_height[did] = fake_height
        self.print_fake()
        return 'normal',''
        

# ***********************************************
# Set up Gtk windows and canvases.
# ************************************************

    def init_canvas(self,options,app):
        
        if len(DisplayManager.displays)==0:
            return 'error','No displays connected',None

        # choose the windowed develop display
        if len(DisplayManager.displays)==1:
            # single display
            self.develop_id=DisplayManager.displays[0]
        else:
            self.develop_id='DSI1'
            if 'HDMI0' in DisplayManager.displays:
                self.develop_id='HDMI0'
            elif'HDMI1' in DisplayManager.displays:
                self.develop_id='HDMI1'
            elif'DSI0' in DisplayManager.displays:
                self.develop_id='DSI0'

                    
        for display in DisplayManager.displays:
            #calculate develop window
            status,message,w_scale,h_scale=self.get_develop_window(display)
            if status != 'normal':
                return 'error',message,None
            DisplayManager.window_width[display]=DisplayManager.monitor_width[display]*w_scale
            DisplayManager.window_height[display]= DisplayManager.monitor_height[display]*h_scale
            
            # setup a canvas onto which will be drawn the images or text
            # canvas covers the whole screen whatever the size of the window
            DisplayManager.canvas_height[display]=DisplayManager.fake_display_height[display]
            DisplayManager.canvas_width[display]=DisplayManager.fake_display_width[display]
            
            #create windows and canvases
            win = Gtk.Window(application=app)
            DisplayManager.window_obj[display]=win
            #print (display,DisplayManager.window_obj[display])
            
            # key controller
            keycont = Gtk.EventControllerKey()   
            keycont.connect('key-pressed' ,self.on_key_press_event, win)
            win.add_controller(keycont) 
                       
            win.connect('close-request',self.e_close_callback)
            
            win.set_title('PP-'+ display)
            #win.set_opacity(1)
            win.set_default_size(DisplayManager.window_width[display],DisplayManager.window_height[display])
            win.set_resizable(True)
            win.set_name('window-background')
            self.css.style_widget(win,'window-background',background_color = 'black')

            #make window scrolled
            scrolled=Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
            
            # fixed layout (canvas)
            canvas = Gtk.Fixed()
            DisplayManager.canvas_obj[display]=canvas
            
            # fake border
            if options['fullscreen'] is False:
                fake_border=Gtk.Frame()
                fake_border.set_name('fake-border')
                self.css.style_widget(fake_border,'fake-border',background_color = 'transparent',border='1px solid yellow')
                fake_border.set_size_request(DisplayManager.canvas_width[display],DisplayManager.canvas_height[display])
                canvas.put(fake_border,0,0)
            
            #cursor control
            if options['fullscreen'] is True and options['cursor'] is False:
                win.set_cursor_from_name('none')


            #construct develop or fullscreen display
            if options['fullscreen'] is False and display == self.develop_id:
                #print('develop',options['fullscreen'],display,self.develop_id)
                #build gui widgets
                scrolled.set_child(canvas)
                win.set_child(scrolled)
                win.present()
            else:
                #print('full',options['fullscreen'],display,self.develop_id)
                win.set_child(canvas)
                #win.set_opacity(0)
                #print ('monitor object',display,DisplayManager.monitor_obj[display])
                win.fullscreen_on_monitor(DisplayManager.monitor_obj[display])
                win.present()                
                #win.set_opacity(1)
        #self.print_canvas()
        return 'normal','',self.get_window_obj(self.develop_id)
        
    def e_close_callback(self,win):
        self.close_callback()
    

    def on_key_press_event(self,keyval, keycode, state, user_data, win):
        keyname=Gdk.keyval_name(keycode)
        if DisplayManager.debug is True:
            print('keyname: ', keyname,"keycode: ", keycode)
            #print("Window: ", win.get_title())
            #print("          State: ", state)
            #print("          keyval: ", keyval)

            #print ('shift mask',enum(Gdk.ModifierType.SHIFT_MASK))
            #print ('State and Shift mask',state & Gdk.ModifierType.SHIFT_MASK)



        if keyname=='F1'and DisplayManager.options['fullscreen'] is False:
            if DisplayManager.dev_is_fullscreen is False:
                win=self.get_window_obj(self.develop_id)
                win.fullscreen()
                DisplayManager.dev_is_fullscreen = True
            else:
                win=self.get_window_obj(self.develop_id)
                win.unfullscreen()
                DisplayManager.dev_is_fullscreen = False
        """
        if keyname =='0':
            DisplayManager.window_obj['HDMI0'].destroy()
            print ('0',DisplayManager.window_obj['HDMI0'])
        if keyname == '1':
            DisplayManager.window_obj['HDMI1'].destroy()
            print ('1',DisplayManager.window_obj['HDMI1'])
        #if keyname =='x':
            #win.close()
        """
        DisplayManager.kbdriver(keycode,win)
        return True



        
    def print_info(self):
        if DisplayManager.debug is True:
            print ('\nMaps:',DisplayManager.display_map,'\n',DisplayManager.display_reverse_map)

    def print_gtk(self):
        if DisplayManager.debug is True:
            print ('\nNumber of Monitors conneted gtk:',DisplayManager.num_displays)
            print ('Monitors Connected gtk:',DisplayManager.displays)
            print ('Monitor Wayland names: ',DisplayManager.monitor_wl_name)
            print ('Monitor Dimensions gtk:',DisplayManager.monitor_width,DisplayManager.monitor_height)

    def print_fake(self):
        if DisplayManager.debug is True:
            print ('\nMonitor Dimensions - fake:',DisplayManager.fake_display_width,DisplayManager.fake_display_height)

    def print_canvas(self):
        if DisplayManager.debug is True:
            print ('\nDevelopment Monitor:',self.develop_id)
            print ('Develop Window Dimensions',DisplayManager.window_width,DisplayManager.window_height)
            #print ('Canvas Widget:',DisplayManager.canvas_obj)
            print ('Canvas Dimensions:',DisplayManager.canvas_width,DisplayManager.canvas_height,'\n\n')



# ***********************************************
# Read and process configuration data
# ************************************************

    # read display.cfg    
    def read_config(self,pp_dir):
        filename=pp_dir+os.sep+'pp_config'+os.sep+'pp_display.cfg'
        if os.path.exists(filename):
            DisplayManager.config = configparser.ConfigParser(inline_comment_prefixes = (';',))
            DisplayManager.config.read(filename)
            return 'normal','display.cfg read'
        else:
            return 'error',"Failed to find display.cfg at "+ filename

    def displays_in_config(self):
        return DisplayManager.config.sections()
        
    def display_in_config(self,section):
        return DisplayManager.config.has_section(section)
        
    def get_item_in_config(self,section,item):
        return DisplayManager.config.get(section,item)

    def item_in_config(self,section,item):
        return DisplayManager.config.has_option(section,item)


    def get_fake_dimensions(self,dname):
        if not self.display_in_config(dname):
            return 'error','display not in display.cfg '+ dname,0,0
        if not self.item_in_config(dname,'fake-dimensions'):
            return 'null','',0,0
        size_text=self.get_item_in_config(dname,'fake-dimensions')
        if size_text=='':
            return 'null','',0,0
        fields=size_text.split('*')
        if len(fields)!=2:
            return 'error','do not understand fake-dimensions in display.cfg for '+dname,0,0
        elif fields[0].isdigit()  is False or fields[1].isdigit()  is False:
            return 'error','fake dimensions are not positive integers in display.cfg for '+dname,0,0
        else:
            return 'normal','',int(fields[0]),int(fields[1])

    def get_develop_window(self,dname):
        x=0
        y=0
        width=0
        height=0
        if not self.display_in_config(dname):
            return 'error','display not in pp_display.cfg '+ dname,0,0
        if not self.item_in_config(dname,'develop-window'):
            return 'normal','',0.45,0.7
        size_text=self.get_item_in_config(dname,'develop-window')
        if size_text=='':
            return 'normal','',0.45,0.7
        if '+' in size_text:
            # parse  x+y+width*height
            fields=size_text.split('+')
            if len(fields) != 3:
                return 'error','Do not understand Display Window in pp_display.cfg for '+dname,0,0
                
            if not fields[0].isdigit():
                return 'error','x is not a positive decimal in pp_display.cfg for '+dname,0,0
            else:
                x=float(fields[0])
            
            if not fields[1].isdigit():
                return 'error','y is not a positive decimal in pp_display.cfg for '+dname,0,0
            else:
                y=float(fields[1])
            status,message,width,height=self.parse_dimensions(dname,fields[2])
            if status =='error':
                return status,message,0.45,0.7
            return 'normal','',width,height                
        else:
            status,message,width,height=self.parse_dimensions(dname,size_text)
            if status =='error':
                return status,message,0.45,0.7
            return 'normal','',width,height
            
            
    def parse_dimensions(self,dname,dim):           
        dimensions=dim.split('*')
        if len(dimensions)!=2:
            return 'error','Do not understand Display Window in pp_display.cfg for '+dname,0,0
        
        if not self.is_scale(dimensions[0]):
            return 'error','width1 is not a positive decimal in display.cfg for '+dname,0,0
        else:
            width=float(dimensions[0])
            
        if not self.is_scale(dimensions[1]):
            return 'error','height is not a positive decimal in display.cfg for '+dname,0,0
        else:
            height=float(dimensions[1])
        #print('dim',width,height)
        return 'normal','',width,height


    def is_scale(self,s):
        try:
            sf=float(s)
            if sf > 0.0 and sf <=1:
                return True
            else:
                return False
        except ValueError:
            return False


# ***********************************************
# HDMI Monitor Commands for DSI and HDMI
# ************************************************
    #gtkdo funny stuff here
    def handle_monitor_command(self,args):
        #print ('args',args)
        if len(args) == 0:
            return 'error','no arguments for monitor command'
        if len (args) == 2:
            command = args[0]
            display= args[1].upper()
            if display not in DisplayManager.display_map:
                return 'error', 'Monitor Command - Display not known: '+ display
            if display not in DisplayManager.displays:
                return 'error', 'Monitor Command - Display not connected: '+ display 
            wayland_name=DisplayManager.display_map[display]
        else:
            return 'error', 'Display not specified: monitor '+ args[0]
        print (command,wayland_name)

        if command == 'on':
            os.system('wlr-randr --output '+ wayland_name + ' --on')
            return 'normal',''
            
        elif command == 'off':
            os.system('wlr-randr --output '+ wayland_name + ' --off')
            return 'normal',''
        else:
            return 'error', 'Illegal Monitor command: '+ command



# ***********************************************
# Touchscreen Backlight Commands
# ************************************************ 
   
    def init_backlight(self):
        self.backlight=None
        self.orig_brightness=20
        if 0 in DisplayManager.displays:
            try:
                from rpi_backlight import Backlight
            except:
                return 'error','touchscreen connected but rpi-backlight is not installed'
            try:
                self.backlight=Backlight()
            except:
                return 'error','Official Touchscreen, problem with rpi-backlight'
            try:
                self.orig_brightness=self.backlight.brightness
            except:
                return 'error','Official Touchscreen,  problem with rpi-backlight'
        #print ('BACKLIGHT',self.backlight,self.orig_brightness)
        return 'normal',''

    def terminate_backlight(self):
        if self.backlight is not None:
            self.backlight.power=True
            self.backlight.brightness=self.orig_brightness

    def do_backlight_command(self,text):
        if self.backlight is None:
            return 'normal','no touchscreen'
        fields=text.split()
        # print (fields)
        if len(fields)<2:
            return 'error','too few fields in backlight command: '+ text
        # on, off, inc val, dec val, set val fade val duration
        #                                      1   2    3
        if fields[1]=='on':
            self.backlight.power = True
            return 'normal',''      
        if fields[1]=='off':
            self.backlight.power = False
            return 'normal',''
        if fields[1] in ('inc','dec','set'):
            if len(fields)<3:
                return 'error','too few fields in backlight command: '+ text
            if not fields[2].isdigit():
                return'error','field is not a positive integer: '+text
            if fields[1]=='set':
                val=int(fields[2])
                if val>100:
                    val = 100
                elif val<0:
                    val=0
                # print (val)
                self.backlight.brightness = val
                return 'normal',''            
            if fields[1]=='inc':
                val = self.backlight.brightness + int(fields[2])
                if val>100:
                    val = 100
                # print (val)
                self.backlight.brightness= val
                return 'normal',''
            if fields[1]=='dec':
                val = self.backlight.brightness - int(fields[2])
                if val<0:
                    val = 0
                # print (val)
                self.backlight.brightness= val
                return 'normal',''
        if fields[1] =='fade':
            if len(fields)<4:
                return 'error','too few fields in backlight command: '+ text
            if not fields[2].isdigit():
                return'error','backlight field is not a positive integer: '+text            
            if not fields[3].isdigit():
                return'error','backlight field is not a positive integer: '+text
            val=int(fields[2])
            if val>100:
                val = 100
            elif val<0:
                val=0
            with selfbacklight.fade(duration=fields[3]):
                self.backlight.brightness=val
                return 'normal',''
        return 'error','unknown backlight command: '+text


# used to test on a machine without a backlight
class FakeBacklight():
    
    def __init__(self):
        self._brightness=100
        self._power = True
        # print ('USING FAKE BACKLIGHT')
        

    def get_power(self):
        return self._power

    def set_power(self, power):
        self._power=power
        print ('POWER',self._power)

    power = property(get_power, set_power)

    def get_brightness(self):
        return self._brightness

    def set_brightness(self, brightness):
        self._brightness=brightness
        print ('BRIGHTNESS',self._brightness)

    brightness = property(get_brightness, set_brightness)    


    
# **************************
# Test Harness
# **************************   

class Display(object):
    
    def __init__(self):
        self.mon=Monitor()
    
    def init(self):
        self.options={'fullscreen':False, 'cursor':True}
        app = Gtk.Application()
        app.connect('activate', self.on_activate)
        app.run(None)       
        
    def on_activate(self,app):
        # set up the displays and create a canvas for each display
        self.dm=DisplayManager()
        self.dm.register_kbdriver(self.callback)
        self.pp_dir=sys.path[0]
        status,message,self.root=self.dm.init(app,self.options,self.end,self.pp_dir,True)
        if status !='normal':
            print ('Error',message)
            
    def callback(self,keycode,win):
        ##print ('callback',keycode)
        pass
        
    
    def end(self,win):
        win.close()
        print ('end')

if __name__ == '__main__':
    """

    # dummy debug monitor
    class Monitor(object):
        
        def err(self,inst,message):
            print ('ERROR: ',message)

        def log(self,inst,message):
            print ('LOG: ',message)

        def warn(self,inst,message):
            print ('WARN: ',message)
            
    """

    disp=Display()
    disp.init()

    #pp=PiPresents()
    
