import os
import json
import configparser
import remi.gui as gui
from remi_plus import AdaptableDialog
from pp_utils import parse_rectangle
from pp_timeofday import TimeOfDay

class ViewBackup(AdaptableDialog):

    def __init__(self):
        self.text=''
        super(ViewBackup, self).__init__('Backup','',width=600,height=700,confirm_name='Done')
        self.textb = gui.TextInput(width=550,height=600,single_line=False)
        self.append_field(self.textb,'text')

    def insert(self,text):
        self.text +=text
        self.textb.set_value(self.text) 

    @gui.decorate_event
    def confirm_dialog(self,emitter):
          self.hide()
          
    def view_tracks_backup(self,pp_profile_dir,medialist):
        if medialist !='':
            backup_dir=pp_profile_dir.replace('pp_profiles','pp_profiles.bak')
            medialist_path=backup_dir+os.sep+medialist
            #print('tracks backup',medialist_path)
            if os.path.exists(medialist_path):
                ifile  = open(medialist_path, 'r')
                mdict = json.load(ifile)
                ifile.close()
                self.insert('\nTRACKS\n=======\n')
                self.insert('Backup Version: '+mdict['issue'])
                for i in mdict['tracks']:
                    self.insert_items(i,'track-ref')
            else:
                self.insert('\nBackup medialist not found: '+medialist_path+'\n')
                
    def view_show_backup(self,pp_profile_dir,show_params):
        backup_dir=pp_profile_dir.replace('pp_profiles','pp_profiles.bak')
        showlist_path=backup_dir+os.sep+'pp_showlist.json'
        #print('show backup',showlist_path)
        show_ref=show_params['show-ref']
        if os.path.exists(showlist_path):
            ifile  = open(showlist_path, 'r')
            mdict = json.load(ifile)
            ifile.close()
            self.insert('\nSHOW\n======\n')
            self.insert('Backup Version: '+mdict['issue'])
            for show in mdict['shows']:
                if show['show-ref']==show_ref:

                    self.insert_items(show,'show-ref')            
        else:
            self.insert('\nBackup showlist not found: '+showlist_path+'\n')            
    
    def insert_items(self,item,ref):
        self.insert('\n----------------------------------------------------------------\n')
        self.insert('\n'+item['type']+' "'+item['title']+'" ['+item[ref]+']'+'\n')
        for field in item:
            if '\n' in item[field]:
                self.insert(field+' = \n')
                lines=item[field].split('\n')
                for line in lines:
                    self.insert(line+'\n')
            else:
                self.insert (field+' = '+item[field]+'\n')
                
               

