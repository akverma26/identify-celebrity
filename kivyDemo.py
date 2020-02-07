from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.loader import Loader
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import *
from kivy.uix.image import *
from kivy.uix.layout import Layout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import *
from glob import glob
from kivy.uix.textinput import TextInput
from sightengine.client import *
from kivy.core.text.text_layout import layout_text
import urllib


filex = 0
img = 1
Builder.load_file('MyApp.kv')

class MyLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
    

class Preview(Image):
    def __init__(self, **kwargs):
        super(Preview, self).__init__(**kwargs)
        
        


class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)




class MyApp(App):
   def build(self):
       self.title = 'Identify Name of the Celebrity'
       return MyLayout()
   def selected(self):
       root = self.root
       path = root.ids.filechooser.selection
       if path:
           ext=path[0][len(path[0])-3]
           ext+=path[0][len(path[0])-2]
           ext+=path[0][len(path[0])-1]
           if (ext=='jpg' or ext=='png' or ext=='bmp'):
               print(path[0])
               global filex
               filex = 1
               root.ids.preview.source=path[0]
               
   def asyncImage(self):
       root=self.root
       ur=root.ids.url.text
       if ur:
           global filex, img
           filex = 2
           urllib.request.urlretrieve(ur, 'temp_'+str(img)+'.png')
           root.ids.preview.source='temp_'+str(img)+'.png'
           img+=1
   
   def identify(self):
       root=self.root
       client = SightengineClient('959050600', 'D4rGDZwWbysdSyT3NpMy')
       image=''
       print(filex)
       if filex==1:
           image=root.ids.filechooser.selection[0]
       elif filex==2:
           image='temp_'+str(img-1)+'.png'
           
       if image:
           output = client.check('celebrities').set_file(image)
           
           for face in output['faces']:
               if 'celebrity' in face:
                   root.ids.name.text=face['celebrity'][0]['name']
                   print(face['celebrity'][0]['name'])
               
   def calc(self,value):
       return value

if __name__ == "__main__":
    MyApp().run()
