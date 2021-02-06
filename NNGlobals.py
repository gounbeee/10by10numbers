import colorsys
from datetime import datetime


class NNGlobals(object):



    # SCREEN SIZE
    SCREEN_WIDTH = 2560
    SCREEN_HEIGHT = 1080 - 30
    #SCREEN_HEIGHT = 1080


    # SCREEN_WIDTH = 1920
    # SCREEN_HEIGHT = 810

    # DURATION FOR JUNCTION SCENE
    DURATION_JUNCTION = 500

    # GLOBAL CURRENT SCENE NUMBER
    SCENE_INDEX = 0

    SCENE_COUNTS = 0

    #SCENE_BG_COL = (0, 0, 0)

    # PREPARING GLOBAL TIMER
    TIMER = None

    # GLOBAL GAME SCENARIOS
    CURRENT_SCENARIO = " "

    # BACKGROUND COLOR


    # STATEMACHINE
    STATEMACHINE = None


    # CONNECT THE RESULT FROM NNPixelarray OBJECT TO THIS OBJECT
    START_POS_WEIGHT_V = None
    START_POS_WEIGHT_W = None
    START_POS_HIDDEN_A = None
    START_POS_HIDDEN_RELU = None
    START_POS_HIDDEN_B = None
    START_POS_OUTPUT_U = None
    START_POS_SOFTMAX = None

    START_POS_WEIGHT_V_NEWTRAIN = None
    START_POS_WEIGHT_W_NEWTRAIN = None

    # FOR PIXEL ARRAYS
    PIXEL_ARRAY_WEIGHT_V = None
    PIXEL_ARRAY_WEIGHT_W = None
    PIXEL_ARRAY_HIDDEN_A = None
    PIXEL_ARRAY_HIDDEN_RELU = None
    PIXEL_ARRAY_HIDDEN_B = None
    PIXEL_ARRAY_OUTPUT_U = None
    PIXEL_ARRAY_SOFTMAX = None
    PIXEL_ARRAY_WEIGHT_V_NEWTRAIN = None
    PIXEL_ARRAY_WEIGHT_W_NEWTRAIN = None

    SURFACE_WEIGHT_V = None
    SURFACE_WEIGHT_W = None
    SURFACE_HIDDEN_A = None
    SURFACE_HIDDEN_RELU = None
    SURFACE_HIDDEN_B = None
    SURFACE_OUTPUT_U = None
    SURFACE_SOFTMAX = None
    SURFACE_WEIGHT_V_NEWTRAIN = None
    SURFACE_WEIGHT_W_NEWTRAIN = None


    NN_NOT_INITIALIZED = True
    NN_WEIGHT_V_NOT_INITIALIZED = True
    NN_HIDDEN_A_NOT_INITIALIZED = True
    NN_HIDDEN_RELU_NOT_INITIALIZED = True
    NN_HIDDEN_B_NOT_INITIALIZED = True
    NN_WEIGHT_W_NOT_INITIALIZED = True
    NN_OUTPUT_U_NOT_INITIALIZED = True
    NN_SOFTMAX_NOT_INITIALIZED = True

    # WE DON'T NEED TO GATE BELOWS
    # -> WE RE-CALCULATE BELOWS WHEN WE ENTER THE SCENE
    #NN_WEIGHT_V_NEWTRAIN_NOT_INITIALIZED = True
    #NN_WEIGHT_W_NEWTRAIN_NOT_INITIALIZED = True


    # USER INPUT
    USER_INPUT = []
    USER_RESULT = 0

    # TKINTER
    TKINTER_QUIT = False


    # DEMO MODE FLAG
    DEMO_MODE_NOW = True
    ALL_BUTTON_DISABLE = False
    #RETURNED_FROM_DEMO = False


    # DISPLAYING MOUSE COORDINATES
    MOUSECOORDS = False


    # GAME COUNT
    GAME_COUNT = 0

    # FILENAME = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    # FILE = open("GAME_RECORD/" + FILENAME + ".txt", "w")
    # G_COUNT_LINE = ["GAME_COUNT : " + str(GAME_COUNT)]
    #
    # FILE.writelines(G_COUNT_LINE)
    # FILE.write("\n")
    #
    # FILE.close()  # to change file access modes
    #
    #

    def __init__(self):
        #self.SCENE_BG_COL = self.hsv2rgb(self.SCENE_INDEX / self.SCENE_COUNTS, 0.2, 0.8)

        pass





    # < COLOR CONVERSION >
    # https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

