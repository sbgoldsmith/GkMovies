from flask import Markup
import math
import json
from json import JSONEncoder
from collections import namedtuple
import logging


    
class Pager():
    def __init__(self):
        self.pageSelected = 1
        self.perPage = 25
        self.numPages = 1
        self.movieStart = 1
        self.movieEnd = 1
        self.groupStart = 1
        self.groupEnd = 10

    
    def previousGroup(self):
        self.groupStart -= 10
        self.groupEnd = self.groupStart + 9

                
    def nextGroup(self):
        self.groupStart += 10
        self.groupEnd += 10
       
        if self.groupEnd > self.numPages:
            self.groupEnd = self.numPages



    def setArgs(self, args, searcher, totalMovies):
        logging.getLogger('gk').info('Pager.setArgs: args=' + str(args))
        
        if searcher.isNew():
            self.pageSelected = 1
            self.groupStart = 1
            self.groupEnd = 10

        elif 'pageSelected' in args:
            self.pageSelected = int(args['pageSelected'])
            
        elif 'perPage' in args:
            if args['perPage'] == 'All':
                self.perPage = 0
            else:
                self.perPage = int(args['perPage'])
                self.pageSelected = 1
                
            self.groupStart = 1
            self.groupEnd = 10
        
        elif 'pageArrow' in args:
            if args['pageArrow'] == 'p2':
                self.previousGroup()
                self.pageSelected = self.groupStart
            elif args['pageArrow'] == 'p1':
                self.pageSelected -= 1
                if self.pageSelected < self.groupStart:
                    self.previousGroup()
            elif args['pageArrow'] == 'n1':
                self.pageSelected += 1
                if self.pageSelected > self.groupEnd:
                    self.nextGroup()
            elif args['pageArrow'] == 'n2':
                self.nextGroup()
                self.pageSelected = self.groupStart
        
        
        if self.perPage == 0:
            self.numPages = 1
        else:
            self.numPages = math.ceil(totalMovies / self.perPage)
        
        self.movieStart = (self.pageSelected - 1) * self.perPage

        
        if self.pageSelected == self.numPages:
            #
            # Last Page, set movie range appropriately
            #
            self.movieEnd = totalMovies
        else:
            self.movieEnd = self.movieStart + min(self.perPage, totalMovies)
            
            
        if self.numPages < 10:
            self.groupEnd = self.numPages;
        
        
    def getPageSelected(self):
        return self.pageSelected
    
    def getNumPages(self):
        return self.numPages

    def getGroupRange(self):
        return range(self.groupStart, self.groupEnd + 1)
    
    def getPerPage(self):
        return self.perPage
    
    def getPerPageSelected(self, per):
        if self.perPage == per:
            return 'selected'
        else:
            return ''

    
    def getMovieRange(self):
        return range(self.movieStart, self.movieEnd)
    
    def strong(self, p):
        if p == self.pageSelected:
            return Markup("<strong>" + str(p) + "</strong>")
        else:
            return str(p)
        
    def getVisibility(self, code):
        if code == 'p2':
            if self.groupStart > 1:
                return 'visible'
            else:
                return 'hidden'
        elif code == 'n2':
            if self.numPages > self.groupEnd:
                return 'visible'
            else:
                return 'hidden'


    def getOpacity(self, code):
        if code == 'p1':
            if self.pageSelected == 1:
                return "0.2"
            else:
                return "1.0"
        elif code == 'n1':
            if self.pageSelected == self.numPages:
                return "0.2"
            else:
                return "1.0"     

            
    def getPointerEvents(self, code):
        if code == 'p1' and self.pageSelected == 1:
            return "none"
        elif code == 'n1'and self.pageSelected == self.numPages:
            return "none"
        else:
            return "auto"     