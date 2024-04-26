import os
import copy
from pp_player import Player
from pp_displaymanager import DisplayManager
from pp_gtkutils import CSS
from pp_utils import parse_rectangle
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib
gi.require_version("WebKit", "6.0")
from gi.repository import WebKit


class WebKitPlayer(Player):

# ***************************************
# EXTERNAL COMMANDS
# ***************************************

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

        self.mon.trace(self,'')
        
        #self.css=CSS
        
        # and initialise things for this player        
        self.dm=DisplayManager()
        
        # get duration limit (secs ) from profile
        if self.track_params['duration'] != '':
            self.duration_text=self.track_params['duration']
        else:
            self.duration_text= self.show_params['duration']

        # process webkit window                  
        if self.track_params['webkit-window'] != '':
            self.webkit_window_text= self.track_params['webkit-window']
        else:
            self.webkit_window_text= self.show_params['webkit-window']

        # process webkit things                  
        if self.track_params['webkit-freeze-at-end'] != '':
            self.freeze_at_end= self.track_params['webkit-freeze-at-end']
        else:
            self.freeze_at_end= self.show_params['webkit-freeze-at-end']
        #print ('track',self.track_params['webkit-freeze-at-end'],'show',self.show_params['webkit-freeze-at-end'])
        if self.track_params['webkit-zoom'] != '':
            self.webkit_zoom_text= self.track_params['webkit-zoom']
        else:
            self.webkit_zoom_text= self.show_params['webkit-zoom']
        self.zoom=float(self.webkit_zoom_text)

        # Initialize variables
        self.command_timer=None
        self.show_timer=None
        self.load_timer=None
        self.quit_signal=False     # signal that user has pressed stop
        self.webview=None
        # initialise the play state
        self.play_state='initialised'
        self.load_state=''


    # LOAD - loads the browser and show stuff
    def load(self,track,loaded_callback,enable_menu):  
        # instantiate arguments
        self.track=track
        self.loaded_callback=loaded_callback   # callback when loaded
        self.mon.trace(self,'')

        #parse duration
        status,message,duration100=Player.parse_duration(self.duration_text)
        if status =='error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            if self.loaded_callback is not  None:
                self.loaded_callback('error',message)
                return
        self.duration=2*duration100

        # Is display valid and connected
        status,message,self.display_name=self.dm.is_display_connected(self.show_canvas_display_name)
        if status == 'error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            if self.loaded_callback is not  None:
                self.loaded_callback('error',message)
                return



        # does media exist    
        if not ':' in self.track:
            if not os.path.exists(self.track):
                self.mon.err(self, 'cannot find file; '+self.track )
                self.play_state='load-failed'
                if self.loaded_callback is not  None:
                    self.loaded_callback('error','cannot find file; '+self.track )
                    return
                    

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

                     
        # parse browser commands to self.command_list
        reason,message=self.parse_commands(self.track_params['browser-commands'])
        if reason == 'error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            if self.loaded_callback is not  None:
                self.loaded_callback('error',message)
                return


        # start loading the browser
        self.play_state='loading'


        # load the images and text
        status,message=self.load_x_content(enable_menu)
        # includes creating the browser and loading the web track
        if status == 'error':
            self.mon.err(self,message)
            self.play_state='load-failed'
            if self.loaded_callback is not  None:
                self.loaded_callback('error',message)
                return
        #print ('end of load')
        self.load_timer=GLib.timeout_add(10,self.load_state_machine)
        
        
    #gtkdo need load timeout  
    def load_state_machine(self):  
        if self.load_timer!=None:
            GLib.source_remove(self.load_timer)
            self.load_timer=None
        if self.webview.is_loading():
            #print ('waiting for browser',self.webview.is_loading())
            self.load_timer=GLib.timeout_add(50, self.load_state_machine)
            return
        else:
            self.play_state='loaded'
            # and start executing the browser commands
            self.play_commands()
            self.mon.log(self,"      State machine: webkit and url loaded")
            if self.loaded_callback is not None:
                self.loaded_callback('normal','webkit loaded')
            return

    def load_track_content(self):
        #create the browser and start loading a url, called from Player

        status,message,self.x,self.y,width,height=self.parse_window(self.webkit_window_text)
        if status =='error':
            return 'error',message
        #print ('load track content')
        self.webview=WebKit.WebView()
        self.webview.set_size_request(width,height)
        self.webview.set_zoom_level(self.zoom)
        self.canvas.put(self.webview,self.x,self.y)        
        self.webview.set_visible(False)
        self.driver_get(self.track) 
        self.mon.log (self,'Loading browser from show Id: '+ str(self.show_id))
        return 'normal',''

    def show_track_content(self):
        #print ('show track content')
        if self.webview!=None:
            #self.canvas.put(self.webview,self.x,self.y)
            self.webview.set_visible(True)
            pass


    def hide_track_content(self):
        if self.webview!=None:
            self.webview.set_visible(False)
            self.canvas.remove(self.webview)
            self.webview=None


    # UNLOAD - abort a load when browser is loading or loaded
    def unload(self):
        self.mon.trace(self,'')
        self.mon.log(self,">unload received from show Id: "+ str(self.show_id))
        self.webview.stop_loading()
        self.play_state = 'closed'


         
     # SHOW - show a track from its loaded state 
    def show(self,ready_callback,finished_callback,closed_callback):
                         
        # instantiate arguments
        self.ready_callback=ready_callback         # callback when ready to show a web page- 
        self.finished_callback=finished_callback         # callback when finished showing  - not used
        self.closed_callback=closed_callback            # callback when closed

        self.mon.trace(self,'')
        self.play_state='showing'        
        # init state and signals  
        self.quit_signal=False
        # do common bits
        Player.pre_show(self)
        self.duration_count=self.duration
        #print ('SHOW',self.webview.is_loading())
        #self.show_state_machine()
        #self.driver_get(self.track)
        self.show_timer=GLib.timeout_add(10, self.show_state_machine)

        
    def show_state_machine(self):
        #print ('state machine',self.play_state)
        if self.show_timer!=None:
            GLib.source_remove(self.show_timer)
            self.show_timer=None
        if self.play_state == 'showing':
            self.duration_count -= 1
            # self.mon.log(self,"      Show state machine: " + self.show_state)
            
            # service any queued stop signals and test duration count
            if self.quit_signal is True or (self.duration != 0 and self.duration_count == 0):
                self.mon.log(self,"      Service stop required signal or timeout")
                if self.command_timer != None:
                    GLib.source_remove(self.command_timer)
                    self.command_timer=None
                if self.quit_signal is True:
                    self.quit_signal=False
                #print ('freeze',self.freeze_at_end)
                if self.freeze_at_end =='yes':
                    self.mon.log(self,'webkit says pause_at_end')
                    if self.finished_callback is not None:
                        self.finished_callback('pause_at_end','pause at end')
                        #self.show_timer=GLib.timeout_add(50, self.show_state_machine)
                else:
                    self.mon.log(self,'webkit says niceday')
                    self.hide_track_content()
                    self.play_state='closed'
                    if self.closed_callback is not  None:
                        self.closed_callback('normal','webkitdriver closed')
                    return
            else:
                #print ('state machine repeat')
                self.show_timer=GLib.timeout_add(50, self.show_state_machine)

                    
    # CLOSE - nothing to do in browserplayer - x content is removed by ready callback and hide browser does not implement pause_at_end
    def close(self,closed_callback):
        self.mon.trace(self,'')
        self.closed_callback=closed_callback
        self.mon.log(self,">close received from show Id: "+ str(self.show_id))
        self.hide_track_content()
        self.play_state='closed'
        if self.closed_callback is not None:
            self.closed_callback('normal','webkit player closed')



    def input_pressed(self,symbol):
        self.mon.trace(self,symbol)
        if symbol == 'pause':
            self.pause()
        elif symbol == 'pause-on':
            self.pause_on()
        elif symbol == 'pause-off':
            self.pause_off()
        elif symbol=='stop':
            self.stop()

    # browsers do not do pause
    def pause(self):
        self.mon.log(self,"!<pause rejected")
        return False

    # browsers do not do pause
    def pause_on(self):
        self.mon.log(self,"!<pause on rejected")
        return False

    # browsers do not do pause
    def pause_off(self):
        self.mon.log(self,"!<pause off rejected")
        return False
        

    # respond to normal stop
    def stop(self):
        # send signal to stop the track to the state machine
        self.mon.log(self,">stop received")
        self.quit_signal=True

