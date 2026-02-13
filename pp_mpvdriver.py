import gi
from pymediainfo import MediaInfo
import time
import sys,os
#import mpv
from python_mpv_jsonipc_plus import MPV
from pp_utils import Monitor
gi.require_version("Gtk", "4.0")
gi.require_version('Gdk', '4.0')
gi.require_version('GdkX11', '4.0')
from gi.repository import Gtk,Gdk,GLib, GdkX11
from pp_gtkutils import CSS
"""
USE


Initial state is idle, this is altered by the calls

load() - start mpv and loads a track and then run to start depending on freeze-at-start.
      load() is non-blocking and returns immeadiately. To determine load is complete poll using get_state() to obtain the state
    load-loading - load in progress
    load-ok - loading complete and ok
    load-fail

show - show a track that has been loaded. Show is non-blocking and returns immeadiately. To determine showing is complete poll using get_state to obtain the state
    show-showing - showing in progress
    show-pauseatend - paused before last frame.
    show-niceday - track has ended
    show-fail
    
stop() - stops showing. To determine if complete poll get_state() for: 
      show-niceday

unload() - stops loading. To determine if complete poll state for:
      load-unloaded

close() - exits mpv and exits pp_mpvdriver.py
    
set_pause() - pause or unpause

set_volume() - set the volume between 0 and 100. Use only when showing
      
set-device - set audio device ??????
pause/ unpause - pauses the track
mute()unmute - mute without changing volume

"""


 
class MPVDriver(object):
    
    # used first time and for every other instance
    def __init__(self,root,canvas,freeze_at_start,freeze_at_end,background_colour):
        self.mon=Monitor()
        self.mon.log (self,'start mpvdriver')
        self.root=root
        self.canvas=canvas
        self.freeze_at_start=freeze_at_start
        self.freeze_at_end=freeze_at_end
        self.background_colour=background_colour

        self.frozen_at_start=False
        self.frozen_at_end=False  
        self.state='idle'      
        self.user_pause=False
        self.quit_load_signal=False
        self.quit_show_signal=False
        self.show_status_timer=None
        self.load_status_timer=None
        self.css=CSS()
      



    def load(self,track,options,x,y,width,height):
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.track=track
        self.options=options
        self.state='load-loading'
        self.load_position=-1

        #video
        self.has_video=self.file_has_video(self.track)
        #print (self.has_video)
        window= self.canvas.get_root()
        wid= str(GdkX11.X11Surface.get_xid(window.get_surface()))
        self.player=MPV(input_default_bindings='no', input_vo_keyboard ='no',profile='fast',
        osc='no',config='no',border='no',wid=wid)

        status,message=self.apply_options(self.options)
        if status == 'error':
            print(message)
        self.player.play(self.track)
        #print('ready',self.player.width,self.player.dwidth,self.player.height,self.player.dheight)
        self.player.volume=100     # was 0
        if self.freeze_at_start == 'before-first-frame':
            self.player.video=0
        else:
            self.player.video=1
        #need a timeout as sometimes a load will fail 
        self.load_timeout= 500    #5 seconds
        
        self.load_status_timer=GLib.timeout_add(1,self.load_status_loop)

    def file_has_video(self,path):
        file_info = MediaInfo.parse(path)
        for track in file_info.tracks:
            if track.track_type == "Video":
                return True
        return False



    def load_status_loop(self):
        #print ('in loop - load')
        GLib.source_remove(self.load_status_timer)
        self.load_status_timer=None
        
        
        if self.quit_load_signal is True:
            self.quit_load_signal=False
            self.player.stop() 
            self.state= 'load-unloaded'
            self.mon.log (self,'unloaded at: '+str(self.load_position))
            return
            
        if self.load_complete() is True:
            #print ('load complete')
            self.duration=self.player.duration

            
            if self.freeze_at_start == 'before-first-frame':
                self.frozen_at_start=True
                self.mon.log (self,'stop-frozen before : ' + str(self.load_position))
                self.state='load-frozen'
                self.player.video=0

                    
            elif self.freeze_at_start == 'after-first-frame':
                self.frozen_at_start=True
                self.mon.log (self,'stop-frozen after: ' + str(self.load_position))
                self.state='load-frozen'
                self.player.video=1
                
            else:
                self.state='load-ok'
                self.player.video=1
                self.mon.log (self,'load-ok at: '+str(self.load_position))
            return
            
        self.load_timeout-=1
        if self.load_timeout <=0:
            self.mon.fatal (self,'load failed due to timeout load position is:'+str(self.load_position))
            self.state='load-fail'
            return

        self.load_status_timer=GLib.timeout_add(10,self.load_status_loop)

    def load_complete(self):
        value=self.player.time_pos
        #print ('load',value)
        if value is not None and value>=0:
            self.player.pause=True
            self.load_position=value
            return True
        return False
        

    def apply_options(self,options):
        #print ('OPTIONS')
        for option in options:
            #print (option[0],option[1])
            try:
                setattr(self.player,option[0],option[1])
                #self.player[option[0]]=option[1]
            except:
                return 'error','bad MPV option: ' + option[0] +' '+ option[1]
        return 'normal',''


    def show(self,initial_volume):
        #print ('showing')
        if self.freeze_at_start == 'no':
            self.state='show-showing'
            self.player.pause=False 
            self.set_volume(initial_volume)
            self.mon.log (self,'no freeze at start, start showing')
            self.frozen_at_start=False
            # print ('duration',self.duration)
            self.show_status_timer=GLib.timeout_add(1,self.show_status_loop)
        return

                
    def show_complete(self):
        value=self.player.time_pos
        #print ('in show complete',self.freeze_at_end,value)
        if self.freeze_at_end =='yes':
            if (value==None)or(value>self.duration-0.12):
                #print('change detected pause ',value)
                self.show_position=value
                return True
            return False
        else:
            if value==None:
                self.show_position=value
                #print('change detected niceday ',value)
                return True
            return False
            #print('missed change',name,value)
 
    def show_status_loop(self):
        #print ('in  show loop')
        if self.show_status_timer !=None:
            GLib.source_remove(self.show_status_timer)
            self.show_status_timer=None
            
        sc=self.show_complete()
                    
        if self.quit_show_signal is True:
            self.quit_show_signal= False
            if self.freeze_at_end == 'yes':
                self.frozen_at_end=True
                self.player.pause=True
                self.state='show-pauseatend'
                self.mon.log(self,'stop caused pause '+self.state)
                return
            else:
                self.player.stop()
                self.state='show-niceday'
                self.mon.log(self,'stop caused no pause '+self.state)
                return
                
        if sc is True:
            self.show_complete_signal=False
            if self.freeze_at_end == 'yes':
                self.player.pause=True
                self.frozen_at_end=True
                #print (self.show_position)
                self.mon.log(self,'paused at end at: '+str(self.show_position))
                self.state='show-pauseatend'
                return
            else:
                self.mon.log(self,'ended with no pause'+str(self.show_position))
                self.state='show-niceday'
                self.frozen_at_end=False
                #self.player.stop()
                return
                
        else:
            #self.mon.log(self,'after '+self.state)
            self.show_status_timer=GLib.timeout_add(30,self.show_status_loop)

    def hide(self):
        pass        

    def close(self):
        #print ('in close')
        self.player.terminate()
        
        if self.load_status_timer != None:
            GLib.source_remove(self.load_status_timer)
            self.load_status_timer=None
        if self.show_status_timer != None:
            GLib.source_remove(self.show_status_timer)
            self.show_status_timer=None

