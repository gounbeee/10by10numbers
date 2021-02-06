#print('------------------ TenByTenNumbers_sub MODULE ENTERED')

import os
from inspect import currentframe, getframeinfo
from NNEditor.application import Application as EditorApp
from NNHelper.application import Application as HelperApp



class TenByTenNumbers_sub(object):

    # =======================================================================================
    # < tkinter >

    # EDITOR MODE FLAG
    editor_mode = False


    def __init__(self, p_receive_main_to_sub, p_send_sub_to_main):
        #####print(f'TenByTenNumbers_sub -- __init__() --  {getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno}')
        #####print(f'PARENT PID --   {os.getppid()}')
        #####print(f'PID --   {os.getpid()}')

        # ----------------------------------------------------------------------
        # < SETTING UP THE PIPES TO COMMNUNICATE WITH MAIN PROCESS >
        #
        # SETTING PIPE OBJECTS TO COMMUNICATE WITH MAIN PROCESS
        self.p_receive_main_to_sub = p_receive_main_to_sub  # FOR RECEIVING
        self.p_send_sub_to_main = p_send_sub_to_main  # FOR SENDING


        if TenByTenNumbers_sub.editor_mode:

            # EDITOR APP WITH TKINTER
            self.editor_app = EditorApp(receiving_pipe=self.p_receive_main_to_sub, sending_pipe=self.p_send_sub_to_main)


        # else:
        #
        #     # HELPER APP WITH TKINTER
        #     self.helper_app = HelperApp(receiving_pipe=self.p_receive_main_to_sub, sending_pipe=self.p_send_sub_to_main)





    # ----------------------------------------------------------------


