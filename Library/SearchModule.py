class Searcher():
    
    def __init__(self):
        self.this = ''
        
        
        self.series = ''
        self.seriesFirst = False
        self.title = ''
        self.genre = ''
        self.actor = ''
        self.plot = ''
        
        self.user01 = ''
        self.user02 = ''
        self.user03 = ''
        self.user04 = ''
        self.user05 = ''
        self.user06 = ''
        self.user07 = ''
        self.user08 = ''
        self.user09 = ''
        self.user10 = ''

        self.reseted = False

    def setArgs(self, args):           
        self.this = ''
        
        if 'reset_search' in args:
            self.reseted = True   
            for var in dir(self):
                if var not in ['setArgs', 'like', 'get', 'isNew', 'reseted', 'seriesFirst'] and "__" not in var:
                    setattr(self, var, '')  
             
        else:
            self.reseted = False 
            for key in args:
                if key.endswith('Search'):
                    self.this = key.replace('Search', '')
                    value = args[key]
                    value = value.replace("+", " ")
                    
                    setattr(self, self.this, value)
                    if key == 'seriesSearch' and value != '':
                        self.seriesFirst = True


    def like(self, name):
        value = getattr(self, name)
        if value == '':
            return None
        else:
            return "%" + value + "%"
        
    def get(self, name):
        rtn = getattr(self, name)
        return rtn
        
    def isNew(self):
        rtn = self.this != '' or self.reseted
        return rtn
    