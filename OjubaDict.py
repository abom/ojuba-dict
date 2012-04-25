#!/usr/bin/python
# -*- coding=utf-8 -*-
import os
from gi.repository import Gtk,WebKit
from looker import WordsListLooker
from pyarabic import araby
from string import strip

home_dir = os.path.expanduser("~")

class OJDict():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ojdict.glade")
		self.get_objects()
		self.connections()
		self.main_window.show_all()
		
		self.view = WebKit.WebView()
		self.scroll_web.add(self.view)
		self.view.show()
		
	def get_objects(self):
		self.main_window = self.builder.get_object("main_window")
		self.btn_about = self.builder.get_object("btn_about")
		self.entry_keyword = self.builder.get_object("entry_keyword")
		self.tv_result = self.builder.get_object("tv_result")
		
		self.scroll_web = self.builder.get_object("scroll_web")
		
		# TreeView Objects
		self.encol = self.builder.get_object("encol")
		self.arcol = self.builder.get_object("arcol")
		self.encell = self.builder.get_object("encell")
		self.arcell = self.builder.get_object("arcell")
		self.encol.add_attribute(self.encell,"text", 0)
		self.select = self.tv_result.get_selection()

	def connections(self):
		self.main_window.connect("delete-event", Gtk.main_quit)   # Terminate the application when close the window
		self.entry_keyword.connect("changed",self.on_keyword_changed)
		self.select.connect("changed", self.on_tree_selection_changed)

	def get_model(self):
		list_store = Gtk.ListStore(str)
		db_list =   os.listdir("dict")
		result_all = ''
		for db in db_list:
			db_name = os.path.splitext(db)[0]
			wlooker = WordsListLooker(None,"dict/"+db)
			wlooker.searchKey = self.entry_keyword.get_text()
			
			if not araby.isArabicword(unicode(wlooker.searchKey)):
				Result='<p dir="ltr"><font color="blue">'+db_name+'</font></p>'+'<html dir="rtl">'
				for row in wlooker.lookup():
					list_store.append([row[0]])
					Result = Result +"<br />"+row[1]
			else:
				Result='<p dir="ltr"><font color="blue"><b>'+db_name+'</b></font></p>'
				for row in wlooker.lookup():
					list_store.append([row[1]])
					Result = Result +"<br />"+row[0]
			result_all = result_all+Result
			self.view.load_string(result_all,"text/html","UTF-8",'www.example.com')
				
			
		return list_store
	
	def on_tree_selection_changed(self,selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
			print "You selected", model[treeiter][0]

	
	def on_keyword_changed(self,widget):
		self.tv_result.set_model(self.get_model())
		