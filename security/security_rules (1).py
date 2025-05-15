class secure_class:
    def __init__(self,_query):
        self.query = list(str(_query))
        
    def filter_string(self):
        blocked_symbols = ['>','<','!','/']
        result = [el for el in self.query if el != 't']
        result_string = ''
        for i in result:
            result_string += i
        return result_string
        
    def filter_integer(self):
        allowed_symbols = [1,2,3,4,5,6,7,8,9,0,'3','4','5','6','7','8','9','0','2','1']
        result = [el for el in self.query if el in allowed_symbols]
        result_integer = ''
        for i in result:
            result_integer += str(i)
        return int(result_integer)    
        
        
        
sec = secure_class(13)
fet = sec.filter_integer()
print(fet)