from flask import Markup
import math
from Library.LoggerModule import info, debug


    
class Pager():
    def __init__(self):
        self.numMovies = 0
        self.pageSelected = 1
        self.perPage = 25
        self.numPages = 1
        self.movieStart = 1
        self.movieEnd = 1
        self.groupStart = 1
        self.groupEnd = 10
        
    def setInit(self):
        i = 0
        
    def previousGroup(self):
        self.groupStart -= 10
        self.groupEnd = self.groupStart + 9

                
    def nextGroup(self):
        self.groupStart += 10
        self.groupEnd += 10
       
        if self.groupEnd > self.numPages:
            self.groupEnd = self.numPages



    def setArg(self, form, resetSearch, searcher, totalMovies):
        debug('form=' + str(form) + ' number movies = ' + str(totalMovies) + ', perPage=' + str(self.perPage) + ', groupEnd=' + str(self.groupEnd))
        
        if 'elementName' in form:  #temporary until routes:displayMovies is  fixed or replaced
            elementName = form['elementName']
            elementValue = form['elementValue']
            debug('elementName=' + elementName + ', elementValue=' + elementValue)
        
        
        #if searcher.isNew() or totalMovies != self.numMovies:
        if resetSearch:
            debug('Resetting pager, searcher.isNew()=' + str(searcher.isNew()) + ', totalMovies=' + str(totalMovies) + ', self.numMovies=' + str(self.numMovies))
            self.pageSelected = 1
            self.groupStart = 1
            self.groupEnd = 10

        elif elementName == 'pageSelected':
            self.pageSelected = int(elementValue)
            
        elif elementName == 'perPage':
            if elementValue == 'All':
                self.perPage = 0
            else:
                self.perPage = int(elementValue)
                self.pageSelected = 1
                
            self.groupStart = 1
            self.groupEnd = 10
        
        elif elementName == 'pageArrow':
            if elementValue == 'p2':
                self.previousGroup()
                self.pageSelected = self.groupStart
            elif elementValue == 'p1':
                self.pageSelected -= 1
                if self.pageSelected < self.groupStart:
                    self.previousGroup()
            elif elementValue == 'n1':
                self.pageSelected += 1
                if self.pageSelected > self.groupEnd:
                    self.nextGroup()
            elif elementValue == 'n2':
                self.nextGroup()
                self.pageSelected = self.groupStart
        elif elementName == 'delete':
            #
            # if we deleted the last movie on a page, go back to the previous page.
            #
            if self.pageSelected == self.numPages and self.numPages > math.ceil(totalMovies / self.perPage):
                self.pageSelected -= 1
                if self.pageSelected < self.groupStart:
                    self.previousGroup()
        

        self.numMovies = totalMovies
        
        if self.perPage == 0:
            self.numPages = 1
        else:
            self.numPages = math.ceil(totalMovies / self.perPage)
        
        self.movieStart = (self.pageSelected - 1) * self.perPage
        debug('perPage=' + str(self.perPage) + ', numPages=' + str(self.numPages) + ', movieStart=' + str(self.movieStart))
        
        if self.pageSelected == self.numPages:
            #
            # Last Page, set movie range appropriately
            #
            self.movieEnd = totalMovies
        else:
            self.movieEnd = self.movieStart + min(self.perPage, totalMovies)
            
        debug('movieEnd=' + str(self.movieEnd) + ', numPages=' + str(self.numPages))
              
        if self.numPages < 10:
            self.groupEnd = self.numPages;
            debug('Set groupEnd = numPages =' + str(self.groupEnd))
        
    def getPageSelected(self):
        return self.pageSelected
    
    def getNumPages(self):
        return self.numPages

    def getGroupRange(self):
        debug('Returning groupStart=' + str(self.groupStart) + ', groupEnd=' + str(self.groupEnd))
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

 