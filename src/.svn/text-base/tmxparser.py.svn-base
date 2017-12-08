import re

class TMXParser:
    
    def __init__(self):
        pass
    
    def create(self,filename):
        file=open(filename)
        stuff=file.read()
        
        o=re.compile(' width=.(..). ')
        width=int(o.findall(stuff)[0])
        
        o=re.compile('<tile gid="(\d*)"/>')
        raw_data=o.findall(stuff)
        
        data=[]
        line=[]
        x=0
        for tile in raw_data:
            line.append(int(tile)-1)
            x+=1
            if x==width:
                data.append(line)
                line=[]
                x=0
                
        return data