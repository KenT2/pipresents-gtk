
import os
import copy
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib

from pp_mpvdriver import MPVDriver
from pp_player import Player
from pp_utils import  Monitor
from pp_displaymanager import DisplayManager
from pp_audiomanager import AudioManager
from pp_gtkutils import CSS


# NO display name
# no layer
# no 
# warp --video-aspect-override=4:3  -1 to disable


class MPVPlayer(Player):
    """
    plays a track using MPVplayer
    _init_ iniitalises state and checks resources are available.
    use the returned instance reference in all other calls.
    At the end of the path (when closed) do not re-use, make instance= None and start again.
    States - 'initialised' when done successfully
    Initialisation is immediate so just returns with error code.
    """

    _LEFT = "fl"
    _RIGHT = "fr"
    _STEREO = "fl-fr"
    _FIVEPONE = "5.1"
    
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
        # print ' !!!!!!!!!!!videoplayer init'
        self.mon.trace(self,'')
    
        
        # output device
        #print ('tack ',self.track_params['mpv-audio'],'show',self.show_params['mpv-audio'])
        if self.track_params['mpv-audio'] != "":
            self.mpv_audio= self.track_params['mpv-audio']
        else:
            self.mpv_audio= self.show_params['mpv-audio']
            
        self.mpv_max_volume_text= self.track_params['mpv-max-volume']
        
        if self.track_params['mpv-volume'] != "":
            self.mpv_volume_text= self.track_params['mpv-volume']
        else:
            self.mpv_volume_text= self.show_params['mpv-volume']

        if self.track_params['mpv-window'] != '':
            self.mpv_window= self.track_params['mpv-window']
        else:
            self.mpv_window= self.show_params['mpv-window']
            
        if self.track_params['mpv-aspect-mode'] != '':
            self.mpv_aspect_mode= self.track_params['mpv-aspect-mode']
        else:
            self.mpv_aspect_mode= self.show_params['mpv-aspect-mode']

        
        if  self.track_params['mpv-speaker'] != "":
            self.mpv_speaker= self.track_params['mpv-speaker']
        else:
            self.mpv_speaker= self.show_params['mpv-speaker']

        

        if self.mpv_speaker == 'left':
            self.speaker_option=MPVPlayer._LEFT
        elif self.mpv_speaker == 'right':
            self.speaker_option=MPVPlayer._RIGHT
        elif self.mpv_speaker == '5.1':
            self.speaker_option=MPVPlayer._FIVEPONE
        else:
            self.speaker_option=MPVPlayer._STEREO

            
        if self.track_params['mpv-other-options'] != '':
            self.mpv_other_options= self.track_params['mpv-other-options']
        else:
            self.mpv_other_options= self.show_params['mpv-other-options']
            
        # FREEZING
        if self.track_params['mpv-freeze-at-start'] != '':
            self.freeze_at_start= self.track_params['mpv-freeze-at-start']
        else:
            self.freeze_at_start= self.show_params['mpv-freeze-at-start']

        if self.track_params['mpv-freeze-at-end'] != '':
            self.freeze_at_end= self.track_params['mpv-freeze-at-end']
        else:
            self.freeze_at_end= self.show_params['mpv-freeze-at-end']
            
        if self.track_params['pause-timeout'] != '':
            self.pause_timeout_text= self.track_params['pause-timeout']
        else:
            self.pause_timeout_text= self.show_params['pause-timeout']
        
        self.dm=DisplayManager()
        self.am=AudioManager() 
        
        #css provider
        self.css=CSS() 
        
        # initialise video playing state and signals
        self.quit_signal=False
        self.unload_signal=False
        self.play_state='initialised'
        self.frozen_at_end=False
        self.pause_timer=None      
        return
    
    def process_params(self):
        
        self.options=[]
        
        self.add_option('input-default-bindings','no')
        self.add_option('input-vo-keyboard','no')
        self.add_option('osc','no')
        
            
        # AUDIO
        #print (self.mpv_audio)
        self.audio_sys=self.am.get_audio_sys()
        if self.audio_sys == 'pulse':
            status,message,self.mpv_sink = self.am.get_sink(self.mpv_audio)
            if status == 'error':
                return status,message
            #print(self.mpv_audio,self.mpv_sink)
                    
            if not self.am.sink_connected(self.mpv_sink):
                self.mon.err(self,'"'+self.mpv_audio +'"audio device not connected\n\n    Expected sink is: '+ self.mpv_sink)
                return 'error',self.mpv_audio +'audio device not connected'
                    
            self.add_option('ao','pulse')
        else:
            self.mon.err(self,'audio systems other than pulseaudio are not supported' )
            return 'error','audio systems other than pulseaudio are not supported' 

                
        #AUDIO SPEAKER
        self.add_option('audio-channels',self.speaker_option)   #fl-fr
                
        # AUDIO DEVICE
        #print (self.mpv_audio,self.mpv_sink)
        self.add_option ('audio-device','pulse/'+self.mpv_sink)
        
        # VOLUME
        if self.mpv_volume_text != "":
            self.mpv_volume= int(self.mpv_volume_text)
        else:
            self.mpv_volume=100
            
        # MAX VOLUME
        if self.mpv_max_volume_text != "":
            if not self.mpv_max_volume_text.isdigit():
                return 'error','mpv Max Volume must be a positive integer: '+self.mpv_max_volume_text
            self.max_volume= int(self.mpv_max_volume_text)
            if self.max_volume>100:
                return 'error','mpv Max Volume must be <= 100: '+ self.mpv_max_volume_text                
        else:
            self.max_volume=100
            
        self.initial_volume=min(self.mpv_volume,self.max_volume)
        self.volume=self.initial_volume
        
        
        # SUBTITLES
        self.mpv_subtitles=self.track_params['mpv-subtitles']
        if self.mpv_subtitles =='yes':
            self.add_option('sid','auto')
        else:
            self.add_option('sid','no')
            
        # DISPLAY
        if self.track_params['mpv-video-display']!='':
            video_display_name=self.track_params['mpv-video-display']
            if video_display_name == self.show_canvas_display_name:
                self.mon.warn(self,'alternate video display is the same as video display')
            #print (video_display_name)
            status,message,dummy=self.dm.is_display_connected(video_display_name)
            if status == 'error':
                return 'error',message            
            self.video_canvas=self.dm.get_canvas_obj(video_display_name)
            self.x=0
            self.y=0
            self.width,self.height=self.dm.get_canvas_dimensions(video_display_name)

        else:
            video_display_name = self.show_canvas_display_name
            # Is it valid and connected
            status,message,self.display_name=self.dm.is_display_connected(video_display_name)
            if status == 'error':
                return 'error',message            
            self.video_canvas=self.canvas 
                       
            # VIDEO WINDOW
            #print (self.mpv_window)     
            status,message,self.x,self.y,self.width,self.height=self.parse_window(self.mpv_window)
            if status=='error':
                return status,message

            #print (self.mpv_window,self.x,self.y,self.width,self.height,self.mpv_aspect_mode)
            
            # ASPECT MODE
            if self.mpv_aspect_mode == 'warp':
                self.add_option('video-aspect-override',str(self.width)+':'+str(self.height))
            elif self.mpv_aspect_mode == 'fit':
                self.add_option('video-aspect-override','-1')
            elif self.mpv_aspect_mode == 'shrink':
                self.add_option('video-unscaled','downscale-big')
            elif self.mpv_aspect_mode == 'clip':
                #self.add_option('panscan','0.5')
                #self.add_option('video-scale-x',str(self.width/576))
                #self.add_option('video-scale-y',str(self.height/576))
                #print ((self.height/576)*576)
                #self.add_option('vf', 'scale=720:720')
                
                #this seems to work but leaves a thin black line. Need to get video size first
                #self.add_option('vf', 'lavfi=[crop=576:576]')
                self.mon.warn(self,'Clip MPV Video Aspect Mode not implemented')                                
                #clip_text=str(self.width)+'x'+str(self.height)    #+'+'+str(self.x)+'+'+str(self.y)
                #print (clip_text)
                #self.add_option('video-crop',clip_text)


        # OTHER OPTIONS
        status,message=self.parse_options(self.track_params['mpv-other-options'])
        if status == 'error':
            self.mon.err(self,message)
            return status,message
            #self.play_state='load-failed'
            #if self.loaded_callback is not  None:
                #self.loaded_callback('error',message)
                #return

        
        # PAUSE TIMEOUT
        if self.pause_timeout_text.isdigit():
            self.pause_timeout= int(self.pause_timeout_text)
        else:
            self.pause_timeout=0
            
        return 'normal',''

    def add_option(self,option,val):
        opt=[option,val]
        #print (option,val)
        self.options.append(opt)
        

   # LOAD - creates a mpv instance, loads a track and then pause
    def load(self,track,loaded_callback,enable_menu):  
        # instantiate arguments
        self.track=track
        self.loaded_callback=loaded_callback   #callback when loaded
        self.mon.log(self,"Load track received from show Id: "+ str(self.show_id) + ' ' +self.track)
        self.mon.trace(self,'')
        
        # do common bits of  load
        Player.pre_load(self) 
        
        # load the plugin, this may modify self.track and enable the plugin drawing to canvas
        if self.track_params['plugin'] != '':
            status,message=self.load_plugin()
            if status == 'error':
                self.mon.err(self,message)
                self.play_state='load-failed'
                if self.loaded_callback is not  None:
                    self.loaded_callback('error',message)
                    return
                    
        # load the images and text
        status,message=self.load_x_content(enable_menu)
        if status == 'error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            if self.loaded_callback is not  None:
                self.loaded_callback('error',message)
                return
                
        self.start_state_machine_load()


    def load_track_content(self):
        #process mpv parameters
        status,message=self.process_params()
        if status == 'error':
            return status,message

        # check file exists if not a mrl
        if not ':'in self.track:        
            if not os.path.exists(self.track):
                return 'error',"Track file not found: "+ self.track

        self.mpvdriver = MPVDriver(self.root,self.video_canvas,self.freeze_at_start,self.freeze_at_end,self.background_colour)

        # load the media
        self.mpvdriver.load(self.track,self.options,self.x,self.y,self.width,self.height)

        return 'normal','mpv track loaded'



     # SHOW - show a track      
    def show(self,ready_callback,finished_callback,closed_callback):
        self.ready_callback=ready_callback         # callback when paused after load ready to show video
        self.finished_callback=finished_callback         # callback when finished showing
        self.closed_callback=closed_callback

        self.mon.trace(self,'')

        #  do animation at start and ready_callback which closes+hides the previous track
        Player.pre_show(self)
        
        # start show state machine
        self.start_state_machine_show()



    # UNLOAD - abort a load when mpvdriver is loading or loaded
    def unload(self):
        self.mon.trace(self,'')
        self.mon.log(self,">unload received from show Id: "+ str(self.show_id))
        self.start_state_machine_unload()


    # CLOSE - quits mpvdriver from 'pause at end' state
    def close(self,closed_callback):
        self.mon.trace(self,'')
        self.mon.log(self,">close received from show Id: "+ str(self.show_id))
        self.closed_callback=closed_callback
        self.start_state_machine_close()





