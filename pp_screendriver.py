import os
import configparser
import copy
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib
from pp_gtkutils import CSS
from pp_utils import Monitor, parse_rectangle
from pp_displaymanager import DisplayManager

class ScreenDriver(object):

    display_names=[]      # name of display
    click_area_names=[]   #name of click area
    canvas_ids=[]         #canvas object on which to display click area
    button_ids=[]         # button object
    image_ids=[]          # image object
    text_ids=[]           # text object
    x=[]
    y=[]
    callback=None

    def __init__(self):
        self.mon=Monitor()
        self.dm=DisplayManager()
        self.css=CSS()
    


    # read screen.cfg    
    def read(self,pp_dir,pp_home,pp_profile):
        self.pp_dir=pp_dir
        self.pp_home=pp_home
        # try inside profile
        tryfile=pp_profile+os.sep+'pp_io_config'+os.sep+'screen.cfg'
        # self.mon.log(self,"Trying screen.cfg in profile at: "+ tryfile)
        if os.path.exists(tryfile):
            filename=tryfile
        else:
            #give congiparser an empty filename so it returns an empty config.
            filename=''
        ScreenDriver.config = configparser.ConfigParser(inline_comment_prefixes = (';',))
        ScreenDriver.config.read(filename)
        if filename != '':
            self.mon.log(self,"screen.cfg read from "+ filename)
        return 'normal','screen.cfg read'

    def click_areas(self):
        return ScreenDriver.config.sections()

    def get(self,section,item):
        return ScreenDriver.config.get(section,item)

    def is_in_config(self,section,item):
        return ScreenDriver.config.has_option(section,item)


    def parse_displays(self,text):
        return text.split(' ')
    
    # make click areas on the screen and hide them
    # canvas is the PiPresents canvas
    
    def make_click_areas(self,callback):
        # called once at start
        ScreenDriver.callback=callback

        for area in self.click_areas():
            #print ('\nNAME',self.get(area,'name'))
            if not self.is_in_config(area,'displays'):
                return 'error','screen.cfg. Missing displays field in ['+area+']'           
            displays_list=self.parse_displays(self.get(area,'displays'))
            # print ('\n\n',displays_list)
            
            status,message,shape,x,y,width,height = self.parse_points(self.get(area,'points'),self.get(area,'name'))
            if status == 'error':
                return status,'screen.cfg, '+message+ ' in ['+area+']'

            for display_name in DisplayManager.display_map:
                #print (display_name,displays_list)
                if display_name in displays_list:
                    status,message,display_name=self.dm.is_display_connected(display_name)
                    #print (status,display_name)
                    if status!='normal':
                        continue
                    # get params from .cfg
                    canvas= self.dm.get_canvas_obj(display_name)
                    ScreenDriver.canvas_ids.append(canvas)
                    ScreenDriver.display_names.append(display_name)
                    click_area_name=self.get(area,'name')
                    ScreenDriver.click_area_names.append(click_area_name)
                    ScreenDriver.x.append(x)
                    ScreenDriver.y.append(y)
                    status,message,image_path=self.get_image(area)
                    if status =='error':
                        return status,'screen.cfg. '+message +  ' in ['+area+']'
                    
                    #make click area
                    status,message,image_path=self.get_image(area)
                    if status =='error':
                        return status,'screen.cfg. '+message +  ' in ['+area+']'                  

                    image=Gtk.Picture.new_for_filename(image_path)
                    image.set_content_fit(Gtk.ContentFit.FILL)
                    image.set_name('click-area-image-'+area)
                    label=None
                    if self.get(area,'text') !='':
                        label=Gtk.Label()
                        label.set_label(self.get(area,'text'))
                        label.set_name('click-area-text-'+area)
                        if self.get (area,'text-colour')=='':
                            message= 'text colour is blank '
                            return 'error','screen.cfg. '+ message +  ' in ['+area+']'  
                        if self.get (area,'text-font')=='':
                            message= 'text font is blank '
                            return 'error','screen.cfg. '+message +  ' in ['+area+']'  
                        self.css.style_widget(label,'click-area-text-'+area,
                                        color = self.get (area,'text-colour'),
                                        font = self.get(area,'text-font'))
                                        
                    button_id=Gtk.Button()
                    button_id.set_size_request(width,height)
                    button_id.set_name('click-area-button-'+area)
                    if self.get (area,'fill-colour')=='':
                            message= 'fill colour is blank '
                            return 'error','screen.cfg. '+message +  ' in ['+area+']'  
                    if self.get (area,'outline-colour')=='':
                            message= 'outline colour is blank '
                            return 'error','screen.cfg. '+message +  ' in ['+area+']'
                    if shape=='circle':
                        button_id.add_css_class ("circular")
                        
                    self.css.style_widget(button_id,'click-area-button-'+area,
                                        background=self.get(area,'fill-colour'),border_color=self.get (area,'outline-colour'),
                                        padding_left='0px',padding_right='0px',padding_top='0px',padding_bottom='0px',
                                        border_left_width='2px',border_right_width='2px',border_top_width='2px',border_bottom_width='2px')
                    overlay=Gtk.Overlay()
                    button_id.set_child(overlay)
                    if image_path!='':
                        overlay.add_overlay(image)
                    if label is not None:
                        overlay.add_overlay(label)
                    button_id.connect('clicked',self.button_clicked,click_area_name)

                    ScreenDriver.button_ids.append(button_id)
                    
        return 'normal','made click areas'
                    


    def get_image(self,area):
        # image for the button
        if not self.is_in_config(area,'image'):
            return 'error','missing image fields in screen.cfg',''
        image_name=self.get(area,'image')
        if image_name !='':
            image_path=self.complete_path(image_name)
            if os.path.exists(image_path) is True:
                #print(image_path)
                return 'normal','',image_path
            else:
                image_path=self.pp_dir+os.sep+'pp_resources'+os.sep+'button.jpg'
                if os.path.exists(image_path) is True:
                    #self.mon.warn(self,'Default button image used for '+ area)
                    return 'normal','',image_path
                else:
                    #self.mon.warn(self,'Button image not found for '+ area)
                    image_path=''
                    return 'error','Button image not found ',''
        else:
            return 'normal','',''


    def find_click_area(self,symname,canvas):
        for index,name in enumerate(ScreenDriver.display_names):
            #print (index,symname,ScreenDriver.click_area_names[index])
            if symname == ScreenDriver.click_area_names[index] and canvas==ScreenDriver.canvas_ids[index]:
                return index
        return -1
                                                      

    # use links with the symbolic name of click areas to enable the click areas in a show
    def enable_click_areas(self,links,canvas):
        for link in links:
            #print (link)
            index=self.find_click_area(link[0],canvas)
            if index!=-1 and link[1] != 'null':
                if ScreenDriver.button_ids[index] !=None:
                    ScreenDriver.canvas_ids[index].put(ScreenDriver.button_ids[index],ScreenDriver.x[index],ScreenDriver.y[index])
                    ScreenDriver.button_ids[index].set_visible(True)
                    ScreenDriver.button_ids[index].set_sensitive(True)

                    
    def button_clicked(self,button,name):
        #print (name)
        ScreenDriver.callback(name,'SCREEN')
        

    def hide_click_areas(self,links,canvas):
        for link in links:
            index=self.find_click_area(link[0],canvas)
            if index!=-1 and link[1] != 'null':
                if ScreenDriver.button_ids[index] !=None:
                    canvas.remove(ScreenDriver.button_ids[index])
                    #ScreenDriver.button_ids[index].set_visible(False)

    def parse_points(self,text,name):
        fields=text.split(' ')
        if len (fields)!=2:
            return 'error','do not understand points: '+text,'',0,0,0,0
        if fields[0] not in ('rectangle','circle'):
            return 'error','unknown shape in: '+text,'',0,0,0,0
        status,message,x,y,width,height=parse_rectangle(fields[1])
        if status =='error':
            return status,message,'',0,0,0,0
        return 'normal','',fields[0],x,y,width,height
                    
                    
    """
    def parse_points(self,points_text,area):
        if points_text.strip() == '':
            return 'error','No points in click area: '+area,[]
        if '+' in points_text:
            # parse  x+y+width*height
            fields=points_text.split('+')
            if len(fields) != 3:
                return 'error','Do not understand click area points: '+area,[]
            dimensions=fields[2].split('*')
            if len(dimensions)!=2:
                return 'error','Do not understand click area points: '+area,[]
            
            if not fields[0].isdigit():
                return 'error','x1 is not a positive integer in click area: '+area,[]
            else:
                x1=int(fields[0])
            
            if not fields[1].isdigit():
                return 'error','y1 is not a positive integer in click area: '+area,[]
            else:
                y1=int(fields[1])
                
            if not dimensions[0].isdigit():
                return 'error','width1 is not a positive integer in click area: '+area,[]
            else:
                width=int(dimensions[0])
                
            if not dimensions[1].isdigit():
                return 'error','height is not a positive integer in click area: '+area,[]
            else:
                height=int(dimensions[1])

            return 'normal','',[str(x1),str(y1),str(x1+width),str(y1),str(x1+width),str(y1+height),str(x1),str(y1+height)]
            
        else:
            # parse unlimited set of x,y,coords
            points=points_text.split()
            if len(points) < 6:
                return 'error','Less than 3 vertices in click area: '+area,[]
            if len(points)%2 != 0:
                return 'error','Odd number of points in click area: '+area,[]      
            for point in points:
                if not point.isdigit():
                    return 'error','point is not a positive integer in click area: '+area,[]
            return 'normal','parsed points OK',points
    """

    def complete_path(self,track_file):
        #  complete path of the filename of the selected entry
        if track_file != '' and track_file[0]=="+":
            track_file=self.pp_home+track_file[1:]
        elif track_file[0] == "@":
            track_file=self.pp_profile+track_file[1:]
        return track_file   
