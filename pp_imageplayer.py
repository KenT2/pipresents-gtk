

import os
from pp_gtkutils import CSS
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib
from pp_utils import StopWatch, parse_rectangle,calculate_text_position
from pp_player import Player

class ImagePlayer(Player):

    """ Displays an image on a canvas for a period of time. Image display can be paused and interrupted
        __init_ just makes sure that all the things the player needs are available
        load and unload loads and unloads the track
        show shows the track,close closes the track after pause at end
        input-pressed receives user input while the track is playing.
    """
    
    mode_map ={'warp':Gtk.ContentFit.FILL,'fit':Gtk.ContentFit.CONTAIN,'shrink':Gtk.ContentFit.SCALE_DOWN,'clip':Gtk.ContentFit.COVER}
    
   

 
    def __init__(self,
                 show_id,
                 showlist,
                 root,
                 canvas,
                 show_params,
                 track_params ,
                 pp_dir,
                 pp_home,
                 pp_profile,
                 end_callback,
                 command_callback):

        # initialise items common to all players   
        Player.__init__( self,
                         show_id,
                         showlist,
                         root,
                         canvas,
                         show_params,
                         track_params ,
                         pp_dir,
                         pp_home,
                         pp_profile,
                         end_callback,
                         command_callback)


        # stopwatch for timing functions
        StopWatch.global_enable=False
        self.sw=StopWatch()
        self.sw.off()
        
        self.css=CSS()
        
        self.mon.trace(self,'')
        # and initialise things for this player
        # print 'imageplayer init'
        # get duration from profile
        if self.track_params['duration'] != '':
            self.duration_text= self.track_params['duration']
        else:
            self.duration_text= self.show_params['duration']
            
            
        # get  image window from profile
        if self.track_params['image-window'].strip() != '':
            self.image_window= self.track_params['image-window'].strip()
        else:
            self.image_window= self.show_params['image-window'].strip()

        if self.track_params['image-aspect-mode'].strip() != '':
            self.image_aspect_mode= self.track_params['image-aspect-mode'].strip()
        else:
            self.image_aspect_mode= self.show_params['image-aspect-mode'].strip()


        if self.track_params['pause-timeout'] != '':
            pause_timeout_text= self.track_params['pause-timeout']
        else:
            pause_timeout_text= self.show_params['pause-timeout']

        if pause_timeout_text.isdigit():
            self.pause_timeout= int(pause_timeout_text)
        else:
            self.pause_timeout=0



        self.track_image_obj=None
        self.tk_img=None
        self.paused=False
        self.pause_text_obj=None
        self.pause_timer= None

        # initialise the state machine
        self.play_state='initialised'    


            
    # LOAD - loads the images and text
    def load(self,track,loaded_callback,enable_menu):  
        # instantiate arguments
        self.track=track
        # print 'imageplayer load',self.track
        self.loaded_callback=loaded_callback   # callback when loaded
        self.mon.trace(self,'')


        Player.pre_load(self)
        #gtkdo is this removed for gtk?
        """
        # parse the image_window
        status,message,self.command,self.has_coords,self.window_x1,self.window_y1,self.window_x2,self.window_y2=self.parse_window(self.image_window)
        if status  == 'error':
            self.mon.err(self,'image window error, '+message+ ': '+self.image_window)
            self.play_state='load-failed'
            self.loaded_callback('error','image window error, '+message+ ': '+self.image_window)
            return
        """
        # load the plugin, this may modify self.track and enable the plugin drawing to canvas
        if self.track_params['plugin'] != '':
            status,message=self.load_plugin()
            if status == 'error':
                self.mon.err(self,message)
                self.play_state='load-failed'
                self.loaded_callback('error',message)
                return

        # parse the duration
        status,message,self.duration=Player.parse_duration(self.duration_text)
        if status  == 'error':
            self.mon.err(self, message)
            self.play_state='load-failed'
            self.loaded_callback('error',message)
            return


        # load the images and text
        status,message=Player.load_x_content(self,enable_menu)
        if status == 'error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            self.loaded_callback('error',message)
            return
        else:
            self.play_state='loaded'
            if self.loaded_callback is not None:
                self.loaded_callback('loaded','image track loaded')

            
    # UNLOAD - abort a load when sub-process is loading or loaded
    def unload(self):
        self.mon.trace(self,'')        
        # nothing to do for imageplayer
        self.mon.log(self,">unload received from show Id: "+ str(self.show_id))
        self.play_state='unloaded'
     
            

     # SHOW - show a track from its loaded state 
    def show(self,ready_callback,finished_callback,closed_callback):
                         
        # instantiate arguments
        self.ready_callback=ready_callback         # callback when ready to show an image - 
        self.finished_callback=finished_callback         # callback when finished showing 
        self.closed_callback=closed_callback            # callback when closed - not used by imageplayer

        self.mon.trace(self,'')
        
        # init state and signals  
        self.tick = 100 # tick time for image display (milliseconds)
        self.dwell = self.duration
        self.dwell_counter=0
        self.quit_signal=False
        self.paused=False
        self.pause_text_obj=None

        # do common bits
        Player.pre_show(self)
        
        # start show state machine
        self.start_dwell()


    # CLOSE - nothing to do in imageplayer - track content is removed by ready callback and hide
    def close(self,closed_callback):
        self.mon.trace(self,'')
        self.closed_callback=closed_callback
        self.mon.log(self,">close received from show Id: "+ str(self.show_id))
        if self.tick_timer!= None:
            GLib.source_remove(self.tick_timer)
            self.tick_timer=None
        self.play_state='closed'
        if self.closed_callback is not None:
            self.closed_callback('normal','imageplayer closed')


    def input_pressed(self,symbol):
        self.mon.trace(self,symbol)
        if symbol  == 'pause':
            self.pause()
        if symbol  == 'pause-on':
            self.pause_on()
        if symbol  == 'pause-off':
            self.pause_off()
        elif symbol == 'stop':
            self.stop()

      
    def pause(self):
        if self.paused is False: 
            self.paused = True
            if self.pause_timeout>0:
                # kick off the pause teimeout timer
                #print("!!toggle pause on")
                self.pause_timer=GLib.timout_add(self.pause_timeout*1000,self.pause_timeout_callback)
        else:
            self.paused=False
            # cancel the pause timer
            if self.pause_timer != None:
                #print("!!toggle pause off")
                GLib.source_remove(self.pause_timer)
                self.pause_timer=None


    def pause_timeout_callback(self):
        #print("!!callback pause off")
        self.pause_off()
        if self.pause_timer != None:
            GLib.source_remove(self.pause_timer)
            self.pause_timer=None


    def pause_on(self):
        self.paused = True
        #print("!!pause on")
        self.pause_timer=GLib.timeout_add(self.pause_timeout*1000,self.pause_timeout_callback)
 

    def pause_off(self):
        self.paused = False
        #print("!!pause off")
        # cancel the pause timer
        if self.pause_timer != None:
            GLib.source_remove(self.pause_timer)
            self.pause_timer=None
 

    def stop(self):
        # cancel the pause timer
        if self.pause_timer != None:
            GLib.source_remove(self.pause_timer)
            self.pause_timer=None
        self.quit_signal=True
        


        