# ***********************
# track showing state machine
# **********************

    """
    STATES OF STATE MACHINE
    Threre are ongoing states and states that are set just before callback

    >init - Create an instance of the class
    <On return - state = initialised   -  - init has been completed, do not generate errors here

    >load
        Fatal errors should be detected in load. If so  loaded_callback is called with 'load-failed'
         Ongoing - state=loading - load called, waiting for load to complete   
    < loaded_callback with status = normal
         state=loaded - load has completed and video paused before or after first frame      
    <loaded_callback with status=error
        state= load-failed -  failure to load   

    On getting the loaded_callback with status=normal the track can be shown using show


    >show
        show assumes a track has been loaded and is paused.
       Ongoing - state=showing - video is showing 
    <finished_callback with status = pause_at_end
            state=showing but frozen_at_end is True
    <closed_callback with status= normal
            state = closed - video has ended mpv has terminated.


    On getting finished_callback with status=pause_at end a new track can be shown and then use close to close the previous video when new track is ready
    On getting closed_callback with status=  nice_day mpvdriver closing should not be attempted as it is already closed
    Do not generate user errors in Show. Only generate system errors such as illegal state and then use end()

    >close
       Ongoing state - closing - mpvdriver processes are dying
    <closed_callback with status= normal - mpvdriver is dead, can close the track instance.

    >unload
        Ongoing states - start_unload and unloading - mpvdriver processes are dying.
        when unloading is complete state=unloaded
        I have not added a callback to unload. its easy to add one if you want.

    closed is needed because wait_for_end in pp_show polls for closed and does not use closed_callback
    
    """


    def start_state_machine_load(self):
        # initialise all the state machine variables
        self.play_state='loading'
        self.tick_timer=GLib.timeout_add(1, self.load_state_machine) #50
        
    def load_state_machine(self):
        if self.tick_timer is not None:
            GLib.source_remove(self.tick_timer)
            self.tick_timer=None
        if self.unload_signal is True:
            self.unload_signal=False
            self.state='unloading'
            self.mpvdriver.unload()
            GLib.timeout_add(100,self.load_state_machine)
            return False
        else:
            resp=self.mpvdriver.get_state()
            # pp_mpvdriver changes state from load-loading when track is frozen at start.
            if resp == 'load-fail':
                self.play_state = 'load-failed'
                self.mon.log(self,"      Entering state : " + self.play_state + ' from show Id: '+ str(self.show_id))
                if self.loaded_callback is not  None:
                    self.loaded_callback('error','timeout when loading mpv track')
                return
            elif resp=='load-unloaded':
                self.play_state = 'unloaded'
                self.mon.log(self,"      Entering state : " + self.play_state + ' from show Id: '+ str(self.show_id))
                # PP does not need this callback
                #if self.loaded_callback is not  None:
                    #self.loaded_callback('normal','unloaded')
                return            
            elif resp in ('load-ok','load-frozen'):
                # stop received while in freeze-at-start - quit showing as soon as it starts
                #if resp=='stop-frozen':
                    #self.quit_signal= True
                    #self.mon.log(self,'stop received while in freeze-at-start')
                self.play_state = 'loaded'
                #if self.mpv_sink!='':
                    #self.set_device(self.mpv_sink)
                #else:
                    #self.set_device('')   
                self.mon.log(self,"      Entering state : " + self.play_state + ' from show Id: '+ str(self.show_id))
                if self.loaded_callback is not  None:
                    self.loaded_callback('normal','loaded')
                return
            else:
                self.tick_timer=GLib.timeout_add(10,self.load_state_machine) #100
                return False
            

    def start_state_machine_unload(self):
        # print ('mpvplayer - starting unload',self.play_state)
        if self.play_state in('closed','initialised','unloaded'):
            # mpvdriver already closed
            self.play_state='unloaded'
            # print ' closed so no need to unload'
        else:
            if self.play_state  ==  'loaded':
                # load already complete so set unload signal and kick off load state machine
                self.play_state='start_unload'
                self.unload_signal=True
                self.tick_timer=GLib.timeout_add(50, self.load_state_machine)
                
            elif self.play_state == 'loading':
                # signal load state machine to start_unloading state and stop mpvdriver
                self.unload_signal=True
            else:
                self.mon.err(self,'illegal state in unload method: ' + self.play_state)
                self.end('error','illegal state in unload method: '+ self.play_state)           


            
    def start_state_machine_show(self):
        if self.play_state == 'loaded':
            self.play_state='showing'
            
            # show the track
            self.mpvdriver.show(self.initial_volume)
            self.mon.log (self,'>showing track from show Id: '+ str(self.show_id))  
            # and start polling for state changes
            self.tick_timer=GLib.timeout_add(0, self.show_state_machine)
            """
            # race condition don't start state machine as unload in progress
            elif self.play_state == 'start_unload':
                pass
            """
        else:
            self.mon.fatal(self,'illegal state in show method ' + self.play_state)
            self.play_state='show-failed'
            if self.finished_callback is not None:
                self.finished_callback('error','illegal state in show method: ' + self.play_state)


    def show_state_machine(self):
        if self.tick_timer is not None:
            GLib.source_remove(self.tick_timer)
            self.tick_timer=None
        if self.play_state=='showing':
            if self.quit_signal is True:
                # service any queued stop signals by sending stop to mpvdriver
                self.quit_signal=False
                self.mon.log(self,"      stop video - Send stop to mpvdriver")
                self.mpvdriver.stop()
                self.tick_timer=GLib.timeout_add(10, self.show_state_machine)
                return False
            else:
                resp=self.mpvdriver.get_state()
                #print (resp)
                # driver changes state from show-showing depending on freeze-at-end.
                if resp == 'show-pauseatend':
                    self.mon.log(self,'mpvdriver says pause_at_end')
                    self.frozen_at_end=True
                    if self.finished_callback is not None:
                        self.finished_callback('pause_at_end','pause at end')
                        
                elif resp == 'show-niceday':
                    self.mon.log(self,'mpvdriver says nice_day')
                    self.play_state='closing'
                    self.mpvdriver.close()
                    self.tick_timer=GLib.timeout_add(10, self.show_state_machine)
                    return False
                                        
                elif resp=='show-fail':
                    self.play_state='show-failed'
                    if self.finished_callback is not None:
                        self.finished_callback('error','pp_mpvdriver says showing failed: '+ self.play_state)
                else:
                    self.tick_timer=GLib.timeout_add(30,self.show_state_machine)
                    return False
                    
        elif self.play_state=='closing':
            self.play_state='closed'
            # state change needed for wait for end
            self.mon.log(self,"      Entering state : " + self.play_state + ' from show Id: '+ str(self.show_id))
            if self.closed_callback is not  None:
                self.closed_callback('normal','mpvdriver closed')             

    # respond to normal stop
    def stop(self):
        self.mon.log(self,">stop received from show Id: "+ str(self.show_id))
        # cancel the pause timer
        if self.pause_timer != None:
            GLib.source_remove(self.pause_timer)
            self.pause_timer=None
        self.mpvdriver.stop()


    def start_state_machine_close(self):
        # self.mon.log(self,">close received from show Id: "+ str(self.show_id))
        # cancel the pause timer
        if self.pause_timer != None:
            GLib.source_remove(self.pause_timer)
            self.pause_timer=None
        self.mpvdriver.close()
        self.play_state='closing'
        #print ('start close state machine close')
        self.tick_timer=GLib.timeout_add(0, self.show_state_machine)



