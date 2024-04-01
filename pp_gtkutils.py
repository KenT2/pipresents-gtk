import os
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib
#from pp_utils import Monitor




# ========================
# CSS 
#=========================
class CSS(object):

    justify_map={'left':Gtk.Justification.LEFT,'center':Gtk.Justification.CENTER,'right':Gtk.Justification.RIGHT}


    def __init__(self):
        return
        #self.mon=Monitor()
        
    def style_widget(self,widget,name,**kwargs):
        css_text=self.format_selector(name,**kwargs)
        status,message,provider=self.get_css(css_text)
        self._add_widget_styling(widget,provider)
      
    def format_selector(self,name,**kwargs):
        css_text='#'+name+'{\n'          
        for key,value in kwargs.items():
            #print (key,value)
            key=key.replace('_','-')
            if key=='font':
                new_value=self.reformat_font(value)

            else:
                new_value=value
            css_text+=key+': '+new_value+';\n'
        css_text+='}\n'
        #print (css_text)
        return css_text
        
    def reformat_font(self,value):
        new_value=''
        if 'pt ' in value or 'px ' in value:
            return value
        fields= value.split(' ')
        #print (fields)
        if len(fields) == 4:
            new_value= fields[3]+' '+fields[2]
        if len(fields)==3:
            new_value=' '+fields[2]
        new_value+= ' '+fields[1]+'pt '+fields[0]
        print ('WARNING: ',value,' should be ',new_value)
        return new_value
        
                   
    def load_css(self, css_fn):
        if not os.path.exists(css_fn):
            return 'error','CSS file does not exist: '+css_fn,None
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_path(css_fn)
        except GLib.Error as e:
            print('ERROR: pp_gtkutils, Error loading CSS from '+css_fn+ ' \nMessage is '+e)
            return 'error','Error loading CSS from '+css_fn+ ' Message is '+e
        return 'normal','Loaded CSS',css_provider


    def get_css(self, css_text):
        with open('/tmp/css_text.txt','w') as f:
            f.write(css_text)
        css_provider = Gtk.CssProvider()
        css_provider.connect('parsing-error',self.css_error,css_text)
        try:
            css_provider.load_from_path('/tmp/css_text.txt')
        except GLib.Error as e:
            print ('failed to load CSS from tmp file: ',e)
            return 'error','Error loading CSS from '+css_text+ ' Message is '+e
        return 'normal','got CSS from string',css_provider


    def css_error(self,provider,section,error,css_text):
        print ('CSS ERROR  IN: \n',css_text,'at',section.to_string(),'\n',error)


    def _add_widget_styling(self, widget,css_provider):
        #print (widget)
        if css_provider:
            context = widget.get_style_context()
            context.add_provider(
                css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def add_custom_styling(self, widget,css_provider):
        self._add_widget_styling(widget,css_provider)
        # iterate children recursive
        for child in widget:
            self.add_custom_styling(child,css_provider)



        
class Test(object):

    def init(self):
        app = Gtk.Application()
        app.connect('activate', self.on_activate)
        app.run(None)       
        
    def on_activate(self,app):
        self.dialog = PPDialog(app,self.on_callback,ok=True,cancel=False,text='hello')
        print ('dropped through')
        
    def on_callback(self):
        print('callback')



if __name__ == '__main__':
    disp=Test()
    disp.init()
