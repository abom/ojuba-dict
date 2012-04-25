'''
Created on 08/04/2012

@author: ahmed
'''
import os
from gi.repository import Gtk
import ConfigParser

home_dir = os.path.expanduser("~")

class PrefDialog():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ojdict.glade")
        self.dicts_store = Gtk.ListStore(str,bool)
        self.get_objects()
        self.connections()
        self.list_dicts()
        
        global my_pref

        my_pref = ConfigParser.RawConfigParser()
        my_pref.add_section("Dicts")

        
    def get_objects(self):
        self.pref_dialog = self.builder.get_object("pref_dialog")
        self.btn_pref_close = self.builder.get_object("btn_pref_close")
        self.combo_lang  = self.builder.get_object("combo_lang")
        

        
        # Dictionary tree view
        self.tv_dicts = self.builder.get_object("tv_dicts")
        self.dictcell = Gtk.CellRendererText()
        self.dictcol = Gtk.TreeViewColumn("Dict",self.dictcell,text=0)
        
        self.togcell = Gtk.CellRendererToggle()
        self.togcol = Gtk.TreeViewColumn("Status",self.togcell,active=1)
        
        self.tv_dicts.append_column(self.dictcol)
        self.tv_dicts.append_column(self.togcol)

        
    def connections(self):
        self.btn_pref_close.connect("clicked",self.on_close_clicked)
        self.combo_lang.connect("changed",self.on_combo_lang_change)
        
        self.togcell.connect("toggled", self.on_toggle)
        
    def on_close_clicked(self,widget):
        self.pref_dialog.hide()
        
        
    def on_combo_lang_change(self,combo):
        itr = self.combo_lang.get_active_iter()
        mod =  self.combo_lang.get_model()
        print mod[itr][0] ,"   is selected "
        
        
    def on_toggle(self,widget,path):

        if not self.dicts_store[path][1]:
            my_pref.set("Dicts",self.dicts_store[path][0],"Enabled")
            
        with open(home_dir+"/.ojdict/config.cfg","wb") as config_file:
            my_pref.write(config_file)
        self.dicts_store[path][1] = not self.dicts_store[path][1]  
            
    def list_dicts(self):
        dicts_list =   os.listdir("dict")
        for dict in dicts_list:
            self.dicts_store.append([dict,False])
        self.tv_dicts.set_model(self.dicts_store)
            
            
        
        