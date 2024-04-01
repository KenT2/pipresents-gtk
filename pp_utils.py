import time
import datetime
import sys
import os
import gc
import subprocess
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib
from pp_gtkutils import CSS 
from pp_statsrecorder import Statsrecorder
# from pympler.tracker import SummaryTracker
# from pympler import summary, muppy
# import types

# Determine model of Pi - 1,2,3,4
## awk '/^Revision/ {sub("^1000", "", $3); print $3}' /proc/cpuinfo 

def find_pi_model():
    command=['cat', '/proc/device-tree/model']
    l_reply=subprocess.run(command,stdout=subprocess.PIPE)
    l_reply_list=l_reply.stdout.decode('utf-8').split(' ')
    if l_reply_list[2] == 'Zero':
        return 0
    elif l_reply_list[2] == 'Model':
        return 1
    else:
        return int(l_reply_list[2])

def calculate_text_position(x_text,y_text,x1,y1,canvas_width,canvas_height,widget):
    
    #print(x_text,y_text,x1,y1,canvas_width,canvas_height)
    size=widget.get_preferred_size()
    text_width=size.natural_size.width
    text_height=size.natural_size.height
    #print (size.natural_size.width,size.natural_size.height)

    if x_text == '':
        x=x1+(canvas_width-text_width)/2 
    else:
        x = x1+int(x_text)
        
    if y_text == '':
        y=y1+(canvas_height-text_height)/2 
    else:
        y=y1+int(y_text)
    #print(x,y)
    return x,y

            
def parse_rectangle(text):
    if text.strip() == '':
        return 'error','Window is blank: '+text,0,0,0,0
    if '+' in text:
        # parse  x+y+width*height
        fields=text.split('+')
        if len(fields) != 3:
            return 'error','Bad window form: '+ text,0,0,0,0
            
        dimensions=fields[2].split('*')
        if len(dimensions)!=2:
            return 'error','Bad window form: '+text,0,0,0,0
        
        if not fields[0].isdigit():
            return 'error','x1 is not a positive integer: '+ text,0,0,0,0
        else:
            x1=int(fields[0])
        
        if not fields[1].isdigit():
            return 'error','y1 is not a positive integer: '+ text,0,0,0,0
        else:
            y1=int(fields[1])
            
        if not dimensions[0].isdigit():
            return 'error','width is not a positive integer: '+text,0,0,0,0
        else:
            width=int(dimensions[0])
            
        if not dimensions[1].isdigit():
            return 'error','height is not a positive integer: '+text,0,0,0,0
        else:
            height=int(dimensions[1])
        return 'normal','',x1,y1,width,height
    else:
        if not '*' in text:
            return 'error','Bad window form: '+text,0,0,0,0
        dimensions=text.split('*')
        if len (dimensions) !=2:
            return 'error','Bad window form: '+ text,0,0,0,0
        if not dimensions[0].isdigit():
            return 'error','width is not a positive integer: '+text,0,0,0,0
        else:
            width=int(dimensions[0])
            
        if not dimensions[1].isdigit():
            return 'error','height is not a positive integer: '+text,0,0,0,0
        else:
            height=int(dimensions[1])
        return 'normal','',-1,-1,width,height     



# !!!!!! used for web_editor only
def calculate_relative_path(file_path,pp_home_dir,pp_profile_dir):
        # is media in the profile
        # print 'pp_profile dir ',pp_profile_dir
        in_profile=False
        if pp_profile_dir in file_path:
            in_profile=True
            
        if in_profile is True:
            # deal with media in profile @
            relpath = os.path.relpath(file_path,pp_profile_dir)
            # print "@ relative path ",relpath
            common = os.path.commonprefix([file_path,pp_profile_dir])
            # print "@ common ",common
            if common == pp_profile_dir:
                location = "@" + os.sep + relpath
                location = str.replace(location,'\\','/')
                # print '@location ',location
                # print
                return location
            else:
                # print '@absolute ',file_path
                return file_path            
        else:
            # deal with media in pp_home  +     
            relpath = os.path.relpath(file_path,pp_home_dir)
            # print "+ relative path ",relpath
            common = os.path.commonprefix([file_path,pp_home_dir])
            # print "+ common ",common
            if common == pp_home_dir:
                location = "+" + os.sep + relpath
                location = str.replace(location,'\\','/')
                # print '+location ', location
                # print
                return location
            else:
                # print '+ absolute ',file_path
                # print
                return file_path

 

