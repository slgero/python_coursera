import tempfile
import os

class File:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            open(self.path, 'w').close()
        
    def write(self, value):
        with open(self.path, 'w') as f:
            return f.write(value)
            
    def read(self):
        with open(self.path) as f:
            return f.read()
    
    def __str__(self):
        return self.path
    
    def __repr__(self):
        return 'Your file in ' + self.path
    
    def __iter__(self):
        self.f = open(self.path, 'r') # for __next__
        return self
    
    def __next__(self):
        line = self.f.readline()
        if(line):
            return line
        self.f.close()
        raise StopIteration('You read the entire file')
    
    def __add__(self, obj):
        new_path = os.path.join(tempfile.gettempdir(), 'new')
        new_file = File(new_path)
        new_file.write(self.read() + obj.read())
        return new_file
