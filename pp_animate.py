import time
import copy
import csv
from pp_utils import Monitor
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GLib


class Animate(object):
    """
     allows players to put events, which request the change of state of pins, into a queue. Events are executed at the required time.
     using the interface to an output driver.
   """

# constants for sequencer events list          
    
    name = 0         # GPIO pin number, the xx in P1-xx
    param_type = 1
    param_values = 2    # off , on
    time = 3        # time since the epoch in seconds
    tag = 4   # tag used to delete all matching events, usually a track reference.
    set_time=5
    delay=6
    event_template=['','','',0,None,0,0]
    
# CLASS VARIABLES (Animate.)
    events=[]
    last_poll_time=0

# executed by main program and by each object using animate
    def __init__(self):
        self.mon=Monitor()

    # executed once from main program   
    def init(self,pp_dir,pp_home,pp_profile,widget,sequencer_tick,event_callback):
        
        # instantiate arguments
        self.widget=widget    #something to hang 'after' on
        self.pp_dir=pp_dir
        self.pp_profile=pp_profile
        self.pp_home=pp_home
        self.sequencer_tick=sequencer_tick
        self.event_callback=event_callback
        
        # Initialise time used by sequencer
        Animate.origin_time=time.time()
        Animate.sequencer_time=0
        self.mon.log(self,'Init actual time'+'   '+str(Animate.origin_time))
                
        # init timer
        self.sequencer_tick_timer=None

    # called by main program only                
    def terminate(self):
        if self.sequencer_tick_timer is not None:
            GLib.source_remove(self.sequencer_tick_timer)
        self.clear_events_list(None)


# ************************************************
# output sequencer
# ************************************************

    # called by main program only         
    def poll(self):
        if self.sequencer_tick_timer is not None:
            GLib.source_remove(self.sequencer_tick_timer)
            self.sequencer_tick_timer=None       
        poll_time=time.time()
        Animate.sequencer_time=poll_time-Animate.origin_time
        #print(Animate.sequencer_time)
        self.do_sequencer()
        self.sequencer_tick_timer=GLib.timeout_add(self.sequencer_tick,self.poll)
        return False

    # execute events at the appropriate time and remove from list (runs from main program only)
    # runs through list a number of times because of problems with pop messing up list
    def do_sequencer(self):
        while True:
            event_found=False
            for index, item in enumerate(Animate.events):
                if Animate.sequencer_time>=item[Animate.time]:
                    #self.mon.log(self,'do event required at '+'%.2f' % (item[Animate.delay]+item[Animate.set_time])+' at actual time '+'%.2f' % (Animate.sequencer_time))
                    event=Animate.events.pop(index)
                    event_found=True
                    self.mon.log(self, 'send event '+ event[Animate.name] + ' ' +event[Animate.param_type] + ' ' + ' '.join(event[Animate.param_values])+' required at '+'%.2f' % (item[Animate.delay]+item[Animate.set_time])+' sent at '+'%.2f' % (Animate.sequencer_time))
                    self.send_event(event[Animate.name],event[Animate.param_type],event[Animate.param_values],item[Animate.time])
                    break
            if event_found is False: break

    def send_event(self,name,param_type,param_values,req_time):
        self.event_callback(name,param_type,param_values,req_time)



# ************************************************
# output sequencer interface methods
# these can be called from many classes so need to operate on class variables
# ************************************************

    def animate(self,text,tag):
        lines = text.split("\n")
        for line in lines:
            #print(line)
            reason,message,delay,name,param_type,param_values=self.parse_animate_fields(line)
            if reason == 'error':
                return 'error',message
            if name !='':
                self.add_event(name,param_type,param_values,delay,tag)
        return 'normal','events processed'


    def add_event(self,name,param_type,param_values,delay,tag):
        #time at start of track
        set_time=Animate.sequencer_time
        # prepare the event
        event=Animate.event_template
        event[Animate.set_time]=set_time
        event[Animate.delay]=delay
        event[Animate.name]=name
        event[Animate.param_type]=param_type
        event[Animate.param_values]=param_values
        abs_time=delay+set_time
        event[Animate.time]=abs_time
        event[Animate.tag]=tag
        #print ('\nadd event ',event)
        # find the place in the events list and insert
        # first item in the list is earliest, if two have the same time then last to be added is fired last.
        # events are fired from top of list
        # print 'new event',abs_time
        copy_event= copy.deepcopy(event)
        length=len(Animate.events)
        if length ==0:
                Animate.events.append(copy_event)
                # print 'append to empty ist',abs_time
                return copy_event
        else:
            index=length-1
            if abs_time>Animate.events[index][Animate.time]:
                Animate.events.append(copy_event)
                # print 'append to end of list if greater than last item',abs_time
                return copy_event
            while index!=-1:
                if abs_time==Animate.events[index][Animate.time]:                
                    Animate.events.insert(index+1,copy_event)
                    # print 'insert after if equal',abs_time
                    return copy_event
                if abs_time>Animate.events[index][Animate.time]:                
                    Animate.events.insert(index+1,copy_event)
                    # print 'insert after if later',abs_time
                    return copy_event
                if index==0:                
                    Animate.events.insert(index,copy_event)
                    # print 'insert before if at start of list',abs_time
                    return copy_event
                index -=1
            # print 'error at start of list',abs_time
        #self.print_events()


    def print_events(self):
        print('events list')
        for event in Animate.events:
            print('EVENT: ',event)

    

    # remove all the events with the same tag, usually a track reference
    def remove_events(self,tag):
        left=[]
        for item in Animate.events:
            if tag != item[Animate.tag]:
                left.append(item)
        Animate.events= left
        # self.print_events()


    # clear event list
    def clear_events_list(self,tag):
        self.mon.log(self,'clear events list ')
        # empty event list
        Animate.events=[]


    # [delay],symbol,type,values(one or more)
    def parse_animate_fields(self,line):
        if line== '':
            return 'normal','no fields','','',[],0
        # split the line using "" for text with spaces
        for l in csv.reader([line], delimiter=' ', skipinitialspace = True,quotechar='"'):
            fields = l

        if len(fields) == 0:
            return 'normal','no fields','','',[],0
            
        elif len(fields) < 3: 
            return 'error','too few fields in : '+ line,'','',[],0

        delay_text=fields[0]
        # check each field
        try:
            delay=float(delay_text)
        except:
            return 'error','Delay is not a number : '+ line,'','',[],0
        if delay< 0:
            return 'error','Delay is negative : '+ line,'','',[],0

        """
        if  not delay_text.isdigit():
            return 'error','Delay is not an integer in : '+ line,'','',[],0
        else:
            delay=int(delay_text)
        """
            
        name=fields[1]


        if len(fields)==2:
            param_type=''
            params=[]
        else:
            param_type=fields[2]
            params=[]
            for index in range(3, len(fields)):
                param=fields[index]
                params.append(param)
    
        # print ('event parsed OK',delay,name,param_type,params)
        return 'normal','event parsed OK',delay,name,param_type,params
        

