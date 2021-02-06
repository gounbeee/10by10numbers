
from inspect import currentframe, getframeinfo, stack



class ManagerObject(object):

    def __init__(self, surface):
        #frameinfo = getframeinfo(currentframe())
        #print(f"{frameinfo.filename} -- {frameinfo.lineno}  ManagerObject::__init__() -- ")

        self.surface = surface
        self.obj_list = []
        self.the_value_dict = {}


    def update(self):
        #frameinfo = getframeinfo(currentframe())
        #print(f"{frameinfo.filename} -- {frameinfo.lineno}  ManagerObject::update() -- ")

        # ALWAYS TRANSFER the_value FROM OBJECT LAYER TO THIS (SCENE) LAYER
        for obj in self.obj_list:

            if obj.the_value is not -1:
                # STORE IT
                # https://pycarnival.com/dict/
                self.the_value_dict[obj.obj_id] = obj.the_value

            obj.update()

    def render(self):
        #frameinfo = getframeinfo(currentframe())
        #print(f"{frameinfo.filename} -- {frameinfo.lineno}  ManagerObject::render() -- ")

        for obj in self.obj_list:
            obj.render()
