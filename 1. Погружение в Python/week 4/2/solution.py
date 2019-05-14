class Value:
    def __init__(self):
        self.value = 0
    
    def __set__(self, obj, value):
        self.value = value
        
    def __get__(self, obj, obj_type):
        return self.value * (1 - obj.commission)

class Account:
    amount = Value()
    
    def __init__(self, commission):
        self.commission = commission
