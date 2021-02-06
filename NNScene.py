import pygame
import pygame.gfxdraw
import ManagerObject
import NNNode
import Timer
from NNGlobals import *
import NNPixelArray
import NNModel
import NNXmlConnector
import colorsys
import math
import os
import numpy



# BASE CLASS
# noinspection PyPackageRequirements
class NNScene(object):
    """
    NNScene CLASS (by sy)
        THIS CLASS IS BASE CLASS FOR IMPLEMENTATION OF SCENE.
   """


    # ENTER THE SCENE NUMBER TO DISPLAY THE NODES AND LAYERS
    display_nn_visuals = {
        "Weight_V": [5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 24, 25, 26, 27, 28, 29, 30, 45, 48, 58, 59],
        "Hidden_A": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 21, 25, 26, 48, 50, 52, 53],
        "Hidden_Relu": [5, 6, 13, 14, 21, 25, 26, 48, 50, 52, 53],
        "Hidden_B": [5, 6, 13, 14, 15, 16, 17, 18, 21, 25, 26, 48, 50, 52, 53],
        "Weight_W": [5, 17, 18, 21, 24, 25, 26, 27, 28, 45, 46, 47],
        "Output_U": [5, 17, 18, 19, 20, 21, 25, 26, 46, 47, 50],
        "Softmax": [5, 19, 20, 21, 22, 25, 26, 35, 41, 42, 46, 47, 50],
        "Weight_v_newtrain": [49],
        "Weight_w_newtrain": [49],
    }


    def __init__(self, surface):
        """
        INITIALIZING SCENE OBJECT

        :param surface: pygame'S SURFACE OBJECT
        """

        # INITIALIZING STATE ID
        self.stateID = ''

        # SCENE NUMBER ** NOT THE INDEX OF SCENE OBJECT LIST !!!!
        self.scene_number = -1

        # pygame SURFACE DATA
        # : DELIVERED FROM OUTSIDE
        self.surface = surface

        # GATE FOR UPDATE FUNCTION
        # : THIS IS MAIN GATE FOR 'ALL PROCESSES' IN THE UPDATE FUNCTION
        self.can_update = False

        # INITIALIZING ObjectManager OBJECT
        # : DELIVERING PYGAME SURFACE OBJECT
        self.obj_manager = ManagerObject.ManagerObject(surface)

        # THE VALUE FOR NNModel ENGINE
        # : 'BLANK' DICTIONARY
        self.the_value_dict = {}

        # ELAPSED TIME FROM MAIN TIMELINE
        # : ELAPSED TIME CALUE FOR ANIMATING
        #   (DELIVERED FROM OUTSIDE INTO update() FUNCTION IN THIS CLASS)
        self.elapsed_time = 0

        # TOTAL DURATION
        self.duration = 0

        # TEMPORARY the_value
        self.value_now = 0

        # FOR INTERACTION
        self.click_left_occured = False
        self.click_right_occured = False

        # COLOR
        self.textcolor_main = (160, 50, 90)

        # NNModel
        self.nnmodel = NNModel.NN.get_instance()
        self.input_for_render_weight_v = ()

        # XML CONNECTOR
        self.xmlconnector = NNXmlConnector.NNXmlConnector('xml_scenes/scenes_xml.xml', self.surface)
        self.count_scenes = len(self.xmlconnector.get_all_scene_layer())

        # PROCESS PIPES
        #self.p_receive_sub_to_main = None
        #self.p_send_main_to_sub = None

        # TEXT TO DISPLAY THE REALTIME PREDICTION IN SCENE 1
        self.text_nn_result = None

        # FOR NN MODEL
        self.input_for_creating_pixels_weight_v = None
        self.input_for_creating_pixels_hidden_a = None
        self.input_for_creating_pixels_hidden_relu = None
        self.input_for_creating_pixels_hidden_b = None
        self.input_for_creating_pixels_output_u = None
        self.input_for_creating_pixels_softmax = None

        self.input_for_creating_pixels_weight_v_newtrain = None
        self.input_for_creating_pixels_weight_w_newtrain = None



        # VARIABLES FOR DISPLAYING NN TRAINING

        # FLAG TO EXECUTE TRAINING WITH NN MODEL
        self.train_flag = False

        # self.epoch = None
        # self.loss = None
        # self.score = None
        self.weight_v_new_train = None
        self.weight_w_new_train = None


    def setup(self, the_value_dict, duration):
        self.duration = duration




    def start(self):
        """
        START NNAnim ENGINE

        """
        # RESET OBJECT'S NNAnim ENGINE
        # : IF ACTUAL OBJECTS IS CREATED...
        if len(self.obj_manager.obj_list) is not 0:
            # RESET AND START THE ANIMATION ENGINE
            # FOR EVERY OBJECTS
            for obj in self.obj_manager.obj_list:
                obj.anim.reset()
                obj.anim.start()

        # GATE FOR update() FUNCTION 'OPENED' HERE
        self.can_update = True

        #####print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene::start() --    len(self.obj_manager.obj_list)  --     {len(self.obj_manager.obj_list)}")




    def update(self, elapsed_time):
        """
        UPDATE FUNCTION

        :param elapsed_time: ELAPSED TIME FROM OUTSIDE OF THIS OBJECT
        """

        self.elapsed_time = elapsed_time

        # MANAGING THE EVENT WITH MOUSE
        self.click_left_occured = pygame.mouse.get_pressed(3)[0]
        self.click_right_occured = pygame.mouse.get_pressed(3)[1]
        #print(self.click_left_occured)

        # TODO :: BELOW IS CRITICAL !
        # UPDATING the_value_dict
        self.exchange_value_dict()


        if self.can_update is True:
            self.obj_manager.update()


        # IF THE KEY WAS PRESSED, COPY THE MOUSE POSITION TO CLIPBOARD !
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LCTRL] and keypressed[pygame.K_c] and keypressed[pygame.K_LSHIFT]:
            #####print("CTRL+SHIFT+C WAS PRESSED !!!!")
            coord = str(pygame.mouse.get_pos()).replace("(", "").replace(")", "").replace(" ", "")
            self.addToClipBoard(coord)



        # -------------------------------------------------------------------------------------------
        # < TRAINING PHASE VISUALIZATION >
        #
        # TODO :: SCENE NUMBER SHOULD BE CHANGED !
        # TRAINING NN MODEL IF THE FLAG IS ON

        if self.train_flag and self.scene_number >= 2:


            self.nnmodel.train_to_visualize_only()


            if self.nnmodel.next_flag:

                # UPDATING TRAINING RESULT
                # self.epoch = self.nnmodel.epoch
                # self.loss = self.nnmodel.loss
                # self.score = self.nnmodel.score
                self.weight_v_new_train = self.nnmodel.V
                self.weight_w_new_train = self.nnmodel.W

                #print(self.nnmodel.next_flag)
                #####print("IN SCENE DATA ::   epoch = %d loss = %f score = %f" % (self.nnmodel.epoch, self.nnmodel.loss, self.nnmodel.score))

                # IF self.epoch IS BIGGER THAN 1, WE CAN START TO UPDATE
                # UPDATING PIXEL ARRAY OF TWO WEIGHTS (V AND W NEWLY TRAINED)
                if self.nnmodel.epoch > 1 and \
                        self.weight_v_new_train is not None and \
                        self.weight_w_new_train is not None:

                    self.weights_new_train_update()





    def render(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene::render() -- ")

        self.surface.fill(self.hsv2rgb(NNGlobals.SCENE_INDEX / self.count_scenes, 0.2, 0.8))


        # < Check if element exists in list in Python >
        # < How to Iterate Through a Dictionary in Python >
        # https://realpython.com/iterate-through-dictionary-python/
        # https://www.geeksforgeeks.org/check-if-element-exists-in-list-in-python/
        for key in self.display_nn_visuals:
            #print(self.display_nn_visuals[key])
            if self.scene_number in self.display_nn_visuals[key]:

                self.nodes_layers_render(key)


        self.display_time_progressbar()

        self.obj_manager.render()


        # ADD THE DUMMY INPUT DATA 1.0 RECTANGLE
        if self.scene_number >= 2:
            self.add_input_dummy()




    def add_input_dummy(self):

        pygame.draw.rect(self.surface, (0, 0, 0), (20, NNGlobals.SCREEN_HEIGHT // 2 + 500 - 9, 18, 18))




    def on_exit(self):
        self.disable_update()

        del self.obj_manager.obj_list[:]
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene::on_exit() --    self.can_update    --    {self.can_update}")
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene::on_exit() --    len(self.obj_manager.obj_list)    --    {len(self.obj_manager.obj_list)}")



    # ----------------------------------------------------------------------
    # BUTTON FUNCTIONS


    def start_button(self):
        """ THIS BUTTON IS FOR SCENE 1 ONLY !!! """
        #####print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene::start_button() --  start FUNCTION IS EXECUTED")

        # GLOBAL DEMO MODE OFF
        NNGlobals.DEMO_MODE_NOW = False
        NNGlobals.ALL_BUTTON_DISABLE = False

        NNGlobals.TIMER.reset()

        NNGlobals.SCENE_INDEX = 1
        NNGlobals.TIMER.timeline_index = 1

        NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

        # SEND MESSAGE TO SUB PROCESS !
        # if self.p_send_main_to_sub is not None:
        #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(2))


        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)




        # TODO :: ARCHIVE BELOW !!!!
        # ----------------------------------------------------------------------------------------
        # < WRITING GAME RECORDS TO FILE >
        # https://www.geeksforgeeks.org/reading-writing-text-files-python/

        #
        filename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        file = open("GAME_RECORD/" + filename + ".txt", "w")
        file.write("\n")
        file.close()


        # ADDING GAME COUNT
        NNGlobals.GAME_COUNT += 1

        # Program to show various ways to read and
        # write data in a file.
        file = open("GAME_RECORD/" + filename + ".txt", "w")

        # DATA TO WRITIE
        date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        newline = ["GAME_COUNT : " + str(NNGlobals.GAME_COUNT)]

        # \n is placed to indicate EOL (End of Line)
        file.writelines(self.list_to_string(NNGlobals.USER_INPUT))
        file.write("\n")
        file.writelines(date)
        file.write("\n")
        file.writelines(newline)
        file.write("\n")

        file.close()  # to change file access modes




    def prev_button(self):
        #####print(f'PREV BUTTON CLICKED -- {self.scene_number}')
        #print(f'                    -- NNGlobals.TIMER.timeline_index -- {NNGlobals.TIMER.timeline_index}')

        if self.scene_number > 2:

            # GLOBAL DEMO MODE OFF
            NNGlobals.DEMO_MODE_NOW = False
            NNGlobals.ALL_BUTTON_DISABLE = False

            NNGlobals.TIMER.reset()

            NNGlobals.SCENE_INDEX -= 2
            NNGlobals.TIMER.timeline_index -= 2

            NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

            # SEND MESSAGE TO SUB PROCESS !
            # if self.p_send_main_to_sub is not None:
            #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(self.scene_number - 1))

        else:
            #print(f'** THERE IS NO NEXT SCENE TO MOVE ! **  NOW  NNGlobals.TIMER.timeline_index --  {NNGlobals.TIMER.timeline_index}')
            pass

        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)



    def next_button(self):
        #####print(f'NEXT BUTTON CLICKED -- {self.scene_number}')
        #print(f'                    -- NNGlobals.TIMER.timeline_index -- {NNGlobals.TIMER.timeline_index}')

        if self.scene_number < self.count_scenes:

            # GLOBAL DEMO MODE OFF
            NNGlobals.DEMO_MODE_NOW = False
            NNGlobals.ALL_BUTTON_DISABLE = False

            NNGlobals.TIMER.reset()

            NNGlobals.SCENE_INDEX += 2
            NNGlobals.TIMER.timeline_index += 2

            NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

            # SEND MESSAGE TO SUB PROCESS !
            # if self.p_send_main_to_sub is not None:
            #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(self.scene_number + 1))


        else:
            #print(f'** THERE IS NO NEXT SCENE TO MOVE ! **  NOW  NNGlobals.TIMER.timeline_index --  {NNGlobals.TIMER.timeline_index}')
            pass

        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)



    def reset_all_flow_button(self):
        #####print(f'ALL RESET BUTTON CLICKED -- {self.scene_number}')

        # SCENE JUMPING
        NNGlobals.SCENE_INDEX = 0

        # GLOBAL FLAGS RESET
        NNGlobals.ALL_BUTTON_DISABLE = False
        NNGlobals.DEMO_MODE_NOW = True
        NNGlobals.USER_INPUT = []
        NNGlobals.USER_RESULT = 0

        # TIMER RESETTING
        NNGlobals.TIMER.reset()
        NNGlobals.TIMER.timeline_index = 0

        NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

        # SEND MESSAGE TO SUB PROCESS !
        # if self.p_send_main_to_sub is not None:
        #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(1))

        # RESET PREVIOUS nnmodel'S PREDICTION
        self.nnmodel.reset_prediction()



    def prev_button_5(self):
        #####print(f'PREV BUTTON CLICKED -- {self.scene_number}')
        #print(f'                    -- NNGlobals.TIMER.timeline_index -- {NNGlobals.TIMER.timeline_index}')

        if self.scene_number > 2 and self.scene_number - 5 >= 2:

            # GLOBAL DEMO MODE OFF
            NNGlobals.DEMO_MODE_NOW = False
            NNGlobals.ALL_BUTTON_DISABLE = False

            NNGlobals.TIMER.reset()

            NNGlobals.SCENE_INDEX -= 10
            NNGlobals.TIMER.timeline_index -= 10

            NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

            # SEND MESSAGE TO SUB PROCESS !
            # if self.p_send_main_to_sub is not None:
            #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(self.scene_number - 5))

        else:
            #print(f'** THERE IS NO NEXT SCENE TO MOVE ! **  NOW  NNGlobals.TIMER.timeline_index --  {NNGlobals.TIMER.timeline_index}')
            pass

        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)


    def next_button_5(self):
        #####print(f'NEXT BUTTON CLICKED -- {self.scene_number}')
        #print(f'                    -- NNGlobals.TIMER.timeline_index -- {NNGlobals.TIMER.timeline_index}')

        if self.scene_number < self.count_scenes and self.scene_number + 5 < self.count_scenes:

            # GLOBAL DEMO MODE OFF
            NNGlobals.DEMO_MODE_NOW = False
            NNGlobals.ALL_BUTTON_DISABLE = False

            NNGlobals.TIMER.reset()

            NNGlobals.SCENE_INDEX += 10
            NNGlobals.TIMER.timeline_index += 10

            NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

            # SEND MESSAGE TO SUB PROCESS !
            # if self.p_send_main_to_sub is not None:
            #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(self.scene_number + 5))
            #

        else:
            #print(f'** THERE IS NO NEXT SCENE TO MOVE ! **  NOW  NNGlobals.TIMER.timeline_index --  {NNGlobals.TIMER.timeline_index}')
            pass

        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)


    def prev_button_10(self):
        #####print(f'PREV BUTTON CLICKED -- {self.scene_number}')
        #print(f'                    -- NNGlobals.TIMER.timeline_index -- {NNGlobals.TIMER.timeline_index}')

        if self.scene_number > 2 and self.scene_number - 10 >= 2:

            # GLOBAL DEMO MODE OFF
            NNGlobals.DEMO_MODE_NOW = False
            NNGlobals.ALL_BUTTON_DISABLE = False

            NNGlobals.TIMER.reset()

            NNGlobals.SCENE_INDEX -= 20
            NNGlobals.TIMER.timeline_index -= 20

            NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

            # SEND MESSAGE TO SUB PROCESS !
            # if self.p_send_main_to_sub is not None:
            #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(self.scene_number - 10))

        else:
            #print(f'** THERE IS NO NEXT SCENE TO MOVE ! **  NOW  NNGlobals.TIMER.timeline_index --  {NNGlobals.TIMER.timeline_index}')
            pass

        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)



    def next_button_10(self):
        #####print(f'NEXT BUTTON CLICKED -- {self.scene_number}')
        #print(f'                    -- NNGlobals.TIMER.timeline_index -- {NNGlobals.TIMER.timeline_index}')

        if self.scene_number < self.count_scenes and self.scene_number + 10 < self.count_scenes:

            # GLOBAL DEMO MODE OFF
            NNGlobals.DEMO_MODE_NOW = False
            NNGlobals.ALL_BUTTON_DISABLE = False

            NNGlobals.TIMER.reset()

            NNGlobals.SCENE_INDEX += 20
            NNGlobals.TIMER.timeline_index += 20

            NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

            # SEND MESSAGE TO SUB PROCESS !
            # if self.p_send_main_to_sub is not None:
            #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(self.scene_number + 10))
            #

        else:
            #print(f'** THERE IS NO NEXT SCENE TO MOVE ! **  NOW  NNGlobals.TIMER.timeline_index --  {NNGlobals.TIMER.timeline_index}')
            pass

        NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
        #####print(NNGlobals.USER_RESULT)



    # ----------------------------------------------------------------------
    # DISPLAYING FUNCTIONS

    def display_loading(self):
        #self.surface.fill((170, 170, 170))

        #surface = pygame.Surface((NNGlobals.SCREEN_WIDTH, NNGlobals.SCREEN_HEIGHT))
        #self.surface.blit(surface, (0, 0))

        # FONT NAME
        font_name = 'GenEiChikugoMin2-R.ttf'
        # SO, BELOW WILL CREATE THE FONT OBJECT
        font = pygame.font.Font(font_name, 50)


        textSurface = font.render('- LOADING -', True, (10,120,170))
        textRect = textSurface.get_rect()
        textRect.x = NNGlobals.SCREEN_WIDTH // 2 - textSurface.get_width() // 2
        textRect.y = 40
        self.surface.blit(textSurface, textRect)



    def display_result_categories(self):

        text_result_numbers = []

        for i in range(10):
            number = NNNode.NNNodeText(self.surface,
                                        'txt_final_categories_' + str(i),
                                         str(i),
                                         (NNGlobals.SCREEN_WIDTH//2 - 900 + (200 * i), NNGlobals.SCREEN_HEIGHT//2 - 390),
                                         (255, 255, 255),
                                         50,
                                         8000,
                                        'Fixed',
                                         0.5,
                                        1.0,
                                        True)

            text_result_numbers.append(number)
            self.obj_manager.obj_list.append(number)



    def display_time_progressbar(self):
        # DRAW ELAPSED TIME GAUGE
        pygame.draw.line(self.surface, (255, 0, 0), (0, 5), (int(NNGlobals.SCREEN_WIDTH * (self.elapsed_time / self.duration)), 5), 2)

        #print( self.duration )



    # < DISPLAYING INPUT LAYER >
    # : 3 STEPS --> THE COMBINATIONS OF ABOVE FUNCTIONS
    #
    def display_input_layer(self, count, the_value_dict):

        # CREATING OBJECTS
        self.drawpad_create(count, 18, True, 10, the_value_dict)

        # POSITIONING OBJECTS
        self.drawpad_spread(count, 18, the_value_dict)

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_2::setup() -- {self.the_value_dict}")

        # SETTING TEXT-OBJECTS WITH the_value
        self.set_text_visible_with_value()




    def drawpad_spread(self, count, size, the_value_dict):
        # CONSTRUCT DRAWING PAD
        drawpad_size = count
        drawpad_button_size = size


        # < ABOUT ERROR 'TypeError: 'tuple' object does not support item assignment' >
        # https://stackoverflow.com/questions/7735838/typeerror-tuple-object-does-not-support-item-assignment-when-swapping-values
        # : Evaluating "1,2,3" results in (1, 2, 3), a tuple. As you've discovered, tuples are immutable. Convert to a list before processing.
        #
        # CONVERTING LIST TO TUPLE
        # https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/

        # POSITIONING OF DRAWPAD BUTTONS
        gap_for_dummy = 15
        center_position = [NNGlobals.SCREEN_WIDTH // 2, NNGlobals.SCREEN_HEIGHT // 2]                                        # LIST TYPE
        left_top_position = [center_position[0] - (drawpad_button_size * drawpad_size * 6.9) + gap_for_dummy, center_position[1] + 500]      # LIST TYPE


        # FOR EVERY OBJECTS...
        for i in range(len(self.obj_manager.obj_list)):

            # ADJUSTING HORIZONTAL POSITIONS
            modified_position = [left_top_position[0] + (drawpad_button_size * (i/1.433)), left_top_position[1]]             # LIST TYPE
            self.obj_manager.obj_list[i].position = tuple(modified_position)                                                 # TUPLE TYPE

            # FOR THE OBJECTS WHICH IS NOT THE 'TEXT'...
            if type(self.obj_manager.obj_list[i]) is not NNNode.NNNodeText and \
                type(self.obj_manager.obj_list[i]) is not NNNode.NNNodeMultiText and \
                type(self.obj_manager.obj_list[i]) is not NNNode.NNNodeIndicator and \
                    type(self.obj_manager.obj_list[i]) is not NNNode.NNNodeButton:

                self.obj_manager.obj_list[i].the_value = the_value_dict[self.obj_manager.obj_list[i].obj_id]

            else:
                self.obj_manager.obj_list[i].the_value = -1


            # < SEARCHING OBJECTS USING ID (STRING) >
            #
            # BUILT-IN OBJECTS ARE THE NUMBERS OF WEIGHTS PLACED ABOVE THE INPUT NODES
            #
            # IF THERE ARE BUILT-IN TEXT OBJECTS,
            # RE-POSITION IT
            got_id = self.obj_manager.obj_list[i].obj_id

            # ACCORDING TO ABOVE SETTING ABOUT OBJECT ID,
            # IF THE ID INCLUDES 'txt_', RE-POSITION IT
            trimmed_id = got_id[:4]

            # IF THE ID IS STARTING FROM 'txt_'...
            if trimmed_id == 'txt_':
                ##print(got_id)
                # RE-POSITION
                repositioned = list(self.obj_manager.obj_list[i].position)                                                      # TUPLE TO LIST
                repositioned = [repositioned[0] - drawpad_button_size - 5, repositioned[1] - drawpad_button_size - 5]           # LIST
                self.obj_manager.obj_list[i].position = tuple(repositioned)                                                     # CONVERTED TO TUPLE

                self.obj_manager.obj_list[i].set_style('0', drawpad_button_size * 2, self.obj_manager.obj_list[i].color)




    def visible_texts(self):
        for i in range(len(self.obj_manager.obj_list)):

            # TODO :: FIX THE DUPLICATION BELOW

            # IF THERE ARE BUILT-IN TEXT OBJECTS,
            got_id = self.obj_manager.obj_list[i].obj_id
            # ACCORDING TO ABOVE SETTING ABOUT OBJECT ID,
            # IF THE ID INCLUDES 'txt_', RE-POSITION IT
            trimmed_id = got_id[:4]
            if trimmed_id is 'txt_':
                ##print(got_id)
                # RE-POSITION
                self.obj_manager.obj_list[i].visible = True




    # ----------------------------------------------------------------------
    # CREATION FUNCTIONS

    def create_scene_index(self):
        scene_num_now = NNNode.NNNodeText(self.surface,
                                          'scene_num_text',
                                          str(self.scene_number) + " / " + str(self.count_scenes),
                                           (NNGlobals.SCREEN_WIDTH // 2, NNGlobals.SCREEN_HEIGHT // 2 - 474),
                                           (90, 90, 90),
                                           25,
                                           8000,
                                           'Fixed',
                                           0.5,
                                           1.0,
                                           True)

        self.obj_manager.obj_list.append(scene_num_now)




    def create_nav_buttons(self):
        margin = 100

        # NAV BUTTONS
        if self.scene_number is 2:
            self.create_nav_next_button('Btn_Next',
                                        (NNGlobals.SCREEN_WIDTH // 2 , 50),
                                        30,
                                        20,
                                        self.next_button)

        # FOR ALL OTHER SCENES
        else:

            self.create_nav_prev_button('Btn_Prev',
                                        (NNGlobals.SCREEN_WIDTH // 2 - margin, 50),
                                        30,
                                        20,
                                        self.prev_button)

            self.create_nav_next_button('Btn_Next',
                                        (NNGlobals.SCREEN_WIDTH // 2 + margin, 50),
                                        30,
                                        20,
                                        self.next_button)


            self.create_nav_reset_button('Btn_Reset',
                                         (60, 50),
                                         20,
                                         15,
                                         self.reset_all_flow_button)


            self.create_nav_prev_button('Btn_Prev_5',
                                        (NNGlobals.SCREEN_WIDTH // 2 - margin*2, 50),
                                        30,
                                        20,
                                        self.prev_button_5)

            self.create_nav_next_button('Btn_Next_5',
                                        (NNGlobals.SCREEN_WIDTH // 2 + margin*2, 50),
                                        30,
                                        20,
                                        self.next_button_5)


            self.create_nav_prev_button('Btn_Prev_10',
                                        (NNGlobals.SCREEN_WIDTH // 2 - margin*4, 50),
                                        30,
                                        20,
                                        self.prev_button_10)

            self.create_nav_next_button('Btn_Next_10',
                                        (NNGlobals.SCREEN_WIDTH // 2 + margin*4, 50),
                                        30,
                                        20,
                                        self.next_button_10)


    # TODO :: MAKE BELOW TO NEW CLASS !!!!
    #         TO DIFFICULT TO GET AND USE THE ATTRIBUTES !
    #         EX :: GETTING THE AREA EASILY
    def drawpad_create(self, count, size, clickable, anim_time, value_dict):
        # the_value_dict
        the_value_dict = value_dict

        # CONSTRUCT DRAWING PAD
        drawpad_size = count
        drawpad_button_size = size

        # POSITIONING OF DRAWPAD BUTTONS
        center_position = [NNGlobals.SCREEN_WIDTH//2,
                           NNGlobals.SCREEN_HEIGHT//2]
        left_top_position = [center_position[0]-(drawpad_button_size*4.5),
                             center_position[1]-(drawpad_button_size*4.5)]

        # TIME ATTRIBUTES
        duration = anim_time
        object_state = 'Fixed'
        xscaler = 0.005
        yscaler = 300

        # CREATING OBJECTS
        # WITH TEXT OBJECTS !
        #
        # BE NOTED !
        # : BELOW'S INDEX IS 'j -> i'
        #
        # BECAUSE WE NEED THIS |
        #                      v
        # ( HORIZONTAL WAY  0 1 2 3 4
        #                   5 6 7 8 9 )
        for j in range(drawpad_size):
            for i in range(drawpad_size):
                obj_id = 'obj' + '_' + str(i) + '_' + str(j)
                text_obj_id = 'txt_' + obj_id

                # BASE POSITION
                position = [left_top_position[0] + (drawpad_button_size * i),
                            left_top_position[1] + (drawpad_button_size * j)]
                # PREPARING the_value
                if len(the_value_dict) is not 0:

                    # CONVERTING LIST TO SET
                    the_value_dict_set = set(list(the_value_dict.keys()))

                    # CHECKING THE EXISTENCE OF MEMBER IN THE LIST
                    # IF OBJECT'S ID IS MATCHED...
                    if obj_id in the_value_dict_set:
                        # the_value SHOULD BE SAME AS LIST
                        self.value_now = the_value_dict[obj_id]
                    else:
                        #print(f'{obj_id}   IS DOES NOT EXISTS !!!')

                        # IF THERE IS NO MATCHES...
                        self.value_now = 0

                else:
                    # IF the_value_list HAS NO LENGTH...
                    self.value_now = 0

                # NODE CREATION
                self.obj_manager.obj_list.append(NNNode.NNNodeObject(self.surface,
                                                                     obj_id,
                                                                     'Rectangle',
                                                                     position,
                                                                     (0, 0),
                                                                     drawpad_button_size,
                                                                     duration,
                                                                     object_state,
                                                                     xscaler,
                                                                     yscaler,
                                                                     clickable,
                                                                     self.value_now
                                                                     ))

                # BUILT-IN TEXT OBJECT CREATION
                text_object_position = [position[0], position[1] - drawpad_button_size]
                self.obj_manager.obj_list.append(NNNode.NNNodeText(self.surface,
                                                                   text_obj_id,
                                                                   'OK',
                                                                   text_object_position,
                                                                   self.textcolor_main,
                                                                   drawpad_button_size,
                                                                   duration,
                                                                   object_state,
                                                                   xscaler,
                                                                   yscaler,
                                                                   False))



    def create_nav_prev_button(self, btn_prev_id, prev_position, prev_size_w, prev_size_h, prev_callback):

        # CREATING BUTTON TO NAVIGATE
        self.obj_manager.obj_list.append(NNNode.NNNodeButton(self.surface,
                                                             prev_callback,
                                                             btn_prev_id,
                                                             'Left_Triangle',
                                                             prev_position,
                                                             (0, 0),
                                                             prev_size_w,
                                                             prev_size_h,
                                                             500,
                                                             'Fixed',
                                                             0.005,
                                                             300,
                                                             True,
                                                             0
                                                             ))



    def create_nav_next_button(self, btn_next_id, next_position, next_size_w, next_size_h, next_callback):

        # CREATING BUTTON TO NAVIGATE
        self.obj_manager.obj_list.append(NNNode.NNNodeButton(self.surface,
                                                             next_callback,
                                                             btn_next_id,
                                                             'Right_Triangle',
                                                             next_position,
                                                             (0, 0),
                                                             next_size_w,
                                                             next_size_h,
                                                             500,
                                                             'Fixed',
                                                             0.005,
                                                             300,
                                                             True,
                                                             0
                                                             ))



    def create_nav_reset_button(self, btn_prev_id, prev_position, prev_size_w, prev_size_h, prev_callback):

        # CREATING BUTTON TO NAVIGATE
        self.obj_manager.obj_list.append(NNNode.NNNodeButton(self.surface,
                                                             prev_callback,
                                                             btn_prev_id,
                                                             'Left_Triangle',
                                                             prev_position,
                                                             (0, 0),
                                                             prev_size_w,
                                                             prev_size_h,
                                                             500,
                                                             'Fixed',
                                                             0.005,
                                                             300,
                                                             True,
                                                             0
                                                             ))

        txt = NNNode.NNNodeText(self.surface,
                                   'text_reset_button',
                                   "最初に戻る",
                                   (150, 50),
                                   (100, 100, 100),
                                   25,
                                   8000,
                                   'Fixed',
                                   0.5,
                                   1.0,
                                   True)

        self.obj_manager.obj_list.append(txt)




    # ----------------------------------------------------------------------
    # IMPORTING AND DISPLAYING DATA FROM NNModel

    def update_nn_data(self, dict_for_input, weight_array):
        """ THIS FUNCTION CREATING AREA TO DISPLAY NN INFORMATION """

        area_w = dict_for_input["areaWidth"]
        area_h = dict_for_input["areaHeight"]
        margin_w = dict_for_input["marginWidth"]
        margin_h = dict_for_input["marginHeight"]
        pos_diff_from_center_x = dict_for_input["posAdjustX"]
        pos_diff_from_center_y = dict_for_input["posAdjustY"]
        weight_color = dict_for_input["Color"]

        # GETTING VALUES FROM NNModel (101 x 128)

        weight_data = weight_array


        # ---------------------------TEST-------------------------

        # area_w = 500
        # area_h = 300
        # margin_w = 10
        # margin_h = 10
        # pos_diff_from_center_x = 0
        # pos_diff_from_center_y = 0
        # weight_color = dict_for_input["Color"]

        #weight_data = np.full((4,10), 0.3)



        # arr1 = np.arange(0.1, 1.1, 0.1)
        #
        # weight_data = []
        # for i in range(4):
        #     weight_data.append(arr1)



        # weight_data = [
        #     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2],
        #     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2],
        #     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2],
        #     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2],
        # ]


        #weight_data = np.array(weight_data).T


        # ---------------------------TEST-------------------------

        # TODO :: NOTE BELOWS !
        # WEIGHTS SHOULD BE TRANSPOSED FOR PROPER 'VISUALIZATION'
        # **** NOT THE 'PROPER CALCULATION'
        weight_data = numpy.array(weight_data).T


        # DRAWING REPRESENTATION OF WEIGHT
        if weight_data is not None and len(weight_data) is not 0:

            # SIZE OF THE AREA WHICH COVERS
            area_width = area_w
            area_height = area_h

            # RETRIEVING COUNTS FROM WEIGHT MATRIX
            count_width = len(weight_data)  # 101

            count_height = 1    # STRATING FROM VALUE 1

            if len(weight_data.shape) > 1:
                count_height = len(weight_data[0])    # 128

            # width = area_width / count_width - margin_w
            # height = area_height / count_height - margin_h

            # TODO :: FIX BELOW FUNCIONALITY
            # FOR NOW, MARGIN VALUE IS OVERWRITED TO 0.0
            width = area_width / count_width - 0
            height = area_height / count_height - 0

            # IF THE VALUE IS UNDER 1.0, KEEP IT THAT TO 1.0
            if width < 1.0:
                width = 1.0

            if height < 1.0:
                height = 1.0


            color = weight_color

            result = {"pos_diff_from_center_x": pos_diff_from_center_x,  # 0
                      "pos_diff_from_center_y": pos_diff_from_center_y,  # 1
                      "countWidth": count_width,  # 2
                      "countHeight": count_height,  # 3
                      "unitWidth": width,  # 4
                      "unitHeight": height,  # 5
                      "marginWidth": margin_w,  # 6
                      "marginHeight": margin_h,  # 7
                      "Color": color,  # 8
                      "ResultValue": weight_data }  # 9

            return result


    # BELOW WILL BE CALLED IN setup() FUNCTION
    def all_nodes_layers_setup(self):

        # UPDATING WEIGHT V
        input_for_weight_v = {"areaWidth": 1600,
                              "areaHeight": 435,
                              "posAdjustX": 0,
                              "posAdjustY": 260,
                              "marginWidth": 5,
                              "marginHeight": 1,
                              "Color": (190, 240, 220)}

        self.input_for_creating_pixels_weight_v = self.update_nn_data(input_for_weight_v, self.nnmodel.weight_V_result)


        # UPDATING HIDDEN 'A' VECTOR
        input_for_hidden_a = {"areaWidth": 2250,
                              "areaHeight": 8,
                              "posAdjustX": 0,
                              "posAdjustY": 35,
                              "marginWidth": 5,
                              "marginHeight": 5,
                              "Color": (160, 220, 240)}

        #self.input_for_creating_pixels_hidden_a = self.update_nn_data(input_for_hidden_a, self.input_for_creating_pixels_weight_v["ResultValue"])
        self.input_for_creating_pixels_hidden_a = self.update_nn_data(input_for_hidden_a, self.nnmodel.weight_v_dot_product(NNGlobals.USER_INPUT))

        # UPDATING HIDDEN 'RELU' FUNCTION
        input_for_hidden_relu = {"areaWidth": 2250,
                                 "areaHeight": 8,
                                 "posAdjustX": 0,
                                 "posAdjustY": 18,
                                 "marginWidth": 5,
                                 "marginHeight": 5,
                                 "Color": (240, 150, 200)}

        self.input_for_creating_pixels_hidden_relu = self.update_nn_data(input_for_hidden_relu, self.nnmodel.hidden_relu(self.input_for_creating_pixels_hidden_a["ResultValue"]))

        # UPDATING HIDDEN 'B' VECTOR
        input_for_hidden_b = {"areaWidth": 2265,
                              "areaHeight": 8,
                              "posAdjustX": -9,
                              "posAdjustY": 0,
                              "marginWidth": 5,
                              "marginHeight": 5,
                              "Color": (140, 240, 120)}

        self.input_for_creating_pixels_hidden_b = self.update_nn_data(input_for_hidden_b, self.nnmodel.insert_dummy_node(self.input_for_creating_pixels_hidden_relu["ResultValue"]))



        # UPDATING WEIGHT W
        input_for_weight_w = {"areaWidth": 600,
                              "areaHeight": 300,
                              "posAdjustX": 0,
                              "posAdjustY": -150,
                              "marginWidth": 4,
                              "marginHeight": 5,
                              "Color": (190, 220, 240)
                              }

        self.input_for_creating_pixels_weight_w = self.update_nn_data(input_for_weight_w, self.nnmodel.weight_W_result)

        # UPDATING OUTPUT 'U' VECTOR
        input_for_output_u = {"areaWidth": 2000,
                              "areaHeight": 8,
                              "posAdjustX": 0,
                              "posAdjustY": -300,
                              "marginWidth": 100,
                              "marginHeight": 5,
                              "Color": (160, 220, 240)}

        self.input_for_creating_pixels_output_u = self.update_nn_data(input_for_output_u, self.nnmodel.weight_w_dot_product(self.input_for_creating_pixels_hidden_b["ResultValue"]))

        # UPDATING OUTPUT 'SOFTMAX' FUNCTION
        input_for_output_softmax = {"areaWidth": 2000,
                                    "areaHeight": 8,
                                    "posAdjustX": 0,
                                    "posAdjustY": -320,
                                    "marginWidth": 100,
                                    "marginHeight": 5,
                                    "Color": (240, 150, 200)}

        self.input_for_creating_pixels_softmax = self.update_nn_data(input_for_output_softmax, self.nnmodel.get_output_with_softmax(self.input_for_creating_pixels_output_u["ResultValue"]))


        """
        # # UPDATING OUTPUT RESULT VECTOR
        # input_for_output_yp = {"areaWidth": 2500,
        #                        "areaHeight": 250,
        #                        "posAdjustX": 0,
        #                        "posAdjustY": -210,
        #                        "marginWidth": 25,
        #                        "marginHeight": 5,
        #                        "Color": (190, 240, 220),
        #                        "InputValue": self.input_for_render_output_softmax["ResultValue"]}
        #
        # self.input_for_render_output_yp = self.update_output_softmax(input_for_output_yp)

        """

        # UPDATING WEIGHT V NEWLY-TRAINED
        input_for_weight_v_newtrain = {"areaWidth": 1600,
                                      "areaHeight": 435,
                                      "posAdjustX": 0,
                                      "posAdjustY": 260,
                                      "marginWidth": 5,
                                      "marginHeight": 1,
                                      "Color": (210, 190, 180)}

        # THERE IS THE CASE self.weight_v_new_train DOES NOT HAVE THE INFORMATION
        # BUT self.weight_v_new_train WILL BE FILLED WHEN THE TRAINING PHASE IS STARTED
        if self.weight_v_new_train is not None:
            self.input_for_creating_pixels_weight_v_newtrain = self.update_nn_data(input_for_weight_v_newtrain, self.weight_v_new_train)


        # UPDATING WEIGHT W NEWLY-TRAINED
        input_for_weight_w_newtrain = {"areaWidth": 600,
                              "areaHeight": 300,
                              "posAdjustX": 0,
                              "posAdjustY": -150,
                              "marginWidth": 4,
                              "marginHeight": 5,
                              "Color": (220, 140, 110)
                              }

        if self.weight_w_new_train is not None:
            self.input_for_creating_pixels_weight_w_newtrain = self.update_nn_data(input_for_weight_w_newtrain, self.weight_w_new_train)


    def weights_new_train_update(self):

        # UPDATING WEIGHT V
        input_for_weight_v_newtrain = {"areaWidth": 1600,
                                      "areaHeight": 435,
                                      "posAdjustX": 0,
                                      "posAdjustY": 260,
                                      "marginWidth": 5,
                                      "marginHeight": 1,
                                      "Color": (210, 190, 180)}

        if self.weight_v_new_train is not None:
            self.input_for_creating_pixels_weight_v_newtrain = self.update_nn_data(input_for_weight_v_newtrain, self.weight_v_new_train)


        # UPDATING WEIGHT W
        input_for_weight_w_newtrain = {"areaWidth": 600,
                              "areaHeight": 300,
                              "posAdjustX": 0,
                              "posAdjustY": -150,
                              "marginWidth": 4,
                              "marginHeight": 5,
                              "Color": (220, 140, 110)
                              }

        if self.weight_w_new_train is not None:
            self.input_for_creating_pixels_weight_w_newtrain = self.update_nn_data(input_for_weight_w_newtrain, self.weight_w_new_train)


        # UPDATING PIXEL ARRAY
        if self.weight_v_new_train is not None and self.weight_w_new_train is not None:
            self.nodes_layers_create_pixelarray("Weight_v_newtrain")
            self.nodes_layers_create_pixelarray("Weight_w_newtrain")



    # ----------------------------------------------------------------------


    def all_nodes_layers_create_pixelarray(self):

        if NNGlobals.NN_NOT_INITIALIZED is True:

            # GETTING PIXEL ARRAY FROM NNPixel OBJECT

            if self.input_for_creating_pixels_weight_v_newtrain is None or \
                    self.input_for_creating_pixels_weight_w_newtrain is None:

                dict_for_pixel_array = {
                    "screen_width": NNGlobals.SCREEN_WIDTH,
                    "screen_height": NNGlobals.SCREEN_HEIGHT,
                    "weight_v": self.input_for_creating_pixels_weight_v,
                    "weight_w": self.input_for_creating_pixels_weight_w,
                    "hidden_a": self.input_for_creating_pixels_hidden_a,
                    "hidden_relu": self.input_for_creating_pixels_hidden_relu,
                    "hidden_b": self.input_for_creating_pixels_hidden_b,
                    "output_u": self.input_for_creating_pixels_output_u,
                    "softmax": self.input_for_creating_pixels_softmax,
                }
            else:
                dict_for_pixel_array = {
                    "screen_width": NNGlobals.SCREEN_WIDTH,
                    "screen_height": NNGlobals.SCREEN_HEIGHT,
                    "weight_v": self.input_for_creating_pixels_weight_v,
                    "weight_w": self.input_for_creating_pixels_weight_w,
                    "hidden_a": self.input_for_creating_pixels_hidden_a,
                    "hidden_relu": self.input_for_creating_pixels_hidden_relu,
                    "hidden_b": self.input_for_creating_pixels_hidden_b,
                    "output_u": self.input_for_creating_pixels_output_u,
                    "softmax": self.input_for_creating_pixels_softmax,
                    "weight_v_newtrain": self.input_for_creating_pixels_weight_v_newtrain,
                    "weight_w_newtrain": self.input_for_creating_pixels_weight_w_newtrain,
                }




            # TODO :: ARCHIVE BELOW !
            #
            # < Python multiprocessing tutorial >
            # http://zetcode.com/python/multiprocessing/
            #
            # : Concurrency means that two or more calculations happen within the same time frame.
            # Parallelism means that two or more calculations happen at the same moment.
            # Parallelism is therefore a specific case of concurrency. It requires multiple CPU
            # units or cores.
            #
            # True parallelism in Python is achieved by creating multiple processes, each having
            # a Python interpreter with its own separate GIL.
            #


            # CREATING NNPixelarray OBJECT AND PROCESS THE ARRAY

            # TODO :: PROFILING
            # TODO :: ARCHIVE THIS !
            #starttime = time.time()
            #print(f"PROFILING... STARTED ...")


            nnpixelarray = NNPixelArray.NNPixelArray(dict_for_pixel_array)
            nnpixelarray.all_nodes_layers_create_pixelarray_threads()


            #endtime = time.time()
            #print(f"         ... ENDED : ELAPSED --> {endtime - starttime}")



            # CONNECT THE RESULT FROM NNPixelarray OBJECT TO THIS OBJECT
            NNGlobals.START_POS_WEIGHT_V = nnpixelarray.start_pos_weight_v
            NNGlobals.START_POS_WEIGHT_W = nnpixelarray.start_pos_weight_w
            NNGlobals.START_POS_HIDDEN_A = nnpixelarray.start_pos_hidden_a
            NNGlobals.START_POS_HIDDEN_RELU = nnpixelarray.start_pos_hidden_relu
            NNGlobals.START_POS_HIDDEN_B = nnpixelarray.start_pos_hidden_b
            NNGlobals.START_POS_OUTPUT_U = nnpixelarray.start_pos_output_u
            NNGlobals.START_POS_SOFTMAX = nnpixelarray.start_pos_softmax

            NNGlobals.START_POS_WEIGHT_V_NEWTRAIN = nnpixelarray.start_pos_weight_v_newtrain
            NNGlobals.START_POS_WEIGHT_W_NEWTRAIN = nnpixelarray.start_pos_weight_w_newtrain


            # FOR PIXEL ARRAYS
            NNGlobals.PIXEL_ARRAY_WEIGHT_V = nnpixelarray.pixel_array_weight_v
            NNGlobals.PIXEL_ARRAY_WEIGHT_W = nnpixelarray.pixel_array_weight_w
            NNGlobals.PIXEL_ARRAY_HIDDEN_A = nnpixelarray.pixel_array_hidden_a
            NNGlobals.PIXEL_ARRAY_HIDDEN_RELU = nnpixelarray.pixel_array_hidden_relu
            NNGlobals.PIXEL_ARRAY_HIDDEN_B = nnpixelarray.pixel_array_hidden_b
            NNGlobals.PIXEL_ARRAY_OUTPUT_U = nnpixelarray.pixel_array_output_u
            NNGlobals.PIXEL_ARRAY_SOFTMAX = nnpixelarray.pixel_array_softmax

            NNGlobals.PIXEL_ARRAY_WEIGHT_V_NEWTRAIN = nnpixelarray.pixel_array_weight_v_newtrain
            NNGlobals.PIXEL_ARRAY_WEIGHT_W_NEWTRAIN = nnpixelarray.pixel_array_weight_w_newtrain



            # CREATING SURFACE USING surfarray CLASS OF PYGAME

            NNGlobals.SURFACE_WEIGHT_V = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_V)
            NNGlobals.SURFACE_WEIGHT_V.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_WEIGHT_W = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_W)
            NNGlobals.SURFACE_WEIGHT_W.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_HIDDEN_A = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_HIDDEN_A)
            NNGlobals.SURFACE_HIDDEN_A.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_HIDDEN_RELU = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_HIDDEN_RELU)
            NNGlobals.SURFACE_HIDDEN_RELU.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_HIDDEN_B = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_HIDDEN_B)
            NNGlobals.SURFACE_HIDDEN_B.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_OUTPUT_U = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_OUTPUT_U)
            NNGlobals.SURFACE_OUTPUT_U.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_SOFTMAX = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_SOFTMAX)
            NNGlobals.SURFACE_SOFTMAX.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_WEIGHT_V_NEWTRAIN = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_V_NEWTRAIN)
            NNGlobals.SURFACE_WEIGHT_V_NEWTRAIN.set_colorkey((0, 0, 0))

            NNGlobals.SURFACE_WEIGHT_W_NEWTRAIN = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_W_NEWTRAIN)
            NNGlobals.SURFACE_WEIGHT_W_NEWTRAIN.set_colorkey((0, 0, 0))

            # CLOSE GATE
            NNGlobals.NN_NOT_INITIALIZED = False



    def nodes_layers_create_pixelarray(self, category):

        # GETTING PIXEL ARRAY FROM NNPixel OBJECT

        if self.input_for_creating_pixels_weight_v_newtrain is None or \
                self.input_for_creating_pixels_weight_w_newtrain is None:

            dict_for_pixel_array = {
                "screen_width": NNGlobals.SCREEN_WIDTH,
                "screen_height": NNGlobals.SCREEN_HEIGHT,
                "weight_v": self.input_for_creating_pixels_weight_v,
                "weight_w": self.input_for_creating_pixels_weight_w,
                "hidden_a": self.input_for_creating_pixels_hidden_a,
                "hidden_relu": self.input_for_creating_pixels_hidden_relu,
                "hidden_b": self.input_for_creating_pixels_hidden_b,
                "output_u": self.input_for_creating_pixels_output_u,
                "softmax": self.input_for_creating_pixels_softmax,
            }
        else:
            dict_for_pixel_array = {
                "screen_width": NNGlobals.SCREEN_WIDTH,
                "screen_height": NNGlobals.SCREEN_HEIGHT,
                "weight_v": self.input_for_creating_pixels_weight_v,
                "weight_w": self.input_for_creating_pixels_weight_w,
                "hidden_a": self.input_for_creating_pixels_hidden_a,
                "hidden_relu": self.input_for_creating_pixels_hidden_relu,
                "hidden_b": self.input_for_creating_pixels_hidden_b,
                "output_u": self.input_for_creating_pixels_output_u,
                "softmax": self.input_for_creating_pixels_softmax,
                "weight_v_newtrain": self.input_for_creating_pixels_weight_v_newtrain,
                "weight_w_newtrain": self.input_for_creating_pixels_weight_w_newtrain,
            }


        nnpixelarray = NNPixelArray.NNPixelArray(dict_for_pixel_array)


        if category == "Weight_V":
            if NNGlobals.NN_WEIGHT_V_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Weight_V")


                # BELOW WHICH IS COMMENTED OUT IS THE PROCESS OF PROFILING

                # pr = cProfile.Profile()
                # pr.enable()

                nnpixelarray.nodes_layers_create_pixelarray("Weight_V")

                # pr.disable()
                # s = io.StringIO()
                # sortby = 'cumulative'
                # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                # ps.print_stats()
                # print(s.getvalue())

                NNGlobals.START_POS_WEIGHT_V = nnpixelarray.start_pos_weight_v
                NNGlobals.PIXEL_ARRAY_WEIGHT_V = nnpixelarray.pixel_array_weight_v
                NNGlobals.SURFACE_WEIGHT_V = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_V)
                NNGlobals.SURFACE_WEIGHT_V.set_colorkey((0, 0, 0))
                NNGlobals.NN_WEIGHT_V_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Weight_V")
                pass

        elif category == "Hidden_A":
            if NNGlobals.NN_HIDDEN_A_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Hidden_A")
                nnpixelarray.nodes_layers_create_pixelarray("Hidden_A")
                NNGlobals.START_POS_HIDDEN_A = nnpixelarray.start_pos_hidden_a
                NNGlobals.PIXEL_ARRAY_HIDDEN_A = nnpixelarray.pixel_array_hidden_a
                NNGlobals.SURFACE_HIDDEN_A = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_HIDDEN_A)
                NNGlobals.SURFACE_HIDDEN_A.set_colorkey((0, 0, 0))
                #NNGlobals.NN_HIDDEN_A_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Hidden_A")
                pass
        elif category == "Hidden_Relu":
            if NNGlobals.NN_HIDDEN_RELU_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Hidden_Relu")
                nnpixelarray.nodes_layers_create_pixelarray("Hidden_Relu")
                NNGlobals.START_POS_HIDDEN_RELU = nnpixelarray.start_pos_hidden_relu
                NNGlobals.PIXEL_ARRAY_HIDDEN_RELU = nnpixelarray.pixel_array_hidden_relu
                NNGlobals.SURFACE_HIDDEN_RELU = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_HIDDEN_RELU)
                NNGlobals.SURFACE_HIDDEN_RELU.set_colorkey((0, 0, 0))
                #NNGlobals.NN_HIDDEN_RELU_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Hidden_Relu")
                pass

        elif category == "Hidden_B":
            if NNGlobals.NN_HIDDEN_B_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Hidden_B")
                nnpixelarray.nodes_layers_create_pixelarray("Hidden_B")
                NNGlobals.START_POS_HIDDEN_B = nnpixelarray.start_pos_hidden_b
                NNGlobals.PIXEL_ARRAY_HIDDEN_B = nnpixelarray.pixel_array_hidden_b
                NNGlobals.SURFACE_HIDDEN_B = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_HIDDEN_B)
                NNGlobals.SURFACE_HIDDEN_B.set_colorkey((0, 0, 0))
                #NNGlobals.NN_HIDDEN_B_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Hidden_B")
                pass

        elif category == "Weight_W":
            if NNGlobals.NN_WEIGHT_W_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Weight_W")
                nnpixelarray.nodes_layers_create_pixelarray("Weight_W")
                NNGlobals.START_POS_WEIGHT_W = nnpixelarray.start_pos_weight_w
                NNGlobals.PIXEL_ARRAY_WEIGHT_W = nnpixelarray.pixel_array_weight_w
                NNGlobals.SURFACE_WEIGHT_W = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_W)
                NNGlobals.SURFACE_WEIGHT_W.set_colorkey((0, 0, 0))
                NNGlobals.NN_WEIGHT_W_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Weight_W")
                pass

        elif category == "Output_U":
            if NNGlobals.NN_OUTPUT_U_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Output_U")
                nnpixelarray.nodes_layers_create_pixelarray("Output_U")
                NNGlobals.START_POS_OUTPUT_U = nnpixelarray.start_pos_output_u
                NNGlobals.PIXEL_ARRAY_OUTPUT_U = nnpixelarray.pixel_array_output_u
                NNGlobals.SURFACE_OUTPUT_U = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_OUTPUT_U)
                NNGlobals.SURFACE_OUTPUT_U.set_colorkey((0, 0, 0))
                #NNGlobals.NN_OUTPUT_U_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Output_U")
                pass

        elif category == "Softmax":
            if NNGlobals.NN_SOFTMAX_NOT_INITIALIZED is True:
                #####print("--=--   CREATING PIXEL ARRAY -- Softmax")
                nnpixelarray.nodes_layers_create_pixelarray("Softmax")
                NNGlobals.START_POS_SOFTMAX = nnpixelarray.start_pos_softmax
                NNGlobals.PIXEL_ARRAY_SOFTMAX = nnpixelarray.pixel_array_softmax
                NNGlobals.SURFACE_SOFTMAX = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_SOFTMAX)
                NNGlobals.SURFACE_SOFTMAX.set_colorkey((0, 0, 0))
                #NNGlobals.NN_SOFTMAX_NOT_INITIALIZED = False
            else:
                #####print("--=--   NO NEED TO CREATE PIXEL ARRAY -- Softmax")
                pass
        elif category == "Weight_v_newtrain":

            #####print("--=--   CREATING PIXEL ARRAY -- Weight_v_newtrain")
            nnpixelarray.nodes_layers_create_pixelarray("Weight_v_newtrain")
            NNGlobals.START_POS_WEIGHT_V_NEWTRAIN = nnpixelarray.start_pos_weight_v_newtrain
            NNGlobals.PIXEL_ARRAY_WEIGHT_V_NEWTRAIN = nnpixelarray.pixel_array_weight_v_newtrain
            NNGlobals.SURFACE_WEIGHT_V_NEWTRAIN = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_V_NEWTRAIN)
            NNGlobals.SURFACE_WEIGHT_V_NEWTRAIN.set_colorkey((0, 0, 0))


        elif category == "Weight_w_newtrain":

            #####print("--=--   CREATING PIXEL ARRAY -- Weight_w_newtrain")
            nnpixelarray.nodes_layers_create_pixelarray("Weight_w_newtrain")
            NNGlobals.START_POS_WEIGHT_W_NEWTRAIN = nnpixelarray.start_pos_weight_w_newtrain
            NNGlobals.PIXEL_ARRAY_WEIGHT_W_NEWTRAIN = nnpixelarray.pixel_array_weight_w_newtrain
            NNGlobals.SURFACE_WEIGHT_W_NEWTRAIN = pygame.surfarray.make_surface(NNGlobals.PIXEL_ARRAY_WEIGHT_W_NEWTRAIN)
            NNGlobals.SURFACE_WEIGHT_W_NEWTRAIN.set_colorkey((0, 0, 0))





    # ----------------------------------------------------------------------
    # RENDERING NN DATA


    # BELOW WILL BE CALLED IN render() FUNCTION
    def all_nodes_layers_render(self):
        self.surface.blit(NNGlobals.SURFACE_WEIGHT_V, NNGlobals.START_POS_WEIGHT_V)
        self.surface.blit(NNGlobals.SURFACE_HIDDEN_A, NNGlobals.START_POS_HIDDEN_A)
        self.surface.blit(NNGlobals.SURFACE_HIDDEN_RELU, NNGlobals.START_POS_HIDDEN_RELU)
        self.surface.blit(NNGlobals.SURFACE_HIDDEN_B, NNGlobals.START_POS_HIDDEN_B)
        self.surface.blit(NNGlobals.SURFACE_WEIGHT_W, NNGlobals.START_POS_WEIGHT_W)
        self.surface.blit(NNGlobals.SURFACE_OUTPUT_U, NNGlobals.START_POS_OUTPUT_U)
        self.surface.blit(NNGlobals.SURFACE_SOFTMAX, NNGlobals.START_POS_SOFTMAX)

        self.surface.blit(NNGlobals.SURFACE_WEIGHT_V_NEWTRAIN, NNGlobals.START_POS_WEIGHT_V_NEWTRAIN)
        self.surface.blit(NNGlobals.SURFACE_WEIGHT_W_NEWTRAIN, NNGlobals.START_POS_WEIGHT_W_NEWTRAIN)

        # self.render_output_yp(self.input_for_render_output_yp)



    # BELOW WILL BE CALLED IN render() FUNCTION
    def nodes_layers_render(self, category):
        if category == "Weight_V":
            self.surface.blit(NNGlobals.SURFACE_WEIGHT_V, NNGlobals.START_POS_WEIGHT_V)
        elif category == "Hidden_A":
            self.surface.blit(NNGlobals.SURFACE_HIDDEN_A, NNGlobals.START_POS_HIDDEN_A)
        elif category == "Hidden_Relu":
            self.surface.blit(NNGlobals.SURFACE_HIDDEN_RELU, NNGlobals.START_POS_HIDDEN_RELU)
        elif category == "Hidden_B":
            self.surface.blit(NNGlobals.SURFACE_HIDDEN_B, NNGlobals.START_POS_HIDDEN_B)
        elif category == "Weight_W":
            self.surface.blit(NNGlobals.SURFACE_WEIGHT_W, NNGlobals.START_POS_WEIGHT_W)
        elif category == "Output_U":
            self.surface.blit(NNGlobals.SURFACE_OUTPUT_U, NNGlobals.START_POS_OUTPUT_U)
        elif category == "Softmax":
            self.surface.blit(NNGlobals.SURFACE_SOFTMAX, NNGlobals.START_POS_SOFTMAX)
        elif category == "Weight_v_newtrain":

            if self.weight_v_new_train is not None and self.input_for_creating_pixels_weight_v_newtrain is not None:
                self.surface.blit(NNGlobals.SURFACE_WEIGHT_V_NEWTRAIN, NNGlobals.START_POS_WEIGHT_V_NEWTRAIN)
                #print("WE RENDERED -- WEIGHT_V_NEWTRAIN")
            else:
                #####print("COULD NOT RENDER -- WEIGHT_V_NEWTRAIN")
                pass

        elif category == "Weight_w_newtrain":

            if self.weight_w_new_train is not None and self.input_for_creating_pixels_weight_w_newtrain is not None:
                self.surface.blit(NNGlobals.SURFACE_WEIGHT_W_NEWTRAIN, NNGlobals.START_POS_WEIGHT_W_NEWTRAIN)
                #print("WE RENDERED -- WEIGHT_W_NEWTRAIN")
            else:
                #####print("COULD NOT RENDER -- WEIGHT_W_NEWTRAIN")
                pass


        # self.render_output_yp(self.input_for_render_output_yp)





    # ----------------------------------------------------------------------
    # UTILITY FUNCTIONS



    def exchange_value_dict(self):

        # EXCHANGE VALUES BETWEEN TWO DICTIONARY EACH OTHER FOR the_value_dict
        if len(self.obj_manager.the_value_dict) != 0 and \
                len(self.the_value_dict) == 0:
            self.the_value_dict = self.obj_manager.the_value_dict

        if len(self.the_value_dict) != 0 and \
                len(self.obj_manager.the_value_dict) == 0:
            self.obj_manager.the_value_dict = self.the_value_dict





    # < COLOR CONVERSION >
    # https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))



    def check_obj_lists(self, list_a, list_b):
        resultObject = []

        for elm_a in list_a:
            for elm_b in list_b:
                # IF THE ID IS SAME, STORE IT
                if elm_a.obj_id == elm_b.obj_id:
                    resultObject.append(elm_a)

        return resultObject


    def realign_value_list(self, list):
        #####print(list.shape)
        pass


    def convert_scene_num_to_index(self, scene_num):
        if 1 <= scene_num:
            return scene_num * 2



    def set_text_visible_with_value(self):
        # SETTING TYPE OBJECTS
        for obj in self.obj_manager.obj_list:
            if type(obj) is NNNode.NNNodeText:

                # THERE ARE TWO TYPES OF STRINGS IN THIS PROGRAM,
                # (TEXT TO DISPLAY THE WEIGHT) and (TEXT FOR EXPLAINING SOMETHING)
                # SO WE NEED TO FILTER ONE
                trimmed_id = obj.obj_id[:4]
                if trimmed_id == "txt_":

                    # GETTING TYPE OBJECT WITH ID(STRING DATA)
                    obj_id = obj.obj_id
                    obj_id = obj_id[4:]

                    # < SETTING THE TEXT FROM ITS OWN 'the_value' (SIZE AND COLOR EITHER) >
                    #

                    # THE FLOAT VALUE WE CALCULATED IS INVERTED BETWEEN 0.0 - 1.0
                    value = abs(1.0 - self.the_value_dict[obj_id] / 255)

                    # < FORMATTING FLOAT VALUE TO 1 LETTER >
                    # https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
                    #
                    value = "{:.1f}".format(value)

                    obj.set_style(value, int(obj.text_size / 2.5), obj.color)
                    # VISIBILITY ON
                    obj.visible = True


    def set_value_dict(self, the_value_dict):
        # SETTING the_value DICTIONARY
        if len(the_value_dict) is not 0:
            self.the_value_dict = the_value_dict


    def set_non_clickable(self):
        for obj in self.obj_manager.obj_list:
            obj.clickable = False


    def disable_update(self):
        self.can_update = False


    def clear_objects(self):

        if len(self.obj_manager.obj_list) is not 0:
            del self.obj_manager.obj_list[:]


    def clear_value_dict(self):
        if len(self.the_value_dict) is not 0:
            self.the_value_dict.clear()


    def set_the_value_dict(self, dict):
        self.the_value_dict = dict



    def reload_scene(self):
        self.disable_update()
        self.clear_objects()




    def addToClipBoard(self, text):
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)




    # Function to convert
    def list_to_string(self, s):
        # initialize an empty string
        str1 = ""

        # traverse in the string
        for ele in s:
            str1 += str(ele) + " "

            # return string
        return str1


