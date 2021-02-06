import math
from inspect import currentframe, getframeinfo, stack
#frameinfo = getframeinfo(currentframe())



class NNFunctions_Identity(object):
    def __init__(self, x):
        self.x = x

    def calculate(self):
        return self.x



class NNFunctions_Fixed(object):
    def __init__(self, x ):
        self.x = x
        self.result = [0, 0]

    def calculate(self):
        return self.result



class NNFunctions_Circular(object):
    def __init__(self, t, radius ):
        self.t = t
        self.radius = radius
        self.result = [0, 0]


    def calculate(self):
        x = self.radius * math.cos(self.t)
        y = self.radius * math.sin(self.t)
        self.result = [x, y]
        return self.result




class NNFunctions_SequentialTextPic(object):

    def __init__(self, x):
        self.x = x
        self.result = 0

    def calculate(self):

        self.result = self.x

        if self.result <= 255:
            return int(self.result)
        else:
            return 255





class NNFunctions_Sine_0_255(object):

    def __init__(self, x, freq):
        # NORMALIZE
        self.x = x / 255.0

        # INITIALIZATION
        self.result = 255
        self.freq = freq


    def calculate(self):
        #print(f'self.x VALUE IS   {self.x}')

        # CALCULATING SINE FUNCTION
        self.result += int(math.sin(self.x * self.freq) * 255)

        # CLAMP THE VALUE OF THE ANIMATED VALUE
        if 0 <= self.result <= 255:
            #print(f'self.result VALUE IS   {self.result}')
            #print('---------------')
            return self.result
        elif self.result < 0:
            self.result = 0
            #print(f'self.result VALUE IS   {self.result}')
            #print('---------------')
            return self.result
        else:
            self.result = 255
            #print(f'self.result VALUE IS   {self.result}')
            #print('---------------')
            return self.result




class NNFunctions_Cosine_0_255(object):

    def __init__(self, x, freq):
        # NORMALIZE
        self.x = x / 255.0

        # INITIALIZATION
        self.result = 255
        self.freq = freq


    def calculate(self):
        #print(f'self.x VALUE IS   {self.x}')

        # CALCULATING SINE FUNCTION
        self.result += int(math.cos(self.x * self.freq) * 255)

        # CLAMP THE VALUE OF THE ANIMATED VALUE
        if 0 <= self.result <= 255:
            #print(f'self.result VALUE IS   {self.result}')
            #print('---------------')
            return self.result
        elif self.result < 0:
            self.result = 0
            #print(f'self.result VALUE IS   {self.result}')
            #print('---------------')
            return self.result
        else:
            self.result = 255
            #print(f'self.result VALUE IS   {self.result}')
            #print('---------------')
            return self.result