class StopWatch(object):
    
    global_enable=False

    def __init__(self):
        self.enable=False

    def on(self):
        self.enable=True

    def off(self):
        self.enable=False
    
    def start(self):
        if StopWatch.global_enable and self.enable:
            self.sstart=time.clock()

    def split(self,text):
        if StopWatch.global_enable and self.enable:
            self.end=time.clock()
            print(text + " " + str(self.end-self.sstart) + " secs")
            self.sstart=time.clock()
        
    def stop(self,text):
        if StopWatch.global_enable and self.enable:
            self.end=time.clock()
            print(text + " " + str(self.end-self.sstart) + " secs")



class PPDialog(object):
    def __init__(self,app,develop_window,callback,ok=True,finish=-1,text='none provided',title='Pi Presents'):
        self.mon=Monitor()
        self.css=CSS()
        self.callback=callback
        self.finish=finish
        self.win=Gtk.Window(application=app)
        self.win.set_deletable(False)
        self.win.set_title(title)
        self.win.set_modal(True)
        self.win.set_transient_for(develop_window)
        #self.win.set_focus()
        self.win.connect('close-request',self.on_ok_clicked)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.win.set_child(box)
        text_box= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        button_box.set_halign(Gtk.Align.END)
        box.append(text_box)
        box.append(button_box)
        
        label=Gtk.Label(label=text)
        label.set_name('dialog-text')
        label.set_justify(Gtk.Justification.CENTER)
        self.css.style_widget(label,'dialog-text',font = '15pt helvetica',padding_top='20px',padding_left='20px',padding_right='20px')
        text_box.append(label)
                    
        if ok is True:
            ok_button = Gtk.Button(label="OK")
            ok_button.connect("clicked", self.on_ok_clicked)
            button_box.append(ok_button)
        develop_window.set_visible(False)
        self.win.present()
        #self.ok_clicked=False
        #self.ok_timer=None
        #GLib.timeout_add(100,self.wait_for_ok)
        print('in dialog')
        
    def wait_for_ok(self):
        if self.ok_timer is not None:
            GLib.source_remove(self.ok_timer)
            self.ok_timer=None
        if self.ok_clicked is True:
            self.ok_clicked=False
            print ('returning from dialog')
            return
        else:
            print ('wait in dialog')
            self.ok_timer=GLib.timeout_add(1000,self.wait_for_ok)
        
        
    def on_ok_clicked(self, widget):
        print("OK clicked")
        #self.ok_clicked=True
        self.mon.finish()
        self.win.destroy()
        if self.callback!=None:
            self.callback()
        if self.finish!=-1:
            sys.exit(self.finish)

        


class Monitor(object):

    delimiter=';'

    m_fatal =1    # fatal erros caused by PiPresents, could be a consequence of an 'error'
    m_err = 2  # PP cannot continue because of an error caused by user in profile or command
    m_warn =4  # warning that something is not quite right but PP recovers gracefully
    m_log =8  # log of interest to profile developers
    m_trace =16 # trace for software development
    m_trace_instance =32 # trace with id of instances of player and showers
    m_leak = 64 # memory leak monitoring
    m_stats = 128  #statistics
    m_sched = 256 #  time of day scheduler

    classes  = []
    
    log_level=0              
    log_path=""            # set in pipresents
    ofile=None

    start_time= time.time()
    tracker=None
    show_count=0
    track_count=0

    stats_file=None
    sr=None          #
    app=None
    develop_window=None