class Validator(AdaptableDialog):

    def __init__(self, title):
        self.text=''
        self.errors=0
        self.warnings=0

        super(Validator, self).__init__('Validation Result','',width=600,height=700,confirm_name='Done')
        self.textb = gui.TextInput(width=550,height=600,single_line=False)
        self.append_field(self.textb,'text')

    @gui.decorate_event
    def confirm_dialog(self,emitter):
          self.hide()

    def display(self,priority,text):
        if priority == 'f':   self.errors+=1
        if priority  == 'w':self.warnings +=1       
        if self.display_it is False: return
        if priority == 't':
            self.insert(text+"\n")
        if priority == 'f':
            self.insert("       ** Error:  "+text+"\n")
        if priority == 'w':
            self.insert("       ** Warning:  "+text+"\n")           

    def insert(self,text):
        self.text +=text
        self.textb.set_value(self.text)



    def stats(self,pp_profile):
        if self.display_it is False: return
        self.text="\nERRORS: "+str(self.errors)+"\nWARNINGS: "+str(self.warnings)+"\n\n"+self.text
        self.text="\nVALIDATING PROFILE '"+ pp_profile + "'\n"+self.text

        self.textb.set_value(self.text)
        
    def num_errors(self):
        return self.errors


    def validate_profile(self, pp_dir, pp_home, pp_profile,editor_issue,display_it):
        self.display_it=display_it
        # USES
        # self.current_showlist

        # CREATES
        # v_media_lists - file names of all medialists in the profile
        # v_shows
        # v_track_labels - list of track labels in current medialist.
        # v_show_labels - list of show labels in the showlist
        # v_medialist_refs - list of references to medialist files in the showlist

        # open results display


        if not  os.path.exists(pp_profile+os.sep+"pp_showlist.json"):
            self.display('f',"pp_showlist.json not in profile")
            self.display('t', "Validation Aborted")
            return False                   
        ifile  = open(pp_profile+os.sep+"pp_showlist.json", 'r')
        sdict= json.load(ifile)
        ifile.close()
        v_shows=sdict['shows']
        if 'issue' in sdict:
            profile_issue= sdict['issue']
        else:
            profile_issue="1.0"
                      
        if profile_issue != editor_issue:
            self.display('f',"Profile version "+profile_issue+ " is different to that editor")
            self.display('t', "Validation Aborted")
            return False                                            
        

        # MAKE LIST OF SHOW LABELS
        v_show_labels=[]
        for show in v_shows:
            if show['type'] != 'start': v_show_labels.append(show['show-ref'])

        # CHECK ALL MEDIALISTS AND THEIR TRACKS
        v_media_lists = []
        for medialist_file in os.listdir(pp_profile):
            if not medialist_file.endswith(".json") and medialist_file not in ('readme.txt') and not os.path.isdir(pp_profile+os.sep+medialist_file):
                self.display('w',"Placing a media file in a profile is discouraged: "+ medialist_file + '\n         Place it in a directory')
                
            if medialist_file.endswith(".json") and medialist_file not in  ('pp_showlist.json','schedule.json'):
                self.display('t',"\nChecking medialist '"+medialist_file+"'")
                v_media_lists.append(medialist_file)

                # open a medialist and test its tracks
                ifile  = open(pp_profile + os.sep + medialist_file, 'r')
                sdict= json.load(ifile)
                ifile.close()                          
                tracks = sdict['tracks']
                if 'issue' in sdict:
                    medialist_issue= sdict['issue']
                else:
                    medialist_issue="1.0"
                      
                # check issue of medialist      
                if medialist_issue  !=  editor_issue:
                    self.display('f',"Medialist version "+medialist_issue+ " is different to that editor")
                    self.display('t', "Validation Aborted")
                    return False

                # open a medialist and test its tracks
                v_track_labels=[]
                anonymous=0
                for track in tracks:
                    self.display('t',"    Checking track '"+track['title']+"'")
                    
                    # check track-ref
                    if track['track-ref'] == '':
                        anonymous+=1
                    else:
                        if track['track-ref'] in v_track_labels:
                            self.display('f',"'duplicate track reference: "+ track['track-ref'])
                        v_track_labels.append(track['track-ref'])
     
                    # warn if media tracks blank  where optional
                    #if track['type'] in ('image'):
                        #if track['location'].strip() == '':
                            #self.display('w',"blank location")

                    # warn if media tracks blank  where optional
                    if track['type'] in ('message'):
                        if track['message-text-location'].strip() == ''and track['text'].strip()=='':
                            self.display('w',"blank Location and Message Text")

                    # check location of relative media tracks where present                   
                    if track['type'] in ('message'):    
                        track_file=track['message-text-location']
                        if track_file.strip() != '' and  track_file[0] == "+":
                            track_file=pp_home+track_file[1:]
                            if not os.path.exists(track_file): self.display('f',"location "+track['location']+ " Media File not Found")
                            
                        if track_file.strip() != '' and  track_file[0] == "@":
                            track_file=pp_profile+track_file[1:]
                            if not os.path.exists(track_file): self.display('f',"location "+track['location']+ " Media File not Found")

                    
                    # check location of relative media tracks where present                   
                    if track['type'] in ('image','mpv'):    
                        track_file=track['location']
                        if track_file.strip() != '' and  track_file[0] == "+":
                            track_file=pp_home+track_file[1:]
                            if not os.path.exists(track_file): self.display('f',"location "+track['location']+ " Media File not Found")
                            
                        if track_file.strip() != '' and  track_file[0] == "@":
                            track_file=pp_profile+track_file[1:]
                            if not os.path.exists(track_file): self.display('f',"location "+track['location']+ " Media File not Found")

                    if track['type'] in ('mpv','message','image','webkit','menu'):
                        
                        # check common fields
                        self.check_animate('animate-begin',track['animate-begin'])
                        self.check_animate('animate-end',track['animate-end'])
                        self.check_plugin(track['plugin'],pp_home,pp_profile)
                        self.check_show_control(track['show-control-begin'],v_show_labels)
                        self.check_show_control(track['show-control-end'],v_show_labels)
                        if track['background-image'] != '':
                            track_file=track['background-image']
                            if track_file[0] == "+":
                                track_file=pp_home+track_file[1:]
                                if not os.path.exists(track_file): self.display('f',"background-image "+track['background-image']+ " background image file not found")                                
                            if track_file[0] == "@":
                                track_file=pp_profile+track_file[1:]
                                if not os.path.exists(track_file): self.display('f',"location "+track['location']+ " Background Image not Found")
                        
                        self.check_font('Plain Text Font',track['track-text-font'])
                        if track['track-text'] != "":
                            if track['track-text-x'] != "" and not track['track-text-x'].isdigit(): self.display('f',"'Track Text x position' is not a positive integer")
                            if track['track-text-y'] != "" and not track['track-text-y'].isdigit(): self.display('f',"'Track Text y Position' is not a positive integer")
                            if track['track-text-justify'] != "" and track['track-text-justify'] not in ('left','right','center'): self.display('f',"'Plain Text Justify' has illegal value")
                            #if track['track-text-colour']=='': self.display('f',"'Plain Text Colour' is blank")
                    
                    if track['type']=='menu':
                        self.check_menu(track)

                    
                    if track['type'] == "image":
                        if track['image-window']=='original': self.display('f',"Image Window is original, use fullscreen")

                        if track['pause-timeout'] != "" and not track['pause-timeout'].isdigit():
                            self.display('f',"'Pause Timeout' is not blank or a positive integer")
                        else:
                            if track['pause-timeout'] != "" and int(track['pause-timeout']) < 1: self.display('f',"'Pause Timeout' is less than 1")
                        self.check_float_duration('track','Image Duration',track['duration'])
                        self.check_player_window('track','Image Window',track['image-window'])

                    if track['type'] == "vlc":
                        self.display('f',"'VLC Video Track has been removed from Pi Presents use mpv")
                        
                    if track['type'] == "audio":
                        self.display('f',"'mplayer Audio Track has been removed from Pi Presents use mpv")
                        
                    if track['type'] == "chrome":
                        self.display('f',"'Chromium Web Track has been removed from Pi Presents use webkit")
                        
                    if track['type'] == "mpv":
                        if track['pause-timeout'] != "" and not track['pause-timeout'].isdigit():
                            self.display('f',"'Pause Timeout' is not blank or a positive integer")
                        else:
                            if track['pause-timeout'] != "" and int(track['pause-timeout']) < 1: self.display('f',"'Pause Timeout' is less than 1")

                        self.check_player_window('track','MPV Window',track['mpv-window'])
                        self.check_mpv_volume('track','MPV Volume',track['mpv-volume'])
                        self.check_mpv_max_volume('track','MPV Max Volume',track['mpv-max-volume'])                        
                        if track['mpv-video-display'].upper()=='HDMI':self.display('f','MPV Alternate Display is HDMI or hdmi, use HDMI0')
                        if track['mpv-video-display'].islower():self.display('f',"Display Name must be Upper Case. Reselect it")

                    if track['type'] == "message":
                        self.check_float_duration('track','Message Duration',track['duration'])
                        self.check_font('Message Font',track['message-font'])
                        if track['text'] != "":
                            if track['message-x'] != '' and not track['message-x'].isdigit(): self.display('f',"'Message x Position' is not blank, a positive integer")
                            if track['message-y'] != '' and not track['message-y'].isdigit(): self.display('f',"'Message y Position' is not blank, a positive integer")
                            if track['message-colour']=='': self.display('f',"'Message Text Colour' is blank")
                            if track['message-font']=='': self.display('f',"Message Text Font' is blank")                        

                    #gtkdo
                    if track['type'] == "webkit":
                        self.check_float_duration('track','Webkit Web Duration',track['duration'])
                        self.check_browser_commands(track['browser-commands'])
                        self.check_player_window('track','Webkit Web Window',track['webkit-window'])
                        self.check_webkit_zoom('track','Webkit Zoom',track['webkit-zoom'])                        
                  
                    # SHOW TRACK - CHECK CROSS REF TRACK TO SHOW
                    if track['type'] == 'show':
                        if track['sub-show'] == "":
                            self.display('f',"No 'Sub-show to Run'")
                        else:
                            if track['sub-show'] not in v_show_labels: self.display('f',"Show "+track['sub-show'] + " does not exist")
                            
                # if anonymous == 0 :self.display('w',"zero anonymous tracks in medialist " + file)

                # check for duplicate track-labels
                # !!!!!!!!!!!!!!!!!! add check for all labels


        # SHOWS
        # find start show and test it, test show-refs at the same time
        found=0
        for show in v_shows:
            if show['type'] == 'start':
                self.display('t',"\nChecking show '"+show['title'] + "' first pass")
                found+=1
                if show['show-ref'] !=  'start': self.display('f',"start show has incorrect label")
            else:
                self.display('t',"\nChecking show '"+show['title'] + "' first pass")
                if show['show-ref'] == '': self.display('f',"Show Reference is blank")
                if ' ' in show['show-ref']: self.display('f',"Spaces not allowed in Show Reference: " + show['show-ref']) 
        if found == 0:self.display('f',"There is no start show")
        if found > 1:self.display('f',"There is more than 1 start show")    


        # check for duplicate show-labels
        for show_label in v_show_labels:
            found = 0
            for show in v_shows:
                if show['show-ref'] == show_label: found+=1
            if found > 1: self.display('f',show_label + " is defined more than once")
            
        # check other things about all the shows and create a list of medialist file references
        v_medialist_refs=[]
        for show in v_shows:
            if show['type'] == "start":
                self.display('t',"\nChecking show '"+show['title']+ "' second pass" )
                self.check_start_shows(show,v_show_labels)               
            else:
                self.display('t',"\nChecking show '"+show['title']+ "' second pass" )

                if show['medialist']=='': self.display('f', show['show-ref']+ " show has blank medialist")
                
                if '.json' not in show['medialist']:
                    self.display('f', show['show-ref']+ " show has invalid medialist")
                    self.display('t', "Validation Aborted")
                    return False

                if show['medialist'] not in v_media_lists:
                    self.display('f', "'"+show['medialist']+ "' medialist not found")
                    self.display('t', "Validation Aborted")
                    return False

                if not os.path.exists(pp_profile + os.sep + show['medialist']):
                    self.display('f', "'"+show['medialist']+ "' medialist file does not exist")
                    self.display('t', "Validation Aborted")
                    return False
                    
                v_medialist_refs.append(show['medialist'])
                
                
                # open medialist and produce a dictionary of its contents for use later
                ifile  = open(pp_profile + os.sep + show['medialist'], 'r')
                tracks = json.load(ifile)['tracks']
                ifile.close()
                
                # make a list of the track labels
                v_track_labels=[]
                for track in tracks:
                    if track['track-ref'] !='':
                        v_track_labels.append(track['track-ref'])
                
                
                # check common fields in the show
                #show
                self.check_show_canvas('show','Show Canvas',show['show-canvas'])
                if show['display-name'].upper()=='HDMI':self.display('f',"'Display Name is HDMI or hdmi, use HDMI0")
                if show['display-name'].islower():self.display('f',"Display Name must be Upper Case. Reselect it")
                #show background and text
                self.check_font('Show Text Font',show['show-text-font'])
                if show['show-text'] != "":
                    if show['show-text-x'] != "" and not show['show-text-x'].isdigit(): self.display('f',"'Show Text x Position' is not a positive integer")
                    if show['show-text-y'] != "" and not show['show-text-y'].isdigit(): self.display('f',"'Show Text y Position' is not a positive integer")
                    if show['show-text-colour']=='': self.display('f',"'Show Text Colour' is blank")
                    if show['show-text-font']=='': self.display('f',"'Show Text Font' is blank")


                background_image_file=show['background-image']
                if background_image_file.strip() != '' and  background_image_file[0] == "+":
                    track_file=pp_home+background_image_file[1:]
                    if not os.path.exists(track_file): self.display('f',"Background Image "+show['background-image']+ " background image file not found")
                if background_image_file.strip() != '' and  background_image_file[0] == "@":
                    track_file=pp_profile+background_image_file[1:]
                    if not os.path.exists(track_file): self.display('f',"Background Image "+show['background-image']+ " background image file not found")


                #track defaults

                if show['track-text-x'] != ''and not show['track-text-x'].isdigit(): self.display('f',"'Track Text x Position' is not a positive integer")
                if show['track-text-y'] != ''and not show['track-text-y'].isdigit(): self.display('f',"'Track Text y Position' is not a positive integer")
                if show['track-text-colour']=='': self.display('f',"'Track Text Colour' is blank")
                if show['track-text-font']=='': self.display('f',"'Track Text Font' is blank")
                if show['mpv-audio'].upper() =='HDMI': self.display('f',"MPV Player Audio is HDMI or hdmi, use HDMI0")
                if show['mpv-audio'].islower():self.display('f',"Display Name must be Upper Case. Reselect it")
                self.check_font('Track Text Font',show['track-text-font'])
                
                self.check_float_duration('show','Duration',show['duration'])
                if show['pause-timeout'] != "" and not show['pause-timeout'].isdigit():
                    self.display('f',"'Pause Timeout' is not blank or a positive integer")
                else:
                    if show['pause-timeout'] != "" and int(show['pause-timeout']) < 1: self.display('f',"'Pause Timeout' is less than 1")

                self.check_player_window('show','MPV Window',show['mpv-window'])
                self.check_mpv_volume('show','MPV Volume',show['mpv-volume'])  
                self.check_player_window('show','Image Window',show['image-window'])
                self.check_player_window('show','Webkit Web Window',show['webkit-window'])
                self.check_webkit_zoom('show','Webkit Zoom',show['webkit-zoom'])
                if show['image-window']=='original': self.display('f',"Image Window is original, use fullscreen")
                
                #eggtimer
                self.check_font('Eggtimer Font',show['eggtimer-font'])
                if show['eggtimer-text'] != "":
                    if show['eggtimer-colour']=='': self.display('f',"'Eggtimer Colour' is blank")
                    if show['eggtimer-font']=='': self.display('f',"'Eggtimer Font' is blank")                
                    if not show['eggtimer-x']!='' and not show['eggtimer-x'].isdigit(): self.display('f',"'Eggtimer x Position' is not a positive integer")
                    if not show['eggtimer-y']!='' and not show['eggtimer-y'].isdigit(): self.display('f',"'Eggtimer y Position' is not a positive integer")

                    
                #check the schedule
                self.check_schedule_for_show(show,v_show_labels) 
 
                # Validate simple fields of each show type
                if show['type'] in ("mediashow",'liveshow'):
                    self.check_font('Hint Font',show['hint-font'])
                    if show['child-track-ref'] != '':
                        if show['child-track-ref'] not in v_track_labels:
                            self.display('f',"'Child Track ' " + show['child-track-ref'] + ' is not in medialist' )             
                        if not show['hint-x']!='' and not show['hint-y'].isdigit(): self.display('f',"'Hint y Position' is not a positive integer")
                        if not show['hint-x']!='' and not show['hint-x'].isdigit(): self.display('f',"'Hint x Position' is not a positive integer")
                        if show['hint-colour']=='': self.display('f',"'Hint Colour' is blank")
                        if show['hint-font']=='': self.display('f',"'Hint Font' is blank")

                        
                    self.check_hh_mm_ss('Show Timeout',show['show-timeout'])
                    
                    self.check_hh_mm_ss('Repeat Interval',show['interval'])
                    
                    if not show['track-count-limit'].isdigit(): self.display('f',"'Track Count Limit' is not 0 or a positive integer")

                    if show['trigger-start-type'] == 'input':
                        self.check_triggers('Start Trigger Parameters',show['trigger-start-param'])

                    if show['trigger-next-type'] == 'input':
                        self.check_triggers('Next Trigger Parameters',show['trigger-next-param'])

                    if show['trigger-end-type'] == 'input':
                        self.check_triggers('End Trigger Parameters',show['trigger-end-param']) 

                                       
                    self.check_controls('controls',show['controls'])

                    #notices
                    self.check_font('Notice Text Font',show['admin-font'])
                    if show['trigger-wait-text'] != "" or show['empty-text'] != "":
                        if show['admin-colour']=='': self.display('f',"' Notice Text Colour' is blank")
                        if show['admin-font']=='': self.display('f',"'Notice Text Font' is blank")                
                        if not show['admin-x']!='' and not show['admin-x'].isdigit(): self.display('f',"'Notice Text x Position' is not a positive integer")
                        if not show['admin-y']!='' and not show['admin-y'].isdigit(): self.display('f',"'Notice Text y Position' is not a positive integer")
                   
                        
                if show['type']== 'liveshow':
                    if  show['repeat']=='repeat':
                        if show['empty-track-ref']=='':
                            self.display('f','Empty List Track is blank')
                        else:
                            if show['empty-track-ref'] not in v_track_labels:
                                self.display('f','Empty List Track is not in medialist: '+show['empty-track-ref'])
                            

                if show['type'] in ("artmediashow",'artliveshow'):
                    
                    #notices
                    self.check_font('Notice Text Font',show['admin-font'])
                    if show['empty-text'] != "":
                        if show['admin-colour']=='': self.display('f',"' Notice Text Colour' is blank")
                        if show['admin-font']=='': self.display('f',"'Notice Text Font' is blank")                
                        if not show['admin-x']!='' and not show['admin-x'].isdigit(): self.display('f',"'Notice Text x Position' is not a positive integer")
                        if not show['admin-y']!='' and not show['admin-y'].isdigit(): self.display('f',"'Notice Text y Position' is not a positive integer")

                        
                    self.check_controls('controls',show['controls'])
                    
                            
                if show['type'] == "menu":
                    self.check_hh_mm_ss('Show Timeout',show['show-timeout'])                 
                    self.check_hh_mm_ss('Track Timeout',show['track-timeout'])

                    if show['menu-track-ref']=='':
                        self.display('f',"'menu track ' is blank")
                    else:
                        if show['menu-track-ref'] not in v_track_labels:
                            self.display('f',"'menu track ' is not in medialist: " + show['menu-track-ref'])     
                    self.check_controls('controls',show['controls'])

  
                if show['type'] == 'hyperlinkshow':
                    if show['first-track-ref']=='':
                        self.display('f',"'First Track ' is blank")
                    else:
                        if show['first-track-ref'] not in v_track_labels:
                            self.display('f',"'First track ' is not in medialist: " + show['first-track-ref'])
                            
                    if show['home-track-ref']=='':
                        self.display('f',"'Home Track ' is blank")
                    else:
                        if show['home-track-ref'] not in v_track_labels:
                            self.display('f',"'Home track ' is not in medialist: " + show['home-track-ref'])

                    if show['timeout-track-ref']=='':
                        self.display('w',"'Timeout Track ' is blank")
                    else:
                        if show['timeout-track-ref'] not in v_track_labels:
                            self.display('f',"'timeout track ' is not in medialist: " + show['timeout-track-ref'])            
                    self.check_hyperlinks('links',show['links'],v_track_labels)
                    self.check_hh_mm_ss('Show Timeout',show['show-timeout'])                 
                    self.check_hh_mm_ss('Track Timeout',show['track-timeout'])

                if show['type'] == 'radiobuttonshow':
                    if show['first-track-ref']=='':
                        self.display('f',"'Home Track ' is blank")
                    else:
                        if show['first-track-ref'] not in v_track_labels:
                            self.display('f',"'first track ' is not in medialist: " + show['first-track-ref'])
                        
                    self.check_radiobutton_links('links',show['links'],v_track_labels)
                    self.check_hh_mm_ss('Show Timeout',show['show-timeout'])                 
                    self.check_hh_mm_ss('Track Timeout',show['track-timeout'])


        self.display('t', "\nVALIDATION COMPLETE")
        self.stats(pp_profile)
        if self.num_errors() == 0:
            return True
        else:
            return False
            
