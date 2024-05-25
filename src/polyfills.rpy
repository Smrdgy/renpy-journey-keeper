
init 1 python:
    class URMGetScreenVariable(x52URM.x52NonPicklable):
        def __init__(self, name, key=None):
            self.name = name
            self.key = key
        
        def __call__(self):
            cs = renpy.current_screen()
            
            if not cs or not self.name in cs.scope:
                return
            
            if(self.key):
                key = self.key if not callable(self.key) else self.key()
                return cs.scope[self.name][key]
            else:
                return cs.scope[self.name]