# ***********************
# Commands
# ***********************
        
    def get_state(self):
        return self.state

    def go(self,initial_volume):
        if self.frozen_at_start is True:
            self.state='show-showing'
            self.mon.log (self,'freeze off, go ok')
            self.player.pause=False
            self.player.video=1
            self.set_volume(initial_volume)
            self.show_complete_signal=False
            self.show_status_timer=GLib.timeout_add(1,self.show_status_loop)
            self.frozen_at_start=False
            return 'go-ok'
        else:
            self.mon.log (self,'go rejected')
            return 'go-reject'
        
        
    def pause(self):
        if self.state== 'show-showing' and self.frozen_at_end is False and self.frozen_at_start is False:
            if self.user_pause is True:
                self.player.pause=False
                self.user_pause=False
                self.mon.log (self,'pause to pause-off ok')
                return 'pause-off-ok'
            else:
                self.user_pause=True
                self.player.pause=True
                self.mon.log (self,'pause to pause-on ok')
                return 'pause-on-ok'
        else:
            self.mon.log (self,'pause rejected')
            return 'pause-reject'


    def pause_on(self):
        if self.state== 'show-showing' and self.frozen_at_end is False and self.frozen_at_start is False:
            self.user_pause=True
            self.player.pause=True
            self.mon.log (self,'pause on ok')
            return 'pause-on-ok'
        else:
            self.mon.log (self,'pause on rejected')
            return 'pause-on-reject'
            
                    
    def pause_off(self):
        if self.state== 'show-showing' and self.frozen_at_end is False and self.frozen_at_start is False:
            self.player.pause=False
            self.user_pause=False
            self.mon.log (self,'pause off ok')
            return 'pause-off-ok'
        else:
            return 'pause-off-reject'

    def stop(self):
        if self.frozen_at_start is True:
            self.player.stop()
            self.state='show-niceday'
            self.mon.log(self,'stop during frozen at start '+self.state)
            return
        else:
            self.quit_show_signal=True
            return

        
    def unload(self):
        if self.state=='load-loading':
            self.quit_load_signal=True
        else:
            self.state='load-unloaded'

    def mute(self):
        self.player.mute=True
        
    def unmute(self):
        self.player.mute=False
                
    def set_volume(self,volume):
        self.player.volume=volume        

    def set_device(self,device_id):
        if device_id=='':
            self.player.audio_output_device_set(None,None) 
        else:           
            self.player.audio_output_device_set(None,device_id)