# ******************************************
# Sequencing
# ********************************************

    def start_dwell(self):
        self.play_state='showing'
        self.tick_timer=GLib.timeout_add(self.tick, self.do_dwell)

        
    def do_dwell(self):
        if self.tick_timer is not None:
            GLib.source_remove(self.tick_timer)
            self.tick_timer=None
        if self.quit_signal is  True:
            self.mon.log(self,"quit received")
            if self.finished_callback is not None:
                self.mon.log(self,'pause_at_end, user quit or duration exceeded')
                self.finished_callback('pause_at_end','user quit or duration exceeded')
                # use finish so that the show will call close
        else:
            if self.paused is False:
                #print (self.dwell_counter,self.dwell)
                if self.dwell !=0:
                    self.dwell_counter=self.dwell_counter+1

            # one time flipping of pause text
            pause_text= self.track_params['pause-text']
            if self.paused is True and self.pause_text_obj is None:
                self.pause_text_obj=Gtk.Label()
                self.pause_text_obj.set_label(pause_text)
                self.pause_text_obj.set_name('pause-text')
                self.css.style_widget(self.pause_text_obj,'pause-text',color=self.track_params['pause-text-colour'],font=self.track_params['pause-text-font'])
                x,y=calculate_text_position(self.track_params['pause-text-x'],self.track_params['pause-text-y'],
                                             self.show_canvas_x1,self.show_canvas_y1,
                                             self.show_canvas_width,self.show_canvas_height,self.pause_text_obj)                
                self.canvas.put(self.pause_text_obj,x,y)

                
            if self.paused is False and self.pause_text_obj is not None:
                self.canvas.remove(self.pause_text_obj)
                self.pause_text_obj=None


            if self.dwell != 0 and self.dwell_counter == self.dwell:
                if self.finished_callback is not None:
                    self.mon.log(self,'pause_at_end, user quit or duration exceeded')
                    self.finished_callback('pause_at_end','user quit or duration exceeded')
                    # use finish so that the show will call close
            else:
                self.tick_timer=GLib.timeout_add(self.tick, self.do_dwell)
                return False



# *****************
# x content
# *****************          
                
    # called from Player, load_x_content      
            
    def load_track_content(self):
        if self.track=='':
            self.track_image_obj=None
            return 'normal','no track content to load'
        else:
            # get the track to be displayed
            if not os.path.exists(self.track) is True:
                return 'error','Track file not found '+ self.track

            status,message,x,y,width,height=self.parse_window(self.image_window)
            if status =='error':
                return 'error',message

            self.track_image_obj=Gtk.Picture.new_for_filename(self.track)
            self.track_image_obj.set_size_request(width,height)
            #gtkdo does this need a css selector
            self.track_image_obj.set_content_fit(ImagePlayer.mode_map[self.image_aspect_mode])
            self.canvas.put(self.track_image_obj,x,y)
            self.track_image_obj.set_visible(False)
            #print (self.image_aspect_mode,x,y,width,height)
            return 'normal','track content loaded'

                   
    def show_track_content(self):
        if self.track_image_obj!=None:
            self.track_image_obj.set_visible(True)


    def hide_track_content(self):
        if self.pause_text_obj is not None:
            self.canvas.remove(self.pause_text_obj)
            self.pause_text_obj=None
            # self.canvas.update_idletasks( )
        if self.track_image_obj!=None:
            self.track_image_obj.set_visible(False)
            self.canvas.remove(self.track_image_obj)
            self.track_image_obj=None

            
      

    
            

    