# END END END

# ***********************************
# START SHOWS
# ************************************
 
    def check_start_shows(self,show,v_show_labels):
        text=show['start-show']
        show_count=0
        fields = text.split()
        for field in fields:
            show_count+=1
            if field not in v_show_labels:
                self.display('f',"start show has undefined Start Show: "+ field)
        if show_count == 0:
            self.display('w',"start show has zero Start Shows")

        #check the schedule
        self.check_schedule_for_show(show,v_show_labels)      


# ***********************************
# TRIGGERS
# ************************************ 

    def check_triggers(self,field,line):
        words=line.split()
        if len(words)!=1: self.display('f','Wrong number of fields in: ' + field + ", " + line)


# ***********************************
# VIDEO
# ************************************ 

 
    def check_mpv_volume(self,track_type,field,line):
        if track_type == 'show' and line.strip() == '':
            self.display('f','Show must specify MPV volume: ' + field + ", " + line)
            return
        if track_type == 'track' and line.strip() == '':
            return
        if not line.isdigit():
            self.display('f','MPV Volume must be a positive integer: ' + field + ", " + line)
            return
        mpv_volume= int(line)
        if mpv_volume>100:
            self.display('f','MPV Volume must be <= 100: ' + field + ", " + line)
            return
        return


    def check_mpv_max_volume(self,track_type,field,line):
        if track_type == 'track' and line.strip() == '':
            return
        if not line.isdigit():
            self.display('f','MPV Max Volume must be a positive integer: ' + field + ", " + line)
            return
        mpv_max_volume= int(line)
        if mpv_max_volume>100:
            self.display('f','MPV Max Volume must be <= 100: ' + field + ", " + line)
            return
        return

        

    