# ***********************
# veneer for controlling chromium browser
# ***********************

    def driver_close(self):
        self.canvas.remove(self.webview)

    def driver_refresh(self):
        self.webview.reload()
            
    def driver_get(self,url):
        self.mon.log(self,'load: '+url)
        if ':' in url:
            self.webview.load_uri(url)
        else:
            f = open(url, "r")
            self.webview.load_html(f.read(),'file:/'+url)
        return 'normal',''

        

            
# *******************   
# browser commands
# ***********************

    def parse_commands(self,command_text):
        self.command_list=[]
        self.max_loops=-1      #loop continuous if no loop command
        lines = command_text.split('\n')
        for line in lines:
            if line.strip() == '':
                continue
            #print (line)
            reason,entry=self.parse_command(line)
            if reason != 'normal':
                return 'error',entry
            self.command_list.append(copy.deepcopy(entry))
            
        num_loops=0
        for entry in self.command_list:
            if entry[0]=='loop':
                num_loops+=1
            if num_loops>1:
                return 'error', str(num_loops) + ' loop commands in browser commands'
        return 'normal',''

    def parse_command(self,line):
        fields = line.split()
        #print (fields)
        if len(fields) not in (1,2):
            return 'error',"incorrect number of fields in command: " + line
        command=fields[0]
        arg=''
        
        if command not in ('load','refresh','wait','loop'):
            return 'error','unknown browser command: '+ line
            
        if command in ('refresh',) and len(fields) !=1:
            return 'error','incorrect number of fields for '+ command + 'in: ' + line
            
        if command in ('refresh',):
            return 'normal',[command,'']
            
        if command == 'load':
            if len(fields)!=2:
                return 'error','incorrect number of fields for '+ command + 'in: ' + line

            arg=fields[1]
            track=self.complete_path(arg)
            # does media exist    
            if not ':' in track:
                if not os.path.exists(track):
                    return 'error','cannot find file: '+track 
            return 'normal',[command,track]
                
        if command == 'loop':
            if len(fields)==1:
                arg='-1'
                self.max_loops=-1    #loop continuously if no argument
                return 'normal',[command,arg]
                
            elif len(fields)==2:
                if not fields[1].isdigit() or fields[1]=='0':
                    return 'error','Argument for Loop is not a positive number in: ' + line
                else:
                    arg = fields[1]
                    self.max_loops=int(arg)
                return 'normal',[command,arg]
                                    
            else:
                return 'error','incorrect number of fields for '+ command + 'in: ' + line
                
        if command == 'wait':
            if len(fields)!=2:
                return 'error','incorrect number of fields for '+ command + 'in: ' + line
            else:
                arg = fields[1]
                if not arg.isdigit():
                    return 'error','Argument for Wait is not 0 or positive number in: ' + line
                else:
                    return 'normal',[command,arg]

 
    def play_commands(self):
        # init
        if len(self.command_list)==0:
            return
        self.loop_index=-1 # -1 no loop  comand found
        self.loop_count=0
        self.command_index=0
        self.next_command_index=0  #start at beginning
        #loop round executing the commands
        self.command_timer=GLib.timeout_add(100,self.execute_command)

        
    def execute_command(self):
        if self.command_timer != None:
            GLib.source_remove(self.command_timer)
            self.command_timer=None
        self.command_index=self.next_command_index
        if self.command_index==len(self.command_list):
            # past end of command list
            self.quit_signal = True
            return
            
        if self.command_index==len(self.command_list)-1 and self.loop_index!=-1:
            # last in list and need to loop
            self.next_command_index=self.loop_index
        else:
            self.next_command_index=self.command_index+1

        entry=self.command_list[self.command_index]
        command=entry[0]
        arg=entry[1]
        self.mon.log (self,str(self.command_index) + ' Do '+command+' '+arg + '  Next: '+str(self.next_command_index))        
                    
        # and execute command
        if command == 'load':
            self.driver_get(arg)
            self.command_timer=GLib.timeout_add(10,self.execute_command)
            
        elif command == 'refresh':
            self.driver_refresh()
            self.command_timer=GLib.timeout_add(10,self.execute_command)
            
        elif command == 'wait':
            self.command_timer=GLib.timeout_add(1000*int(arg),self.execute_command)
                   
        elif command=='loop':
            if self.loop_index==-1:
                # found loop for first time
                self.loop_index=self.command_index
                self.loop_count=0
                self.mon.log (self,'Loop init To: '+str(self.loop_index) + '  Count: '+str(self.loop_count))
                self.command_timer=GLib.timeout_add(10,self.execute_command)
            else:
                self.loop_count+=1
                self.mon.log (self,'Inc loop count: '+ '  Count: '+str(self.loop_count))
                # hit loop command after the requied number of loops
                if self.loop_count==self.max_loops:   #max loops is -1 for continuous
                    self.mon.log (self,'end of loop: '+ '  Count: '+str(self.loop_count))
                    self.quit_signal=True
                    return
                else:
                    self.mon.log (self,'Looping to: '+str(self.loop_index) + ' Count: '+str(self.loop_count))
                    self.command_timer=GLib.timeout_add(10,self.execute_command)
                    
        elif  command=='exit':
            self.quit_signal=True
            return


                