# ************************
# COMMANDS
# ************************

    def input_pressed(self,symbol):
        print ('mpv',symbol)
        if symbol == 'inc-volume':
            self.inc_volume()
        elif symbol == 'dec-volume':
            self.dec_volume()            
        elif symbol  == 'pause':
            self.pause()
        elif symbol  == 'go':
            self.go()
        elif symbol  == 'unmute':
            self.unmute()
        elif symbol  == 'mute':
            self.mute()
        elif symbol  == 'pause-on':
            self.pause_on()    
        elif symbol  == 'pause-off':
            self.pause_off()
        elif symbol == 'stop':
            self.stop()


    def inc_volume(self):
        self.mon.log(self,">inc-volume received from show Id: "+ str(self.show_id))
        if self.play_state  == 'showing':
            if self.volume < self.max_volume:
                self.volume+=1
            self.set_volume(self.volume)
            return True
        else:
            self.mon.log(self,"!<inc-volume rejected " + self.play_state)
            return False

    def dec_volume(self):
        self.mon.log(self,">dec-volume received from show Id: "+ str(self.show_id))

        if self.play_state  == 'showing':
            if self.volume > 0:
                self.volume-=1
            self.set_volume(self.volume)
            return True
        else:
            self.mon.log(self,"!<dec-volume rejected " + self.play_state)
            return False

    def set_volume(self,vol):
        # print ('SET VOLUME',vol)
        self.mpvdriver.set_volume(vol)
        


    def mute(self):
        self.mon.log(self,">mute received from show Id: "+ str(self.show_id))
        self.mpvdriver.mute()
        return True        
                

    def unmute(self):
        self.mon.log(self,">unmute received from show Id: "+ str(self.show_id))
        self.mpvdriver.unmute()


    # ???? why no test if already paused or unpaused
    # toggle pause
    def pause(self):
        self.mon.log(self,">toggle pause received from show Id: "+ str(self.show_id))
        reply=self.mpvdriver.pause()
        if reply == 'pause-on-ok':
            if self.pause_timeout>0:
                # kick off the pause timeout timer
                self.pause_timer=GLib.timeout_add(self.pause_timeout*1000,self.pause_timeout_callback)
            return True
        elif reply == 'pause-off-ok':
            if self.pause_timer != None:
                # cancel the pause timer
                GLib.source_remove(self.pause_timer)
                self.pause_timer=None
            return True
        else:
            self.mon.log(self,"!<toggle pause rejected " + self.play_state)
            return False              
            

    def pause_timeout_callback(self):
        self.pause_off()
        GLib.source_remove(self.pause_timer)
        self.pause_timer=None

    # pause on
    def pause_on(self):
        self.mon.log(self,">pause on received from show Id: "+ str(self.show_id))
        reply=self.mpvdriver.pause_on()
        if reply == 'pause-on-ok':
            if self.pause_timeout>0:
                # kick off the pause timeout timer
                self.pause_timer=GLib.timeout_add(self.pause_timeout*1000,self.pause_timeout_callback)
            return True
        else:
            self.mon.log(self,"!<pause on rejected " + self.play_state)
            return False

    # pause off
    def pause_off(self):
        self.mon.log(self,">pause off received from show Id: "+ str(self.show_id))
        reply=self.mpvdriver.pause_off()
        if reply == 'pause-off-ok':
            if self.pause_timer != None:
                # cancel the pause timer
                GLib.source_remove(self.pause_timer)
                self.pause_timer=None
            return True
        else:
            self.mon.log(self,"!<pause off rejected " + self.play_state)
            return False

    # go after freeze at start
    def go(self):
        reply=self.mpvdriver.go(self.initial_volume)
        if reply == 'go-ok':
            return True
        else:
            self.mon.log(self,"!<go rejected " + self.play_state)
            return False



    def parse_options(self,text):
        if text.strip() == '':
            return 'normal',''
        options=text.split(',')
        print (options)
        for option in options:
            if option.count('=') !=1:
                return 'error','malformed option: '+ option
            result=option.split('=')
            self.add_option(result[0].strip(),result[1].strip())
        return 'normal',''


# *****************************
# SETUP
# *****************************


        
