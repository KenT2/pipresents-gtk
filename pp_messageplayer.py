
from pp_utils import StopWatch,calculate_text_position
from pp_player import Player
from pp_gtkutils import CSS
import os
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib
gi.require_version("WebKit", "6.0")
from gi.repository import WebKit


class MessagePlayer(Player):

    """ Displays a message on a canvas for a period of time. Message display can be  interrupted
          Differs from other players in that text is passed as parameter rather than file containing the text

        __init_ just makes sure that all the things the player needs are available
        load and unload loads and unloads the track
        show shows the track,close closes the track after pause at end
        input-pressed receives user input while the track is playing.
    """
    
 
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
        
        #self.css=CSS()

        self.mon.trace(self,'')
        # and initilise things for this player
        
        # get duration from profile
        if self.track_params['duration'] != "":
            self.duration_text= self.track_params['duration']
        else:
            self.duration_text= self.show_params['duration']       
        
        self.html_message_text_obj = None
        self.track_object=None
        
        # initialise the state machine
        self.play_state='initialised'    
            
            
    # LOAD - loads the images and text
    def load(self,text,loaded_callback,enable_menu):  
        # instantiate arguments
        self.track=text
        self.loaded_callback=loaded_callback   # callback when loaded
        self.mon.trace(self,'')
        


        # do common bits of  load
        Player.pre_load(self)   
        
        # parse the duration
        status,message,self.duration=Player.parse_duration(self.duration_text)
        if status  == 'error':
            self.mon.err(self, message)
            self.play_state='load-failed'
            self.loaded_callback('error',message)
            return

        # load the plugin, this may modify self.track and enable the plugin drawing to canvas
        if self.track_params['plugin'] != '':
            status,message=self.load_plugin()
            # can modify self.track with new text, does not touch message location
            if status == 'error':
                self.mon.err(self,message)
                self.play_state='load-failed'
                if self.loaded_callback is not  None:
                    self.loaded_callback('error',message)
                    return


        # load the images and text including message text
        status,message=self.load_x_content(enable_menu)
        if status == 'error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            if self.loaded_callback is not  None:
                self.loaded_callback('error',message)
                return
        
        self.play_state='loaded'
        if self.loaded_callback is not None:
            self.loaded_callback('loaded','message track loaded')

            
    # UNLOAD - abort a load when omplayer is loading or loaded
    def unload(self):
        self.mon.trace(self,'')
        # nothing to do for Messageplayer
        self.mon.log(self,">unload received from show Id: "+ str(self.show_id))
        self.play_state='unloaded'
     
            

     # SHOW - show a track from its loaded state 
    def show(self,ready_callback,finished_callback,closed_callback):
                         
        # instantiate arguments
        self.ready_callback=ready_callback         # callback when ready to show an image - 
        self.finished_callback=finished_callback         # callback when finished showing 
        self.closed_callback=closed_callback            # callback when closed - not used by Messageplayer

        self.mon.trace(self,'')
        # init state and signals  
        self.tick = 100 # tick time for image display (milliseconds)
        self.dwell = self.duration
        self.dwell_counter=0
        self.quit_signal=False

        # do common bits
        Player.pre_show(self)
        
        # start show state machine
        self.start_dwell()

    # CLOSE - nothing to do in messageplayer - x content is removed by ready callback
    def close(self,closed_callback):
        self.mon.trace(self,'')
        self.closed_callback=closed_callback
        self.mon.log(self,">close received from show Id: "+ str(self.show_id))
        if self.tick_timer!= None:
            GLib.source_remove(self.tick_timer)
        self.play_state='closed'
        if self.closed_callback is not None:
            self.closed_callback('normal','Messageplayer closed')


    def input_pressed(self,symbol):
        if symbol ==  'stop':
            self.stop()


    def stop(self):
        self.quit_signal=True
        


        