# ***********************************
# TIME SCHEDULER
# ************************************ 

    def check_schedule_for_show(self,show,v_show_labels):
        show_type=show['type']
        show_ref=show['show-ref']
        # print('check schedule for show ',show_type,show_ref)
        if 'sched-everyday' in show:
            text=show['sched-everyday']
            lines=text.splitlines()
            #chunk text into lines for one day line (day_lines) and leftover (lines)
            while len(lines) != 0:
                status,message,day_lines,lines=self.chunk_one_day(lines,show_ref,'everyday')
                if status == 'error':
                    return
                if len(day_lines)!=0:
                    # check one day line and its times
                   self.check_day(day_lines,'everyday',show_ref,show_type,v_show_labels)


        if 'sched-weekday' in show:
            text=show['sched-weekday']
            lines=text.splitlines()
            while len(lines) != 0:
                status,message,day_lines,lines=self.chunk_one_day(lines,show_ref,'weekday')
                if status == 'error':
                    return
                if len(day_lines)!=0:
                    self.check_day(day_lines,'weekday',show_ref,show_type,v_show_labels)


        if 'sched-monthday' in show:
            text=show['sched-monthday']
            lines=text.splitlines()
            while len(lines) != 0:
                status,message,day_lines,lines=self.chunk_one_day(lines,show_ref,'monthday')
                # print 'in monthday',day_lines
                if status == 'error':
                    return
                if len(day_lines)!=0:
                    self.check_day(day_lines,'monthday',show_ref,show_type,v_show_labels)
            

        if 'sched-specialday' in show:
            text=show['sched-specialday']
            lines=text.splitlines()
            while len(lines) != 0:
                status,message,day_lines,lines=self.chunk_one_day(lines,show_ref,'specialday')
                if status == 'error':
                    return 
                if len(day_lines)!=0:
                    self.check_day(day_lines,'specialday',show_ref,show_type,v_show_labels)
               



    def chunk_one_day(self,lines,show_ref,section):
        this_day=[]
        left_over=[]
        #print 'get one day',lines
        # check first line is day and move to output
        #print lines[0]
        if not lines[0].startswith('day'):
            self.display('f','Schedule - first line of section ' + section + ' is not day:  ' + lines[0] )
            return 'error','',[],[]
        this_day=[lines[0]]
        #print ' this day',this_day
        left_over=lines[1:]
        # print 'left over',left_over
        x_left_over=lines[1:]
        for line in x_left_over:
            #print 'in loop',line
            if line.startswith('day'):
                # print 'one day day',this_day,left_over
                return 'normal','',this_day,left_over
            this_day.append(line)
            left_over=left_over[1:]
        # print 'one day end',this_day,left_over
        return 'normal','',this_day,left_over
                
    def check_day(self,lines,section,show_ref,show_type,v_show_labels):
        if section == 'everyday':
            self.check_everyday(lines[0],show_ref,'everyday')
        elif section == 'weekday':
            self.check_weekday(lines[0],show_ref,'weekday')
        elif section == 'monthday':
            self.check_monthday(lines[0],show_ref,'monthday')
        elif section == 'specialday':
            self.check_specialday(lines[0],show_ref,'specialday')
        else:
            self.display('f','Schedule - invalid section name: '+ section)
            return

        if len(lines) >1:
            time_lines=lines[1:]
            self.check_time_lines(time_lines,show_ref,show_type,v_show_labels,section)
        else:
            self.display('w','Schedule - In '+ section+ ' there are zero time lines')

 

    def check_everyday(self,line,show_ref,section):
        words=line.split()
        if words[0]!='day':
            self.display('f', 'error','Schedule - In section '+ section + ' day line does not contain day:  '+ line)
        if words[1] != 'everyday':
            self.display('f','Schedule - In section '+ section + ' day line does not contain everyday:  '+ line)

       
    def check_weekday(self,line,show_ref,section):
        words=line.split()
        if words[0]!='day':
            self.display('f','Schedule - In section '+ section + ' day line does not contain day:  ' + line)
        days=words[1:]
        for day in days:
            if day not in TimeOfDay.DAYS_OF_WEEK:
                self.display('f','Schedule - In section '+ section + ' day line has invalid day: '+ line)


    def check_monthday(self,line,show_ref,section):
        words=line.split()
        if words[0]!='day':
            self.display('f','Schedule - In section '+ section + ' day line does not contain day:  ' + line)
        days=words[1:]
        for day in days:
            if not day.isdigit():
                self.display('f','Schedule - In section '+ section + ' day line has invalid day: '+ line)
                return
            if int(day) <1 or int(day)>31:
                self.display('f','Schedule - In section '+ section + ' day line has out of range day: '+ line)
        return

    def check_specialday(self,line,show_ref,section):
        words=line.split()
        if words[0]!='day':
            self.display('f','Schedule - In section '+ section + ' day line does not contain day:  ' + line)
        days=words[1:]
        for day in days:
            self.check_date(day,show_ref,section)

   
    def check_time_lines(self,lines,show_ref,show_type,v_show_labels,section):
        # lines - list of  lines each with text 'command time'
        # returns list of lists each being [command, time]
        time_lines=[]
        for line in lines:
            # split line into time,command
            words=line.split()
            if len(words)<2:
                self.display('f','Schedule - In section '+ section + ' time line has wrong length: '+ line)
                return
            self.check_time(words[0],show_ref,section)

            if show_type=='start':
                command = ' '.join(words[1:])
                self.check_show_control_fields(command,v_show_labels)
            else:
                if words[1] not in ('open','close'):
                    self.display('f','Schedule - In section '+ section+ ' illegal command: '+ line)
        return



    def check_time(self,item,show_ref,section):        
        fields=item.split(':')
        if len(fields) == 0:
            self.display('f','Schedule - In section ' + section + ' time field is empty: '+ item)
            return
        if len(fields)>3:
            self.display('f','Schedule - In section ' + section + ' time line has  too many fields: ' + item)
            return
        if len(fields) == 1:
            seconds=fields[0]
            minutes='0'
            hours='0'
        if len(fields) == 2:
            seconds=fields[1]
            minutes=fields[0]
            hours='0'
        if len(fields) == 3:
            seconds=fields[2]
            minutes=fields[1]
            hours=fields[0]
        if not seconds.isdigit() or not  minutes.isdigit() or  not hours.isdigit():
            self.display('f','Schedule - In section ' + section + ' time field is invalid: ' + item)
            return
        if int(minutes)>59:
            self.display('f','Schedule - In section ' + section + ' Minutes of  '+ item + ' is out of range')
        if int(seconds)>59:
            self.display('f','Schedule - In section ' + section + '  Seconds of  '+ item + ' is out of range')
        if int(hours)>23:
            self.display('f','Schedule - In section ' + section + ' Hours of  '+ item + ' is out of range')         
        return


    def check_date(self,item,show_ref,section):
        fields=item.split('-')
        if len(fields) == 0:
            self.display('f','Schedule - In section ' + section + ' Date field is empty: '+item)
            return
        if len(fields)!=3:
            self.display('f','Schedule - In section ' + section + ' Too many or few fields in date: ' + item)
            return
        year=fields[0]
        month=fields[1]
        day = fields[2]
        if not year.isdigit() or not  month.isdigit() or  not day.isdigit():
            self.display('f','Schedule - In section ' + section + ' Fields of  '+ item + ' are not positive integers ' )
            return
        if int(year)<2018:
            self.display('f','Schedule - In section ' + section + ' Year of  '+ item + ' is out of range ')
        if int(month)>12:
            self.display('f','Schedule - In section ' + section + ' Month of  '+ item + ' is out of range ')
        if int(day)>31:
            self.display('f','Schedule - In section ' + section + ' Day of  '+ item + ' is out of range ')

   


    def check_duration(self,field,line):          
        fields=line.split(':')
        if len(fields) == 0:
            self.display('f','End Trigger, ' + field +' Field is empty: ' + line)
            return
        if len(fields)>3:
            self.display('f','End Trigger, ' + field + ' More then 3 fields: ' + line)
            return
        if len(fields) == 1:
            secs=fields[0]
            minutes='0'
            hours='0'
        if len(fields) == 2:
            secs=fields[1]
            minutes=fields[0]
            hours='0'
        if len(fields) == 3:
            secs=fields[2]
            minutes=fields[1]
            hours=fields[0]
        if not hours.isdigit() or not  minutes.isdigit() or  not secs.isdigit():
            self.display('f','End Trigger, ' + field + ' Fields are not positive integers: ' + line)
            return
        
        if int(hours)>23 or int(minutes)>59 or int(secs)>59:
            self.display('f','End Trigger, ' + field + ' Fields are out of range: ' + line)
            return