"""
THIS NEEDS UPDATING FOR GTK4

"""
class PP(object):

    def __init__(self):
        print ('__init__')
        self.mon=Monitor()

        
    def start(self):
        self.options=[['sid','auto']]
        self.root,self.canvas,width,height=self.create_gui()
        print ('C W H', self.canvas,width,height)
        self.width=width-100
        self.height=height-100
        self.root.after(1,self.load_first)
        self.root.mainloop()
        
    def load_first(self):
        print ('load first')
        self.dd1=MPVDriver(self.root,self.canvas,'no','no','green')
        self.dd1.load('/home/pp/pp_home/media/suits-short.mkv',self.options,100,100,self.width,self.height)
        self.monitor_load1()
        
    def monitor_load1(self):
        state=self.dd1.get_state()
        print ('load1 state', state)
        if state=='load-ok':
            self.show_first()
            return
        GLib.timeout_add(100,self.monitor_load1)        
        
    def show_first(self):
        print ('ready to show first')
        self.dd1.show(100)
        self.monitor_show1()
        
    def monitor_show1(self):
        state=self.dd1.get_state()
        #print ('show1 state', state)
        if state in ('show-pauseatend','show-niceday'):
            self.load_second()
            return
        GLib.timeout_add(100,self.monitor_show1)  

        
    def load_second(self):
        self.dd2=MPVDriver(self.root,self.canvas,'no','yes','white')
        self.dd2.load('/home/pp/pp_home/media/suits-short.mkv',self.options,100,100,self.width,self.height)
        self.monitor_load2()   
        
        
    def monitor_load2(self):
        state=self.dd2.get_state()
        #print ('load state', state)
        if state=='load-ok':
            self.show_second()
            return
        GLib.timeout_add(100,self.monitor_load2)            
        
        
    def show_second(self):
        #print ('ready to show second')
        self.dd2.show(100)
        self.dd1.close() 
                
        
    def close_callback(self):
        self.root.destroy()
        exit()
    
    
    def create_gui(self):
        # print (this_id, self.develop_id)            
        tk_window=tk.Tk()
        root=tk_window
        tk_window.title('Pi Presents - ')
        tk_window.iconname('Pi Presents')
        tk_window.config(bg='black')


        # set window dimensions and decorations
        # fullscreen for all displays that are not develop_id
        window_width=1920
        # krt changed
        window_height=1080
        window_x=0
        window_y=0
        #KRT
        tk_window.attributes('-fullscreen', False)
        
        # print ('Window Position FS', this_id, window_x,window_y,window_width,window_height)
        tk_window.geometry("%dx%d%+d%+d"  % (window_width,window_height,window_x,window_y))
        tk_window.attributes('-zoomed','1')
  
        # define response to main window closing.
        tk_window.protocol ("WM_DELETE_WINDOW", self.close_callback)
        root.bind('x',self.close_callback)

        # setup a canvas onto which will be drawn the images or text
        # canvas covers the whole screen whatever the size of the window

        
        canvas_height=1080/2+300
        canvas_width=1920/2+300
        
        tk_canvas = tk.Canvas(tk_window, bg='red')
        tk_canvas.config(height=canvas_height,
                                 width=canvas_width,
                                 highlightthickness=2,
                                highlightcolor='yellow')
        tk_canvas.place(x=0,y=0)

        tk_canvas.config(bg='red')

        tk_window.focus_set()
        tk_canvas.focus_set()
    

        return root,tk_canvas,canvas_width,canvas_height

        

        
if __name__ == '__main__':
    import tkinter as tk
    print("TEST HARNESS NEEDS UPDATING FOR GTK4")
    #p = PP()
    #p.start()

    




  
    

    