# ******************************************
# Sequencing
# ********************************************

    def start_dwell(self):
        self.play_state='showing'
        self.tick_timer=GLib.timeout_add(self.tick, self.do_dwell)

        
    def do_dwell(self):
        GLib.source_remove(self.tick_timer)
        self.tick_timer=None
        if self.quit_signal  is   True:
            self.mon.log(self,"quit received")
            if self.finished_callback is not None:
                self.finished_callback('pause_at_end','user quit or duration exceeded')
                # use finish so that the show will call close
        else:
            if self.dwell !=0:
                self.dwell_counter=self.dwell_counter+1

            if self.dwell != 0 and self.dwell_counter ==  self.dwell:
                if self.finished_callback is not None:
                    self.finished_callback('pause_at_end','user quit or duration exceeded')
                    # use finish and pause_at_end so that the show will call close
            else:
                self.tick_timer=GLib.timeout_add(self.tick, self.do_dwell)

# *****************
# x content
# *****************    



    # called from Player, load_x_content       
    def load_track_content(self):
        # load message text

            
        self.message_html_background_colour= self.track_params['message-html-background-colour']
        if self.track_params['message-html-width'] == '':
            self.message_html_width=self.show_canvas_x2-self.show_canvas_x1
        else:
            self.message_html_width=self.track_params['message-html-width']
            
        if self.track_params['message-html-height'] == '':
            self.message_html_height=self.show_canvas_y2-self.show_canvas_y1
        else:
            self.message_html_height=self.track_params['message-html-height']
            
        self.message_text_type=self.track_params['message-text-type']
        
        if self.track_params['message-text-location'] != '':
            text_path=self.complete_path(self.track_params['message-text-location'])
            if not os.path.exists(text_path):
                return 'error',"Message Text file not found "+ text_path,''
            with open(text_path) as f:
                message_text=f.read()
        else:
            message_text= self.track
                        
    
        if message_text=='':
            self.track_object=None
            return 'normal','no message to load'
        else:
        
            if self.message_text_type=='html':
                if self.track_params['message-text-location'] == '':
                    with open('/tmp/html_text.html','w') as f:
                        f.write(message_text)
                self.track_object=WebKit.WebView()
                color = Gdk.RGBA()
                color.parse(self.message_html_background_colour)
                self.track_object.set_background_color(color)
                self.track_object.set_size_request(int(self.message_html_width),int(self.message_html_height))
                x,y=calculate_text_position(self.track_params['message-x'],self.track_params['message-y'],
                                     self.show_canvas_x1,self.show_canvas_y1,                                    
                                     self.show_canvas_width,self.show_canvas_height,self.track_object)

                self.canvas.put(self.track_object,x,y)        
                self.track_object.set_visible(False)
                if message_text !='' and self.message_text_type=='html':
                    self.track_object.load_html(message_text,'file:/tmp/html_text.html')
                else:  
                    self.track_object.load_html(message_text,'file:/'+text_path)
            else:
                self.track_object=Gtk.Label()
                self.track_object.set_label(message_text.rstrip('\n'))
                self.track_object.set_name('message-text')
                self.track_object.set_justify(CSS.justify_map[self.track_params['message-justify']])
                if self.track_params['message-colour']=='':
                    return 'error','Message Text Colour is blank'
                if self.track_params['message-font']=='':
                    return 'error','Message Text Font is blank'
                self.css.style_widget(self.track_object,'message-text',color=self.track_params['message-colour'],font=self.track_params['message-font'])
                x,y=calculate_text_position(self.track_params['message-x'],self.track_params['message-y'],
                                         self.show_canvas_x1,self.show_canvas_y1,
                                         self.show_canvas_width,self.show_canvas_height,self.track_object)
                self.canvas.put(self.track_object,x,y)
                self.track_object.set_visible(False)
        return 'normal','message loaded'
    

    def show_track_content(self):
        #print ('showing message')
        self.mon.log(self,">show received from show Id: "+ str(self.show_id))
        if self.track_object!=None:
            self.track_object.set_visible(True)


    def hide_track_content(self):
        self.mon.log(self,">hide received from show Id: "+ str(self.show_id))
        if self.track_object!= None:
            self.track_object.set_visible(False)
            self.canvas.remove(self.track_object)



    