# *******************   
# MENU
# ***********************               
        
    def check_menu(self,track):

        if not track['menu-rows'].isdigit(): self.display('f'," Menu Rows is not 0 or a positive integer")
        if not track['menu-columns'].isdigit(): self.display('f'," Menu Columns is not 0 or a positive integer")     
        if not track['menu-icon-width'].isdigit(): self.display('f'," Icon Width is not 0 or a positive integer") 
        if not track['menu-icon-height'].isdigit(): self.display('f'," Icon Height is not 0 or a positive integer")
        if not track['menu-horizontal-padding'].isdigit(): self.display('f'," Horizontal Padding is not 0 or a positive integer")
        if not track['menu-vertical-padding'].isdigit(): self.display('f'," Vertical padding is not 0 or a positive integer") 
        if not track['menu-text-width'].isdigit(): self.display('f'," Text Width is not 0 or a positive integer") 
        if not track['menu-text-height'].isdigit(): self.display('f'," Text Height is not 0 or a positive integer")
        if not track['menu-horizontal-separation'].isdigit(): self.display('f'," Horizontal Separation is not 0 or a positive integer") 
        if not track['menu-vertical-separation'].isdigit(): self.display('f'," Vertical Separation is not 0 or a positive integer")
        if not track['menu-strip-padding'].isdigit(): self.display('f'," Stipple padding is not 0 or a positive integer")    

        if not track['hint-x']!='' and not track['hint-x'].isdigit(): self.display('f',"'Hint x Position' is not a positive integer")
        if not track['hint-y']!='' and not track['hint-y'].isdigit(): self.display('f',"'Hint y Position' is not a positive integer")
        self.check_font('Hint Font',track['hint-font'])
        if track['hint-colour']=='': self.display('f',"'Hint Colour' is blank")

        #if track['track-text-x'] != "" and not track['track-text-x'].isdigit(): self.display('f'," Menu Text x Position is not a positive integer") 
        #if track['track-text-y'] != "" and not track['track-text-y'].isdigit(): self.display('f'," Menu Text y Position is not a positive integer")
        #self.check_font('Plain Text Font',track['track-text-font'])
        #if track['track-text-colour']=='': self.display('f',"'Plain Text Colour' is blank")
        
        self.check_font('Entry Font',track['entry-font'])
        if track['entry-colour']=='': self.display('f',"'Entry Colour' is blank")
        
        if track['menu-icon-mode'] == 'none' and track['menu-text-mode'] == 'none':
            self.display('f'," Icon and Text are both None") 

        if track['menu-icon-mode'] == 'none' and track['menu-text-mode'] == 'overlay':
            self.display('f'," cannot overlay none icon") 
            
        self.check_menu_window(track['menu-window'])

    def check_menu_window(self,line):
        if line  == '':
            self.display('f'," menu Window: may not be blank")
            return

        fields = line.split()
        if len(fields) !=1:
            self.display('f','wrong number of fields in Menu Window')
        if fields[0] == 'fullscreen':
            return
        status,message,x1,y1,width,height = parse_rectangle (fields[0])
        if status == 'error':
            self.display('f',message)
            return
        if x1==-1 and y1==-1:
            self.display( 'f','rectangle must include x and y')
            return
        return
            

