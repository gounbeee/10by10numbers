#print('------------------ TenByTenNumbers_main MODULE ENTERED')
import pygame
import Timer
import os
import colorsys
import Statemachine
import NNSceneData
import NNScene
from NNGlobals import *
import NNXmlConnector
import copy




# GETTING CURRENT FILE NAME AND LINE NUMBER
# https://qastack.jp/programming/3056048/filename-and-line-number-of-python-script
#
# < EXAMPLE >
# from inspect import currentframe, getframeinfo
#
# frameinfo = getframeinfo(currentframe())
# print(frameinfo.filename, frameinfo.lineno)
#
from inspect import currentframe, getframeinfo, stack



class TenByTenNumbers_main(object):



    # ---------------------------------------------------------------------------------------

    def __init__(self):

        # GLOBAL EDITOR MODE
        self.editor_mode = False


        self.scenario_and_functions = {
            "FIRST_SCENE": [self.main_timer_flows,
                            self.check_disabling_scene,
                            self.jump_to_next_scene,
                            self.update_statemachine,
                            self.render_statemachine,
                            ],

            "STARTED_JUNCTIONING": [self.main_timer_flows,
                                    self.check_disabling_scene,
                                    self.jump_to_next_scene,
                                    self.update_statemachine,
                                    self.render_statemachine,
                                    ],

            "NORMAL_EXECUTION": [self.main_timer_flows,
                                    self.check_disabling_scene,
                                    self.jump_to_next_scene,
                                    self.update_statemachine,
                                    self.render_statemachine,
                                    ],

            "CONNECT_TO_NORMAL": [self.main_timer_flows,
                                   self.check_disabling_scene,
                                   self.jump_to_next_scene,
                                   self.update_statemachine,
                                   self.render_statemachine,
                                   ],
            "CONNECT_TO_JUNCTION": [self.main_timer_flows,
                                   self.check_disabling_scene,
                                   self.jump_to_next_scene,
                                   self.update_statemachine,
                                   self.render_statemachine,
                                   ],
            "LAST_SCENE": [self.main_timer_flows,
                           self.check_disabling_scene,
                           self.jump_to_next_scene,
                           self.update_statemachine,
                           self.render_statemachine,
                           ],
            "BACK_TO_FIRST": [self.main_timer_flows,
                              self.check_disabling_scene,
                              self.jump_to_next_scene,
                              self.update_statemachine,
                              self.render_statemachine,
                              ],
        }

        self.current_main_scenario = " "



        #####print(f'TenByTenNumbers_main -- init() --  {getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno}')
        #####print(f'PARENT PID --   {os.getppid()}')
        #####print(f'PID --   {os.getpid()}')

        self.mainloop = True

        self.screen = None
        self.scenes = []
        self.final_scenes = []
        self.final_durations = []
        self.final_durations_backup = []

        #self.p_receive_sub_to_main = p_receive_sub_to_main
        #self.p_send_main_to_sub = p_send_main_to_sub


        self.msg_from_sub = ' '

        # RECEIVING MESSAGE WILL CONTINUE BUT PROCESS WILL BE GATED
        self.flag_ipc = False


        self.setup()
        self.run()



    def setup(self):
        # =======================================================================================
        # < PYGAME >

        #####print(f'TenByTenNumbers_main -- run() --  {getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno}')
        #####print(f'PARENT PID --   {os.getppid()}')
        #####print(f'PID --   {os.getpid()}')


        # SCREEN SIZE
        screen_width = NNGlobals.SCREEN_WIDTH
        screen_height = NNGlobals.SCREEN_HEIGHT


        # POSITIONING SDL(PYGAME) WINDOW
        # https://stackoverflow.com/questions/4135928/pygame-display-position
        x = 0
        y = 30
        #y = 100
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


        # PYGAME ENGINE INITIALIZATION
        pygame.init()
        pygame.display.set_caption('10 by 10 NUMBER(S) by sy')

        # SCREEN INITIALIZING
        #flags = pygame.DOUBLEBUF
        #self.screen = pygame.display.set_mode([screen_width, screen_height], flags, vsync=1)

        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((screen_width, screen_height), flags, vsync=1)


        # -----------------------------------------------------------
        # < SCENE CREATION WITH XML >

        # XML CONNECTOR
        xmlconnector = NNXmlConnector.NNXmlConnector('xml_scenes/scenes_xml.xml', self.screen)

        # GETTING SCENE ELEMENT WITH SCENE NUMBER
        all_scenes_layer = xmlconnector.get_all_scene_layer()

        self.scenes = []
        timeline_scenes = []


        # < SCENE CREATION >
        # < RETRIEVING DURATION OF SCENES >

        for scene in all_scenes_layer:
            scene_to_be_added = NNSceneData.NNScene_For_All(self.screen, int(scene.attrib["number"]))

            #scene_to_be_added.set_process_to_main(self.p_receive_sub_to_main, self.p_send_main_to_sub)

            self.scenes.append(scene_to_be_added)
            timeline_scenes.append(int(scene.attrib["duration"]))





        # -----------------------------------------------------------


        # CREATING IN-GAME CLOCK
        self.clock = pygame.time.Clock()

        # PREPARING STATEMACHINE TO CHANGE THE SCENE
        #
        # PARAMETER:
        # Statemachine( flag_to_use_junction_state=True or False )
        #
        flag_to_junction = True



        # -----------------------------------------------------------



        # PREPARING FINAL SCENE AND DURATION LIST
        self.final_scenes = []


        timeline_junct = []
        duration_junct = NNGlobals.DURATION_JUNCTION

        # CREATING JUNCTION SCENES
        if flag_to_junction is True:
            junct_scenes = []

            for index in range(len(self.scenes)-1):
                state = NNScene.NNScene_Junction(self.screen,
                                                 self.scenes[index].stateID,
                                                 self.scenes[index+1].stateID,
                                                 duration_junct,
                                                 self.scenes[index].the_value_dict
                                                 )
                junct_scenes.append(state)
                timeline_junct.append(duration_junct)

            #print(junct_scenes)

            for index in range(len(self.scenes) + len(junct_scenes)):
                self.final_scenes.append(None)
                self.final_durations.append(None)

            #print(self.final_scenes)
            #print(len(self.scenes) + len(junct_scenes) - 1)


            # CONSTRUCT FINAL SCENES INCLUDING JUNCTION STATES
            for index in range(len(self.scenes) + len(junct_scenes)):
                if index == 0:
                    self.final_scenes[index] = self.scenes[0]
                    self.final_durations[index] = timeline_scenes[0]
                elif index == 1:
                    self.final_scenes[index] = junct_scenes[0]
                    self.final_durations[index] = timeline_junct[0]
                elif index % 2 == 0:
                    self.final_scenes[index] = self.scenes[index // 2]
                    self.final_durations[index] = timeline_scenes[index // 2]
                else:
                    self.final_scenes[index] = junct_scenes[index // 2]
                    self.final_durations[index] = timeline_junct[index // 2]

        else:
            self.final_scenes = self.scenes
            self.final_durations = timeline_scenes
            self.final_durations_backup = self.final_durations


        self.final_durations_backup = copy.deepcopy(self.final_durations)


        # UNTIL HERE, WE GET THE LIST OF SCENE OBJECTS LIST
        # THEY WILL BE INITIALIZED BUT NOT FILLED WITH THE ACTUAL OBJECTS.
        # FROM HERE, BELOWS WILL BE DONE BY PROPER FUNCTIONS.
        #
        # setup()  -- CREATING ACTUAL OBJECTS BUT DO NOT RUN THE ANIMATION
        # start()  -- STARTING THE ANIMATION


        # SETTING UP GLOBAL TIMER
        NNGlobals.TIMER = Timer.Timer(self.final_durations)
        self.final_scenes[0].setup(self.final_scenes[0].the_value_dict, self.final_durations[0])
        self.final_scenes[0].start()


        # CREATING STATEMACHINE
        NNGlobals.STATEMACHINE = Statemachine.Statemachine(flag_to_junction, self.final_scenes, self.final_durations)
        NNGlobals.STATEMACHINE.pushState(self.final_scenes[0])


        # CURSOR SETTING
        # https://www.pygame.org/docs/ref/mouse.html
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


        # TODO :: SAVING RECORDS TO DATABASE !!!
        # MUST TODO :: PREPARATION FOR BLIND PEOPLE !!!



        # -----------------------------------------------------------------------------------
        self.current_main_scenario = "FIRST_SCENE"
        NNGlobals.CURRENT_SCENARIO = self.current_main_scenario




    def reset_all_flow(self):
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




    def run(self):
        #####print('------------------ TenByTenNumbers_main OBJECT run() METHOD ENTERED')



        # -----------------------------------------------------------------------------------
        # MAIN EVENT LOOP
        while self.mainloop:

            # GETTING GLOBAL GAME SCENARIO
            self.current_main_scenario = NNGlobals.CURRENT_SCENARIO

            # BEFORE WE CHECK THE PYGAME EVENT,
            # WE CHECK THE MESSAGE FROM SUB PROCESS (TKINTER)
            # THEN EXECUTE SOMETHING ACCORDING TO THE MESSAGES
            #self.check_message_and_execute_with_sub()

            # GETTING EVENT OBJECT FROM PYGAME ENGINE
            for event in pygame.event.get():

                if event.type == pygame.QUIT and self.editor_mode:
                    #self.p_send_main_to_sub.send('EXIT')
                    pass

                elif event.type == pygame.QUIT:
                    self.mainloop = False


            # UPDATING SCENE COUNTS
            NNGlobals.SCENE_COUNTS = len(self.final_scenes)


            # UPDATING SCENE INDEX FROM TIMER
            NNGlobals.SCENE_INDEX = NNGlobals.TIMER.get_result()["elem_index"]

            # BELOW CHECKS MAIN TIMELINE IS FULFILLED
            if NNGlobals.DEMO_MODE_NOW and NNGlobals.SCENE_INDEX == -1:
                #####print("==================================     MAIN TIMELINE ENDED IN DEMO MODE   ============================")
                self.reset_all_flow()

            elif NNGlobals.DEMO_MODE_NOW is False and NNGlobals.SCENE_INDEX == -1:
                #####print("==================================     MAIN TIMELINE ENDED IN NORMAL MODE   ============================")

                # SCENE JUMPING
                NNGlobals.SCENE_INDEX = 0

                # GLOBAL FLAGS RESET
                NNGlobals.ALL_BUTTON_DISABLE = False
                NNGlobals.DEMO_MODE_NOW = True
                #NNGlobals.USER_INPUT = []
                NNGlobals.USER_RESULT = 0

                # TIMER RESETTING
                NNGlobals.TIMER.reset()
                NNGlobals.TIMER.timeline_index = 0

                # STORE THE VALUES TO GLOBAL VARIABLE
                #value_dict = NNGlobals.STATEMACHINE.state_list[-1].obj_manager.the_value_dict

                # CHANGING THE SCENE
                NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

                #NNGlobals.STATEMACHINE.state_list[-1].the_value_dict = value_dict

                # SEND MESSAGE TO SUB PROCESS !
                # if self.p_send_main_to_sub is not None:
                #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(1))
                #



            # IN THE PYGAME EVENT LOOP,
            # WHEN WE ARE IN THE DEMO MODE,
            # AND MOUSE CURSOR WAS MOVED

            mouse_movement = pygame.mouse.get_rel()
            if mouse_movement[0] != 0 or mouse_movement[1] != 0:
                if NNGlobals.SCENE_INDEX == 0:
                    NNGlobals.TIMER.reset()


                if NNGlobals.DEMO_MODE_NOW and NNGlobals.SCENE_INDEX >= 2:
                    ######print(mouse_movement)

                    #####print("$$$$$$$$$$$$$$$   DEMO MODE SHOULD BE OFFED   !!!!!!!!!!!!!")
                    self.reset_all_flow()



            # -----------------------------------------------------------------------------------
            # EXECUTING FUNCTIONS WITH SCENARIOS
            if self.current_main_scenario is not " ":

                for cb in self.scenario_and_functions[self.current_main_scenario]:
                    cb()



            # -----------------------------------------------------------------------------------
            # PYGAME ENGINE DISPLAY UPDATE
            pygame.display.update()

            # SETTING PYGAME'S TIMER
            self.clock.tick(30)
            ######print('_____________= ONE MAIN LOOP DONE =_____________')






        #####print('============')
        #####print('PROCESS DONE')
        #####print('============')




    # -------------------------------------------------------------------
    # < COMMUNICATION WITH MESSAGE BETWEEN TWO PROCESSES ! >
    #
    def check_message_and_execute_with_sub(self):
        """ CHECKING MESSAGE FROM SUB PROCESS """
        #
        # if self.p_receive_sub_to_main.poll():
        #     self.msg_from_sub = self.p_receive_sub_to_main.recv()
        #     #print(f'~~~~~~~~~~ MAIN PROCESS :: CHECKING MESSAGES FROM SUB PROCESS ~~~~~~~~~~~~     {self.msg_from_sub}')
        #
        #     # < ROUTING WITH THE MESSAGES >
        #     # CLOSING APP
        #     if self.msg_from_sub == 'EXIT':
        #         self.mainloop = False
        #
        #     # OPEN THE FLAG open_flag_ipc
        #     elif self.msg_from_sub == 'OPEN_IPC':
        #         self.open_flag_ipc()
        #
        #     # SEND THE CURRENT SCENE NUMBER TO SUB PROCESS !
        #     elif self.msg_from_sub == 'Request_SceneNumber_Current':
        #         #self.do_with_message_with_sub(self.msg_from_sub)
        #         pass
        #
        #     # SEND THE CURRENT SCENE NUMBER TO SUB PROCESS !
        #     elif 'Reload_CurrentScene_' in self.msg_from_sub :
        #
        #         self.open_flag_ipc()
        #
        #         # RELOADING THE CURRENT SCENE
        #         #self.do_with_message_with_sub(self.msg_from_sub)
        #
        #     # THE MESSAGE WHEN THE SCENE WAS CHANGED !
        #     elif 'SCENE_CHANGED_TO_' in self.msg_from_sub:
        #
        #         self.open_flag_ipc()
        #
        #         # RELOADING THE CURRENT SCENE
        #         #self.do_with_message_with_sub(self.msg_from_sub)
        #
        #
        # elif self.msg_from_sub == " ":
        #     self.msg_from_sub = " "

        pass

    def do_with_message_with_sub(self, message):
        """ DOING SOME ACTION ACCORDING WITH MESSAGE FROM SUB PROCESS """

        # TODO :: MAKING THIS TO BE GATED !!!!!
        #####print(f'~~~~~~~~~~ MAIN PROCESS :: do_with_message_with_sub -- CURRENT self.flag_ipc ~~~~~~~~~~~~     {self.flag_ipc}')


        # MESSAGE FOR SENDING CURRENT SCENE NUMBER
        if self.flag_ipc is True:
            #print(f'~~~~~~~~~~ MAIN PROCESS :: DOING SOMETHING WITH MESSAGE ~~~~~~~~~~~~     {self.msg_from_sub}')

            if message == 'Request_SceneNumber_Current':
                #print('~~~~~~~~~~ MAIN PROCESS ~~~~~~~~~~~~   SENDING CURRENT SCENE NUMBER TO SUB PROCESS !!!')
                #print(self.final_scenes[NNGlobals.SCENE_INDEX].scene_number)

                # SEND THE CURRENT SCENE NUMBER TO SUB PROCESS !
                #self.p_send_main_to_sub.send('ScnCurrent_' + str(self.final_scenes[NNGlobals.SCENE_INDEX].scene_number))

                # CLOSE THE GATE
                self.flag_ipc = False

            elif 'Reload_CurrentScene_' in message:
                #print('~~~~~~~~~~ MAIN PROCESS ~~~~~~~~~~~~   SENDING CURRENT SCENE NUMBER TO SUB PROCESS !!!')
                #print(self.final_scenes[NNGlobals.SCENE_INDEX].scene_number)

                # < RELOAD THE CURRENT SCENE >

                # RETRIEVING PAST-CURRENT SCENE (DEEP COPYING)
                past_scene_the_value_dict = self.final_scenes[NNGlobals.SCENE_INDEX].the_value_dict

                # RETRIEVING THE SCENE NUMBER WHICH IS SAVED (NEW-CURRENT SCENE)
                current_scene_number = int(message[20:])

                # CONVERT SCENE NUMBER TO SCENE INDEX
                NNGlobals.SCENE_INDEX = 2 * current_scene_number - 2



                # -----------------------------------------------------------
                # < SCENE CREATION WITH XML >
                new_scene = NNSceneData.NNScene_For_All(self.screen, current_scene_number)



                # TRANSFER VALUE DICT FROM PAST
                new_scene.the_value_dict = past_scene_the_value_dict


                #new_scene.set_process_to_main(self.p_receive_sub_to_main, self.p_send_main_to_sub)


                # EXCHANGE THE CHANGED SCENE OBJECT
                #####print(f'{getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno} -- do_with_message_with_sub -- CHANGING final_scenes SCENE LIST -- NNGlobals.SCENE_INDEX -->  {NNGlobals.SCENE_INDEX}')
                NNGlobals.STATEMACHINE.scene_objects[NNGlobals.SCENE_INDEX] = self.final_scenes[NNGlobals.SCENE_INDEX] = new_scene


                # CHANGE THE SCENE USING STATEMACHINE
                # SETTING UP AND STARTING THE SCENE WILL BE DONE IN THE STATEMACHINE
                NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)




            #print(f'~~~~~~~~~~ MAIN PROCESS :: do_with_message_with_sub()  --  flag_ipc IS NOW... ~~~~~~~~~~~~     {self.flag_ipc}')



    def open_flag_ipc(self):
        """
        THIS OPENS THE GATE TO THE FUNCTION
        WHICH EXECUTES THE FUNCTIONALITIES WE WANT

        SO USE THIS FUNCTION WITH THE MESSAGES FROM THE OUTSIDE OF THIS PROCESS !
        """

        # OPEN THE GATE
        self.flag_ipc = True
        #print(f'~~~~~~~~~~ MAIN PROCESS :: open_flag_ipc()  --  flag_ipc IS NOW... ~~~~~~~~~~~~     {self.flag_ipc}')



    # -------------------------------------------------------------------
    def close_program(self):
        self.mainloop = False




    # < COLOR CONVERSION >
    # https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))



    # ---------------------------------------------------------------------------------------
    # CALLBACKS

    def pause_main_timer(self):
        # IF THERE 'IS' INITIALIZED "JUNCTION_STATE" ALREADY,
        # AND,
        # THAT "JUNCTION STATE" IS 'NOT COMPLETED' (STILL RUNNING)

        NNGlobals.TIMER.pause()

        # if NNGlobals.STATEMACHINE.junction_state is not None and \
        #         NNGlobals.STATEMACHINE.junction_state.complete is False:
        #     # 'MAIN TIMELINE' SHOULD BE PAUSED
        #     NNGlobals.TIMER.pause()


    def main_timer_flows(self):
        # MAIN TIMER FLOWS
        NNGlobals.TIMER.timer_tick()


    def check_disabling_scene(self):
        # < CHECKING THE TIMER'S STATUS >
        # IF THE TIMER'S STATUS IS CHANGED TO "FULFILLED"
        if NNGlobals.TIMER.is_done is True:
            # DISABLE TO UPDATE
            NNGlobals.STATEMACHINE.state_list[-1].disable_update()


    def jump_to_next_scene(self):
        # < JUMPING TO NEXT SCENE >
        # WHEN WE CAPTURED THE Timer'S timer.is_jumping FLAG IS True...
        if NNGlobals.TIMER.is_jumping:

            # < ACTUAL CHANGE >
            if NNGlobals.DEMO_MODE_NOW:

                NNGlobals.SCENE_INDEX += 1
                NNGlobals.ALL_BUTTON_DISABLE = True

                #####print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  MAIN_LOOP -- ~~~~~~~~~~~~~~~~  JUMPING TO NEXT ~~~~~~~~~~~~~~~~~   stateID  --     {self.final_scenes[NNGlobals.SCENE_INDEX].stateID}')
                #####print(f'NNGlobals.SCENE_INDEX  IS   {NNGlobals.SCENE_INDEX}')

                NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)

                # SEND MESSAGE TO SUB PROCESS !
                # if self.p_send_main_to_sub is not None:
                #     self.p_send_main_to_sub.send('SCENE_CHANGED_TO_' + str(NNGlobals.STATEMACHINE.state_list[-1].scene_number))
                #

            else:
                NNGlobals.SCENE_INDEX += 1
                NNGlobals.ALL_BUTTON_DISABLE = False

                #####print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  MAIN_LOOP -- ~~~~~~~~~~~~~~~~  JUMPING TO NEXT ~~~~~~~~~~~~~~~~~   stateID  --     {self.final_scenes[NNGlobals.SCENE_INDEX].stateID}')
                #####print(f'NNGlobals.SCENE_INDEX  IS   {NNGlobals.SCENE_INDEX}')

                NNGlobals.STATEMACHINE.changeState(NNGlobals.SCENE_INDEX)


    def update_statemachine(self):
        #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  MAIN_LOOP -- update_statemachine  --')

        # STATE MACHINE UPDATE
        NNGlobals.STATEMACHINE.update(NNGlobals.TIMER.time_elapsed)



    def render_statemachine(self):
        # STATE MACHINE RENDER
        NNGlobals.STATEMACHINE.render()

