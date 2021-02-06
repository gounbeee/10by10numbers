import pygame
import NNFunctions
from inspect import currentframe, getframeinfo, stack


# TODO :: SHOULD I INTEGRATE TIMER CLASS I MADE TO THIS ANIMATION ENGINE ?


# CLASS FOR ANIMATION
class NNAnim(object):

    def __init__(self, duration=1000, animation_type="Fixed", scaler_x=0.005, scaler_y=300, freq=1):
        # INITIAL PROPERTIES FOR ANIMATION
        self.duration = duration

        # ANIMATION TYPE AND VALUE SCALER
        self.animation_type = animation_type
        self.scaler_x = scaler_x
        self.scaler_y = scaler_y

        # FORMATTING result_value ACCORDING TO THE ANIMATION TYPE ( SIMPLE FLOAT OR VECTOR TYPE etc.)
        self.result_value = self.initialize_with_type(self.animation_type)

        # TIME VARIABLES
        self.newTime = pygame.time.get_ticks()
        self.createdTime = pygame.time.get_ticks()
        self.deltaTime = 0

        # FLAGS FOR ANIMATION GATE
        self.animation_start = False
        self.animation_done = False

        # FREQUENCY FOR LOOPING ANIMATION
        self.freq = freq


    def reset(self):
        self.initialize_with_type(self.animation_type)


        # TIME VARIABLES
        self.newTime = pygame.time.get_ticks()
        self.createdTime = pygame.time.get_ticks()
        self.deltaTime = 0

        # FLAGS FOR ANIMATION GATE
        self.animation_start = False
        self.animation_done = False



    def initialize_with_type(self, type):
        result_value = None

        # TODO :: CAN I FIX THIS WITH POLYMORPHISM ?


        # TODO :: ARCHIVE BELOW !
        #
        # < == AND is >
        # https://stackoverflow.com/questions/132988/is-there-a-difference-between-and-is
        #
        # : == is for value equality.
        #   Use it when you would like to know if two objects have the same value.
        #   is is for reference equality.
        #   Use it when you would like to know if two references refer to the same object.
        #
        # >>> a = 500
        # >>> b = 500
        # >>> a == b                                --> VALUE ITSELF, IS THE SAME
        # True
        # >>> a is b
        # False                                     --> BUT WE HAVE TWO DIFFERENT PLACES TO BE POSITIONED IN MEMORY,
        #                                               SO WE GET THE DIFFERENT RESULT
        #
        #
        # ****** BUT, THIS HAPPENS ******
        #
        # >>> c = 200                                --> THIS VALUE IS THE POINT, IT IS LOWER THAN 256 ! ( -5 ~ 256)
        # >>> d = 200                                    BECAUSE OF PERFORMANCE REASON, PYTHON USES 'SINGLETON OBJECT'
        # >>> c == d                                     FOR THESE LOW VALUE.
        # True
        # >>> c is d                                     THAT IS WHY THEY HAVE SAME MEMORY ALLOCATION, AND WE GOT THIS RESULT.
        # True
        #

        # DEFINE THE RETURN TYPE
        if type == "Circular" or type == "Fixed":
            result_value = [0, 0]

        elif type == "SequentialPic" or type == "SequentialText" or type == "Sine_0_255" or type == "Cosine_0_255":
            result_value = 0

        else:
            return

        return result_value



    def update(self):

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::update() -- ")

        # TIME ANIMATING
        if self.animation_start is True:
            if self.animation_done is False:

                # IF THE ELAPSED TIME IS PASSED OVER THE LIMIT,
                if self.deltaTime >= self.duration:

                    #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::update() -- OBJECT LOCAL TIME WAS ENDED')

                    # RESET PREVIOUSLY ELAPSED TIME
                    self.deltaTime = 0
                    # ANIMATION IS ENDED
                    self.animation_done = True

                    #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::update() --  ELAPSED TIME IS PASSED OVER THE LIMIT   {self.result_value}')

                    return self.result_value

                else:
                    # IF THE ANIMATION CONTINUES...
                    #
                    # UPDATING CURRENT TIME
                    self.newTime = pygame.time.get_ticks()

                    # CALCULATING DELTA TIME (ELAPSED TIME IN THIS CONTEXT)
                    self.deltaTime = self.newTime - self.createdTime

                    # ADJUSTING X VALUE FOR FUNCTION
                    scaled_value = self.deltaTime * self.scaler_x

                    #print(scaled_value)

                    # GETTING INTERPOLATED VALUE THROUGH THE FUNCTION
                    self.result_value = self.interpolate(scaled_value)

                    #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::update() --  IF THE ANIMATION CONTINUES...  TYPE --  {self.animation_type}')
                    #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::update() --  IF THE ANIMATION CONTINUES... VALUE --  {self.result_value}')

                    return self.result_value

            # TypeError: unsupported operand type(s) for -: 'float' and 'NoneType' python
            # https://stackoverflow.com/questions/23037408/typeerror-unsupported-operand-types-for-float-and-nonetype-python
            # : So this means that somewhere in your code for the function simple_nn you are not returning
            #   anything. Perhaps if you used conditions you didn't evaluate every end path and the function simply returned.
            #
            return self.result_value

        else:
            # IF THE ANIMATION IS OVER, JUST KEEP THE LAST VALUE
            #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::update() --  self.animation_start == False   {self.result_value}')

            return self.result_value




    # THE 'Y' VALUE WILL BE INTERPOLATED BY MATHEMATICAL FUNCTION
    def interpolate(self, xscaled):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNAnim::interpolate() -- ")

        if self.animation_type == 'Fixed':
            function = NNFunctions.NNFunctions_Fixed(xscaled)
            return function.calculate()

        elif self.animation_type == 'Circular':
            function = NNFunctions.NNFunctions_Circular(xscaled, 5)
            return function.calculate()

        elif self.animation_type == 'SequentialText':
            function = NNFunctions.NNFunctions_SequentialTextPic(xscaled)
            return function.calculate()

        elif self.animation_type == 'SequentialPic':
            function = NNFunctions.NNFunctions_SequentialTextPic(xscaled)
            return function.calculate()

        elif self.animation_type == 'Sine_0_255':
            function = NNFunctions.NNFunctions_Sine_0_255(xscaled, self.freq)
            return function.calculate()

        elif self.animation_type == 'Cosine_0_255':
            function = NNFunctions.NNFunctions_Cosine_0_255(xscaled, self.freq)
            return function.calculate()



    def start(self):
        self.animation_start = True


    def end(self):
        self.animation_start = False



    def get_result(self):
        return self.result_value