# *******************   
# TRACK PLUGIN
# *******************             
             
    def check_plugin(self,plugin_cfg,pp_home,pp_profile):
        if plugin_cfg.strip() != '' and  plugin_cfg[0] == "+":
            plugin_cfg=pp_home+plugin_cfg[1:]
            if not os.path.exists(plugin_cfg):
                self.display('f','track plugin configuration file not found: '+ plugin_cfg)
        if plugin_cfg.strip() != '' and  plugin_cfg[0] == "@":
            plugin_cfg=pp_profile+plugin_cfg[1:]
            if not os.path.exists(plugin_cfg):
                self.display('f','plugin configuration file not found: '+ plugin_cfg)

# *******************   
# BROWSER COMMANDS
# *******************            
             
    def check_browser_commands(self,command_text):
        lines = command_text.split('\n')
        for line in lines:
            if line.strip() == "":
                continue
            self.check_webkit_command(line)

    def check_webkit_command(self,line):
        fields = line.split()
        
        if len(fields) not in (1,2):
            self.display('f','incorrect number of fields in browser command: '+ line)
            return
            
        command = fields[0]
    
        
        if command not in ('load','refresh','wait','loop'):
            self.display('f','unknown command in browser commands: '+ line)
            return
           
        if command in ('refresh',) and len(fields) != 1:
            self.display('f','incorrect number of fields for '+ command + ' in: '+ line)
            return
            
        if command =='loop' and len(fields)==1:
            return
            
        if command == 'load':
            if len(fields) != 2:
                self.display('f','incorrect number of fields for '+ command + ' in: '+ line)
                return

        if command in ('wait','loop'):
            if len(fields) != 2:
                self.display('f','incorrect number of fields for '+ command + ' in: '+ line)
                return          
            arg = fields[1]
            if not arg.isdigit():
                self.display('f','Argument for "wait" or "loop" is not 0 or positive number in: '+ line)
                return




             
