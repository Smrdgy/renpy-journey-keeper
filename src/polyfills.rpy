
init -1600 python:
    class GetScreenVariable(SSSSS.x52NonPicklable):
        def __init__(self, name):
            self.name = name
        
        def __call__(self):
            cs = renpy.current_screen()
            
            if cs and self.name in cs.scope:
                return cs.scope[self.name]
