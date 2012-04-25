#!bin/python

#############################################
# Author : Ahmed Youssef
# License: GPL v3
# Date   : 06-05-08
# Purpose: Helper module for querying the db.
#############################################

import sqlite3 as sqlite

class SearchKeyNotFound(Exception):
    pass

class WordsListLooker(object):
    
    def __init__(self, key=None, dbName=""):
        self.__searchKey=key
        self.__sqlConnection=sqlite.connect(dbName)
        self.__sqlCursor=self.__sqlConnection.cursor()
        
    def __getSearchKey(self):
        return self.__searchKey
    
    def __setSearchKey(self, newSearchKey):
        self.__searchKey=newSearchKey
        
    searchKey=property(fget=__getSearchKey, fset=__setSearchKey, doc="Gets/Sets the search_key")
    
    def __buildQuery(self, maxResults):
        if self.__searchKey:

            sqlQuery="""
               SELECT * FROM wordlist WHERE en LIKE '%s%s' or ar LIKE '%s%s' LIMIT %d
            """%(self.__searchKey,'%', self.__searchKey, '%', maxResults)

   
            
            return sqlQuery
        raise SearchKeyNotFound
        
    def lookup(self, maxResults=5):
        try:
            query=self.__buildQuery(maxResults)
            self.__sqlCursor.execute(query)
            for row in self.__sqlCursor.fetchall():
                yield  row #row (en, ar).
        except SearchKeyNotFound, e:
            print e.message
        except Exception, e:
            print e.message
        
if __name__=="__main__":
    
    wlk=WordsListLooker()
    wlk.searchKey="About"
    for row in wlk.lookup():
        print row
    
    
 