# *******************   
# CONTROLS
# *******************

    def check_controls(self,name,controls_text):
        lines = controls_text.split('\n')
        for line in lines:
            if line.strip() == "":
                continue
            self.check_control(line)


    def check_control(self,line):
        fields = line.split()
        if len(fields) != 2 :
            self.display('f',"incorrect number of fields in Control: " + line)
            return
        operation=fields[1]
        if operation in ('repeat','up','down','play','stop','exit','pause','no-command','null','pause-on','pause-off','mute','unmute','go','inc-volume','dec-volume') or operation[0:6] == 'mplay-':
            return
        else:
            self.display('f',"unknown Command in Control: " + line)


# ***********************   
# HYPERLINKSHOW CONTROLS
# ***********************

    def check_hyperlinks(self,name,links_text,v_track_labels):
        lines = links_text.split('\n')
        for line in lines:
            if line.strip() == "":
                continue
            self.check_hyperlink(line,v_track_labels)


    def check_hyperlink(self,line,v_track_labels):
        fields = line.split()
        if len(fields) not in (2,3):
            self.display('f',"Incorrect number of fields in Control: " + line)
            return
        symbol=fields[0]
        operation=fields[1]
        if operation in ('home','null','stop','exit','repeat','pause','no-command','pause-on','pause-off','mute','unmute','go') or operation[0:6] == 'mplay-':
            return

        elif operation in ('call','goto','jump'):
            if len(fields)!=3:
                self.display('f','Incorrect number of fields in Control: ' + line)
                return
            else:
                operand=fields[2]
                if operand not in v_track_labels:
                    self.display('f',operand + " Command argument is not in medialist: " + line)
                    return

        elif operation == 'return':
            if len(fields)==2:
                return
            else:
                operand=fields[2]
                if operand.isdigit() is True:
                    return
                else:
                    if operand not in v_track_labels:
                        self.display('f',operand + " Command argument is not in medialist: " + line)
                        return
        else:
            self.display('f',"unknown Command in Control: " + line)


# ************************   
# RADIOBUTTONSHOW CONTROLS
# ************************

    def check_radiobutton_links(self,name,links_text,v_track_labels):
        lines = links_text.split('\n')
        for line in lines:
            if line.strip() == "":
                continue
            self.check_radiobutton_link(line,v_track_labels)

    def check_radiobutton_link(self,line,v_track_labels):
        fields = line.split()
        if len(fields) not in (2,3):
            self.display('f',"Incorrect number of fields in Control: " + line)
            return
        symbol=fields[0]
        operation=fields[1]
        if operation in ('return','stop','exit','pause','no-command','pause-on','pause-off','mute','unmute','go') or operation[0:6] == 'mplay-':
            return
        
        elif operation == 'play':
            if len(fields)!=3:
                self.display('f','Incorrect number of fields in Control: ' + line)
                return
            else:
                operand=fields[2]
                if operand not in v_track_labels:
                    self.display('f',operand + " Command argument is not in medialist: " + line)
                    return
        else:
            self.display('f',"unknown Command in Control: " + line)




# ***********************************
# SHOW CONTROL
# ************************************ 

    def check_show_control(self,text,v_show_labels):
        lines = text.split("\n")
        for line in lines:
            self.check_show_control_fields(line,v_show_labels)
            

    def check_show_control_fields(self,line,v_show_labels):
        fields = line.split()
        if len(fields) == 0:
            return
        elif fields[0]=='counter':
            self.check_counters(line,fields[1:])
            return
        # OSC command
        elif fields[0] in ('osc','OSC'):
            if len(fields)<3:
                self.display('f','Show control - Too few fields in OSC command: ' + line)
                return
            else:
                dest=fields[1]
                self.check_osc(line,dest,fields[2:],v_show_labels)
            return

        if fields[0] not in ('beep','exitpipresents','shutdownnow','reboot','open','openexclusive','close','closeall','monitor','event'):
                self.display('f','Show control - Unknown command in: ' + line)
                return
            
        if len(fields)==1:
            if fields[0] not in ('exitpipresents','shutdownnow','reboot','closeall'):
                self.display('f','Show control - Incorrect number of fields in: ' + line)
                return
            
        if len(fields) == 2:
            if fields[0] not in ('beep','open','close','monitor','cec','event','openexclusive'):
                self.display('f','Show Control - Incorrect number of fields: ' + line)
            else:
                if fields[0] =='monitor' and fields[1] not in ('on','off'):
                    self.display('f',"Show Control - monitor parameter not on or off: "+ line)
                    return

                if fields[0] =='cec' and fields[1] not in ('on','standby','scan'):
                    self.display('f',"Show Control - monitor parameter not on standby or scan: "+ line)
                    return

                if fields[0] in ('open','close','openexclusive') and fields[1] not in v_show_labels:
                    self.display('f',"Show Control - cannot find Show Reference: "+ line)
                    return