# ----------------------------------------------








# ----------------------------------------------
# BELOW SCENE IS SPECIAL BECAUSE IT HAS THE SELF-TIMER
class NNScene_Junction(NNScene):
    def __init__(self, surface, pre_state_id, post_state_id, duration, the_value_dict):
        super().__init__(surface)

        self.stateID = pre_state_id + '-' + post_state_id

        self.scene_number = -1

        self.the_value_dict = the_value_dict

        self.duration = duration

        #frameinfo = getframeinfo(currentframe())
        #print(f"{frameinfo.filename} -- {frameinfo.lineno}  NNScene_Junction::__init__() -- stateID --  {self.stateID}")

        # SETTING UP OBJECT LIST
        self.pre_state_objs = []
        self.post_state_objs = []

        #self.setup_objects(pre_state_objs, post_state_objs)

        self.differ_position = []
        self.differ_position_dict = {}


        self.timer = None
        self.now_time = 0
        self.last_time = 0


        # SETTING UP FLAG FOR COMPLETION
        self.complete = False

        # BELOW IS FOR TRANSITION
        self.changing_color = (0, 0, 0)
        self.transition_count = 48
        self.transition_count_index = 0
        self.rect_size = NNGlobals.SCREEN_WIDTH // self.transition_count


    def setup_objects(self, pre_objects, post_objects):
        # < MANAGE OBJECTS >
        # GETTING TWO SCENES
        self.pre_state_objs = pre_objects
        self.post_state_objs = post_objects

        # INITIALIZE OBJECT LIST
        # GATHERING OBJECTS FOR THIS OBJECT
        self.obj_manager.obj_list = self.check_obj_lists(self.pre_state_objs, self.post_state_objs)



    def setup_duration(self):
        # SETTING DURATION
        # TODO :: CHANGE BELOW TO RELATIVE VALUE BASED ON THE DISTANCE?
        #                                                      v- THIS IS CONSTANT NOW
        self.set_duration_to_objs(self.obj_manager.obj_list, self.duration)


    def setup(self, the_value_dict, duration):

        # print(self.obj_manager.obj_list)
        assert len(self.obj_manager.obj_list) != 0, "######## ERROR ------ THERE IS NO MATCHED OBJECTS ------- NO JUNCTION STATE"

        self.the_value_dict = the_value_dict

        # DETERMINE THE DIFFERENCES OF POSITION BETWEEN TWO OBJECTS

        self.differ_position_dict = self.calculate_position_diff_dict(self.pre_state_objs, self.post_state_objs)
        # print(self.differ_position)


        # SETUP OBJECTS TO NON-CLICKABLE
        self.set_non_clickable()




    def update(self, elapsed_time):
        # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() -- self.scene_number IS   {self.scene_number}")
        # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() -- elapsed_time IS   {elapsed_time}")
        # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() -- NNGlobals.SCENE_INDEX IS   {NNGlobals.SCENE_INDEX}")
        # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() -- self.can_update IS   {self.can_update}")
        # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() -- self.duration IS   {self.duration}")



        # IF THE FLAG FOR UPDATING IS ON...
        if self.can_update is True:

            super().update(elapsed_time)

            # STORING the_value
            self.the_value_dict = self.obj_manager.the_value_dict
            #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() --                self.the_value_dict                   ***** {self.the_value_dict} *****')


            # COLORING
            for obj in self.obj_manager.obj_list:
                if type(obj) is not NNNode.NNNodeText and \
                        type(obj) is not NNNode.NNNodeMultiText and \
                        type(obj) is not NNNode.NNNodeButton and \
                        type(obj) is not NNNode.NNNodeLine and \
                        type(obj) is not NNNode.NNNodeIndicator:

                    obj.set_color_with_the_value(self.the_value_dict[obj.obj_id])


            # STORING ELAPSED TIME TO NOW TIME
            self.now_time = elapsed_time

            # CALCULATING THE FRAGMENT BETWEEN NOW AND LAST
            milli_per_tick = self.now_time - self.last_time

            #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_Junction::update() --                                            ***** {self.timer.get_result()} *****')

            # UPDATE THE OBJECTS
            # FOR LOOP USING INDEX

            for obj in self.obj_manager.obj_list:
                if type(obj) is not NNNode.NNNodeText and type(obj) is not NNNode.NNNodeMultiText:

                    # INTERPOLATE TWO POSITION TO TARGET POSITION
                    obj.position = [obj.position[0] + self.differ_position_dict[obj.obj_id][0] / self.duration * milli_per_tick,
                                    obj.position[1] + self.differ_position_dict[obj.obj_id][1] / self.duration * milli_per_tick]


            # COUNT CHANGING FOR TRANSITION
            self.transition_count_index = int(elapsed_time / self.duration * 100) // (100 // self.transition_count) + 1


            # STORING PASSED TIMING
            self.last_time = self.now_time





    def render(self):

        # SCENE BG
        #self.surface.fill(self.hsv2rgb(NNGlobals.SCENE_INDEX / self.count_scenes, 0.2, 0.8))


        # ---------------------------------------------------------------------------------

        super().render()

        # ---------------------------------------------------------------------------------
        # DISPLAYING TRANSITIONS
        tr_color_int = self.hsv2rgb(NNGlobals.SCENE_INDEX / self.count_scenes, 0.2, 0.8)

        normalized_count = self.transition_count_index / self.transition_count

        sine_value = math.sin(3.14 * normalized_count)
        if sine_value >= 1:
            sine_value = 1.0
        elif sine_value <= 0:
            sine_value = 0.0

        if NNGlobals.SCENE_INDEX >= 2:

            for i in range(self.transition_count_index):

                transition_val = i / self.transition_count + sine_value
                value_r = tr_color_int[0] + int(transition_val * 100) - 80
                value_g = tr_color_int[1] + int(transition_val * 100) - 80
                value_b = tr_color_int[2] + int(transition_val * 100) - 80

                if value_r > 255:
                    value_r = 255
                elif value_r <= 0:
                    value_r = 0

                if value_g > 255:
                    value_g = 255
                elif value_g <= 0:
                    value_g = 0

                if value_b > 255:
                    value_b = 255
                elif value_b <= 0:
                    value_b = 0

                pygame.draw.rect(self.surface,
                                 (value_r, value_g, value_b),
                                 (0 + i*self.rect_size, 0, self.rect_size, NNGlobals.SCREEN_WIDTH))




    def on_exit(self):
        # TODO :: BELOW IS CRITICAL
        # RESETTING last_time WHICH WE USED FOR STORING PAST TIME
        self.last_time = 0

        super().on_exit()



    def calculate_position_diff_dict(self, obj_list_a, obj_list_b):
        result_dict = {}
        for obj_a in obj_list_a:
            for obj_b in obj_list_b:
                # IF THE ID IS SAME, CALCULATE THE DIFFERENCES OF POSITION
                if obj_a.obj_id == obj_b.obj_id:
                    diff = [obj_b.position[0] - obj_a.position[0],
                            obj_b.position[1] - obj_a.position[1]]

                    result_dict[obj_a.obj_id] = diff

        return result_dict





    def calculate_position_diff(self, list_a, list_b):
        resultDistance = []

        # CHECK IF THE OBJECTS IN THE LIST HAVE THE SAME OBJECT ID,
        for elm_a in list_a:
            for elm_b in list_b:
                # IF THE ID IS SAME, CALCULATE THE DIFFERENCES OF POSITION
                if elm_a.obj_id == elm_b.obj_id:
                    diff = [elm_b.position[0] - elm_a.position[0],
                            elm_b.position[1] - elm_a.position[1]]

                    # TODO :: BELOW IS FOR TEST
                    #pygame.draw.line(self.surface, (0, 0, 255), elm_b.position, elm_a.position, 6)

                    resultDistance.append(diff)

        return resultDistance





    def set_duration_to_objs(self, objs, duration):
        for obj in objs:
            obj.anim.duration = duration



    def setup_timer(self):
        # CREATE TIMER FOR THIS OBJECT
        self.timer = Timer.Timer([self.duration])
        self.now_time = self.timer.time_elapsed
        self.last_time = self.timer.time_elapsed

