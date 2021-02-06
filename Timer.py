import pygame
from inspect import currentframe, getframeinfo, stack
from NNGlobals import *



class Timer(object):

    def __init__(self, timeline):
        self.timeline = timeline
        self.timeline_index = 0
        self.time_now = pygame.time.get_ticks()
        self.time_last = pygame.time.get_ticks()

        self.is_done = False

        self.result = {"elem_index": 0, "time_elapsed": 0}
        self.time_elapsed = 0

        self.is_jumping = False



    def reset(self):
        self.time_now = pygame.time.get_ticks()
        self.time_last = pygame.time.get_ticks()

        self.is_done = False

        self.result = {"elem_index": 0, "time_elapsed": 0}
        self.time_elapsed = 0

        self.is_jumping = False



    def pause(self):
        #frameinfo = getframeinfo(currentframe())
        #print(f'{frameinfo.filename} -- {frameinfo.lineno}  Timer::pause() -- ')

        self.time_now = pygame.time.get_ticks()
        self.time_last = pygame.time.get_ticks()



    def timer_tick(self):

        #print(f'{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  Timer::timer_tick() -- {self.time_elapsed}')

        if not self.is_done:

            # JUMPING FLAG TO False (DEFAULT VALUE)
            self.is_jumping = False

            # UPDATE CURRENT TIME
            self.time_now = pygame.time.get_ticks()

            # CALCULATING DELTA TIME FROM LAST TIME
            self.time_elapsed = self.time_now - self.time_last

            if self.timeline_index < len(self.timeline):

                # CHANGING INDEX TO NEXT
                if self.time_elapsed > self.timeline[self.timeline_index]:

                    # JUMPING FLAG TO True
                    self.is_jumping = True

                    #frameinfo = getframeinfo(currentframe())
                    #print(f'{frameinfo.filename} -- {frameinfo.lineno}  ............ TIMELINE ELEMENT \'{self.timeline_index}\' WAS EXPIRED, \'{self.time_elapsed}\' PASSED')

                    # RECORD CURRENT TIME TO 'LAST' TIMING
                    self.time_last = pygame.time.get_ticks()

                    # RESET ELAPSED TIME
                    self.time_elapsed = 0

                    # IF THE INDEX NUMBER DID NOT REACHED THE LIMITS, PLUS 1 TO INDEX
                    if self.timeline_index < len(self.timeline):
                        # PLUS 1 TO timeline_index TO INDICATE THE NEXT ELEMENT IN THE TIMELINE
                        self.timeline_index += 1


                    # CHECK THE ENDPOINT OF THE TIMELINE
                    if self.timeline_index >= len(self.timeline):
                        # CLOSE THE GATE FOR THIS LOOP
                        self.is_done = True

                        # JUMPING FLAG TO False (RETURN TO DEFAULT)
                        self.is_jumping = False


            # < SETTING RESULTS >
            # TODO :: BELOW COULD BE CHANGED FOR SOMETHING DIFFERENT PURPOSE !
            self.result["elem_index"] = self.timeline_index
            self.result["time_elapsed"] = self.time_elapsed




    def get_result(self):
        """
        Timer::get_result() FUNCTION
         : THIS FUNCTION RETURNS 'CURRENT STATUS' OF THE TIMER

        Returns:
            [ "elem_index"=index_of_cut, "time_elapsed"=elapsed_time_in_the_cut ]

        """
        # IF THE TIMER IS STILL FLOWS (NOT FULFILLED)
        if not self.is_done:
            #frameinfo = getframeinfo(currentframe())
            #print(f'{frameinfo.filename} -- {frameinfo.lineno}  Timer::getresult() -- ')

            # JUST RETURN THE RESULT
            return self.result


        else:

            # IF TIMER IS FULFILLED,
            # SET THE -1 VALUE TO INDEX AND ELAPSED TIME
            # TODO : MAYBE BETTER SOLUTION ?
            self.result["elem_index"] = -1
            self.result["time_elapsed"] = -1

            # THEN RETURN THAT CONSTANT VALUE
            return self.result