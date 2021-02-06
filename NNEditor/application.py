from os import environ
import NNXmlConnector
from inspect import currentframe, getframeinfo
import tkinter as tk
from tkinter import ttk
from functools import partial
import xml.etree.ElementTree as ET
from xml.dom import minidom


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


    # TODO :: ARCHIVE BELOW !
    # < HOW TO PLACE WIDGET IN THE CANVAS (WITH CREATING WINDOW OBJECT IN THE CANVAS) >
    # https://stackoverflow.com/questions/4080413/how-to-place-a-widget-in-a-canvas-widget-in-tkinter


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
            #####print("{} is {}".format(key, value))

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
        self.title("XML EDITOR by sy")
        #self.resizable(width=False, height=False)


        # < TRANSPARENT WINDOW TKINTER >
        # https://stackoverflow.com/questions/18394597/is-there-a-way-to-create-transparent-windows-with-tkinter
        self.attributes('-alpha', 0.8)


        # ----------------------------------------------------------------------
        # < READING XML FILE >
        # use the parse() function to load and parse an XML file



        self.elem_scene = None
        self.scene_number = -1
        self.scene_number_past = -1

        self.xml_doc_path = 'xml_scenes/scenes_xml.xml'
        self.xmlconnector = NNXmlConnector.NNXmlConnector(self.xml_doc_path, None)

        self.scene_is_displayed = False

        self.container = {}

        self.dupl_strvar = None





        # ---------------------------------------------------------------------------



        # SETTING UP THE MENU
        self.create_main_gui()


        # INITIALIZING FRAMES

        # PARENTS
        self.main_frame_other = None
        self.main_frame = None
        self.main_frame_indicator = None


        # ROOT OF CHILDREN
        self.frame_textnode_root = None
        self.frame_multitextnode_root = None
        self.frame_picnode_root = None
        self.frame_indicator_root = None
        self.frame_line_root = None


        # CHILDREN
        self.frame_duplicator = None
        self.frame_drawpad = None
        self.frame_textnode = None
        self.frame_multitextnode = None
        self.frame_picnode = None
        self.frame_clickable = None
        self.frame_indicator = None
        self.frame_line = None
        self.frame_nav_buttons = None


        # ---------------------------------------------------------------------------
        # PREPARING VALIDATION FUNCTION FOR WIDGETS

        # FOR SPIN BOX WIDGETS
        #
        self.val_cmd_spinbox = (self.register(self.validate_value_spinbox))

        # FOR ALL OTHER WIDGETS
        #
        self.val_cmd_allothers = (self.register(self.validate_value_allothers))

        # VALIDATION FUNCTION FOR DUPLICATE ENTRY
        self.val_cmd_duplicate_entry = self.register(self.validate_duplicate_entry)


        # ----------------------------------------------------------------------
        # < ENTERING MAIN EVENT LOOP >

        self.mainloop()





        # ---------------------------------------------------------

        # IMAGE PLACEMENT
        #
        # self.taskbar_icon = tk.PhotoImage(file=ABQ_LOGO_64)
        # self.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        #
        #
        #
        # self.logo = tk.PhotoImage(file=ABQ_LOGO_32)
        # tk.Label(self, image=self.logo).grid(row=0)



    # ------------------------------------------------------------------



    def create_main_gui(self):


        # https://pythonexamples.org/python-tkinter-set-window-size/
        #self.geometry("500x100")

        positionRight = 100
        positionDown = 100

        # Positions the window in the center of the page.
        #self.geometry("{}x{}+{}+{}".format(1000, 800, positionRight, positionDown))
        #self.resizable()


        # ---------------------------------------------------------------------------



        # TODO :: ARCHIVE BELOW !
        # < UNDERSTANDING PACK AND STICKY >
        # https://watlab-blog.com/2020/07/18/tkinter-frame-pack-grid/

        # MAIN FRAME SETTING
        self.main_frame_other = tk.Frame(self, bg="GREEN", borderwidth=2)
        self.main_frame_other.pack(side=tk.TOP, anchor=tk.NW)

        self.main_frame_indicator = tk.Frame(self, bg="YELLOW", borderwidth=2)
        self.main_frame_indicator.pack(side=tk.TOP, anchor=tk.W)

        self.main_frame = tk.Frame(self, bg="GRAY", borderwidth=2)
        self.main_frame.pack(side=tk.TOP, anchor=tk.SW)


        # SCROLLBAR SETTING
        scrollbar = ttk.Scrollbar(self.main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.main_frame)




        # ----------------------------------------------------------
        # SETTING UP MENU WITH CALLBACK FUNCTION

        # CREATING FRAME FOR MENU
        self.main_menu_frame = tk.Frame(self, relief='raised', bd=2)
        self.main_menu_frame.pack(fill=tk.X)

        # CREATING MENU BUTTON

        # CREATING MENU ITEM FOR IMPORTING SCENE FROM XML
        menu_bar = tk.Menu(self.main_menu_frame)
        xml_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu = tk.Menu(menu_bar, tearoff=0)

        # MENU 'XML'
        xml_menu.add_command(label="IMPORT SCENE", command=self.get_current_scene_number)
        #xml_menu.add_separator()
        #xml_menu.add_command(label="SAVE TO XML", command=self.save_to_xml)
        menu_bar.add_cascade(label='XML', menu=xml_menu)

        # MENU 'VIEW'
        view_menu.add_command(label="VIEW ALL", command=self.view_all_widget)
        view_menu.add_command(label="HIDE ALL", command=self.hide_all_widget)
        view_menu.add_separator()

        view_menu.add_command(label="VIEW INDICATOR", command=self.view_indicator)
        view_menu.add_command(label="HIDE INDICATOR", command=self.hide_indicator)
        view_menu.add_separator()

        view_menu.add_command(label="VIEW LINE", command=self.view_line)
        view_menu.add_command(label="HIDE LINE", command=self.hide_line)
        view_menu.add_separator()

        view_menu.add_command(label="VIEW TEXT", command=self.view_text)
        view_menu.add_command(label="HIDE TEXT", command=self.hide_text)
        view_menu.add_separator()

        view_menu.add_command(label="VIEW MULTITEXT", command=self.view_multitext)
        view_menu.add_command(label="HIDE MULTITEXT", command=self.hide_multitext)

        menu_bar.add_cascade(label='VIEW', menu=view_menu)


        self.config(menu=menu_bar)



    # ------------------------------------------------------------------
    #
    # TODO :: ARCHIVE BELOW !
    # < Python tkinter accessing object properties >
    # https://stackoverflow.com/questions/17114338/python-tkinter-accessing-object-properties



    # ------------------------------------------------------------------


    def view_all_widget(self):
        #####print("VIEW ALL WIDGETS !!!!!")

        if self.frame_indicator_root:
            self.frame_indicator_root.pack(side=tk.LEFT, anchor=tk.NW)

        if self.frame_line_root:
            self.frame_line_root.pack(side=tk.LEFT, anchor=tk.NW)

        if self.frame_textnode_root:
            self.frame_textnode_root.pack(side=tk.LEFT, anchor=tk.NW)

        if self.frame_multitextnode_root:
            self.frame_multitextnode_root.pack(side=tk.LEFT, anchor=tk.NW)



    def hide_all_widget(self):
        #####print("HIDE ALL WIDGETS !!!!!")
        if self.frame_indicator_root:
            self.frame_indicator_root.pack_forget()

        if self.frame_line_root:
            self.frame_line_root.pack_forget()

        if self.frame_textnode_root:
            self.frame_textnode_root.pack_forget()

        if self.frame_multitextnode_root:
            self.frame_multitextnode_root.pack_forget()

        # TODO :: ARCHIVE BELOW !
        # < pack_forget() Method to Hide Tkinter Widgets >
        # https://www.delftstack.com/howto/python-tkinter/how-to-hide-recover-and-delete-tkinter-widgets/#hide-and-recover-tkinter-widgets

        # for widget in self.winfo_children():
        #     widget.pack_forget()


    def view_indicator(self):
        #####print("VIEW INDICATORS !")
        if self.frame_indicator_root:
            self.frame_indicator_root.pack(side=tk.LEFT, anchor=tk.NW)



    def hide_indicator(self):
        #####print("HIDE INDICATORS !")
        if self.frame_indicator_root:
            self.frame_indicator_root.pack_forget()



    def view_line(self):
        #####print("VIEW LINE !")
        if self.frame_line_root:
            self.frame_line_root.pack(side=tk.LEFT, anchor=tk.NW)



    def hide_line(self):
        #####print("HIDE LINE !")
        if self.frame_line_root:
            self.frame_line_root.pack_forget()



    def view_text(self):
        #####print("VIEW TEXT !")
        if self.frame_textnode_root:
            self.frame_textnode_root.pack(side=tk.LEFT, anchor=tk.NW)



    def hide_text(self):
        #####print("HIDE TEXT !")
        if self.frame_textnode_root:
            self.frame_textnode_root.pack_forget()



    def view_multitext(self):
        #####print("VIEW MULTI TEXT !")
        if self.frame_multitextnode_root:
            self.frame_multitextnode_root.pack(side=tk.LEFT, anchor=tk.NW)



    def hide_multitext(self):
        #####print("HIDE MULTI TEXT !")
        if self.frame_multitextnode_root:
            self.frame_multitextnode_root.pack_forget()



    def delete_all_widgets(self):
        # TODO :: ARCHIVE BELOW !
        #
        # < CLEARING THE ALL WIDGETS >
        # https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
        for widget in self.winfo_children():
            widget.destroy()



    # ----------------------------------------------------------------------------------------------------------
    #
    # < DISPLAYING ELEMENTS >


    def display_duplicator(self):

        # -------------------------------------------------------------------

        # DUPLICATING ELEMENT

        # FRAME FOR DRAWPAD
        self.frame_duplicator = tk.Frame(self.main_frame_other, bd=2, relief=tk.GROOVE)
        self.frame_duplicator.pack(side=tk.TOP, anchor=tk.NW)

        # LABEL SETTING FOR DRAWPAD
        tk.Label(self.frame_duplicator, text="DUPLICATOR").grid(row=0, column=0, sticky=tk.W)

        # ELEM NAME
        tk.Label(self.frame_duplicator, text="ELEM_NAME").grid(row=1, column=0, sticky=tk.W)
        self.dupl_strvar = tk.StringVar(value="NONE")
        dupl_entry = tk.Entry(self.frame_duplicator,
                              textvariable=self.dupl_strvar,
                              validate="all",
                              validatecommand=(self.val_cmd_duplicate_entry, "%V", "%P"))

        dupl_entry.grid(row=1, column=1, sticky=tk.W)



        # DUPLICATE BUTTON
        callback_dupl = partial(self.duplicate_elem_button)

        dupl_button = tk.Button(self.frame_duplicator, text="DUPLICATE", command=callback_dupl)
        dupl_button.grid(row=1, column=2, sticky=tk.W)


    def display_drawpad(self):
        # -------------------------------------------------------------------
        #
        # < DRAWPAD >
        #
        # IF THERE IS drawpad ELEMENT, RUN super().drawpad_create()
        elem_drawpad = self.elem_scene.find('drawpad')

        if elem_drawpad is not None:
            # INITIALIZATION OF REQUIRED VALUES
            unitcount = unitsize = flag_clickable = anim_duration = None

            # < INITIALIZE DICTIONARY WITH KEYS >
            # https://stackoverflow.com/questions/2241891/how-to-initialize-a-dict-with-keys-from-a-list-and-empty-value-in-python
            keys = ["unitcount", "unitsize", "flag_clickable", "anim_duration"]
            self.container['drawpad'] = {key: None for key in keys}

            # VALUE TAGS IN THE DRAWPAD ELEMENT
            for value in elem_drawpad.findall('value'):

                # < CHECKING KEY IN THE DICTIONARY >
                # https://www.geeksforgeeks.org/python-dictionary-has_key/
                #
                if "unitcount" in value.attrib.keys():
                    unitcount = int(value.attrib["unitcount"])
                    self.container['drawpad']['unitcount'] = unitcount
                elif "unitsize" in value.attrib.keys():
                    unitsize = int(value.attrib["unitsize"])
                    self.container['drawpad']['unitsize'] = unitsize
                elif "flag_clickable" in value.attrib.keys():
                    flag_clickable = str(value.attrib["flag_clickable"])
                    self.container['drawpad']['flag_clickable'] = flag_clickable
                elif "anim_duration" in value.attrib.keys():
                    anim_duration = int(value.attrib["anim_duration"])
                    self.container['drawpad']['anim_duration'] = anim_duration

            # ------------------------------------------------------------------------------------------------

            # < GUI SETTINGS >

            # FRAME FOR DRAWPAD
            self.frame_drawpad = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
            self.frame_drawpad.pack(side=tk.LEFT, anchor=tk.NW)

            # LABEL SETTING FOR DRAWPAD
            tk.Label(self.frame_drawpad, text="DRAWPAD").grid(row=0, column=0, sticky=tk.W)


            # < validatecommand ATTRIBUTE WITH ADDITIONAL ARGUMENT !! >
            # https://stackoverflow.com/questions/18218401/entry-validation-extra-arguments

            # ELEMENTS
            tk.Label(self.frame_drawpad, text="unitcount").grid(row=1, column=0, sticky=tk.W)
            unitcount_intvar = tk.IntVar(value=unitcount)
            unitcount_spnbox = tk.Spinbox(self.frame_drawpad, state='normal', from_=1, to=28, increment=1, textvariable=unitcount_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "drawpad", "unitcount"))
            unitcount_spnbox.grid(row=1, column=1,sticky=tk.W)

            tk.Label(self.frame_drawpad, text="unitsize").grid(row=2, column=0, sticky=tk.W)
            unitsize_intvar = tk.IntVar(value=unitsize)
            unitsize_spnbox = tk.Spinbox(self.frame_drawpad, state='normal', from_=1, to=28, increment=1, textvariable=unitsize_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "drawpad", "unitsize"))
            unitsize_spnbox.grid(row=2, column=1,sticky=tk.W)

            tk.Label(self.frame_drawpad, text="flag_clickable").grid(row=3, column=0, sticky=tk.W)
            flag_clickable_strvar = tk.StringVar(value=flag_clickable)
            flag_clickable_entry = tk.Entry(self.frame_drawpad, textvariable=flag_clickable_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "drawpad", "flag_clickable"))
            flag_clickable_entry.grid(row=3, column=1, sticky=tk.W)

            tk.Label(self.frame_drawpad, text="anim_duration").grid(row=4, column=0, sticky=tk.W)
            anim_duration_intvar = tk.IntVar(value=anim_duration)
            anim_duration_spnbox = tk.Spinbox(self.frame_drawpad, state='normal', from_=1, to=20000, increment=1, textvariable=anim_duration_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "drawpad", "anim_duration"))
            anim_duration_spnbox.grid(row=4, column=1, sticky=tk.W)


    def display_text(self):
        # -------------------------------------------------------------------
        #
        # < TEXT NODES >
        #
        # **** THIS OBJECTS WILL EXECUTE THE VALIDATION FUNCTION ! ****
        #
        #
        # GETTING CHILD ELEMENTS WHICH TAG NAME IS 'node_text'
        elem_node_texts = self.elem_scene.findall('node_text')

        node_text_count = 0

        # FOR ALL node_text

        self.frame_textnode_root = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.frame_textnode_root.pack(side=tk.LEFT, anchor=tk.NW)

        for node_text in elem_node_texts:


            if node_text is not None:
                # INITIALIZATION OF REQUIRED VALUES
                target_surface = \
                    name = \
                    text = \
                    text_size = \
                    anim_duration = \
                    anim_type = \
                    anim_scaler_x = \
                    anim_scaler_y = \
                    position_x = \
                    position_y = \
                    color_r = \
                    color_g = \
                    color_b = \
                    visible = \
                    align = None

                keys = ["target_surface", "name", "text", "text_size", "anim_duration", "anim_type", "anim_scaler_x", "anim_scaler_y", "position_x", "position_y", "color_r", "color_g", "color_b", "visible", "align"]
                self.container['node_text_' + str(node_text_count)] = {key: None for key in keys}

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in node_text.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = str(value.attrib["target_surface"])
                        self.container['node_text_' + str(node_text_count)]['target_surface'] = target_surface
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                        self.container['node_text_' + str(node_text_count)]['name'] = name
                    elif "text" in value.attrib.keys():
                        text = str(value.attrib["text"])
                        self.container['node_text_' + str(node_text_count)]['text'] = text
                    elif "text_size" in value.attrib.keys():
                        text_size = int(value.attrib["text_size"])
                        self.container['node_text_' + str(node_text_count)]['text_size'] = text_size
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                        self.container['node_text_' + str(node_text_count)]['anim_duration'] = anim_duration
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                        self.container['node_text_' + str(node_text_count)]['anim_type'] = anim_type
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                        self.container['node_text_' + str(node_text_count)]['anim_scaler_x'] = anim_scaler_x
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                        self.container['node_text_' + str(node_text_count)]['anim_scaler_y'] = anim_scaler_y
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                        self.container['node_text_' + str(node_text_count)]['position_x'] = position_x
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                        self.container['node_text_' + str(node_text_count)]['position_y'] = position_y
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                        self.container['node_text_' + str(node_text_count)]['color_r'] = color_r
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                        self.container['node_text_' + str(node_text_count)]['color_g'] = color_g
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                        self.container['node_text_' + str(node_text_count)]['color_b'] = color_b
                    elif "visible" in value.attrib.keys():
                        visible = str(value.attrib["visible"])
                        self.container['node_text_' + str(node_text_count)]['visible'] = visible
                    elif "align" in value.attrib.keys():
                        align = value.attrib["align"]
                        self.container['node_text_' + str(node_text_count)]['align'] = align



                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_textnode = tk.Frame(self.frame_textnode_root, bd=2, relief=tk.GROOVE)
                self.frame_textnode.pack(side=tk.LEFT, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_textnode, text="TEXT NODE").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_textnode, text="target_surface").grid(row=1, column=0, sticky=tk.W)
                target_surface_strvar = tk.StringVar(value=target_surface)
                target_surface_entry = tk.Entry(self.frame_textnode, textvariable=target_surface_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_text_" + str(node_text_count), "target_surface"))
                target_surface_entry.grid(row=1, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="name").grid(row=2, column=0, sticky=tk.W)
                name_strvar = tk.StringVar(value=name)
                name_entry = tk.Entry(self.frame_textnode, textvariable=name_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_text_" + str(node_text_count), "name"))
                name_entry.grid(row=2, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="text").grid(row=3, column=0, sticky=tk.W)
                text_strvar = tk.StringVar(value=text)
                text_entry = tk.Entry(self.frame_textnode, textvariable=text_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_text_" + str(node_text_count), "text"))
                text_entry.grid(row=3, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="text_size").grid(row=4, column=0, sticky=tk.W)
                text_size_intvar = tk.StringVar(value=text_size)
                text_size_spnbox = tk.Spinbox(self.frame_textnode, state='normal', takefocus=False, from_=1, to=500, increment=1, textvariable=text_size_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "text_size"))
                text_size_spnbox.grid(row=4, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="anim_duration").grid(row=5, column=0, sticky=tk.W)
                anim_duration_intvar = tk.IntVar(value=anim_duration)
                anim_duration_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=1, to=1000000, increment=1, textvariable=anim_duration_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "anim_duration"))
                anim_duration_spnbox.grid(row=5, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="anim_type").grid(row=6, column=0, sticky=tk.W)
                anim_type_strvar = tk.StringVar(value=anim_type)
                anim_type_entry = tk.Entry(self.frame_textnode, textvariable=anim_type_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_text_" + str(node_text_count), "anim_type"))
                anim_type_entry.grid(row=6, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="anim_scaler_x").grid(row=7, column=0, sticky=tk.W)
                anim_scaler_x_doublevar = tk.DoubleVar(value=anim_scaler_x)
                anim_scaler_x_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_x_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "anim_scaler_x"))
                anim_scaler_x_spnbox.grid(row=7, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="anim_scaler_y").grid(row=8, column=0, sticky=tk.W)
                anim_scaler_y_doublevar = tk.DoubleVar(value=anim_scaler_y)
                anim_scaler_y_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_y_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "anim_scaler_y"))
                anim_scaler_y_spnbox.grid(row=8, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="position_x").grid(row=9, column=0, sticky=tk.W)
                position_x_intvar = tk.IntVar(value=position_x)
                position_x_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_x_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "position_x"))
                position_x_spnbox.grid(row=9, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="position_y").grid(row=10, column=0, sticky=tk.W)
                position_y_intvar = tk.IntVar(value=position_y)
                position_y_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_y_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "position_y"))
                position_y_spnbox.grid(row=10, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="color_r").grid(row=11, column=0, sticky=tk.W)
                color_r_intvar = tk.IntVar(value=color_r)
                color_r_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=0, to=255, increment=1, textvariable=color_r_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "color_r"))
                color_r_spnbox.grid(row=11, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="color_g").grid(row=12, column=0, sticky=tk.W)
                color_g_intvar = tk.IntVar(value=color_g)
                color_g_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=0, to=255, increment=1, textvariable=color_g_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "color_g"))
                color_g_spnbox.grid(row=12, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="color_b").grid(row=13, column=0, sticky=tk.W)
                color_b_intvar = tk.IntVar(value=color_b)
                color_b_spnbox = tk.Spinbox(self.frame_textnode, state='normal', from_=0, to=255, increment=1, textvariable=color_b_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_text_" + str(node_text_count), "color_b"))
                color_b_spnbox.grid(row=13, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="visible").grid(row=14, column=0, sticky=tk.W)
                visible_strvar = tk.StringVar(value=visible)
                visible_entry = tk.Entry(self.frame_textnode, textvariable=visible_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_text_" + str(node_text_count), "visible"))
                visible_entry.grid(row=14, column=1, sticky=tk.W)

                tk.Label(self.frame_textnode, text="align").grid(row=15, column=0, sticky=tk.W)
                align_strvar = tk.StringVar(value=align)
                align_entry = tk.Entry(self.frame_textnode, textvariable=align_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_text_" + str(node_text_count), "align"))
                align_entry.grid(row=15, column=1, sticky=tk.W)


            node_text_count += 1


    def display_multitext(self):
        # -------------------------------------------------------------------
        #
        # < TEXT NODES >
        #
        # **** THIS OBJECTS WILL EXECUTE THE VALIDATION FUNCTION ! ****
        #
        #
        # GETTING CHILD ELEMENTS WHICH TAG NAME IS 'node_multitext'
        elem_node_multitexts = self.elem_scene.findall('node_multitext')

        node_multitext_count = 0

        # FOR ALL node_text

        self.frame_multitextnode_root = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.frame_multitextnode_root.pack(side=tk.LEFT, anchor=tk.NW)

        for node_multitext in elem_node_multitexts:

            if node_multitext is not None:
                # INITIALIZATION OF REQUIRED VALUES
                target_surface = \
                    name = \
                    text = \
                    text_size = \
                    anim_duration = \
                    anim_type = \
                    anim_scaler_x = \
                    anim_scaler_y = \
                    position_x = \
                    position_y = \
                    color_r = \
                    color_g = \
                    color_b = \
                    visible = \
                    align = \
                    line_margin = \
                    text_align = \
                    rotation = None

                keys = ["target_surface", "name", "text", "text_size", "anim_duration", "anim_type", "anim_scaler_x", "anim_scaler_y", "position_x", "position_y", "color_r", "color_g", "color_b", "visible", "align", "line_margin", "text_align", "rotation"]
                self.container['node_multitext_' + str(node_multitext_count)] = {key: None for key in keys}

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in node_multitext.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = str(value.attrib["target_surface"])
                        self.container['node_multitext_' + str(node_multitext_count)]['target_surface'] = target_surface
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                        self.container['node_multitext_' + str(node_multitext_count)]['name'] = name
                    elif "text" in value.attrib.keys():
                        text = str(value.attrib["text"])
                        self.container['node_multitext_' + str(node_multitext_count)]['text'] = text
                    elif "text_size" in value.attrib.keys():
                        text_size = int(value.attrib["text_size"])
                        self.container['node_multitext_' + str(node_multitext_count)]['text_size'] = text_size
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                        self.container['node_multitext_' + str(node_multitext_count)]['anim_duration'] = anim_duration
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                        self.container['node_multitext_' + str(node_multitext_count)]['anim_type'] = anim_type
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                        self.container['node_multitext_' + str(node_multitext_count)]['anim_scaler_x'] = anim_scaler_x
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                        self.container['node_multitext_' + str(node_multitext_count)]['anim_scaler_y'] = anim_scaler_y
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                        self.container['node_multitext_' + str(node_multitext_count)]['position_x'] = position_x
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                        self.container['node_multitext_' + str(node_multitext_count)]['position_y'] = position_y
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                        self.container['node_multitext_' + str(node_multitext_count)]['color_r'] = color_r
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                        self.container['node_multitext_' + str(node_multitext_count)]['color_g'] = color_g
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                        self.container['node_multitext_' + str(node_multitext_count)]['color_b'] = color_b
                    elif "visible" in value.attrib.keys():
                        visible = str(value.attrib["visible"])
                        self.container['node_multitext_' + str(node_multitext_count)]['visible'] = visible
                    elif "align" in value.attrib.keys():
                        align = value.attrib["align"]
                        self.container['node_multitext_' + str(node_multitext_count)]['align'] = align
                    elif "line_margin" in value.attrib.keys():
                        line_margin = value.attrib["line_margin"]
                        self.container['node_multitext_' + str(node_multitext_count)]['line_margin'] = line_margin
                    elif "text_align" in value.attrib.keys():
                        text_align = value.attrib["text_align"]
                        self.container['node_multitext_' + str(node_multitext_count)]['text_align'] = text_align
                    elif "rotation" in value.attrib.keys():
                        rotation = value.attrib["rotation"]
                        self.container['node_multitext_' + str(node_multitext_count)]['rotation'] = rotation


                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_multitextnode = tk.Frame(self.frame_multitextnode_root, bd=2, relief=tk.GROOVE)
                self.frame_multitextnode.pack(side=tk.LEFT, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_multitextnode, text="MULTITEXT").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_multitextnode, text="target_surface").grid(row=1, column=0, sticky=tk.W)
                target_surface_strvar = tk.StringVar(value=target_surface)
                target_surface_entry = tk.Entry(self.frame_multitextnode, textvariable=target_surface_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "target_surface"))
                target_surface_entry.grid(row=1, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="name").grid(row=2, column=0, sticky=tk.W)
                name_strvar = tk.StringVar(value=name)
                name_entry = tk.Entry(self.frame_multitextnode, textvariable=name_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "name"))
                name_entry.grid(row=2, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="text").grid(row=3, column=0, sticky=tk.W)
                text_strvar = tk.StringVar(value=text)
                text_entry = tk.Entry(self.frame_multitextnode, textvariable=text_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "text"))
                text_entry.grid(row=3, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="text_size").grid(row=4, column=0, sticky=tk.W)
                text_size_intvar = tk.StringVar(value=text_size)
                text_size_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', takefocus=False, from_=1, to=500, increment=1, textvariable=text_size_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "text_size"))
                text_size_spnbox.grid(row=4, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="anim_duration").grid(row=5, column=0, sticky=tk.W)
                anim_duration_intvar = tk.IntVar(value=anim_duration)
                anim_duration_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=1, to=1000000, increment=1, textvariable=anim_duration_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "anim_duration"))
                anim_duration_spnbox.grid(row=5, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="anim_type").grid(row=6, column=0, sticky=tk.W)
                anim_type_strvar = tk.StringVar(value=anim_type)
                anim_type_entry = tk.Entry(self.frame_multitextnode, textvariable=anim_type_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "anim_type"))
                anim_type_entry.grid(row=6, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="anim_scaler_x").grid(row=7, column=0, sticky=tk.W)
                anim_scaler_x_doublevar = tk.DoubleVar(value=anim_scaler_x)
                anim_scaler_x_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_x_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "anim_scaler_x"))
                anim_scaler_x_spnbox.grid(row=7, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="anim_scaler_y").grid(row=8, column=0, sticky=tk.W)
                anim_scaler_y_doublevar = tk.DoubleVar(value=anim_scaler_y)
                anim_scaler_y_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_y_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "anim_scaler_y"))
                anim_scaler_y_spnbox.grid(row=8, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="position_x").grid(row=9, column=0, sticky=tk.W)
                position_x_intvar = tk.IntVar(value=position_x)
                position_x_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_x_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "position_x"))
                position_x_spnbox.grid(row=9, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="position_y").grid(row=10, column=0, sticky=tk.W)
                position_y_intvar = tk.IntVar(value=position_y)
                position_y_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_y_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "position_y"))
                position_y_spnbox.grid(row=10, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="color_r").grid(row=11, column=0, sticky=tk.W)
                color_r_intvar = tk.IntVar(value=color_r)
                color_r_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=0, to=255, increment=1, textvariable=color_r_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "color_r"))
                color_r_spnbox.grid(row=11, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="color_g").grid(row=12, column=0, sticky=tk.W)
                color_g_intvar = tk.IntVar(value=color_g)
                color_g_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=0, to=255, increment=1, textvariable=color_g_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "color_g"))
                color_g_spnbox.grid(row=12, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="color_b").grid(row=13, column=0, sticky=tk.W)
                color_b_intvar = tk.IntVar(value=color_b)
                color_b_spnbox = tk.Spinbox(self.frame_multitextnode, state='normal', from_=0, to=255, increment=1, textvariable=color_b_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "node_multitext_" + str(node_multitext_count), "color_b"))
                color_b_spnbox.grid(row=13, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="visible").grid(row=14, column=0, sticky=tk.W)
                visible_strvar = tk.StringVar(value=visible)
                visible_entry = tk.Entry(self.frame_multitextnode, textvariable=visible_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "visible"))
                visible_entry.grid(row=14, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="align").grid(row=15, column=0, sticky=tk.W)
                align_strvar = tk.StringVar(value=align)
                align_entry = tk.Entry(self.frame_multitextnode, textvariable=align_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "align"))
                align_entry.grid(row=15, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="line_margin").grid(row=16, column=0, sticky=tk.W)
                line_margin_intvar = tk.IntVar(value=line_margin)
                line_margin_entry = tk.Entry(self.frame_multitextnode, textvariable=line_margin_intvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "line_margin"))
                line_margin_entry.grid(row=16, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="text_align").grid(row=17, column=0, sticky=tk.W)
                text_align_strvar = tk.StringVar(value=text_align)
                text_align_entry = tk.Entry(self.frame_multitextnode, textvariable=text_align_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "text_align"))
                text_align_entry.grid(row=17, column=1, sticky=tk.W)

                tk.Label(self.frame_multitextnode, text="rotation").grid(row=18, column=0, sticky=tk.W)
                rotation_strvar = tk.StringVar(value=rotation)
                rotation_entry = tk.Entry(self.frame_multitextnode, textvariable=rotation_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "node_multitext_" + str(node_multitext_count), "rotation"))
                rotation_entry.grid(row=18, column=1, sticky=tk.W)


            node_multitext_count += 1


    def display_picture(self):

        # -------------------------------------------------------------------
        #
        # < PIC NODES >
        #
        # **** THIS OBJECTS WILL EXECUTE THE VALIDATION FUNCTION ! ****
        #
        #
        # GETTING CHILD ELEMENTS WHICH TAG NAME IS 'node_text'
        elem_picures = self.elem_scene.findall('picture')

        picture_count = 0

        # FOR ALL node_text
        self.frame_picnode_root = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.frame_picnode_root.pack(side=tk.LEFT, anchor=tk.NW)

        for pic in elem_picures:


            if pic is not None:
                # INITIALIZATION OF REQUIRED VALUES
                target_surface = \
                    name = \
                    pic_file = \
                    pic_size = \
                    anim_duration = \
                    anim_type = \
                    anim_scaler_x = \
                    anim_scaler_y = \
                    position_x = \
                    position_y = \
                    rotation = \
                    visible = \
                    align = None


                keys = ["target_surface", "name", "pic_file", "pic_size", "anim_duration", "anim_type", "anim_scaler_x", "anim_scaler_y", "position_x", "position_y", "rotation", "visible", "align"]
                self.container['picture_' + str(picture_count)] = {key: None for key in keys}

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in pic.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = str(value.attrib["target_surface"])
                        self.container['picture_' + str(picture_count)]['target_surface'] = target_surface
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                        self.container['picture_' + str(picture_count)]['name'] = name
                    elif "pic_file" in value.attrib.keys():
                        pic_file = str(value.attrib["pic_file"])
                        self.container['picture_' + str(picture_count)]['text'] = pic_file
                    elif "pic_size" in value.attrib.keys():
                        pic_size = int(value.attrib["pic_size"])
                        self.container['picture_' + str(picture_count)]['text_size'] = pic_size
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                        self.container['picture_' + str(picture_count)]['anim_duration'] = anim_duration
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                        self.container['picture_' + str(picture_count)]['anim_type'] = anim_type
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                        self.container['picture_' + str(picture_count)]['anim_scaler_x'] = anim_scaler_x
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                        self.container['picture_' + str(picture_count)]['anim_scaler_y'] = anim_scaler_y
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                        self.container['picture_' + str(picture_count)]['position_x'] = position_x
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                        self.container['picture_' + str(picture_count)]['position_y'] = position_y
                    elif "rotation" in value.attrib.keys():
                        rotation = int(value.attrib["rotation"])
                        self.container['picture_' + str(picture_count)]['rotation'] = rotation
                    elif "visible" in value.attrib.keys():
                        visible = bool(value.attrib["visible"])
                        self.container['picture_' + str(picture_count)]['visible'] = visible
                    elif "align" in value.attrib.keys():
                        align = value.attrib["align"]
                        self.container['picture_' + str(picture_count)]['align'] = align



                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_picnode = tk.Frame(self.frame_picnode_root, bd=2, relief=tk.GROOVE)
                self.frame_picnode.pack(side=tk.LEFT, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_picnode, text="PIC NODE").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_picnode, text="target_surface").grid(row=1, column=0, sticky=tk.W)
                target_surface_strvar = tk.StringVar(value=target_surface)
                target_surface_entry = tk.Entry(self.frame_picnode, textvariable=target_surface_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "target_surface"))
                target_surface_entry.grid(row=1, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="name").grid(row=2, column=0, sticky=tk.W)
                name_strvar = tk.StringVar(value=name)
                name_entry = tk.Entry(self.frame_picnode, textvariable=name_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "name"))
                name_entry.grid(row=2, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="pic_file").grid(row=3, column=0, sticky=tk.W)
                pic_file_strvar = tk.StringVar(value=pic_file)
                pic_file_entry = tk.Entry(self.frame_picnode, textvariable=pic_file_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "pic_file"))
                pic_file_entry.grid(row=3, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="pic_size").grid(row=4, column=0, sticky=tk.W)
                pic_size_intvar = tk.StringVar(value=pic_size)
                pic_size_spnbox = tk.Spinbox(self.frame_picnode, state='normal', takefocus=False, from_=1, to=500, increment=1, textvariable=pic_size_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "picture_" + str(picture_count), "pic_size"))
                pic_size_spnbox.grid(row=4, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="anim_duration").grid(row=5, column=0, sticky=tk.W)
                anim_duration_intvar = tk.IntVar(value=anim_duration)
                anim_duration_spnbox = tk.Spinbox(self.frame_picnode, state='normal', from_=1, to=1000000, increment=1, textvariable=anim_duration_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "picture_" + str(picture_count), "anim_duration"))
                anim_duration_spnbox.grid(row=5, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="anim_type").grid(row=6, column=0, sticky=tk.W)
                anim_type_strvar = tk.StringVar(value=anim_type)
                anim_type_entry = tk.Entry(self.frame_picnode, textvariable=anim_type_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "anim_type"))
                anim_type_entry.grid(row=6, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="anim_scaler_x").grid(row=7, column=0, sticky=tk.W)
                anim_scaler_x_doublevar = tk.DoubleVar(value=anim_scaler_x)
                anim_scaler_x_spnbox = tk.Spinbox(self.frame_picnode, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_x_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "picture_" + str(picture_count), "anim_scaler_x"))
                anim_scaler_x_spnbox.grid(row=7, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="anim_scaler_y").grid(row=8, column=0, sticky=tk.W)
                anim_scaler_y_doublevar = tk.DoubleVar(value=anim_scaler_y)
                anim_scaler_y_spnbox = tk.Spinbox(self.frame_picnode, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_y_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "picture_" + str(picture_count), "anim_scaler_y"))
                anim_scaler_y_spnbox.grid(row=8, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="position_x").grid(row=9, column=0, sticky=tk.W)
                position_x_intvar = tk.IntVar(value=position_x)
                position_x_spnbox = tk.Spinbox(self.frame_picnode, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_x_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "picture_" + str(picture_count), "position_x"))
                position_x_spnbox.grid(row=9, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="position_y").grid(row=10, column=0, sticky=tk.W)
                position_y_intvar = tk.IntVar(value=position_y)
                position_y_spnbox = tk.Spinbox(self.frame_picnode, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_y_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "picture_" + str(picture_count), "position_y"))
                position_y_spnbox.grid(row=10, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="rotation").grid(row=11, column=0, sticky=tk.W)
                rotation_strvar = tk.StringVar(value=rotation)
                rotation_entry = tk.Entry(self.frame_picnode, textvariable=rotation_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "rotation"))
                rotation_entry.grid(row=11, column=1, sticky=tk.W)

                tk.Label(self.frame_picnode, text="visible").grid(row=12, column=0, sticky=tk.W)
                visible_cmbbox = ttk.Combobox(self.frame_picnode, values=["False", "True"], validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "visible"))
                visible_cmbbox.grid(row=12, column=1, sticky=tk.W)
                visible_cmbbox.current(int(visible))

                tk.Label(self.frame_picnode, text="align").grid(row=13, column=0, sticky=tk.W)
                align_strvar = tk.StringVar(value=align)
                align_entry = tk.Entry(self.frame_picnode, textvariable=align_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "picture_" + str(picture_count), "align"))
                align_entry.grid(row=13, column=1, sticky=tk.W)


            picture_count += 1


    def display_clickable(self):

        # -------------------------------------------------------------------
        #
        # < SETTING CLICKABLE >
        #
        elem_clickable = self.elem_scene.findall('clickable')

        if elem_clickable is not None:
            # < INITIALIZE DICTIONARY WITH KEYS >
            # https://stackoverflow.com/questions/2241891/how-to-initialize-a-dict-with-keys-from-a-list-and-empty-value-in-python
            keys = ["mode"]
            self.container['clickable'] = {key: None for key in keys}

            for flag_elem in elem_clickable:
                attrib = str(flag_elem.attrib["mode"])
                self.container['clickable']['mode'] = attrib

                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_clickable = tk.Frame(self.main_frame_other, bd=2, relief=tk.GROOVE)
                self.frame_clickable.pack(side=tk.TOP, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_clickable, text="CLICKABLE").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_clickable, text="clickable").grid(row=1, column=0, sticky=tk.W)
                clickable_strvar = tk.StringVar(value=attrib)
                clickable_entry = tk.Entry(self.frame_clickable, textvariable=clickable_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "clickable", "mode"))
                clickable_entry.grid(row=1, column=1, sticky=tk.W)


    def display_indicator(self):

        # -------------------------------------------------------------------
        #
        # < INDICATORS >
        #
        elem_indicators = self.elem_scene.findall('indicator')

        indicator_count = 0

        # FOR ALL node_text
        self.frame_indicator_root = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.frame_indicator_root.pack(side=tk.LEFT, anchor=tk.NW)

        for indicator in elem_indicators:

            if indicator is not None:
                # INITIALIZATION OF REQUIRED VALUES
                target_surface = \
                    name = \
                    shape = \
                    size_w = \
                    size_h = \
                    anim_duration = \
                    anim_type = \
                    anim_scaler_x = \
                    anim_scaler_y = \
                    position_x = \
                    position_y = \
                    center_x = \
                    center_y = \
                    color_r = \
                    color_g = \
                    color_b = \
                    freq = \
                    style = None


                # < INITIALIZE DICTIONARY WITH KEYS >
                # https://stackoverflow.com/questions/2241891/how-to-initialize-a-dict-with-keys-from-a-list-and-empty-value-in-python
                keys = ["target_surface", "name", "shape", "size_w", "size_h", "anim_duration", "anim_type", "anim_scaler_x", "anim_scaler_y", "position_x", "position_y", "center_x", "center_y", "color_r", "color_g", "color_b", "freq", "style"]
                self.container['indicator_' + str(indicator_count)] = {key: None for key in keys}


                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in indicator.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = str(value.attrib["target_surface"])
                        self.container['indicator_' + str(indicator_count)]['target_surface'] = target_surface
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                        self.container['indicator_' + str(indicator_count)]['name'] = name
                    elif "shape" in value.attrib.keys():
                        shape = str(value.attrib["shape"])
                        self.container['indicator_' + str(indicator_count)]['shape'] = shape
                    elif "size_w" in value.attrib.keys():
                        size_w = int(value.attrib["size_w"])
                        self.container['indicator_' + str(indicator_count)]['size_w'] = size_w
                    elif "size_h" in value.attrib.keys():
                        size_h = int(value.attrib["size_h"])
                        self.container['indicator_' + str(indicator_count)]['size_h'] = size_h
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                        self.container['indicator_' + str(indicator_count)]['anim_duration'] = anim_duration
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                        self.container['indicator_' + str(indicator_count)]['anim_type'] = anim_type
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                        self.container['indicator_' + str(indicator_count)]['anim_scaler_x'] = anim_scaler_x
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                        self.container['indicator_' + str(indicator_count)]['anim_scaler_y'] = anim_scaler_y
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                        self.container['indicator_' + str(indicator_count)]['position_x'] = position_x
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                        self.container['indicator_' + str(indicator_count)]['position_y'] = position_y
                    elif "center_x" in value.attrib.keys():
                        center_x = int(value.attrib["center_x"])
                        self.container['indicator_' + str(indicator_count)]['center_x'] = center_x
                    elif "center_y" in value.attrib.keys():
                        center_y = int(value.attrib["center_y"])
                        self.container['indicator_' + str(indicator_count)]['center_y'] = center_y
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                        self.container['indicator_' + str(indicator_count)]['color_r'] = color_r
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                        self.container['indicator_' + str(indicator_count)]['color_g'] = color_g
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                        self.container['indicator_' + str(indicator_count)]['color_b'] = color_b
                    elif "freq" in value.attrib.keys():
                        freq = float(value.attrib["freq"])
                        self.container['indicator_' + str(indicator_count)]['freq'] = freq
                    elif "style" in value.attrib.keys():
                        style = str(value.attrib["style"])
                        self.container['indicator_' + str(indicator_count)]['style'] = style




                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_indicator = tk.Frame(self.frame_indicator_root, bd=2, relief=tk.GROOVE)
                self.frame_indicator.pack(side=tk.LEFT, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_indicator, text="INDICATOR").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_indicator, text="target_surface").grid(row=1, column=0, sticky=tk.W)
                target_surface_strvar = tk.StringVar(value=target_surface)
                target_surface_entry = tk.Entry(self.frame_indicator, textvariable=target_surface_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "indicator_" + str(indicator_count), "target_surface"))
                target_surface_entry.grid(row=1, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="name").grid(row=2, column=0, sticky=tk.W)
                name_strvar = tk.StringVar(value=name)
                name_entry = tk.Entry(self.frame_indicator, textvariable=name_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "indicator_" + str(indicator_count), "name"))
                name_entry.grid(row=2, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="shape").grid(row=3, column=0, sticky=tk.W)
                shape_strvar = tk.StringVar(value=shape)
                shape_entry = tk.Entry(self.frame_indicator, textvariable=shape_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "indicator_" + str(indicator_count), "shape"))
                shape_entry.grid(row=3, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="size_w").grid(row=4, column=0, sticky=tk.W)
                size_w_intvar = tk.StringVar(value=size_w)
                size_w_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=1, to=5000, increment=1, textvariable=size_w_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "size_w"))
                size_w_spnbox.grid(row=4, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="size_h").grid(row=5, column=0, sticky=tk.W)
                size_h_intvar = tk.StringVar(value=size_h)
                size_h_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=1, to=5000, increment=1, textvariable=size_h_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "size_h"))
                size_h_spnbox.grid(row=5, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="anim_duration").grid(row=6, column=0, sticky=tk.W)
                anim_duration_intvar = tk.IntVar(value=anim_duration)
                anim_duration_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=1, to=1000000, increment=1, textvariable=anim_duration_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "anim_duration"))
                anim_duration_spnbox.grid(row=6, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="anim_type").grid(row=7, column=0, sticky=tk.W)
                anim_type_strvar = tk.StringVar(value=anim_type)
                anim_type_entry = tk.Entry(self.frame_indicator, textvariable=anim_type_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "indicator_" + str(indicator_count), "anim_type"))
                anim_type_entry.grid(row=7, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="anim_scaler_x").grid(row=8, column=0, sticky=tk.W)
                anim_scaler_x_doublevar = tk.DoubleVar(value=anim_scaler_x)
                anim_scaler_x_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_x_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "anim_scaler_x"))
                anim_scaler_x_spnbox.grid(row=8, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="anim_scaler_y").grid(row=9, column=0, sticky=tk.W)
                anim_scaler_y_doublevar = tk.DoubleVar(value=anim_scaler_y)
                anim_scaler_y_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_y_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "anim_scaler_y"))
                anim_scaler_y_spnbox.grid(row=9, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="position_x").grid(row=10, column=0, sticky=tk.W)
                position_x_intvar = tk.IntVar(value=position_x)
                position_x_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_x_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "position_x"))
                position_x_spnbox.grid(row=10, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="position_y").grid(row=11, column=0, sticky=tk.W)
                position_y_intvar = tk.IntVar(value=position_y)
                position_y_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_y_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "position_y"))
                position_y_spnbox.grid(row=11, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="center_x").grid(row=12, column=0, sticky=tk.W)
                center_x_intvar = tk.IntVar(value=center_x)
                center_x_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=-10000, to=10000, increment=1, textvariable=center_x_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "center_x"))
                center_x_spnbox.grid(row=12, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="center_y").grid(row=13, column=0, sticky=tk.W)
                center_y_intvar = tk.IntVar(value=center_y)
                center_y_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=-10000, to=10000, increment=1, textvariable=center_y_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "center_y"))
                center_y_spnbox.grid(row=13, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="color_r").grid(row=14, column=0, sticky=tk.W)
                color_r_intvar = tk.IntVar(value=color_r)
                color_r_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=0, to=255, increment=1, textvariable=color_r_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "color_r"))
                color_r_spnbox.grid(row=14, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="color_g").grid(row=15, column=0, sticky=tk.W)
                color_g_intvar = tk.IntVar(value=color_g)
                color_g_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=0, to=255, increment=1, textvariable=color_g_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "color_g"))
                color_g_spnbox.grid(row=15, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="color_b").grid(row=16, column=0, sticky=tk.W)
                color_b_intvar = tk.IntVar(value=color_b)
                color_b_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=0, to=255, increment=1, textvariable=color_b_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "color_b"))
                color_b_spnbox.grid(row=16, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="freq").grid(row=17, column=0, sticky=tk.W)
                freq_doublevar = tk.DoubleVar(value=freq)
                freq_spnbox = tk.Spinbox(self.frame_indicator, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=freq_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "indicator_" + str(indicator_count), "freq"))
                freq_spnbox.grid(row=17, column=1, sticky=tk.W)

                tk.Label(self.frame_indicator, text="style").grid(row=18, column=0, sticky=tk.W)
                style_strvar = tk.StringVar(value=style)
                style_entry = tk.Entry(self.frame_indicator, textvariable=style_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "indicator_" + str(indicator_count), "style"))
                style_entry.grid(row=18, column=1, sticky=tk.W)

            indicator_count += 1


    def display_line(self):

        # -------------------------------------------------------------------
        #
        # < LINES >
        #
        elem_lines = self.elem_scene.findall('line')

        line_count = 0

        # FOR ALL node_text
        self.frame_line_root = tk.Frame(self.main_frame, bd=2, relief=tk.GROOVE)
        self.frame_line_root.pack(side=tk.LEFT, anchor=tk.NW)

        for line in elem_lines:

            if line is not None:
                # INITIALIZATION OF REQUIRED VALUES
                target_surface = \
                    name = \
                    type = \
                    vertices = \
                    anim_duration = \
                    anim_type = \
                    anim_scaler_x = \
                    anim_scaler_y = \
                    position_x = \
                    position_y = \
                    color_r = \
                    color_g = \
                    color_b = \
                    freq = \
                    style = \
                    view_cv = \
                    arrow_scale = \
                    arrow_adjust = \
                    arrow_visible = \
                    adding_direction_x = \
                    adding_direction_y = None


                # < INITIALIZE DICTIONARY WITH KEYS >
                # https://stackoverflow.com/questions/2241891/how-to-initialize-a-dict-with-keys-from-a-list-and-empty-value-in-python
                keys = ["target_surface", "name", "type", "vertices", "anim_duration", "anim_type", "anim_scaler_x", "anim_scaler_y", "position_x", "position_y", "color_r", "color_g", "color_b", "freq", "style", "view_cv", "arrow_scale", "arrow_adjust", "arrow_visible", "adding_direction_x", "adding_direction_y"]
                self.container['line_' + str(line_count)] = {key: None for key in keys}


                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in line.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = str(value.attrib["target_surface"])
                        self.container['line_' + str(line_count)]['target_surface'] = target_surface
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                        self.container['line_' + str(line_count)]['name'] = name
                    elif "type" in value.attrib.keys():
                        type = str(value.attrib["type"])
                        self.container['line_' + str(line_count)]['type'] = type

                    elif "vertices" in value.attrib.keys():
                        vertices = value.attrib["vertices"]
                        self.container['line_' + str(line_count)]['vertices'] = vertices

                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                        self.container['line_' + str(line_count)]['anim_duration'] = anim_duration
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                        self.container['line_' + str(line_count)]['anim_type'] = anim_type
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                        self.container['line_' + str(line_count)]['anim_scaler_x'] = anim_scaler_x
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                        self.container['line_' + str(line_count)]['anim_scaler_y'] = anim_scaler_y
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                        self.container['line_' + str(line_count)]['position_x'] = position_x
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                        self.container['line_' + str(line_count)]['position_y'] = position_y
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                        self.container['line_' + str(line_count)]['color_r'] = color_r
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                        self.container['line_' + str(line_count)]['color_g'] = color_g
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                        self.container['line_' + str(line_count)]['color_b'] = color_b
                    elif "freq" in value.attrib.keys():
                        freq = float(value.attrib["freq"])
                        self.container['line_' + str(line_count)]['freq'] = freq
                    elif "style" in value.attrib.keys():
                        style = str(value.attrib["style"])
                        self.container['line_' + str(line_count)]['style'] = style
                    elif "view_cv" in value.attrib.keys():
                        view_cv = str(value.attrib["view_cv"])
                        self.container['line_' + str(line_count)]['view_cv'] = view_cv
                    elif "arrow_scale" in value.attrib.keys():
                        arrow_scale = float(value.attrib["arrow_scale"])
                        self.container['line_' + str(line_count)]['arrow_scale'] = arrow_scale
                    elif "arrow_adjust" in value.attrib.keys():
                        arrow_adjust = float(value.attrib["arrow_adjust"])
                        self.container['line_' + str(line_count)]['arrow_adjust'] = arrow_adjust
                    elif "arrow_visible" in value.attrib.keys():
                        arrow_visible = str(value.attrib["arrow_visible"])
                        self.container['line_' + str(line_count)]['arrow_visible'] = arrow_visible
                    elif "adding_direction_x" in value.attrib.keys():
                        adding_direction_x = str(value.attrib["adding_direction_x"])
                        self.container['line_' + str(line_count)]['adding_direction_x'] = adding_direction_x
                    elif "adding_direction_y" in value.attrib.keys():
                        adding_direction_y = str(value.attrib["adding_direction_y"])
                        self.container['line_' + str(line_count)]['adding_direction_y'] = adding_direction_y

                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_line = tk.Frame(self.frame_line_root, bd=2, relief=tk.GROOVE)
                self.frame_line.pack(side=tk.LEFT, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_line, text="LINE").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_line, text="target_surface").grid(row=1, column=0, sticky=tk.W)
                target_surface_strvar = tk.StringVar(value=target_surface)
                target_surface_entry = tk.Entry(self.frame_line, textvariable=target_surface_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "target_surface"))
                target_surface_entry.grid(row=1, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="name").grid(row=2, column=0, sticky=tk.W)
                name_strvar = tk.StringVar(value=name)
                name_entry = tk.Entry(self.frame_line, textvariable=name_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "name"))
                name_entry.grid(row=2, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="type").grid(row=3, column=0, sticky=tk.W)
                type_strvar = tk.StringVar(value=type)
                type_entry = tk.Entry(self.frame_line, textvariable=type_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "type"))
                type_entry.grid(row=3, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="vertices").grid(row=4, column=0, sticky=tk.W)
                vertices_strvar = tk.StringVar(value=vertices)
                vertices_entry = tk.Entry(self.frame_line, textvariable=vertices_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "vertices"))
                vertices_entry.grid(row=4, column=1, sticky=tk.W)


                tk.Label(self.frame_line, text="anim_duration").grid(row=5, column=0, sticky=tk.W)
                anim_duration_intvar = tk.IntVar(value=anim_duration)
                anim_duration_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=1, to=1000000, increment=1, textvariable=anim_duration_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "anim_duration"))
                anim_duration_spnbox.grid(row=5, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="anim_type").grid(row=6, column=0, sticky=tk.W)
                anim_type_strvar = tk.StringVar(value=anim_type)
                anim_type_entry = tk.Entry(self.frame_line, textvariable=anim_type_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "anim_type"))
                anim_type_entry.grid(row=6, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="anim_scaler_x").grid(row=7, column=0, sticky=tk.W)
                anim_scaler_x_doublevar = tk.DoubleVar(value=anim_scaler_x)
                anim_scaler_x_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_x_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "anim_scaler_x"))
                anim_scaler_x_spnbox.grid(row=7, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="anim_scaler_y").grid(row=8, column=0, sticky=tk.W)
                anim_scaler_y_doublevar = tk.DoubleVar(value=anim_scaler_y)
                anim_scaler_y_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=anim_scaler_y_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "anim_scaler_y"))
                anim_scaler_y_spnbox.grid(row=8, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="position_x").grid(row=9, column=0, sticky=tk.W)
                position_x_intvar = tk.IntVar(value=position_x)
                position_x_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_x_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "position_x"))
                position_x_spnbox.grid(row=9, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="position_y").grid(row=10, column=0, sticky=tk.W)
                position_y_intvar = tk.IntVar(value=position_y)
                position_y_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=-10000, to=10000, increment=1, textvariable=position_y_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "position_y"))
                position_y_spnbox.grid(row=10, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="color_r").grid(row=11, column=0, sticky=tk.W)
                color_r_intvar = tk.IntVar(value=color_r)
                color_r_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=0, to=255, increment=1, textvariable=color_r_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "color_r"))
                color_r_spnbox.grid(row=11, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="color_g").grid(row=12, column=0, sticky=tk.W)
                color_g_intvar = tk.IntVar(value=color_g)
                color_g_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=0, to=255, increment=1, textvariable=color_g_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "color_g"))
                color_g_spnbox.grid(row=12, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="color_b").grid(row=13, column=0, sticky=tk.W)
                color_b_intvar = tk.IntVar(value=color_b)
                color_b_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=0, to=255, increment=1, textvariable=color_b_intvar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "color_b"))
                color_b_spnbox.grid(row=13, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="freq").grid(row=14, column=0, sticky=tk.W)
                freq_doublevar = tk.DoubleVar(value=freq)
                freq_spnbox = tk.Spinbox(self.frame_line, state='normal', from_=0.0, to=255.0, increment=0.1, textvariable=freq_doublevar, validate="all", validatecommand=(self.val_cmd_spinbox, "%V", "%P", "line_" + str(line_count), "freq"))
                freq_spnbox.grid(row=14, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="style").grid(row=15, column=0, sticky=tk.W)
                style_strvar = tk.StringVar(value=style)
                style_entry = tk.Entry(self.frame_line, textvariable=style_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "style"))
                style_entry.grid(row=15, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="view_cv").grid(row=16, column=0, sticky=tk.W)
                view_cv_strvar = tk.StringVar(value=view_cv)
                view_cv_entry = tk.Entry(self.frame_line, textvariable=view_cv_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "view_cv"))
                view_cv_entry.grid(row=16, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="arrow_scale").grid(row=17, column=0, sticky=tk.W)
                arrow_scale_doublevar = tk.DoubleVar(value=arrow_scale)
                arrow_scale_entry = tk.Entry(self.frame_line, textvariable=arrow_scale_doublevar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "arrow_scale"))
                arrow_scale_entry.grid(row=17, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="arrow_adjust").grid(row=18, column=0, sticky=tk.W)
                arrow_adjust_doublevar = tk.DoubleVar(value=arrow_adjust)
                arrow_adjust_entry = tk.Entry(self.frame_line, textvariable=arrow_adjust_doublevar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "arrow_adjust"))
                arrow_adjust_entry.grid(row=18, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="arrow_visible").grid(row=19, column=0, sticky=tk.W)
                arrow_visible_strvar = tk.StringVar(value=arrow_visible)
                arrow_visible_entry = tk.Entry(self.frame_line, textvariable=arrow_visible_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "arrow_visible"))
                arrow_visible_entry.grid(row=19, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="adding_direction_x").grid(row=20, column=0, sticky=tk.W)
                adding_direction_x_strvar = tk.DoubleVar(value=adding_direction_x)
                adding_direction_x_entry = tk.Entry(self.frame_line, textvariable=adding_direction_x_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "adding_direction_x"))
                adding_direction_x_entry.grid(row=20, column=1, sticky=tk.W)

                tk.Label(self.frame_line, text="adding_direction_y").grid(row=21, column=0, sticky=tk.W)
                adding_direction_y_strvar = tk.DoubleVar(value=adding_direction_y)
                adding_direction_y_entry = tk.Entry(self.frame_line, textvariable=adding_direction_y_strvar, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "line_" + str(line_count), "adding_direction_y"))
                adding_direction_y_entry.grid(row=21, column=1, sticky=tk.W)

            line_count += 1


    def display_nav_button(self):

        # -------------------------------------------------------------------
        #
        # < NAVI BUTTONS >
        #
        # CREATING NAV BUTTON
        elem_nav_buttons = self.elem_scene.findall('nav_buttons')

        if elem_nav_buttons is not None:
            keys = ['mode']
            self.container['nav_buttons'] = {key: None for key in keys}

            for nav_button in elem_nav_buttons:
                attrib = nav_button.attrib["mode"]
                self.container['nav_buttons']['mode'] = attrib

                # ------------------------------------------------------------------------------------------------

                # < GUI SETTINGS >

                # FRAME FOR TEXT NODES
                self.frame_nav_buttons = tk.Frame(self.main_frame_other, bd=2, relief=tk.GROOVE)
                self.frame_nav_buttons.pack(side=tk.TOP, anchor=tk.NW)

                # LABEL SETTING FOR DRAWPAD
                tk.Label(self.frame_nav_buttons, text="NAV_BUTTONS").grid(row=0, column=0, sticky=tk.W)

                # ELEMENTS
                tk.Label(self.frame_nav_buttons, text="visible").grid(row=1, column=0, sticky=tk.W)
                values = ["Function", "Manual"]
                visible_cmbbox = ttk.Combobox(self.frame_nav_buttons, values=values, validate="all", validatecommand=(self.val_cmd_allothers, "%V", "%P", "nav_buttons", "mode"))
                visible_cmbbox.grid(row=1, column=1, sticky=tk.W)
                visible_cmbbox.current(values.index(attrib))


    # DISPLAY THE DATA WE GOT TO PROPER WIDGETS IN TKINTER
    def display_current_scene_xml(self):

        self.display_drawpad()
        self.display_duplicator()
        self.display_text()
        self.display_multitext()
        self.display_picture()
        self.display_clickable()
        self.display_indicator()
        self.display_line()
        self.display_nav_button()




    # ------------------------------------------------------------------
    #
    # < MESSAGE MANAGEMENT >

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
            #####print(f'++++ SUB PROCESS ::  ----------------check_for_scene_number == ScnCurrent_ --  {self.msg_from_main[11:]}')

            # SLICING THE STRING AND RETRIEVE THE SCENE NUMBER ONLY
            self.scene_number = int(message[11:])
            # SETTING THE SCENE NUMBER
            self.set_scene_number_current(self.scene_number)

        # IF THE SCENE WAS CHANGED IN MAIN PROCESS...
        elif 'SCENE_CHANGED_TO_' in message:

            # RELOAD THE WIDGETS

            # SLICING THE STRING AND RETRIEVE THE SCENE NUMBER ONLY
            self.scene_number = int(message[17:])
            #####print(f'++++ SUB PROCESS ::  ---------------- MESSAGE << SCENE_CHANGED_TO_ >> RECEIVED --  self.scene_number  --   {self.scene_number}')

            # DELETE ALL WIDGETS
            self.delete_all_widgets()
            #####print(f'++++ SUB PROCESS ::  ---------------- MESSAGE << SCENE_CHANGED_TO_ >> RECEIVED --  DELETED ALL WIDGETS')

            # SETTING UP THE MENU
            self.create_main_gui()
            #####print(f'++++ SUB PROCESS ::  ---------------- MESSAGE << SCENE_CHANGED_TO_ >> RECEIVED --  RE-CREATED TKINTER MENU')



    # ---------------------------------------------------------------
    #
    # < SAVING SCENE DATA TO XML >

    def save_to_xml(self, xml_tagname, xml_valuename, value):
        #####print("SAVE TO XML !!!!")

        # ------------------------------------------------------------------------------------
        # APPLY CHANGES TO CONTAINER DICTIONARY
        #
        # USING update() FUNCTION OF BUILT-IN FUNCTION
        # https://www.programiz.com/python-programming/methods/dictionary/update
        #
        data_to_update = {xml_valuename: value}
        self.container[xml_tagname].update(data_to_update)
        #print(self.container)


        # ------------------------------------------------------------------------------------
        # MODIFY XML
        self.elem_scene = self.modify_xml(self.elem_scene, xml_tagname, xml_valuename, value)


        # ------------------------------------------------------------------------------------
        # EXPORT TO XML FILE
        #
        # < WRITING XML WITH UTF-8 >
        # https://stackoverflow.com/questions/10046755/write-xml-utf-8-file-with-utf-8-data-with-elementtree
        #
        self.xmlconnector.xml_tree.write('xml_scenes/scenes_xml.xml', encoding="UTF-8", xml_declaration=True)


        # SEND MESSAGE TO MAIN PROCESS FOR RELOADING THE SCENE
        self.pipe_send.send('Reload_CurrentScene_' + str(self.scene_number))


        #####print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #####print(f'++++             SCENE NUMBER -- {self.scene_number}                                ++++')
        #####print(f'++++             SUB PROCESS ::  save_to_xml                   ++++')
        #####print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")



    def modify_xml(self, target_elem, xml_tagname, xml_valuename, value):

        # TODO :: SEARCHING METHOD SHOULD BE STORED TO SEPERATED FUNCTION
        # < SPECIFY THE ELEMENT >

        # IF 'node_text' STRING IS IN THE TAGNAME STRING...
        if 'node_text' in xml_tagname:

            # SPECIFYING node_text INDEX NUMBER
            modified_node_text_number = int(xml_tagname[10:])

            # GETTING ALL node_text ELEMENTS FROM XML
            elem_node_texts = target_elem.findall('node_text')

            # FOR ALL node_text IN THE XML...
            for node_text in elem_node_texts:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if node_text is not None and \
                        int(node_text.get('number')) == modified_node_text_number:

                    # FOR ALL VALUE-TAGS IN THE node_text ELEMENT...
                    for value_elem in node_text.findall('value'):

                        # IF THE VALUE TAG ELEMEMT EXISTS...
                        if xml_valuename in value_elem.attrib.keys():
                            # SET THE VALUE TO THAT ELEMENT
                            value_elem.set(xml_valuename, value)


        # IF 'node_multitext' STRING IS IN THE TAGNAME STRING...
        elif 'node_multitext' in xml_tagname:

            # SPECIFYING node_text INDEX NUMBER
            modified_node_multitext_number = int(xml_tagname[15:])

            # GETTING ALL node_text ELEMENTS FROM XML
            elem_node_multitexts = target_elem.findall('node_multitext')

            # FOR ALL node_text IN THE XML...
            for node_multitext in elem_node_multitexts:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if node_multitext is not None and \
                        int(node_multitext.get('number')) == modified_node_multitext_number:

                    # FOR ALL VALUE-TAGS IN THE node_text ELEMENT...
                    for value_elem in node_multitext.findall('value'):

                        # IF THE VALUE TAG ELEMEMT EXISTS...
                        if xml_valuename in value_elem.attrib.keys():
                            # SET THE VALUE TO THAT ELEMENT
                            value_elem.set(xml_valuename, value)

        # IF 'picture' STRING IS IN THE TAGNAME STRING...
        elif 'picture' in xml_tagname:

            # SPECIFYING node_text INDEX NUMBER
            modified_pic_number = int(xml_tagname[8:])

            # GETTING ALL node_text ELEMENTS FROM XML
            elem_pics = target_elem.findall('picture')

            # FOR ALL node_text IN THE XML...
            for pic in elem_pics:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if pic is not None and \
                        int(pic.get('number')) == modified_pic_number:

                    # FOR ALL VALUE-TAGS IN THE picture ELEMENT...
                    for value_elem in pic.findall('value'):

                        # IF THE VALUE TAG ELEMEMT EXISTS...
                        if xml_valuename in value_elem.attrib.keys():
                            # SET THE VALUE TO THAT ELEMENT
                            value_elem.set(xml_valuename, value)

        # IF 'indicator' STRING IS IN THE TAGNAME STRING...
        elif 'indicator' in xml_tagname:

            # SPECIFYING indicator INDEX NUMBER
            modified_indicator_number = int(xml_tagname[10:])

            # GETTING ALL indicator ELEMENTS FROM XML
            elem_indicators = target_elem.findall('indicator')

            # FOR ALL indicator IN THE XML...
            for indicator in elem_indicators:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if indicator is not None and \
                        int(indicator.get('number')) == modified_indicator_number:

                    # FOR ALL VALUE-TAGS IN THE node_text ELEMENT...
                    for value_elem in indicator.findall('value'):

                        # IF THE VALUE TAG ELEMEMT EXISTS...
                        if xml_valuename in value_elem.attrib.keys():
                            # SET THE VALUE TO THAT ELEMENT
                            value_elem.set(xml_valuename, value)

        # IF 'line' STRING IS IN THE TAGNAME STRING...
        elif 'line' in xml_tagname:

            # SPECIFYING indicator INDEX NUMBER
            modified_line_number = int(xml_tagname[5:])

            # GETTING ALL indicator ELEMENTS FROM XML
            elem_lines = target_elem.findall('line')

            # FOR ALL indicator IN THE XML...
            for line in elem_lines:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if line is not None and \
                        int(line.get('number')) == modified_line_number:

                    # FOR ALL VALUE-TAGS IN THE node_text ELEMENT...
                    for value_elem in line.findall('value'):

                        # IF THE VALUE TAG ELEMEMT EXISTS...
                        if xml_valuename in value_elem.attrib.keys():
                            # SET THE VALUE TO THAT ELEMENT
                            value_elem.set(xml_valuename, value)

        # IF 'clickable' STRING IS IN THE TAGNAME STRING...
        elif 'clickable' in xml_tagname:

            # GETTING ALL node_text ELEMENTS FROM XML
            elem_clickables = target_elem.findall('clickable')

            # FOR ALL node_text IN THE XML...
            for clickable in elem_clickables:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if clickable is not None:
                    # SET THE VALUE TO THAT ELEMENT
                    clickable.set(xml_valuename, value)

        # IF 'nav_buttons' STRING IS IN THE TAGNAME STRING...
        elif 'nav_buttons' in xml_tagname:

            # GETTING ALL nav_buttons ELEMENTS FROM XML
            elem_nav_buttons = target_elem.findall('nav_buttons')

            # FOR ALL nav_buttons IN THE XML...
            for nav_button in elem_nav_buttons:

                # IF THE ELEMENT IS NOT None AND
                # number ATTRIBUTE OF THE XML IS SAME AS THE INDEX WE SPECIFIED ABOVE...
                if nav_button is not None:
                    # SET THE VALUE TO THAT ELEMENT
                    nav_button.set(xml_valuename, value)


        return target_elem


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



    # AFTER WE SENT THE REQUEST MESSAGE
    # AND THEN RECEIVED THE CURRENT SCENE NUMBER,
    # LOAD AND DISPLAY THE DATA WITH TKINTER
    def set_scene_number_current(self, number):
        """ SETTING CURRENT SCENE NUMBER """
        self.scene_number = number

        # **** SCENE NUMBER 1 IS FILTERED HERE !!!!

        if self.scene_number == 1:
            #####print("++++ SUB PROCESS :: SCENE NUMBER 1 CANNOT BE EDITED WITH XML")
            self.load_display_current_scene_xml()
        else:
            # DOING SOMETHING WITH THE SCENE NUMBER
            self.load_display_current_scene_xml()



    # THIS FUNCTION USES BELOW TWO FUNCTIONS
    # WITH THE SCENARIOS WE CAN EXPECT
    def load_display_current_scene_xml(self):

        # SCENE NUMBER FROM MAIN PROCESS
        # -1 MEANS THAT THE SCENE IS NOW JUNCTION SCENE,
        # SO WE NEED TO FILTER IT
        if self.scene_number != -1:

            # CLEAR THE WIDGETS
            # print("RE-DISPLAY THE NEW SCENE")

            # DELETE ALL WIDGETS
            self.delete_all_widgets()

            # SETTING UP THE MENU
            self.create_main_gui()

            # DISPLAY AGAIN
            self.elem_scene = self.load_current_scene_xml(self.scene_number)
            self.display_current_scene_xml()


            # IF THE CURRENT SCENE WAS DISPLAYED ONCE,
            # WE DO NOT WANT TO DISPLAY AGAIN
            # SO WE CHECK THE PAST SCENE NUMBER AND NEWLY OBTAINED NUMBER IS DIFFERENT



    # ---------------------------------------------------------------
    # THEN, LOAD THE PROPER DATA FROM XML
    # BASED ON THE CURRENT SCENE NUMBER
    def load_current_scene_xml(self, scene_number):

        # GETTING SCENE ELEMENT WITH SCENE NUMBER
        elem_scene = self.xmlconnector.get_scene_elem(scene_number)
        return elem_scene



    # ---------------------------------------------------------------
    # VALIDATE THE VALUES WE INPUT

    # IN CASE OF USING SPINBOX
    def validate_value_spinbox(self, event_type, value, xml_tagname, xml_valuename ):
        # FOR SPINBOX INPUT,
        #print(f"WE ARE VALIDATING THE VALUE OF SPINBOX ! ----  event_type --  {event_type}    value --  {value}    xml_tagname --  {xml_tagname}    xml_valuename --  {xml_valuename}")

        # IF TYPE OF EVENT IS 'focusout',
        # WE WANT TO EXECUTE UPDATING XML !
        if event_type == 'focusout':
            #print(f"ACCEPTED ----  SPINBOX  ----  event_type --  focusout DOING save_to_xml")
            self.save_to_xml(xml_tagname, xml_valuename, value)
            return True

        # IN CASE OF FOCUSING IN TO WIDGET
        elif event_type == 'focusin':
            #print(f"ACCEPTED ----  SPINBOX  ----  event_type --  focusin")
            return True

        # IN CASE OF TYPING THE VALUE
        elif event_type == 'key':
            #print(f"----  event_type --  key")
            # IF THAT VALUE IS NOT THE INTEGER OR FLOAT TYPE

            # < CHECKING IF THE ERROR OCCURS >
            # https://docs.python.org/3/tutorial/errors.html#handling-exceptions
            try:
                stringcheck = int(value)
            except ValueError:
                #print("/*////*  THERE IS INVALID VALUE FROM SPINBOX  /*////*")
                value = None

            if value is None:
                #print("INVALID VALUE INPUTTED !")
                # RETURN FALSE
                return False
            else:
                # OR NOT RETURN TRUE
                #print(f"ACCEPTED ----  SPINBOX  ----  event_type --  key")
                return True

        else:
            #print(f"ACCEPTED ----  SPINBOX  ----  event_type --  OTHER CASES")
            return True


    # IN CASE OF USING SPINBOX
    def validate_value_allothers(self, event_type, value, xml_tagname, xml_valuename ):
        # FOR ALL OTHER WIDGETS,
        #print(f"WE ARE VALIDATING THE ALL OTHER WIDGETS ! ----  event_type --  {event_type}    value --  {value}    xml_tagname --  {xml_tagname}    xml_valuename --  {xml_valuename}")

        # ACTUALLY WE ARE DOING NOTHING EXCEPT FOR THE CASE WE HAVE 'FOCUSED OUT'
        #
        # IF TYPE OF EVENT IS 'focusout',
        # WE WANT TO EXECUTE UPDATING XML !
        if event_type == 'focusout':
            #print(f"ACCEPTED ----  NOT-SPINBOX  ----  event_type --  focusout DOING save_to_xml")
            self.save_to_xml(xml_tagname, xml_valuename, value)
            return True
        # IN CASE OF FOCUSING IN TO WIDGET
        elif event_type == 'focusin':
            #print(f"BLOCKED ----  NOT-SPINBOX  ----  event_type --  focusin")
            return False
        # IN CASE OF TYPING THE VALUE
        elif event_type == 'key':
            #print(f"ACCEPTED ----  NOT-SPINBOX  ----  event_type --  key")
            return True

        else:
            #print(f"ACCEPTED ----  NOT-SPINBOX  ----  event_type --  OTHER CASES")
            return True


    # IN CASE OF USING DUPLICATE BUTTON
    def validate_duplicate_entry(self, event_type, name):

        if event_type == 'focusout':
            #####print(f"BLOCKED ----  DUPLICATION ENTRY  ----  event_type --  focusout ")
            return False

        # IN CASE OF FOCUSING IN TO WIDGET
        elif event_type == 'focusin':
            #####print(f"BLOCKED ----  DUPLICATION ENTRY  ----  event_type --  focusin")
            return False

        # IN CASE OF TYPING THE VALUE
        elif event_type == 'key':
            #####print(f"ACCEPTED ----  DUPLICATION ENTRY  ----  event_type --  key")
            if self.check_name_exists(self.container, name):
                self.dupl_strvar.set(name)
            return True

        else:
            #####print(f"ACCEPTED ----  DUPLICATION ENTRY  ----  event_type --  key")
            if self.check_name_exists(self.container, name):
                self.dupl_strvar.set(name)
            return True




    # ---------------------------------------------------------------
    # UTILITIES


    def check_name_exists(self, dict, name):
        for item in dict.items():

            # DIVE INTO INNER DICTIONARY
            # item[1] <== {'target_surface': 'self.surface', 'name': 'text_explain_2_1', 'text': 'それでは', 'text_size': 120, 'anim_dura......
            inner_dict = item[1]
            keys_in_item = inner_dict.keys()

            for key in keys_in_item:
                if key == "name":
                    if inner_dict['name'] == name:
                        return True



    def get_item_with_name(self, dict, name):
        for item in dict.items():

            # DIVE INTO INNER DICTIONARY
            # item[1] <== {'target_surface': 'self.surface', 'name': 'text_explain_2_1', 'text': 'それでは', 'text_size': 120, 'anim_dura......
            inner_dict = item[1]
            keys_in_item = inner_dict.keys()

            for key in keys_in_item:
                if key == "name":
                    if inner_dict["name"] == name:
                        return item



    def duplicate_elem_dict(self, dict, name):

        if self.check_name_exists(dict, name):
            item_to_duplicate = self.get_item_with_name(dict, name)

            # WE WILL GET
            # item_to_duplicate <== ('node_text_1', {'target_surface': 'self.surface', 'name': 'text_explain_2_2', 'text': '始めましょう', 'text_size': 164, 'anim_duration': 8000, 'anim_type': 'SequentialText', 'anim_scaler_x': 0.5, 'anim_scaler_y': 1.0, 'p

            # -----------------------------------------------------------------------------
            # < MAKING NEW KEY NAME AND VALUE NAME >
            new_keyname = ""
            new_valuename = ""

            old_keyname = item_to_duplicate[0]
            old_keyname_split = old_keyname.split("_")

            old_valuename = item_to_duplicate[1]["name"]
            old_valuename_split = old_valuename.split("_")


            # CHECKING THE LAST ITEM IS INTEGER NUMBER OR NOT...
            if type(int(old_keyname_split[-1])) is int and \
                    type(int(old_valuename_split[-1])) is int:

                # -----------------------------------------
                # CONSTRUCTING KEY-NAME

                # FOR THE ELEMENT ONE BEFORE THE END,
                # IT WILL BE SAME AS ORIGINAL ONE
                for i in range(len(old_keyname_split)-1):
                    new_keyname += old_keyname_split[i] + "_"

                # ADD 1-PLUSED NUMBER TO LAST
                newcount = int(old_keyname_split[-1]) + 1
                new_keyname += str(newcount)


                # -----------------------------------------
                # CONSTRUCTING VALUE-NAME

                # FOR THE ELEMENT ONE BEFORE THE END,
                # IT WILL BE SAME AS ORIGINAL ONE
                for i in range(len(old_valuename_split)-1):
                    new_valuename += old_valuename_split[i] + "_"

                # ADD 1-PLUSED NUMBER TO LAST
                newcount = int(old_valuename_split[-1]) + 1
                new_valuename += str(newcount)


            # ADD THE item_to_duplicate TO MAIN CONTAINER
            item_to_duplicate[1]["name"] = new_valuename
            self.container[new_keyname] = item_to_duplicate[1]

            return new_keyname


    def duplicate_elem_button(self):
        #####print(f"DUPLICATE ELEMENT !!!!   --  self.dupl_strvar.get() is   {self.dupl_strvar.get()}")

        # BELOW MODIFIES self.container
        new_keyname = self.duplicate_elem_dict(self.container, self.dupl_strvar.get() )

        # SAVE THE XML WITH self.container
        updated_items = self.container[new_keyname]

        # EDIT XML FILE
        new_keyname_split = new_keyname.split("_")

        new_tag_name = ""

        # CONSTRUCT NEW TAG NAME
        for i in range(len(new_keyname_split)-1):
            new_tag_name += new_keyname_split[i] + "_"

        # DELETE LAST LETTER "_"
        new_tag_name = new_tag_name[:-1]
        new_tag_number = int(new_keyname_split[-1])

        # CREATING NEW ELEMENT WITH TAG NAME
        # https://stackoverflow.com/questions/14440375/how-to-add-an-element-to-xml-file-by-using-elementtree
        #
        new_element = ET.Element(new_tag_name)

        # SET THE ATTRIBUTE number
        new_element.set('number', str(new_tag_number))

        # < FORMATTING ElementTree >
        # https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
        new_element.tail = "\n\t"
        new_element.text = "\n\t\t\t"

        # FILLING WITH value TAGS
        for key in updated_items:
            sub = ET.SubElement(new_element, 'value')
            sub.set(key, str(updated_items[key]))
            sub.tail = "\n\t\t\t"


        # ADD THE NEW ELEMENT TO SCENE ELEMENT
        self.elem_scene.append(new_element)


        # WRITING XML FILE
        self.xmlconnector.xml_tree.write('xml_scenes/scenes_xml.xml', encoding="UTF-8", xml_declaration=True)


        # SEND MESSAGE TO MAIN PROCESS FOR RELOADING THE SCENE
        self.pipe_send.send('Reload_CurrentScene_' + str(self.scene_number))


        # RELOAD GUI
        self.get_current_scene_number()


        #####print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #####print(f'++++             SCENE NUMBER -- {self.scene_number}                                ++++')
        #####print(f'++++             SUB PROCESS ::  save_to_xml                   ++++')
        #####print( "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


    # < PRETTIFY XML ELEMENT >
    # https://stackoverflow.com/questions/14440375/how-to-add-an-element-to-xml-file-by-using-elementtree
    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")



    # CLOSING THIS OBJECT
    def close_program(self):
        self.destroy()



    # BELOW IS TO OVERRIDE THE EXIT BUTTON !
    def disable_event(self):
        pass