# called at start by pipresents
    def init(self,app,develop_window):
        Monitor.app=app
        Monitor.develop_window=develop_window
        # Monitor.tracker = SummaryTracker()
        if Monitor.ofile is None:
            bufsize=-1
            Monitor.ofile=open(Monitor.log_path+ os.sep+'pp_logs' + os.sep + 'pp_log.txt','w',bufsize)
        Monitor.log_level=0     # set in pipresents
        Monitor.manager=False  #set in pipresents
        Monitor.classes  = []
        Monitor.enable_in_code = False  # enables use of self.mon.set_log_level(nn) in classes
        
        Monitor.sr=Statsrecorder()
        Monitor.sr.init(Monitor.log_path)



    def leak_diff(self):
        Monitor.tracker.print_diff()

    def leak_summary(self):
        all_objects = muppy.get_objects()
        sum1 = summary.summarize(all_objects)
        summary.print_(sum1)   


    def leak_anal(self):
        all_objects = muppy.get_objects()
        my_types = muppy.filter(all_objects, Type=ImagePlayer)
        print(len(my_types))                                    
        for t in my_types:
            print(t,sys.getrefcount(t))
            # ,gc.get_referrers(t) 

    # CONTROL

    def __init__(self):
        # default value for individual class logging
        self.this_class_level= Monitor.m_fatal|Monitor.m_err|Monitor.m_warn

    def set_log_level(self,level):
        self.this_class_level = level


    # PRINTING
  
    def newline(self,num):
        if Monitor.manager is False:
            if Monitor.log_level & ~ (Monitor.m_warn|Monitor.m_err|Monitor.m_fatal|Monitor.m_sched) != 0:
                for i in range(0,num):
                    print()

    def fatal(self,caller,text):
        r_class=caller.__class__.__name__
        r_func = sys._getframe(1).f_code.co_name
        r_line =  str(sys._getframe(1).f_lineno)
        if self.enabled(r_class,Monitor.m_fatal) is True: 
            print("%.2f" % (time.time()-Monitor.start_time), " System Error: ",r_class+"/"+ r_func + "/"+ r_line + ": ", text)
            Monitor.ofile.write (" SYSTEM ERROR: " + r_class +"/"+ r_func + "/"+ r_line + ": " + text + "\n")
        if Monitor.manager is False:
            all_text=r_class +'\n'+text
            PPDialog(Monitor.app,Monitor.develop_window,None,ok=True,finish=102,text=all_text,title='System Error')

    def err(self,caller,text):
        r_class=caller.__class__.__name__
        if self.enabled(r_class,Monitor.m_err) is True:        
            print("%.2f" % (time.time()-Monitor.start_time), " Profile Error: ",r_class+": ", text)
            Monitor.ofile.write (" ERROR: " + self.pretty_inst(caller)+ ":  " + text + "\n")
        if Monitor.manager is False:
            all_text=r_class +'\n'+text
            PPDialog(Monitor.app,Monitor.develop_window,None,ok=True,finish=102,text=all_text,title='Profile Error')
            
                                        
    def warn(self,caller,text):
        r_class=caller.__class__.__name__
        if self.enabled(r_class,Monitor.m_warn) is True:     
            print("%.2f" % (time.time()-Monitor.start_time), " Warning: ",self.pretty_inst(caller) +": ", text)
            Monitor.ofile.write (" WARNING: " + self.pretty_inst(caller)+ ":  " + text + "\n")

    def sched(self,caller,pipresents_time,text):
        r_class=caller.__class__.__name__
        if self.enabled(r_class,Monitor.m_sched) is True:
            if pipresents_time is None:
                ptime='       '
            else:
                ptime=str(pipresents_time)
            print(ptime +" "+r_class+": " + text)
            # print "%.2f" % (time.time()-Monitor.start_time) +" "+self.pretty_inst(caller)+": " + text
            Monitor.ofile.write (time.strftime("%Y-%m-%d %H:%M") + " " + self.pretty_inst(caller)+": " + text+"\n")



    def log(self,caller,text):
        r_class=caller.__class__.__name__
        if self.enabled(r_class,Monitor.m_log) is True:
            print("%.2f" % (time.time()-Monitor.start_time) +" "+r_class+": " + text)
            # print "%.2f" % (time.time()-Monitor.start_time) +" "+self.pretty_inst(caller)+": " + text
            Monitor.ofile.write (str(time.time()-Monitor.start_time) + " " + self.pretty_inst(caller)+": " + text+"\n")

    def start_stats(self,profile):
            Monitor.profile = profile        
            self.stats((""),(""),(""),("start"),(""),(""),(""),(profile))

    def stats(self,*args):
        if (Monitor.m_stats & Monitor.log_level) != 0:
            Monitor.sr.write_stats(datetime.datetime.now(),Monitor.profile,*args)
     
            
    def trace(self,caller,text):
        r_class=caller.__class__.__name__
        r_class = type(caller).__name__
        r_func = sys._getframe(1).f_code.co_name
        r_line =  str(sys._getframe(1).f_lineno)
        r_id = 'id='+str(id(caller))
        r_longid = caller
        # self.print_info(r_class,Monitor.m_trace)
        if self.enabled(r_class,Monitor.m_trace) is True:
            print(self.pretty_inst(caller)+'/'+r_func, text)
            Monitor.ofile.write ( self.pretty_inst(caller)+" /" + r_func +" " + text+"\n")

    def print_info(self,r_class,mask):
        print('called from', r_class)
        print('Global Log level',Monitor.log_level)
        print('Global enable in code', Monitor.enable_in_code)
        print('in code log level',self.this_class_level)
        print('Trace mask',mask)
             
    def enabled(self,r_class,report):
        enabled_in_code=(report & self.this_class_level) != 0 and Monitor.enable_in_code is True
        
        globally_enabled=(report & Monitor.log_level) !=0 and r_class in Monitor.classes
        
        if enabled_in_code is True or globally_enabled is True:
            return True
        else:
            return False

    def pretty_inst(self,inst):
        if inst is None:
            return 'None'
        else:
            return inst.__class__.__name__ + '_' + str(id(inst))
  
    def finish(self):
        Monitor.ofile.close()
        Monitor.sr.close()
        # krt
        Monitor.ofile=None

##    def id(self,caller):
##        return self.pretty_inst(caller)

