class PPdefinitions(object):
    DEFINITIONS_VERSION_STRING='1.6.1'
    IMAGE_FILES=('Image files', '.gif','.jpg','.jpeg','.bmp','.png','.tif')
    VIDEO_FILES= ('Video Files','.asf','.avi','.mpg','.mp4','.mpeg','.m2v','.m1v','.vob','.divx','.xvid','.mov','.m4v','.m2p','.mkv','.m2ts','.ts','.mts','.wmv','.webm')
    AUDIO_FILES=('Audio files','.mp3','.wav','.ogg','.ogm','.wma','.asf','.mp2')
    WEB_FILES=('Web files','.htm','.html')


    def definitions_version(self):
        vitems=PPdefinitions.DEFINITIONS_VERSION_STRING.split('.')
        return 1000*int(vitems[0])+100*int(vitems[1])+int(vitems[2])

    # order of fields for editor display and which tab they are in.
    show_types={

        'artliveshow':[
            'tab-show','sep',  
                'type','title','show-ref', 'display-name','medialist','live-tracks-dir1','live-tracks-dir2','sequence','repeat','show-canvas',
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-justify','eggtimer-font','eggtimer-colour',
            'tab-notices','sep',              
                'empty-text','admin-x','admin-y','admin-font','admin-colour','admin-justify',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep',
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',
                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',
                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                'webkit-window','webkit-zoom','webkit-freeze-at-end',
                
            'tab-controls','sep',  
                'disable-controls','controls',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','sep','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',

            ],

        'artmediashow':[
            'tab-show','sep',  
                'type','title','show-ref', 'display-name','medialist','sequence','repeat','show-canvas',
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-justify','eggtimer-font','eggtimer-colour',
            'tab-notices','sep',              
                'empty-text','admin-x','admin-y','admin-font','admin-colour','admin-justify',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep',  
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',
                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',
                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                'webkit-window','webkit-zoom','webkit-freeze-at-end',

            'tab-controls','sep',  
                'disable-controls','controls',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','sep','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',
            ],
    
        'mediashow':[
            'tab-show','sep',  
                     'type','title','show-ref', 'display-name', 'medialist','show-timeout',
            'trigger-start-type','trigger-start-param','trigger-next-type','trigger-next-param','sequence','track-count-limit','repeat','interval','trigger-end-type','trigger-end-param',
            'empty-track-ref','escape-track-ref','sep','show-canvas',
            'tab-child','sep',  
                'child-track-ref', 'hint-text', 'hint-x','hint-y','hint-justify','hint-font','hint-colour',
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-justify','eggtimer-font','eggtimer-colour',
            'tab-notices','sep',              
            'trigger-wait-text','admin-x','admin-y','admin-justify','admin-font','admin-colour',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep',
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',
                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',
                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                 'webkit-window','webkit-zoom','webkit-freeze-at-end',
                
            'tab-controls','sep',  
                    'disable-controls', 'controls',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','sep','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',
            ],
                 
        'menu':[
            'tab-show','sep',  
                'type','title','show-ref','display-name','medialist','show-timeout','track-timeout','menu-track-ref','show-canvas',
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-justify','eggtimer-font','eggtimer-colour',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep',
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',
                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',

                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                 'webkit-window','webkit-zoom','webkit-freeze-at-end',

            'tab-controls','sep',  
               'disable-controls','controls',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','sep','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',
            ],

        
        'liveshow':[
            'tab-show','sep',  
                'type','title','show-ref', 'display-name','medialist','live-tracks-dir1','live-tracks-dir2','show-timeout','sep',
            'trigger-start-type','trigger-start-param','trigger-next-type','trigger-next-param','sequence','track-count-limit','repeat','interval','trigger-end-type','trigger-end-param',
            'empty-track-ref','escape-track-ref','sep','show-canvas',
            'tab-child','sep',  
                    'child-track-ref', 'hint-text', 'hint-x','hint-y','hint-justify','hint-font','hint-colour',
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-justify','eggtimer-font','eggtimer-colour',
            'tab-notices','sep',              
                'trigger-wait-text','admin-x','admin-y','admin-justify','admin-font','admin-colour',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep',
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',

                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',

                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                 'webkit-window','webkit-zoom','webkit-freeze-at-end',
                                
            'tab-controls','sep',  
                'disable-controls','controls',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','show-control-empty','show-control-not-empty','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',
            ],


                   
        'hyperlinkshow':[
            'tab-show','sep',  
                'type','title','show-ref','display-name','medialist','first-track-ref','home-track-ref','show-timeout','track-timeout','timeout-track-ref','show-canvas', 'debug-path',         
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-justify','eggtimer-font','eggtimer-colour',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep', 
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',
                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',

                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                 'webkit-window','webkit-zoom','webkit-freeze-at-end',
           
            'tab-links','sep',
                'disable-controls','links',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','sep','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',
            ],
        

        'radiobuttonshow':[
            'tab-show','sep',  
                'type','title','show-ref','display-name','medialist','first-track-ref','show-timeout','track-timeout','show-canvas','controls-in-subshows',
            'tab-eggtimer','sep',  
                 'eggtimer-text','eggtimer-x','eggtimer-y','eggtimer-font','eggtimer-justify','eggtimer-colour',
            'tab-show-text','sep',
                   'background-image','background-colour','show-text','show-text-location','show-text-x','show-text-y','show-text-type','sep','show-text-font','show-text-colour','show-text-justify',
                   'sep','show-html-height','show-html-width','show-html-background-colour',
            'tab-tracks','sep',  
                 'duration','pause-timeout','image-window','image-aspect-mode','transition','sep',
                'mpv-audio','mpv-speaker','mpv-volume','mpv-window','mpv-aspect-mode','mpv-freeze-at-start','mpv-freeze-at-end','mpv-other-options','sep',

                 'track-text-font','track-text-colour','track-text-x','track-text-y','track-text-justify','sep',
                 'webkit-window','webkit-zoom','webkit-freeze-at-end',
            
            'tab-links','sep',
                'disable-controls','links',
            'tab-show-control','sep',
                'show-control-begin','show-control-end','sep','disable-show-control-events','sep','show-control-events',
            'tab-sched','sep',
                'sched-everyday','sched-weekday','sched-monthday','sched-specialday','enable-catchup',
                    ],


              
            'start':[
            'tab-sched','sep',
                'start-show','sep','sched-enable','sched-everyday','sched-weekday','sched-monthday','sched-specialday',
            'tab-simulatetime','sep',
                'simulate-time','sim-year','sim-month','sim-day','sim-hour','sim-minute','sim-second',           
            'tab-background','sep',  
                'background-colour',
            'tab-counters','sep',
                'counters-store','counters-initial',
            'tab-show','sep',
                'type','title','start-show-ref',

                    ]

             }


    # field details for creating new shows and for update of profile    
    new_shows={

                'artliveshow':{'title': 'New ArtLiveshow','show-ref':'','show-canvas':'', 'display-name':'HDMI0', 'type': 'artliveshow', 'disable-controls':'no','sequence': 'ordered','repeat':'repeat','medialist': '',
                        'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'0','show-text-y':'0','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                           'eggtimer-text':'Loading....', 'eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',
                               'empty-text':'Nothing to show','admin-font':'bold 10pt Helvetica','admin-colour':'white','admin-x':'100','admin-y':'200','admin-justify':'left',
                         'transition': 'cut', 'duration': '5','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',

                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             
                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',
                            'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                            'live-tracks-dir1':'','live-tracks-dir2':'',
                            'controls':'pp-down down\npp-stop stop\npp-pause pause\n',
                               'show-control-begin':'','show-control-end':'','show-control-events':'','disable-show-control-events':'no',
                               'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'},

                'artmediashow':{'title': 'New ArtMediashow','show-ref':'','show-canvas':'', 'display-name':'HDMI0', 'type': 'artmediashow', 'disable-controls':'no','sequence': 'ordered','repeat':'repeat','medialist': '',
                        'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'0','show-text-y':'0','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                        'eggtimer-text':'Loading....','eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',
                        'empty-text':'Nothing to show','admin-font':'bold 10pt Helvetica','admin-colour':'white','admin-x':'100','admin-y':'200','admin-justify':'left',
                         'transition': 'cut', 'duration': '5','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',
                            
                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             
                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',

                                'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                            'controls':'pp-down down\npp-stop stop\npp-pause pause\n',
                                'show-control-begin':'','show-control-end':'','show-control-events':'','disable-show-control-events':'no',
                                'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'},

               'hyperlinkshow':{ 'type':'hyperlinkshow','title':'New Hyperlink Show','show-ref':'', 'show-canvas':'', 'display-name':'HDMI0','medialist':'','debug-path':'no',
                    'links':'','first-track-ref':'','home-track-ref':'','timeout-track-ref':'','disable-controls':'no','show-timeout': '0','track-timeout': '0',
                             'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'0','show-text-y':'0','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                             'eggtimer-text':'Loading....','eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',
                            'transition': 'cut', 'duration': '0','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',
                            
                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             

                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',

                                 'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                                 'show-control-begin':'','show-control-end':'','show-control-events':'','disable-show-control-events':'no',
                                 'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'
                            },

    
               'radiobuttonshow':{ 'type':'radiobuttonshow','title':'New Radio Button Show','show-ref':'', 'show-canvas':'', 'display-name':'HDMI0','medialist':'',
                    'links':'','first-track-ref':'','disable-controls':'no','show-timeout': '0','track-timeout': '0',
                             'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'0','show-text-y':'0','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                             'eggtimer-text':'Loading....','eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',
                            'transition': 'cut', 'duration': '0','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',

                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             

                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',

                                   'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                                   'show-control-begin':'','show-control-end':'','show-control-events':'','disable-show-control-events':'no','controls-in-subshows':'no',
                                   'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'
                                   },
    
                'mediashow':{'title': 'New Mediashow','show-ref':'', 'show-canvas':'','display-name':'HDMI0', 'type': 'mediashow','medialist': '','show-timeout': '0','interval':'0','track-count-limit':'0',
                          'disable-controls':'no','trigger-start-type': 'start','trigger-start-param':'','trigger-next-type': 'continue','trigger-next-param':'','sequence': 'ordered','repeat': 'repeat','trigger-end-type':'none', 'trigger-end-param':'',
                            'child-track-ref': '', 'hint-text': '', 'hint-x':'200','hint-y': '750','hint-justify':'left','hint-font': 'bold 30pt Helvetica','hint-colour': 'white',
                             'eggtimer-text':'Loading....','eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',
                             'trigger-wait-text':'Waiting for Trigger....','empty-track-ref':'','escape-track-ref':'','admin-font':'bold 10pt Helvetica','admin-colour':'white','admin-x':'100','admin-y':'200','admin-justify':'left',
                            'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'0','show-text-y':'0','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                            'transition': 'cut', 'duration': '5','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',
                                                          
                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             

                             
                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',
                             
                             'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                             'controls':'pp-down down\npp-up up\npp-play play\npp-stop stop\npp-pause pause\n',
                             'show-control-begin':'','show-control-end':'','show-control-events':'','disable-show-control-events':'no',
                             'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'},
                                     
                'liveshow':{'title': 'New Liveshow','show-ref':'','show-canvas':'', 'display-name':'HDMI0','type': 'liveshow','show-timeout': '0','interval':'0','track-count-limit':'0',
                            'disable-controls':'no','trigger-start-type':'start','trigger-start-param':'','trigger-next-type': 'continue','trigger-next-param':'','sequence': 'ordered','repeat': 'repeat','trigger-end-type':            'none', 'trigger-end-param':'','medialist': '',
                        'child-track-ref': '', 'hint-text': '','hint-x':'200', 'hint-y': '750','hint-justify':'left','hint-font': 'bold 30pt Helvetica','hint-colour': 'white',
                        'trigger-wait-text':'Waiting for Trigger....','empty-track-ref':'','escape-track-ref':'','admin-font':'bold 10pt Helvetica','admin-colour':'white','admin-x':'100','admin-y':'200','admin-justify':'left',
                        'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'0','show-text-y':'0','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                        'eggtimer-text':'Loading....','eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',
                         'transition': 'cut', 'duration': '5','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',
                             
                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             

                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',
                             
                            'live-tracks-dir1':'','live-tracks-dir2':'',
                            'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                            'controls':'pp-down down\npp-up up\npp-play play\npp-stop stop\npp-pause pause\n',
                            'show-control-begin':'','show-control-end':'','show-control-empty':'','show-control-not-empty':'','show-control-events':'','disable-show-control-events':'no',
                            'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'},
                
       
              'menu':{'show-ref': '', 'title': 'New Menu','type': 'menu','medialist': '','show-canvas':'','display-name':'HDMI0',
                        'show-timeout': '0','track-timeout':'0','menu-track-ref':'menu-track',
                         'eggtimer-text':'Loading....','eggtimer-x':'100','eggtimer-y':'100','eggtimer-justify':'left','eggtimer-font':'bold 10pt Helvetica','eggtimer-colour':'white',                       
                        'show-text':'','show-text-font':'bold 20pt Helvetica','show-text-colour':'white','show-text-x':'100','show-text-y':'50','show-text-justify':'left','background-image':'','background-colour':'',
                       'show-text-type':'text','show-html-width':'300','show-html-height':'300','show-html-background-colour':'white','show-text-location':'',
                       'transition': 'cut',  'duration': '5','pause-timeout':'','image-window':'200+200+400*300','image-aspect-mode':'warp',

                            
                            'mpv-audio': 'HDMI0','mpv-speaker':'stereo','mpv-volume':'100','mpv-window':'200+200+400*300','mpv-other-options':'','mpv-aspect-mode':'warp',
                             'mpv-freeze-at-start':'no','mpv-freeze-at-end':'yes',
                             

                            'webkit-window':'200+200+600*400','webkit-zoom':'1.0','webkit-freeze-at-end':'yes',
                      'track-text-colour':'white','track-text-x':'0','track-text-y':'40','track-text-justify':'left','track-text-font': 'bold 20pt Helvetica',
                        'disable-controls':'no','controls':'pp-down down\npp-up up\npp-play play\npp-stop stop\npp-pause pause\n',
                      'show-control-begin':'','show-control-end':'','show-control-events':'','disable-show-control-events':'no',
                      'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'','enable-catchup':'yes'},   
                      
                       
            
                'start':{'title': 'Start','start-show-ref':'start', 'type': 'start','background-colour':'#000000','start-show':'','show-ref':'start',
                         'sched-enable':'no','simulate-time':'no','sim-year':'','sim-month':'','sim-day':'','sim-hour':'','sim-minute':'','sim-second':'',
                         'sched-everyday':'','sched-weekday':'','sched-monthday':'','sched-specialday':'',
                         'counters-store':'no','counters-initial':''}
                            
            }
    
    show_field_specs={
                    'sep':{'shape':'sep'},
                    'admin-font':{'shape':'font','text':'Notice Text Font','must':'no','read-only':'no'},
                    'admin-colour':{'shape':'colour','text':'Notice Text Colour','must':'no','read-only':'no'},
                    'admin-x':{'shape':'entry','text':'Notice Text x Position','must':'no','read-only':'no'},
                    'admin-y':{'shape':'entry','text':'Notice Text y Position','must':'no','read-only':'no'},
                    'admin-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                                       'values':['left','center','right']},
                    'background-colour':{'shape':'colour','text':'Background Colour','must':'no','read-only':'no'},
                    'background-image':{'shape':'browse','text':'Background Image','must':'no','read-only':'no'},
                    'child-track-ref':{'shape':'entry','text':'Child Track','must':'no','read-only':'no'},
                    'controls':{'shape':'text','text':'Controls','must':'no','read-only':'no'},
                    'controls-in-subshows':{'shape':'option-menu','text':'Controls in Subshows','must':'no','read-only':'no',
                                    'values':['no','yes']},
                    'counters-store':{'shape':'option-menu','text':'Store Counters ','must':'no','read-only':'no','values':['yes','no']},
                    'counters-initial':{'shape':'text','text':'Initial Values','must':'no','read-only':'no'},
                    'track-count-limit':{'shape':'entry','text':'Track Count Limit','must':'no','read-only':'no'},
                    'debug-path':{'shape':'option-menu','text':'Print Path Debug ','must':'no','read-only':'no','values':['yes','no']},
                    'disable-show-control-events':{'shape':'option-menu','text':'Disable Show Control on Event ','must':'no','read-only':'no','values':['yes','no']},
                    'display-name':{'shape':'option-menu','text':'Display','must':'no','read-only':'no',
                                    'values':['HDMI0','HDMI1','DSI0','DSI1','A/V','NODISPLAY']},
                    'disable-controls':{'shape':'option-menu','text':'Disable Controls ','must':'no','read-only':'no','values':['yes','no']},
                    'duration':{'shape':'entry','text':'Duration (secs)','must':'no','read-only':'no'},
                    'eggtimer-text':{'shape':'text','text':'Egg Timer Text','must':'no','read-only':'no'},
                    'eggtimer-x':{'shape':'entry','text':'Egg Timer x Position','must':'no','read-only':'no'},
                    'eggtimer-y':{'shape':'entry','text':'Egg Timer y Position','must':'no','read-only':'no'},
                    'eggtimer-font':{'shape':'font','text':'Egg Timer Font','must':'no','read-only':'no'},
                    'eggtimer-colour':{'shape':'colour','text':'Egg Timer Colour','must':'no','read-only':'no'},
                    'eggtimer-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                                    'values':['left','center','right']},
                    'empty-text':{'shape':'text','text':'List Empty Text','must':'no','read-only':'no'},
                    'empty-track-ref':{'shape':'entry','text':'Empty List Track','must':'no','read-only':'no'},
                    'enable-catchup':{'shape':'option-menu','text':'Enable Catchup','must':'no','read-only':'no','values':['yes','no']},
                    'escape-track-ref':{'shape':'entry','text':'Escape Track','must':'no','read-only':'no'},
                    'first-track-ref':{'shape':'entry','text':'First Track','must':'no','read-only':'no'},
                    'has-background':{'shape':'option-menu','text':'Has Background Image','must':'no','read-only':'no','values':['yes','no']},
                    'home-track-ref':{'shape':'entry','text':'Home Track','must':'no','read-only':'no'},
                    'hint-text':{'shape':'text','text':'Hint Text','must':'no','read-only':'no'},
                    'hint-x':{'shape':'entry','text':'Hint Text x Position','must':'no','read-only':'no'},
                    'hint-y':{'shape':'entry','text':'Hint Text y Position','must':'no','read-only':'no'},
                    'hint-font':{'shape':'font','text':'Hint Font','must':'no','read-only':'no'},
                    'hint-colour':{'shape':'colour','text':'Hint Colour','must':'no','read-only':'no'},
                    'hint-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                                       'values':['left','center','right']},                    
                    'image-window':{'shape':'entry','text':'Image Window','must':'no','read-only':'no'},
                    'image-aspect-mode':{'shape':'option-menu','text':'Image Aspect Mode','must':'no','read-only':'no',
                                       'values':['clip','fit','shrink','warp','']},
                    'interval':{'shape':'entry','text':'Repeat Interval','must':'no','read-only':'no'},
                    'links':{'shape':'text','text':'Controls','must':'no','read-only':'no'},
                    'live-tracks-dir1':{'shape':'entry','text':'Live Tracks Directory 1','must':'no','read-only':'no'},
                    'live-tracks-dir2':{'shape':'entry','text':'Live Tracks Directory 2 ','must':'no','read-only':'no'},
                    'medialist':{'shape':'entry','text':'Medialist','must':'no','read-only':'no'},
                    'menu-track-ref':{'shape':'entry','text':'Menu Track','must':'no','read-only':'no'},
                    'message-font':{'shape':'font','text':'Text Font','must':'yes','read-only':'no'},
                    'message-colour':{'shape':'colour','text':'Text Colour','must':'yes','read-only':'no'},
                    'message-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                                       'values':['left','center','right']},
                    
                                       
                    'mpv-audio':{'shape':'option-menu','text':'MPV Player Audio','must':'no','read-only':'no',
                                       'values':['HDMI0','HDMI1','USB','bluetooth','USB2','A/V','']},
                    'mpv-other-options':{'shape':'entry','text':'MPV Player Options','must':'no','read-only':'no'},
                    'mpv-volume':{'shape':'entry','text':'MPV Player Volume','must':'no','read-only':'no'},
                    'mpv-window':{'shape':'entry','text':'MPV Window','must':'no','read-only':'no'},
                    'mpv-aspect-mode':{'shape':'option-menu','text':'MPV Aspect Mode','must':'no','read-only':'no',
                                       'values':['clip','fit','shrink','warp']},
                    'mpv-freeze-at-start':{'shape':'option-menu','text':'MPV Freeze at Start','must':'no','read-only':'no',
                                       'values':['no','before-first-frame','after-first-frame']},
                    'mpv-freeze-at-end':{'shape':'option-menu','text':'MPV Freeze at End','must':'no','read-only':'no',
                                       'values':['yes','no']}, 
                    'mpv-speaker':{'shape':'option-menu','text':'MPV Speaker','must':'no','read-only':'no',
                             'values':['left','right','stereo','5.1']},
                                       
                    'pause-timeout':{'shape':'entry','text':'Pause Timeout','must':'no','read-only':'no'},

                    'repeat':{'shape':'option-menu','text':'Repeat/Single','must':'no','read-only':'no',
                                        'values':['repeat','single-run']},
                    'sched-enable':{'shape':'option-menu','text':'Enable Scheduler','must':'no','read-only':'no','values':['yes','no']},
                    'simulate-time':{'shape':'option-menu','text':'Simulated Time','must':'no','read-only':'no','values':['yes','no']},
                    'sim-second':{'shape':'entry','text':'Second','must':'no','read-only':'no'},
                    'sim-minute':{'shape':'entry','text':'Minute','must':'no','read-only':'no'},
                    'sim-hour':{'shape':'entry','text':'Hour','must':'no','read-only':'no'},
                    'sim-day':{'shape':'entry','text':'Day','must':'no','read-only':'no'},
                    'sim-month':{'shape':'entry','text':'Month','must':'no','read-only':'no'},
                    'sim-year':{'shape':'entry','text':'Year','must':'no','read-only':'no'},
                    'sched-everyday':{'shape':'text','text':'Every day','must':'no','read-only':'no'},
                    'sched-weekday':{'shape':'text','text':'Week day','must':'no','read-only':'no'},
                    'sched-monthday':{'shape':'text','text':'Month day','must':'no','read-only':'no'},
                    'sched-specialday':{'shape':'text','text':'Special day','must':'no','read-only':'no'},
                    'sequence':{'shape':'option-menu','text':'Sequence','must':'no','read-only':'no',
                                        'values':['ordered','shuffle','reverse']},
                    'show-canvas':{'shape':'entry','text':'Show Canvas','must':'no','read-only':'no'},
                    'show-control-begin':{'shape':'text','text':'Show Control at Beginning','must':'no','read-only':'no'},
                    'show-control-end':{'shape':'text','text':'Show Control at End','must':'no','read-only':'no'},
                    'show-control-events':{'shape':'text','text':'Show Control on Event','must':'no','read-only':'no'},

                    'show-control-empty':{'shape':'text','text':'Show Control on Empty','must':'no','read-only':'no'},
                    'show-control-not-empty':{'shape':'text','text':'Show Control on Not Empty','must':'no','read-only':'no'},
                    'start-show-ref':{'shape':'entry','text':'Show Reference','must':'no','read-only':'yes'},
                    'show-ref':{'shape':'entry','text':'Show Reference','must':'no','read-only':'no'},
                    'show-text':{'shape':'text','text':'Show Text','must':'no','read-only':'no'},
                    'show-text-font':{'shape':'font','text':'Plain Text Font','must':'no','read-only':'no'},
                    'show-text-colour':{'shape':'colour','text':'Plain Text Colour','must':'no','read-only':'no'},
                    'show-text-x':{'shape':'entry','text':'Show Text x Position','must':'no','read-only':'no'},
                    'show-text-y':{'shape':'entry','text':'Show Text y Position','must':'no','read-only':'no'},
                    'show-text-justify':{'shape':'option-menu','text':'Plain Text Justify','must':'no','read-only':'no',
                                       'values':['left','center','right']},
                    'show-text-type':{'shape':'option-menu','text':'Text Type','must':'no','read-only':'no',
                                       'values':['plain','html']}, 
                    'show-text-location':{'shape':'browse','text':'Show Text Location','must':'no','read-only':'no'},
                    'show-html-width':{'shape':'entry','text':'HTML Text Width','must':'no','read-only':'no'},
                    'show-html-height':{'shape':'entry','text':'HTML Text Height','must':'no','read-only':'no'},
                    'show-html-background-colour':{'shape':'colour','text':'HTML Background Colour','must':'no','read-only':'no'},           
 
                    'show-timeout':{'shape':'entry','text':'Show Timeout','must':'no','read-only':'no'},
                    'start-show':{'shape':'entry','text':'Start Shows','must':'no','read-only':'no'},
                    'tab-animation':{'shape':'tab','name':'animation','text':'Animation'},
                    'tab-background':{'shape':'tab','name':'background','text':'Background'},
                    'tab-child':{'shape':'tab','name':'child','text':'Child Track'},
                    'tab-controls':{'shape':'tab','name':'controls','text':'Controls'},
                    'tab-counters':{'shape':'tab','name':'counters','text':'Counters'},
                    'tab-eggtimer':{'shape':'tab','name':'eggtimer','text':'Egg Timer'},
                    'tab-links':{'shape':'tab','name':'links','text':'Controls'},
                    'tab-notices':{'shape':'tab','name':'notices','text':'Notices'},
                    'tab-sched':{'shape':'tab','name':'sched','text':'Schedule'},
                    'tab-simulatetime':{'shape':'tab','name':'schedcontrol','text':'Simulate Time'},
                    'tab-show':{'shape':'tab','name':'show','text':'Show '},
                    'tab-show-control':{'shape':'tab','name':'show-control','text':'Show Control'},
                    'tab-show-text':{'shape':'tab','name':'show-text','text':'Show Background and Text'},
                    'tab-menu-text':{'shape':'tab','name':'menu-text','text':'Menu Text'},
                    'tab-track':{'shape':'tab','name':'track','text':'Track'},
                    'tab-tracks':{'shape':'tab','name':'tracks','text':'Track Defaults'},                   
                    'text':{'shape':'text','text':'Message Text','must':'no','read-only':'no'},
                    'timeout-track-ref':{'shape':'entry','text':'Timeout Track','must':'no','read-only':'no'},
                    'title':{'shape':'entry','text':'Title','must':'no','read-only':'no'},
                    'track-timeout':{'shape':'entry','text':'Track Timeout (secs)','must':'no','read-only':'no'},
                    'track-text-font':{'shape':'font','text':'Track Text Font','must':'no','read-only':'no'},
                    'track-text-colour':{'shape':'colour','text':'Track Text Colour','must':'no','read-only':'no'},
                    'track-text-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                                       'values':['left','center','right']},
                    'track-text-x':{'shape':'entry','text':'Track Text x Position','must':'no','read-only':'no'},
                    'track-text-y':{'shape':'entry','text':'Track Text y Position','must':'no','read-only':'no'},
  
                    'transition':{'shape':'option-menu','text':'Transition','must':'no','read-only':'no',
                                 'values':['cut',]},
                    'trigger-start-type':{'shape':'option-menu','text':'Trigger for Start','must':'no','read-only':'no',
                                 'values':['start','input']},
                    'trigger-end-type':{'shape':'option-menu','text':'Trigger for End','must':'no','read-only':'no','values':['none','input']},
                    'trigger-next-type':{'shape':'option-menu','text':'Trigger for next','must':'no','read-only':'no','values':['continue','input']},
                    'trigger-next-param':{'shape':'entry','text':'Next Trigger Parameters','must':'no','read-only':'no'},
                    'trigger-start-param':{'shape':'entry','text':'Start Trigger Parameters','must':'no','read-only':'no'},
                    'trigger-end-param':{'shape':'entry','text':'End Trigger Parameters','must':'no','read-only':'no'},
                    'trigger-wait-text':{'shape':'text','text':'Trigger Wait Text','must':'no','read-only':'no'},

                    'type':{'shape':'entry','text':'Type','must':'no','read-only':'yes'},
                    'webkit-window':{'shape':'entry','text':'webkit Web Window','must':'no','read-only':'no'},

                    'webkit-freeze-at-end':{'shape':'option-menu','text':'webkit Freeze at End','must':'no','read-only':'no',
                                       'values':['yes','no']},

                    'webkit-zoom':{'shape':'entry','text':'webkit Zoom','must':'no','read-only':'no'},
                   


                          }

    track_types={
    
            'mpv':[
            'tab-track','sep',  
                    'type','title','track-ref','location','thumbnail','mpv-audio','mpv-speaker','mpv-volume','mpv-max-volume',
                    'mpv-window','mpv-aspect-mode','mpv-subtitles','mpv-freeze-at-start','mpv-freeze-at-end','mpv-video-display','mpv-other-options',
                    'background-colour','background-image','display-show-background','plugin','pause-timeout',
            'tab-track-text','sep',
                'track-text','track-text-location','track-text-x','track-text-y','track-text-type','sep',
                'track-text-font','track-text-colour','track-text-justify','sep',
                'track-html-height','track-html-width','track-html-background-colour','sep',
                'display-show-text',
            'tab-links','sep',
                'links',
            'tab-show-control','sep',
                'show-control-begin','show-control-end',
            'tab-animate','sep',
                'animate-begin','animate-clear','animate-end'
            ],    

    
        'message':[
            'tab-track','sep',  
                'type','title','track-ref','thumbnail','duration','background-colour','background-image','display-show-background','plugin',
            'tab-message','sep',
                'text','message-text-location','message-x','message-y','message-text-type','sep',
                'message-font','message-colour','message-justify','sep',
                'message-html-height','message-html-width','message-html-background-colour',
            
           'tab-track-text','sep',
                'track-text','track-text-location','track-text-x','track-text-y','track-text-type','sep',
                'track-text-font','track-text-colour','track-text-justify','sep',
                'track-html-height','track-html-width','track-html-background-colour','sep',
                'display-show-text',
            'tab-links','sep',
                'links',
            'tab-show-control','sep',
                'show-control-begin','show-control-end',
            'tab-animate','sep',
                'animate-begin','animate-clear','animate-end'
            ],
        
                
        'show':[
            'tab-track','sep',  
                'type','title','track-ref','sub-show','thumbnail'
            ],
        
                 
        'image':[
            'tab-track','sep',  
                'type','title','track-ref','location','thumbnail','duration','transition','image-window','image-aspect-mode','background-colour','background-image','display-show-background','plugin','pause-timeout',
           'tab-track-text','sep',
                'track-text','track-text-location','track-text-x','track-text-y','track-text-type','sep',
                'track-text-font','track-text-colour','track-text-justify','sep',
                'track-html-height','track-html-width','track-html-background-colour','sep',
                'display-show-text',                
                'sep','pause-text','pause-text-font','pause-text-colour','pause-text-x','pause-text-y','pause-text-justify',
            'tab-links','sep',
                'links',
            'tab-show-control','sep',
                'show-control-begin','show-control-end',
            'tab-animate','sep',
                'animate-begin','animate-clear','animate-end'
            ],


        'menu':[
            'tab-track','sep',
                'type','title','track-ref','background-colour','background-image','entry-font','entry-colour', 'entry-select-colour','display-show-background','plugin',
            'tab-menu-geometry','sep',
                'menu-window','menu-direction','menu-rows','menu-columns','menu-icon-mode','menu-text-mode','menu-bullet','menu-icon-width','menu-icon-height',
                'menu-horizontal-padding','menu-vertical-padding','menu-text-width','menu-text-height','menu-horizontal-separation','menu-vertical-separation',
                'menu-strip','menu-strip-padding','menu-guidelines',
            'tab-track-text','sep',
                'track-text','track-text-location','track-text-x','track-text-y','track-text-type','sep',
                'track-text-font','track-text-colour','track-text-justify','sep',
                'track-html-height','track-html-width','track-html-background-colour','sep',
                'display-show-text','sep',
                'hint-text', 'hint-x', 'hint-y','hint-justify', 'hint-font', 'hint-colour',
            'tab-links','sep',  
               'links',
            'tab-show-control','sep',
                 'show-control-begin','show-control-end',
            'tab-animate','sep',
                 'animate-begin','animate-clear','animate-end'
            ],
               
 
                 
         'webkit':[
            'tab-track','sep',  
                'type','title','track-ref','location','thumbnail','duration','webkit-window','webkit-freeze-at-end','webkit-zoom',
                       'background-colour','background-image','display-show-background','plugin',
            'tab-track-text','sep',
                'track-text','track-text-location','track-text-x','track-text-y','track-text-type','sep',
                'track-text-font','track-text-colour','track-text-justify','sep',
                'track-html-height','track-html-width','track-html-background-colour','sep',
                'display-show-text','sep',
            'tab-browser-commands','sep',
                 'browser-commands',
            'tab-links','sep',
                 'links',
            'tab-show-control','sep',
                 'show-control-begin','show-control-end',
            'tab-animate','sep',
                 'animate-begin','animate-clear','animate-end'
                 ]
                         }                   

    new_tracks={
    
                'mpv':{'title':'New MPV Video','track-ref':'','type':'mpv','location':'','thumbnail':'',
                         'mpv-audio':'','mpv-speaker':'','mpv-volume':'','mpv-max-volume':'','mpv-window':'','mpv-other-options': '','mpv-aspect-mode':'',
                         'mpv-subtitles':'no',
                         'mpv-freeze-at-start':'','mpv-freeze-at-end':'','mpv-video-display':'',
                         
                         'background-colour':'','background-image':'','display-show-background':'yes','display-show-text':'yes',
                         'track-text':'','track-text-font':'',
                       'track-text-colour':'','track-text-x':'','track-text-y':'','track-text-justify':'',
                       'track-text-type':'plain','track-html-width':'300','track-html-height':'300','track-html-background-colour':'white','track-text-location':'',
                       'links':'','show-control-begin':'','show-control-end':'','animate-begin':'','animate-clear':'no','animate-end':'','plugin':'','pause-timeout':''},
 
                      
                'message':{'title':'New Message','track-ref':'','type':'message','text':'','thumbnail':'','duration':'','message-font':'bold 30pt Helvetica','message-colour':'white','message-justify':'left','message-x':'100','message-y':'100','message-justify':'left',
                           'message-text-type':'plain','message-html-width':'300','message-html-height':'300','message-html-background-colour':'white','message-text-location':'',
                           'track-text':'','track-text-font':'','track-text-colour':'','track-text-x':'','track-text-y':'','track-text-justify':'',
                           'track-text-type':'plain','track-html-width':'300','track-html-height':'300','track-html-background-colour':'white','track-text-location':'',
                           'background-colour':'','background-image':'','display-show-background':'yes','display-show-text':'yes','links':'','show-control-begin':'','show-control-end':'','animate-begin':'','animate-clear':'no','animate-end':'','plugin':''},
                
                'show':{'title':'New Show','track-ref':'','type':'show','sub-show':'','thumbnail':''},   
                
                'image':{'title':'New Image','track-ref':'','type':'image','location':'','thumbnail':'','duration':'','transition':'','image-window':'','image-window':'','image-aspect-mode':'',
                          'pause-text':'Paused......','pause-text-font':'bold 20pt Helvetica','pause-text-colour':'white','pause-text-x':'10','pause-text-y':'40','pause-text-justify':'left',
                         'background-colour':'','background-image':'','display-show-background':'yes','display-show-text':'yes','track-text':'','track-text-font':'',
                       'track-text-colour':'','track-text-x':'','track-text-y':'','track-text-justify':'',
                       'track-text-type':'plain','track-html-width':'300','track-html-height':'300','track-html-background-colour':'white','track-text-location':'',
                       'links':'','show-control-begin':'','show-control-end':'','animate-begin':'','animate-clear':'no','animate-end':'','plugin':'','pause-timeout':''},
                       

                'webkit':{'title':'New WebKit Web','track-ref':'','type':'webkit','location':'', 'thumbnail':'','duration':'',
                        'webkit-window':'','webkit-freeze-at-end':'','webkit-zoom':'',
                        'display-show-text':'yes','background-colour':'','background-image':'','display-show-background':'yes',
                       'track-text':'','track-text-font':'','track-text-colour':'','track-text-x':'','track-text-y':'','track-text-justify':'',
                       'track-text-type':'plain','track-html-width':'300','track-html-height':'300','track-html-background-colour':'white','track-text-location':'',
                       'links':'',
                       'show-control-begin':'','show-control-end':'','animate-begin':'','animate-clear':'no','animate-end':'','browser-commands':'','plugin':''},



                'menu':{'type':'menu','title':'Menu Track','track-ref':'menu-track','background-colour':'','background-image':'','display-show-background':'yes','plugin':'',
                        'entry-font': 'bold 30pt Helvetica','entry-colour': 'white', 'entry-select-colour': 'red',
                         'menu-window':'300+250+500*500','menu-direction':'vertical','menu-rows':'10','menu-columns':'1','menu-icon-mode':'bullet','menu-text-mode':'right',
                        'menu-bullet':'',
                        'menu-icon-width':'80','menu-icon-height':'80',
                        'menu-horizontal-padding':'10','menu-vertical-padding':'10','menu-text-width':'800','menu-text-height':'50',
                        'menu-horizontal-separation':'20','menu-vertical-separation':'20','menu-strip':'no','menu-strip-padding':'5','menu-guidelines':'never',
                        'hint-text': 'Up, down to Select, Return to Play', 'hint-x':'200','hint-y': '980','hint-justify':'left', 'hint-font': 'bold 30pt Helvetica', 'hint-colour': 'white',
                         'display-show-text':'yes','track-text': '', 'track-text-x':'','track-text-y': '','track-text-justify':'', 'track-text-font': '', 'track-text-colour': '',
                         'track-text-type':'plain','track-html-width':'300','track-html-height':'300','track-html-background-colour':'white','track-text-location':'',
                        'show-control-begin':'','show-control-end':'','animate-begin':'','animate-clear':'no','animate-end':'',
                        'links':'pp-down down\npp-up up\npp-play play\npp-stop stop\n'
                         }
                }





    
    track_field_specs={'sep':{'shape':'sep'},
        'animate-begin':{'shape':'text','text':'Animation at Beginning','must':'no','read-only':'no'},
        'animate-end':{'shape':'text','text':'Animation at End','must':'no','read-only':'no'},
        'animate-clear':{'shape':'option-menu','text':'Clear Animation','must':'no','read-only':'no',
                  'values':['yes','no']},

        'background-image':{'shape':'browse','text':'Background Image','must':'no','read-only':'no'},
        'background-colour':{'shape':'colour','text':'Background Colour','must':'no','read-only':'no'},
        'browser-commands':{'shape':'text','text':'Browser Commands','must':'no','read-only':'no'},
        'display-show-background':{'shape':'option-menu','text':'Display Show Background','must':'no','read-only':'no',
                   'values':['yes','no','']},
        'display-show-text':{'shape':'option-menu','text':'Display Show Text','must':'no','read-only':'no',
                   'values':['yes','no','']},
        'duration':{'shape':'entry','text':'Duration (secs)','must':'no','read-only':'no'},
        
           
        'entry-font':{'shape':'font','text':'Entry Font','must':'no','read-only':'no'},
        'entry-colour':{'shape':'colour','text':'Entry Colour','must':'no','read-only':'no'},
        'entry-select-colour':{'shape':'colour','text':'Selected Entry Colour','must':'no','read-only':'no'},

        'hint-text':{'shape':'text','text':'Hint Text','must':'no','read-only':'no'},
        'hint-x':{'shape':'entry','text':'Hint Text x Position','must':'no','read-only':'no'},

        'hint-y':{'shape':'entry','text':'Hint Text y Position','must':'no','read-only':'no'},
        'hint-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                           'values':['left','center','right']},
        'hint-font':{'shape':'font','text':'Hint Font','must':'no','read-only':'no'},
        'hint-colour':{'shape':'colour','text':'Hint Colour','must':'no','read-only':'no'},

        'image-window':{'shape':'entry','text':'Image Window','must':'no','read-only':'no'},
        'image-aspect-mode':{'shape':'option-menu','text':'Image Aspect Mode','must':'no','read-only':'no',
                           'values':['clip','fit','shrink','warp','']}, 
        'location':{'shape':'browse','text':'Location','must':'no','read-only':'no'},
        'links':{'shape':'text','text':'Controls','must':'no','read-only':'no'},
        'menu-background-colour':{'shape':'colour','text':'Menu Background Colour','must':'no','read-only':'no'},
        'menu-background-image':{'shape':'browse','text':'Menu Background Image','must':'no','read-only':'no'},


        'menu-window':{'shape':'entry','text':'Menu Window','must':'no','read-only':'no'},
        'menu-direction':{'shape':'option-menu','text':'Direction','must':'no','read-only':'no',
                           'values':['horizontal','vertical']},
        'menu-rows':{'shape':'entry','text':'Rows','must':'no','read-only':'no'},
        'menu-columns':{'shape':'entry','text':'Columns','must':'no','read-only':'no'},
        'menu-icon-mode':{'shape':'option-menu','text':'Icon Mode','must':'no','read-only':'no',
                           'values':['none','thumbnail','bullet']},
        'menu-text-mode':{'shape':'option-menu','text':'Text Mode','must':'no','read-only':'no',
                           'values':['none','overlay','right','below']},
        'menu-strip':{'shape':'option-menu','text':'Stipple Background','must':'no','read-only':'no',
                           'values':['no','yes']},
        'menu-strip-padding':{'shape':'entry','text':'Stipple Bckgrnd Pddng','must':'no','read-only':'no'},

        'menu-guidelines':{'shape':'option-menu','text':'Guidelines','must':'no','read-only':'no',
                           'values':['never','auto','always']},
        'menu-bullet':{'shape':'browse','text':'Bullet','must':'no','read-only':'no'},
        'menu-icon-width':{'shape':'entry','text':'Icon Width','must':'no','read-only':'no'},
        'menu-icon-height':{'shape':'entry','text':'Icon Height','must':'no','read-only':'no'},
        'menu-horizontal-padding':{'shape':'entry','text':'Horizontal Padding','must':'no','read-only':'no'},
        'menu-vertical-padding':{'shape':'entry','text':'Vertical Padding','must':'no','read-only':'no'},
        'menu-horizontal-separation':{'shape':'entry','text':'Horizontal Separation','must':'no','read-only':'no'},
        'menu-vertical-separation':{'shape':'entry','text':'Vertical Separation','must':'no','read-only':'no'},
        'menu-text-width':{'shape':'entry','text':'Text Width','must':'no','read-only':'no'},
        'menu-text-height':{'shape':'entry','text':'Text Height','must':'no','read-only':'no'},
        
       'text':{'shape':'text','text':'Message Text','must':'no','read-only':'no'},
        'message-font':{'shape':'font','text':'Plain Text Font','must':'no','read-only':'no'},
        'message-colour':{'shape':'colour','text':'Plain Text Colour','must':'no','read-only':'no'},
        'message-justify':{'shape':'option-menu','text':'Plain Text Justify','must':'no','read-only':'no',
                   'values':['left','center','right']},
        'message-x':{'shape':'entry','text':'Message x Position','must':'no','read-only':'no'},
        'message-y':{'shape':'entry','text':'Message y Position','must':'no','read-only':'no'},
        'message-text-type':{'shape':'option-menu','text':'Message Text Type','must':'no','read-only':'no',
                   'values':['plain','html']}, 
        'message-text-location':{'shape':'browse','text':'Message Text Location','must':'no','read-only':'no'},
        'message-html-width':{'shape':'entry','text':'HTML Text Width','must':'no','read-only':'no'},
        'message-html-height':{'shape':'entry','text':'HTML Text Height','must':'no','read-only':'no'},
        'message-html-background-colour':{'shape':'colour','text':'HTML Background Colour','must':'no','read-only':'no'},           

        'mpv-audio':{'shape':'option-menu','text':'MPV Audio Device','must':'no','read-only':'no',
                   'values':['HDMI0','HDMI1','USB','bluetooth','USB2','A/V','NODISPLAY','']},
        'mpv-other-options':{'shape':'entry','text':'MPV Other Options','must':'no','read-only':'no'},
        'mpv-volume':{'shape':'entry','text':'MPV Audio Volume','must':'no','read-only':'no'},
        'mpv-max-volume':{'shape':'entry','text':'MPV Audio Max Volume','must':'no','read-only':'no'},
        'mpv-speaker':{'shape':'option-menu','text':'MPV Speaker','must':'no','read-only':'no',
                       'values':['left','right','stereo','5.1','']},
        'mpv-video-display':{'shape':'option-menu','text':'Alternate Video Display','must':'no','read-only':'no',
                    'values':['','HDMI0','HDMI1','DSI0','DSI1','A/V']},
        'mpv-window':{'shape':'entry','text':'MPV Video Window','must':'no','read-only':'no'},
        'mpv-aspect-mode':{'shape':'option-menu','text':'MPV Aspect Mode','must':'no','read-only':'no',
                   'values':['clip','fit','shrink','warp','']},  
         'mpv-subtitles':{'shape':'option-menu','text':'MPV Subtitles','must':'no','read-only':'no',
                   'values':['yes','no']},
        'mpv-freeze-at-start':{'shape':'option-menu','text':'MPV Freeze at Start','must':'no','read-only':'no',
                   'values':['no','before-first-frame','after-first-frame','']},
        'mpv-freeze-at-end':{'shape':'option-menu','text':'MPV Freeze at End','must':'no','read-only':'no',
                   'values':['yes','no','']},

                
        
        'pause-text':{'shape':'text','text':'Pause Text','must':'no','read-only':'no'},
   
        'pause-text-font':{'shape':'font','text':'Pause Text Font','must':'no','read-only':'no'},
        'pause-text-colour':{'shape':'colour','text':'Pause Text Colour','must':'no','read-only':'no'},
        'pause-text-justify':{'shape':'option-menu','text':'Justification','must':'no','read-only':'no',
                   'values':['left','center','right']},
        'pause-text-x':{'shape':'entry','text':'Pause Text x Position','must':'no','read-only':'no'},
        'pause-text-y':{'shape':'entry','text':'Pause Text y Position','must':'no','read-only':'no'},
        'pause-timeout':{'shape':'entry','text':'Pause Timeout','must':'no','read-only':'no'},

        'plugin':{'shape':'browse','text':'Plugin Config File','must':'no','read-only':'no'},

        'show-ref':{'shape':'entry','text':'Show Reference','must':'no','read-only':'no'},
        'show-control-begin':{'shape':'text','text':'Show Control at Beginning','must':'no','read-only':'no'},
        'show-control-end':{'shape':'text','text':'Show Control at End','must':'no','read-only':'no'},
        'sub-show':{'shape':'option-menu','text':'Show to Run','must':'no','read-only':'no'},

        'tab-animate':{'shape':'tab','name':'animate','text':'Animation'},
        'tab-browser-commands':{'shape':'tab','name':'browser-commands','text':'Browser Commands'},
        'tab-menu-geometry':{'shape':'tab','name':'menu-geometry','text':'Geometry'},
        'tab-show-control':{'shape':'tab','name':'show-control','text':'Show Control'},
        'tab-links':{'shape':'tab','name':'links','text':'Controls'},
        'tab-message':{'shape':'tab','name':'message','text':'Message'},
        'tab-track-text':{'shape':'tab','name':'track-text','text':'Text'},
        'tab-track':{'shape':'tab','name':'track','text':'Track'},
        'thumbnail':{'shape':'browse','text':'Thumbnail','must':'no','read-only':'no'},
        'title':{'shape':'entry','text':'Title','must':'no','read-only':'no'},
        'track-ref':{'shape':'entry','text':'Track Reference','must':'no','read-only':'no'},
        'track-text':{'shape':'text','text':'Track Text','must':'no','read-only':'no'},
        'track-text-font':{'shape':'font','text':'Plain Text Font','must':'no','read-only':'no'},
        'track-text-colour':{'shape':'colour','text':'Plain Text Colour','must':'no','read-only':'no'},
        'track-text-justify':{'shape':'option-menu','text':'Plain Text Justify','must':'no','read-only':'no',
                   'values':['left','center','right','']},
        'track-text-type':{'shape':'option-menu','text':'Track Text Type','must':'no','read-only':'no',
                   'values':['plain','html']}, 
        'track-text-location':{'shape':'browse','text':'Track Text Location','must':'no','read-only':'no'},
        'track-html-width':{'shape':'entry','text':'HTML Text Width','must':'no','read-only':'no'},
        'track-html-height':{'shape':'entry','text':'HTML Text Height','must':'no','read-only':'no'},
        'track-html-background-colour':{'shape':'colour','text':'HTML Background Colour','must':'no','read-only':'no'},           
        'track-text-x':{'shape':'entry','text':'Track Text x Position','must':'no','read-only':'no'},
        'track-text-y':{'shape':'entry','text':'Track Text y Position','must':'no','read-only':'no'},
        'transition':{'shape':'option-menu','text':'Transition','must':'no','read-only':'no','values':['cut','']},
        'type':{'shape':'entry','text':'Type','must':'no','read-only':'yes'},
        'webkit-window':{'shape':'entry','text':'webkit Window','must':'no','read-only':'no'},
        'webkit-freeze-at-end':{'shape':'option-menu','text':'webkit Freeze at End','must':'no','read-only':'no',
                   'values':['yes','no','']},
        'webkit-zoom':{'shape':'entry','text':'webkit Zoom','must':'no','read-only':'no'},
       


                          }
        

if __name__  ==  "__main__":
    print('Version of Definitions is  ',    PPdefinitions.DEFINITIONS_VERSION_STRING, '>',PPdefinitions().definitions_version())
