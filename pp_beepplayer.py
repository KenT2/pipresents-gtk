import os
import copy
from pp_utils import Monitor
from pp_audiomanager import AudioManager

class BeepPlayer(object):

    pp_home=''
    pp_profile=''

    def __init__(self):
        self.mon=Monitor()

    def init(self,pp_home,pp_profile):
        BeepPlayer.pp_home=pp_home
        BeepPlayer.pp_profile = pp_profile



    def play_animate_beep(self,location,device):
        # check location
        path=self.complete_path(location)
        # print (location,path)
        if not os.path.exists(path):
            return 'error','beep file does not exist: '+ path

        status,message=self.do_beep(path,device)
        if status=='error':
            return 'error',message
        return 'normal',''



    def play_show_beep(self,command_text):
        fields = command_text.split()
        if len(fields) not in (2,3) :
            return 'error',"incorrect number of fields in beep command" + line
        symbol=fields[0]
        location=fields[1]
        if len(fields) == 3:
            device=fields[2]
        else:
            device=''

        path=self.complete_path(location)
        if not os.path.exists(path):
            return 'error','beep file does not exist: '+ path

        status,message=self.do_beep(path,device)
        if status == 'error':
            return 'error',message
        return 'normal',''



    def complete_path(self,track_file):
        # print (BeepPlayer.pp_profile)
        #  complete path of the filename of the selected entry
        if track_file != '' and track_file[0]=="+":
            track_file=BeepPlayer.pp_home+track_file[1:]
        elif track_file[0] == "@":
            track_file=BeepPlayer.pp_profile+track_file[1:]
        return track_file


    def do_beep(self,path,device):
        self.am=AudioManager()
        self.mon.log(self,'Do Beep: '+ path + ' ' +device)
        status,message,sink=self.am.get_sink(device)
        if status =='error':
            return 'error',message
        if not self.am.sink_connected(sink):
            return 'error','sound device not connected - '+device
        fields = path.split('.')
        if fields[1] != 'mp3':
            # other than mp3
            if sink != '':
                driver_option=' --device='+ sink +' --stream-name=pipresents '
            else:
                driver_option=' --stream-name=pipresents '
            #print ('pulse wav',device)
            os.system('paplay ' + driver_option + path)
            return 'normal',''
        else:
            #mp3
            if sink =='':
                driver_option = ' -o pulse '
            else:
                driver_option= ' -o pulse -a ' + sink
            #print ('pulse mp3',device)
            command = 'mpg123 -q ' + driver_option + ' ' + path
            # print (command)
            os.system (command)
            return 'normal',''
            
