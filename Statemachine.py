import NNScene
import NNGlobals
from inspect import currentframe, getframeinfo, stack


class Statemachine(object):
    """
    STATEMACHINE CLASS WITH JUNCTION STATE (by sy)

        THIS CLASS SUPPORTS JUNCTION STATE WHICH WILL BE AN INTERMISSION SCENE.
        AND, THAT JUNCTION SCENE WILL BE AUTOMATICALLY INTERPOLATE THE VALUE BETWEEN TWO SCENES.
        (e.g. POSITION OF TWO OBJECTS)
    """

    def __init__(self, usingStateConnect, final_scenes, final_durations):

        # INITIALIZE state_list TO EMPTY
        self.state_list = []

        # ELASPED TIME VARIABLE
        # : THIS WILL BE INPUTTED FROM OUTSIDE OF THIS OBJECT
        self.elapsed_time = 0

        # ALL SCENE LIST
        self.scene_objects = final_scenes

        # ALL SCENE'S DURATION LIST
        self.scene_durations = final_durations

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe())lineno}  Statemachine::__init__() -- {self.state_list}")

        # PREPARING StateConnector
        self.using_connect = usingStateConnect
        self.junction_state = None

        # INITIALIZING THE DICTIONARY OF the_value
        self.the_value_dict = {}

        # CURRENT SCENE
        #self.current_scene = None


    def update(self, elapsed_time):

        # GETTING ELAPSED TIME FROM OUTSIDE OF THIS OBJECT
        # (DELTA TIME FROM STARTING POINT OF THIS SCENE)
        self.elapsed_time = elapsed_time

        #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::update()    MAIN  elapsed_time    {self.elapsed_time}')

        self.exchange_value_dict()

        # UPDATE CURRENT SCENE
        # WITH ELAPSED TIME
        self.state_list[-1].update(self.elapsed_time)


    def render(self):

        # RENDERING CURRENT SCENE
        self.state_list[-1].render()

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::render() -- {self.state_list}")


    def pushState(self, new_state):

        # APPEND THE SCENE TO STATE LIST
        self.state_list.append(new_state)

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::pushState() -- {self.state_list}")


    def popState(self):
        self.state_list.pop()

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::popState() -- {self.state_list}")



    def exchange_value_dict(self):
        # EXCHANGE VALUES BETWEEN TWO DICTIONARY EACH OTHER FOR the_value_dict
        if len(self.state_list[-1].obj_manager.the_value_dict) != 0 and \
                len(self.state_list[-1].the_value_dict) == 0:
            self.state_list[-1].the_value_dict = self.state_list[-1].obj_manager.the_value_dict

        if len(self.state_list[-1].the_value_dict) != 0 and \
                len(self.state_list[-1].obj_manager.the_value_dict) == 0:
            self.state_list[-1].obj_manager.the_value_dict = self.state_list[-1].the_value_dict




    def changeState(self, new_index):
        """
        CHANGING SCENE TO NEW ONE WITH INDEX NUMBER.

        :param new_index: Index number of new state
        """
        #####print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::changeState()   --    new_index (INPUTTED AS PARAMETER)   --   {new_index}")

        self.exchange_value_dict()

        next_scene = None
        # IF NEXT SCENE IS JUNCTION SCENE...
        if type(self.scene_objects[new_index]) is NNScene.NNScene_Junction:
            next_scene = self.jump_to_junction(new_index, self.scene_durations[new_index] )
            self.junction_state = next_scene

        elif type(self.scene_objects[new_index]) is not NNScene.NNScene_Junction:
            next_scene = self.jump_to_normalstate(new_index, self.scene_durations[new_index])
            self.junction_state = None


        # ANIMATION RESETTING AND STARTING AGAIN
        NNGlobals.NNGlobals.TIMER.reset()
        #NNGlobals.NNGlobals.TIMER.is_jumping = True
        NNGlobals.NNGlobals.TIMER.time_elapsed = 0


        # < SAME PROCESSES IN TWO ABOVE CASES >
        # FIRST, EXECUTE THE FINALIZE FUNCTION(on_exit()) OF EXISTING STATE
        self.state_list[-1].on_exit()
        self.popState()

        # PUSH THE JUNCTION STATE
        self.pushState(next_scene)


    def jump_to_junction(self, new_index, duration):
        """
        FUNCTION WHEN IT JUMPS TO THE 'JUNCTION SCENE'

        :param new_index: Index number of scene to jump
        :return:
        """
        # CHANGING SCENE UNTIL len(self.scene_objects)-1 INDEX
        if new_index < len(self.scene_objects) - 1:
            # NEW SCENE TO JUMP FROM PASSED SCENE
            #current_scene = self.scene_objects[new_index-1]
            current_scene = self.state_list[-1]

            # TO CALCULATE THE AMOUNT OF DIFFERENCES OF POSITION,
            # WE GET THE 'NEXT' SCENE
            # (NORMAL SCENE)
            scene_after_junction = self.scene_objects[new_index+1]
            scene_after_junction.setup(current_scene.the_value_dict, self.scene_durations[new_index+1])


            # THIS IS JUNCTION SCENE WE NEED TO SETUP
            junction_scene = self.scene_objects[new_index]

            # SETUP 'NEXT SCENE' WITH PREVIOUS SCENE
            # (JUNCTION SCENE)
            junction_scene.setup_objects(current_scene.obj_manager.obj_list, scene_after_junction.obj_manager.obj_list)
            junction_scene.setup_duration()
            junction_scene.setup(current_scene.obj_manager.the_value_dict, self.scene_durations[new_index])
            junction_scene.start()


            # AFTER SETTING UP THE JUNCTION SCENE,
            # CLEAR THE OBJECT LIST AND the_value_dict OF NEXT SCENE
            scene_after_junction.clear_objects()
            scene_after_junction.clear_value_dict()

            # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::changeState() -- THE SCENE IS JUMPING TO SCENE INDEX   {new_index}")
            # #####print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::changeState() -- THE SCENE IS JUMPING TO SCENE INDEX   {len(self.state_list[-1].obj_manager.obj_list)}")

            return junction_scene


    def jump_to_normalstate(self, new_index, duration):
        """
        NOW IS JUNCTION SCENE -> NEW SCENE WILL BE NORMAL SCENE
        """

        # NEW SCENE TO JUMP FROM PASSED SCENE
        next_scene = self.scene_objects[new_index]

        next_scene.setup(self.state_list[-1].the_value_dict, duration)
        next_scene.start()

        # print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::changeState() -- THE SCENE IS JUMPING TO SCENE INDEX   {new_index}")
        # #####print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Statemachine::changeState() -- THE SCENE IS JUMPING TO SCENE INDEX   {len(self.state_list[-1].obj_manager.obj_list)}")

        return next_scene
