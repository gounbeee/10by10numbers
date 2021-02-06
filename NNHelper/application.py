from os import environ
from inspect import currentframe, getframeinfo
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.font import Font
import time


# THIS STYLE; INHERITING THE CLASS WHICH WE WANT TO INVOLVE
# IS SIMILAR WITH MFC I HAVE SEEN EARLIER !

class Application(tk.Tk):
    """Application root window"""
    config_dirs = {
        'Linux': environ.get('$XDG_CONFIG_HOME', '~/.config'),
        'freebsd7': environ.get('$XDG_CONFIG_HOME', '~/.config'),
        'Darwin': '~/Library/Application Support',
        'Windows': '~/AppData/Local'
    }


    # STATIC VARIABLE
    #element_type = ['node_text', 'clickable', 'indicator', 'nav_buttons']



    def __init__(self, *args, **kwargs):

        super().__init__(*args)

        # MESSAGE
        self.msg_from_main = ' '


        # ----------------------------------------------------------
        # SETTING PIPE OBJECTS

        # < USING *args, **keywords_args >
        # https://www.programiz.com/python-programming/args-and-kwargs
        self.pipe_receive = None
        self.pipe_send = None

        # FOR ALL INPUT PARAMETER
        # WE SEARCH THE PIPE OBJECTS FROM OUTSIDE OF THIS OBJECT
        for key, value in kwargs.items():
            #####print(("{} is {}".format(key, value))

            if key == 'receiving_pipe':
                self.pipe_receive = value
            elif key == 'sending_pipe':
                self.pipe_send = value



        # < DISABLE WINDOW'S X BUTTON FOR QUIT >
        #
        # ----------------------------------------------------------
        # TODO :: ARCHIVE BELOW !
        #
        # : USING OVERRIDE THE FUNCTION
        # https://stackoverflow.com/questions/45467143/disable-exit-or-x-in-tkinter-window
        #
        self.protocol("WM_DELETE_WINDOW", self.disable_event)


        # ----------------------------------------------------------
        #
        # < MAKING ADDITIONAL EVENT LOOP USING CALLBACK FUNCTION >
        #
        # SETTING ADDITIONAL LOOP TO CHECK THE EXIT COMMAND FROM MAIN PROCEESS
        # https://www.codegrepper.com/code-examples/python/run+a+loop+in+tkinter
        #
        #
        # TODO :: ARCHIVE BELOW !
        #
        # ----------------------------------------------------------
        #
        # < PERFORMANCE IMPACT !!!! >
        # https://stackoverflow.com/questions/40582797/tkinter-after-goes-slow-on-windows
        #
        # : ******  DO NOT SET THE INTERVAL TO '0' !!!!! ******
        #   IT WILL DELAY THE GUI WIDGETS VER SLOW !!!!!
        #
        #  At 1ms it runs ~0.37s then doubles at 2ms and triples at 3ms, etc
        #  time = 0.37 * freq more or less. Tk.after does not guarantee the
        #  function will run at exactly Xms every time due to any processing
        #  that takes place. Run it on 1ms and wildly move the window around,
        #  you'll notice that it takes more time because of the increased load.
        #
        #
        self.after(1, self.check_message_from_main)



        # ----------------------------------------------------------
        # < FLOATING WINDOW TO TKINTER WINDOW >
        #
        # TODO :: CHECKING THIS FLOATING WINDOW IS FLOATING OR NOT !
        #
        # How to make a Tkinter window jump to the front?
        # https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
        self.lift()
        self.attributes("-topmost", True)


        # SETTING TITLE OF TKINTER WINDOW
        self.title("NN TUTOR by sy")
        self.resizable(width=False, height=False)



        # ----------------------------------------------------------------------
        # < RESIZING TKINTER WINDOW AND POSITION >
        # https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/

        # Gets the requested values of the height and widhth.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        #####print(("Width", windowWidth, "Height", windowHeight)

        positionRight = 100
        positionDown = 100

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))





        # ----------------------------------------------------------------------
        # < READING XML FILE >
        # use the parse() function to load and parse an XML file
        self.elem_scene = None
        self.scene_number = -1
        self.scene_number_past = -1

        #self.xml_doc_path = 'xml_scenes/scenes_xml.xml'
        #self.xmlconnector = NNXmlConnector.NNXmlConnector(self.xml_doc_path, None)

        #self.scene_is_displayed = False

        #self.container = {}



        # ----------------------------------------------------------------------
        # FONT SETTING
        self.font_a = Font(family="GenEiChikugoMin2-R.ttf", size=12)
        self.font_b = Font(family="GenEiChikugoMin2-R.ttf", size=22)
        self.font_c = Font(family="GenEiChikugoMin2-R.ttf", size=32)
        self.font_d = Font(family="GenEiChikugoMin2-R.ttf", size=42)
        self.font_e = Font(family="GenEiChikugoMin2-R.ttf", size=52)


        self.col_1 = '#b25178'
        self.col_2 = '#5178b2'
        self.col_3 = '#dfa847'



        # ----------------------------------------------------------------------
        # INITIALIZING
        self.initialize()



        # PREPARING VALIDATION FUNCTION FOR WIDGETS

        # FOR SPIN BOX WIDGETS
        #
        #self.val_cmd_spinbox = (self.register(self.validate_value_spinbox))

        # FOR ALL OTHER WIDGETS
        #
        #self.val_cmd_allothers = (self.register(self.validate_value_allothers))




        # ----------------------------------------------------------------------
        # < ENTERING MAIN EVENT LOOP >

        self.mainloop()






    # ------------------------------------------------------------------
    # CREATION FUNCTION

    def initialize(self):

        #####print(("++++ SUB ++++  initialize() FUNCTION ")
        self.get_current_scene_number()


    def view_with_scene_number(self):
        #####print(("++++ SUB ++++  view_with_scene_number() FUNCTION ")


        # https://pythonbasics.org/tkinter-frame/


        # < hyperlink with a Label in Tkinter? >
        # https://stackoverflow.com/questions/23482748/how-to-create-a-hyperlink-with-a-label-in-tkinter
        #text = tk.Label(self, text='TEST TEXT', fg="blue", cursor="hand2")

        # < JUSTIFING LABEL TEXT WITH LINE \n >
        # https://www.youtube.com/watch?v=LV1GBHsz5YY

        # -----------------------------------------------------------------------------------------------
        if self.scene_number == 1:
            self.delete_all_widgets()
            #####print(("++++ SUB ++++  DO SOMETHING WITH scene_number               1   !!!!!!")

            bg = '#eaeaea'

            frame = tk.Frame(width=500, height=600, bg=bg).pack()

            text = tk.Label(frame, text='ニューラルネットワーク\n（以下 NN）は、\n訓練に使った情報を元に\n答えを見つけます。', fg=self.col_1, bg=bg, justify="left")
            text.config(font=self.font_c)
            text.place(x=20, y=20)

            text = tk.Label(frame, text='つまり、右側の\n訓練データに近いほど\n高い確率の\n答えが得られます。', fg=self.col_1, bg=bg, justify="left")
            text.config(font=self.font_c)
            text.place(x=20, y=240)

            text = tk.Label(frame, text='左クリック：描く        右クリック：消す', fg=self.col_2, bg=bg, justify="center")
            text.config(font=self.font_b)
            text.place(x=30, y=470)

            text = tk.Label(frame, text='中央の三角形：内部を見てみる', fg=self.col_3, bg=bg, justify="center")
            text.config(font=self.font_b)
            text.place(x=50, y=520)


        # -----------------------------------------------------------------------------------------------
        elif self.scene_number == 2:
            self.delete_all_widgets()
            #####print(("++++ SUB ++++  DO SOMETHING WITH scene_number               2   !!!!!!")

            # Positions the window in the center of the page.
            self.geometry("+{}+{}".format(50, 50))


            bg = 'blue'
            frame = tk.Frame(width=600, height=300, bg=bg).pack()

            text = tk.Label(frame, text='こんにちは\nはははははは', fg="red", bg=bg, justify="left")
            text.config(font=self.font_a)
            text.place(x=40, y=37)


            # IMAGE PLACEMENT
            # https://pythonbasics.org/tkinter-image/

            img_1 = Image.open("images_sub/image_sub_1_1.png")
            img_1_render = ImageTk.PhotoImage(img_1)
            img_1_lb = tk.Label(frame, image=img_1_render, bg=bg)
            img_1_lb.image = img_1_render
            img_1_lb.place(x=0, y=200)






        # -----------------------------------------------------------------------------------------------
        elif self.scene_number == 3:
            #####print(("++++ SUB ++++  DO SOMETHING WITH scene_number               3   !!!!!!")
            pass







    # ------------------------------------------------------------------



    # TODO :: ARCHIVE BELOW !
    # < Use TkInter without mainloop >
    # https://gordonlesti.com/use-tkinter-without-mainloop/
    # : The method mainloop has an important role for TkInter, it
    #   is waiting for events and updating the GUI. But this method
    #   is blocking the code after it. You have a conflict, if the
    #   core of your application has also a blocking loop that is
    #   waiting for some events. In my case waiting for input from
    #   a bluetooth device.

    # CHECKING MESSAGE FROM MAIN PROCESS WITH ADDITIONAL LOOP
    def check_message_from_main(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  TenByTenNumbers_sub::check_message_from_main() -- UPDATING MESSAGE RECEIVING FROM MAIN PROCESS")

        if self.pipe_receive.poll():
            self.msg_from_main = self.pipe_receive.recv()
            #print(f'~~~~~~~~~~ MESSAGE FROM MAIN PROCESS ~~~~~~~~~~~~     {self.msg_from_main}')

            # DOING SOMETHING WITH THE MESSAGES FROM MAIN PROCESS
            self.do_with_message_from_sub(self.msg_from_main)

        elif self.msg_from_main is " ":
            self.msg_from_main = " "


        # **** MAKING LOOP ****
        self.after(1, self.check_message_from_main)





    def do_with_message_from_sub(self, message):

        # TODO :: HOW CAN WE DEFINE THE SPECIFICATION EFFECTIVELY ?
        #
        # TODO :: THERE ARE TWO TYPES OF MESASGES
        #         EXIT AND ScnCurrent_XX
        #                  ^--------^-------------------- THIS CAN BE CHANGED

        # < ROUTING WITH THE MESSAGES >
        #
        if message != 'EXIT':
            check_for_scene_number = message[:11]
        else:
            check_for_scene_number = ' '

        # CLOSING APP
        if message == 'EXIT':
            self.pipe_send.send('EXIT')
            self.close_program()

        # RECEIVING CURRENT SCENE NUMBER
        elif check_for_scene_number == 'ScnCurrent_':

            # SLICING THE STRING AND RETRIEVE THE SCENE NUMBER ONLY
            self.scene_number = int(message[11:])

            #####print((f"+++++++ SUB ++ MESSAGE FROM MAIN PROCESS --   ScnCurrent_  ----    self.scene_number  ------>    {self.scene_number}")
            self.view_with_scene_number()


        # IF THE SCENE WAS CHANGED IN MAIN PROCESS...
        elif 'SCENE_CHANGED_TO_' in message:

            # SLICING THE STRING AND RETRIEVE THE SCENE NUMBER ONLY
            self.scene_number = int(message[17:])

            # DELETE ALL WIDGETS
            self.delete_all_widgets()

            #####print((f"+++++++ SUB ++ MESSAGE FROM MAIN PROCESS --   SCENE_CHANGED_TO_  ----    self.scene_number  ------>    {self.scene_number}")
            self.view_with_scene_number()




    # < GETTING CURRENT SCENE NUMBER WITH IPC AND EXECUTES SOME FUNCTIONS >

    # SEND THE MESSAGE TO MAIN PROCESS
    # THEN GET THE CURRENT SCENE NUMBER
    #
    # THIS FUNCTION IS CALLBACK FUNCTION FOR THE MENU BUTTON !
    def get_current_scene_number(self):
        #self.recordlist.tkraise()
        #print("++++ SUB PROCESS :: SENDING REQUEST TO GET THE CURRENT SCENE NUMBER!")
        self.pipe_send.send('OPEN_IPC')
        self.pipe_send.send('Request_SceneNumber_Current')







    # ------------------------------------------------------------------
    # UTILITIES

    def delete_all_widgets(self):


        if self.winfo_children():

            # TODO :: ARCHIVE BELOW !
            #
            # < CLEARING THE ALL WIDGETS >
            # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
            for widget in self.winfo_children():
                widget.destroy()



    # CLOSING THIS OBJECT
    def close_program(self):
        self.destroy()



    # BELOW IS TO OVERRIDE THE EXIT BUTTON !
    def disable_event(self):
        pass