# ***********************************
# OSC
# ************************************ 

    def check_osc(self,line,dest,fields,v_show_labels):
        if fields[0] not in ('exitpipresents','shutdownnow','reboot','open','close','openexclusive','closeall','monitor','event','send','server-info','loopback','animate'):
                self.display('f','Show control - Unknown command in: ' + line)
                return
            
        if len(fields)==1:
            if fields[0] not in ('exitpipresents','shutdownnow','reboot','closeall','server-info','loopback'):
                self.display('f','Show control, OSC - Incorrect number of fields in: ' + line)
                return
            
        if len(fields) == 2:
            if fields[0] not in ('open','close','openexclusive','monitor','event','send'):
                self.display('f','Show Control, OSC - Incorrect number of fields: ' + line)
            else:
                if fields[0] =='monitor' and fields[1] not in ('on','off'):
                    self.display('f',"Show Control, OSC - monitor parameter not on or off: "+ line)
                    return


# ***********************************
# COUNTERS
# ************************************ 
 
    def check_counters(self,line,fields):
        if len(fields) < 2:
            self.display('f','Show Control too few fields in counter command - ' + ' ' +line)
            return          
        name=fields[0]
        command=fields[1]
        
        if command =='set':
            if len(fields) < 3:
                self.display('f','Show Control too few fields in counter command - ' +line)
                return          

            value=fields[2]
            if not value.isdigit():
                self.display('f','Show Control: value of counter is not a positive integer - ' +line)
                return

        elif command in ('inc','dec'):
            if len(fields) < 3:
                self.display('f','Show Control too few fields in counter command - '  +line)
                return          

            value=fields[2]
            if not value.isdigit():
                self.display('f','Show Control: value of counter is not a positive integer - ' +line)
                return      
        
        elif command =='delete':
            return

        else:
            self.display('f','Show Control: illegal counter comand - ' +line)
            return      

        return

                 
            
# ***********************************
# ANIMATION
# ************************************ 

    def check_animate_fields(self,field,line):
        fields= line.split()
        if len(fields) == 0: return

        if len(fields)<3:
            self.display('f','Too few fields in: ' + field + ", " + line)
            return

        delay_text=fields[0]
        try:
            delay=float(delay_text)
        except:
             self.display('f','Delay is not a number in: ' + field + ", " + line)
             return
        if delay< 0:
            self.display('f','Delay is negative in: ' + field + ", " + line)
        return
    

    
    def check_animate(self,field,text):
        lines = text.split("\n")
        for line in lines:
            self.check_animate_fields(field,line)


# *************************************
#  WEBKIT ZOOM
# ************************************

    def check_webkit_zoom(self,track_type,field,line):
        if track_type=='show' and line.strip()=='':
            self.display('f','show must have Webkit Zoom: ' + field + ", " + line)
            return
            
        if track_type=='track' and line.strip()=='':
            return
            
        try:
            val=float(line)
        except:
            self.display('f','zoom must be a decimal number: ' + field + ", " + line)
            return
        if val< 0:
            self.display('f','zoom must be a positive number: ' + field + ", " + line)
            return
        return 


                
# *************************************
# SHOW CANVAS
# ************************************              
                           
    def check_show_canvas(self,track_type,name,line):
        fields=line.split()
        if len(fields)== 0:
            return

        if len(fields) != 1:
            self.display('f','Wrong number of fields in Show canvas: '+ line)

        status,message,x1,y1,width,height=parse_rectangle(line)
        if status=='error':
            self.display('f','Show Canvas: '+message)
            return
        if x1==-1 and y1==-1:
            self.display('f','Show Canvas: window must include x and y')
            return






            
                     
# *************************************
# PLAYER WINDOW
# ************************************

    def check_player_window(self,track_type,field,line):
        
        words=line.split()
        if track_type == 'show' and len(words) == 0:
            self.display('f','show must have player window: ' + field + ", " + line)
            return
            
        if len(words) == 0:
            return
            
        if len(words) !=1:
            self.display('f','bad track player window form: ' + field + ", " + line)
            return
            
        if words[0] == 'fullscreen':
            return

        status,message,x,y,width,height=parse_rectangle(words[0])
        if status =='error':
            self.display('f',message +': '+ field)
            return
            
        return

# *************************************
#  FONT          
# **********************************

    def check_font(self,field,line):
        if line.strip()=='':
            return
        if 'pt' not in line and 'px' not in line:
             self.display('w','Font does not contain pt or px: '+ field + ", " + line)
             return
        
# *************************************
#  DURATION
# ************************************

    def check_float_duration(self,track_type,field,line):
        if track_type=='show' and line.strip()=='':
            self.display('f','show must have duration: ' + field + ", " + line)
            return
            
        if track_type=='track' and line.strip()=='':
            return
        if line =='0':
            return
        try:
            val=float(line)*10
        except:
            self.display('f','duration must be a decimal number: ' + field + ", " + line)
            return
        if val< 0:
            self.display('f','duration must be a positive number: ' + field + ", " + line)
            return
        if val<1:
            self.display('f','duration must be >= 0.1 or be 0: ' + field + ", " + line)
            return
        return  
        
        
# *************************************
#  HOUR MINUTE SECOND
# ************************************

    def check_hh_mm_ss(self,name,item):          
        fields=item.split(':')
        if len(fields) == 0:
            return
        if len(fields)>3:
            self.display('f','Too many fields in '+ name + ': '  + item)
            return
        if len(fields) == 1:
            seconds=fields[0]
            minutes='0'
            hours='0'
        if len(fields) == 2:
            seconds=fields[1]
            minutes=fields[0]
            hours='0'
        if len(fields) == 3:
            seconds=fields[2]
            minutes=fields[1]
            hours=fields[0]
        if not seconds.isdigit() or not  minutes.isdigit() or  not hours.isdigit():
            self.display('f','Fields of  '+ name + ' are not positive integers: ' + item)
            return        
        if int(minutes)>59 or int(seconds)>59:
            if len(fields)!=1:
                self.display('f','Fields of  '+ name + ' are out of range: ' + item)
            else:
                self.display('w','Seconds or Minutes is greater then 59 in '+ name + ': ' + item)          
            return    
