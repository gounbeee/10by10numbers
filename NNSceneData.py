import numpy
from NNScene import *
import NNNode
from NNGlobals import *
import random

# ----------------------------------------------


class NNScene_For_All(NNScene):


    def __init__(self, surface, scene_number):
        super().__init__(surface)

        self.scene_number = scene_number
        self.stateID = 'State' + str(self.scene_number)
        self.count = 10
        self.elem_scene = None

        # DISPLAYING TRAINSET
        self.surface_trainset = None
        self.surface_trainset_w = 180
        self.surface_trainset_h = 180
        self.surface_trainset_bg = pygame.Surface((self.surface_trainset_w, self.surface_trainset_h))
        self.surface_trainset_bg.fill(pygame.Color(255, 255, 255))

        # TEXT OBJECT FOR DEMO MODE
        self.surface_text_demo_mode = None

        # FOR DISPLAYING MOUSE COORDINATE
        self.mouse_coord = None

        # FOR DISPLAYING TRAINING VARIABLES
        self.text_epoch = None
        self.text_loss = None
        self.text_score = None

        # FOR DISPLAYING MANY TRAINSETS
        many_trainsets_count = 21
        self.disp_trainsets = []
        for i in range(many_trainsets_count):
            self.disp_trainsets.append(pygame.Surface((125, 125)))

        # FOR DISPLAYING TRAINSET FROM SCENE 40
        self.disp_trainset_surface = pygame.Surface((300, 300))
        self.disp_trainset_surface_2 = pygame.Surface((300, 300))

        # FOR DISPLAYING USER-INPUTTED SURFACE
        self.userinput_surface = None



    def setup(self, the_value_dict, duration):


        # DRAWING DRAWPAD
        super().setup(the_value_dict, duration)

        # SETTING the_value DICTIONARY
        self.set_value_dict(the_value_dict)



        # -----------------------------------------------------------------------------

        # GETTING SCENE ELEMENT WITH SCENE NUMBER

        self.elem_scene = self.xmlconnector.get_scene_elem(self.scene_number)



        # -------------------------------------------------------------------
        #
        # < DRAWPAD >
        #
        # IF THERE IS drawpad ELEMENT, RUN super().drawpad_create()
        elem_drawpad = self.elem_scene.find('drawpad')

        if elem_drawpad is not None:
            # INITIALIZATION OF REQUIRED VALUES
            unitcount = unitsize = flag_clickable = anim_duration = None

            # VALUE TAGS IN THE DRAWPAD ELEMENT
            for value in elem_drawpad.findall('value'):

                # < CHECKING KEY IN THE DICTIONARY >
                # https://www.geeksforgeeks.org/python-dictionary-has_key/
                #
                if "unitcount" in value.attrib.keys():
                    unitcount = value.attrib["unitcount"]
                elif "unitsize" in value.attrib.keys():
                    unitsize = value.attrib["unitsize"]
                elif "flag_clickable" in value.attrib.keys():
                    flag_clickable = value.attrib["flag_clickable"]
                elif "anim_duration" in value.attrib.keys():
                    anim_duration = value.attrib["anim_duration"]


            # RUN super().drawpad_create()
            # TO CREATE DRAWPAD FOR SCENE 1
            super().drawpad_create(int(unitcount),
                                   int(unitsize),
                                   bool(flag_clickable),
                                   int(anim_duration),
                                   self.the_value_dict)



        # IF THERE IS NO DRAWPAD ELEMENT,
        # IT MEANS THAT WE ARE SEEING SPREADED INPUT LAYER IN THE LOWER SCREEN
        else:
            # DISPLAYING INPUT LAYER
            super().display_input_layer(self.count, self.the_value_dict)



        # TODO :: ARCHIVE BELOW !
        # Element.findall() はタグで現在の要素の直接の子要素のみ検索します。
        # Element.find() は特定のタグで 最初の 子要素を検索し、
        # Element.text は要素のテキストコンテンツにアクセスします。
        # Element.get() は要素の属性にアクセスします:

        # -------------------------------------------------------------------
        #
        # < TEXT NODES >
        #
        # GETTING CHILD ELEMENTS WHICH TAG NAME IS 'node_text'
        elem_node_texts = self.elem_scene.findall('node_text')

        is_user_result = False

        # FOR ALL node_text
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

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in node_text.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = self.xmlconnector.check_string(value.attrib["target_surface"])
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                    elif "text" in value.attrib.keys():
                        text = str(self.xmlconnector.check_string(value.attrib["text"]))
                    elif "text_size" in value.attrib.keys():
                        text_size = int(value.attrib["text_size"])
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                    elif "visible" in value.attrib.keys():
                        visible = value.attrib["visible"]
                        if visible == "True":
                            visible = True
                        elif visible == "False":
                            visible = False
                    elif "align" in value.attrib.keys():
                        align = value.attrib["align"]


                text_node = NNNode.NNNodeText(     target_surface,
                                                    name,
                                                    text,
                                                    (position_x, position_y),
                                                    (color_r, color_g, color_b),
                                                    text_size,
                                                    anim_duration,
                                                    anim_type,
                                                    anim_scaler_x,
                                                    anim_scaler_y,
                                                    visible,
                                                    align)

                # IF THIS IS SCENE IS 'FIRST SCENE'
                # IT WILL BE NEEDED TO ADD self.text_nn_result MEMBER VARIABLE !
                if self.scene_number == 1 and name == "text_nn_result":
                    self.text_nn_result = text_node
                    self.obj_manager.obj_list.append(self.text_nn_result)



                else:
                    self.obj_manager.obj_list.append(text_node)



        # -------------------------------------------------------------------
        #
        # < MULTI-TEXT NODES >
        #
        # GETTING CHILD ELEMENTS WHICH TAG NAME IS 'node_multitext'
        elem_node_multitexts = self.elem_scene.findall('node_multitext')

        # FOR ALL node_multitext
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

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in node_multitext.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = self.xmlconnector.check_string(value.attrib["target_surface"])
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                    elif "text" in value.attrib.keys():
                        text = str(value.attrib["text"])
                    elif "text_size" in value.attrib.keys():
                        text_size = int(value.attrib["text_size"])
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                    elif "visible" in value.attrib.keys():
                        visible = value.attrib["visible"]
                        if visible == "True":
                            visible = True
                        elif visible == "False":
                            visible = False
                    elif "align" in value.attrib.keys():
                        align = value.attrib["align"]
                    elif "line_margin" in value.attrib.keys():
                        line_margin = int(value.attrib["line_margin"])
                    elif "text_align" in value.attrib.keys():
                        text_align = value.attrib["text_align"]
                    elif "rotation" in value.attrib.keys():
                        rotation = int(value.attrib["rotation"])


                multitext_node = NNNode.NNNodeMultiText(
                                                    target_surface,
                                                    name,
                                                    text,
                                                    (position_x, position_y),
                                                    (color_r, color_g, color_b),
                                                    text_size,
                                                    anim_duration,
                                                    anim_type,
                                                    anim_scaler_x,
                                                    anim_scaler_y,
                                                    visible,
                                                    align,
                                                    line_margin,
                                                    text_align,
                                                    rotation)

                self.obj_manager.obj_list.append(multitext_node)




        # -------------------------------------------------------------------
        #
        # < PICTURES >
        #
        # GETTING CHILD ELEMENTS WHICH TAG NAME IS 'picture'
        elem_pics = self.elem_scene.findall('picture')

        # FOR ALL picture
        for pic in elem_pics:

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

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in pic.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = self.xmlconnector.check_string(value.attrib["target_surface"])
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                    elif "pic_file" in value.attrib.keys():
                        pic_file = str(value.attrib["pic_file"])
                    elif "pic_size" in value.attrib.keys():
                        pic_size = int(value.attrib["pic_size"])
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                    elif "rotation" in value.attrib.keys():
                        rotation = int(value.attrib["rotation"])
                    elif "visible" in value.attrib.keys():
                        visible = value.attrib["visible"]
                        if visible == "True":
                            visible = True
                        elif visible == "False":
                            visible = False
                    elif "align" in value.attrib.keys():
                        align = value.attrib["align"]


                pic = NNNode.NNNodePic(     target_surface,
                                            name,
                                            pic_file,
                                            (position_x, position_y),
                                            pic_size,
                                            anim_duration,
                                            anim_type,
                                            anim_scaler_x,
                                            anim_scaler_y,
                                            visible,
                                            rotation,
                                            align)

                self.obj_manager.obj_list.append(pic)



        # -------------------------------------------------------------------
        #
        # < SETTING CLICKABLE >
        #
        elem_clickable = self.elem_scene.findall('clickable')

        for flag_elem in elem_clickable:
            attrib = flag_elem.attrib["mode"]

            if attrib == 'All_Non_Clickable':

                # SETUP OBJECTS TO NON-CLICKABLE
                self.set_non_clickable()



        # -------------------------------------------------------------------
        #
        # < INDICATORS >
        #
        elem_indicators = self.elem_scene.findall('indicator')

        # FOR ALL node_text
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

                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in indicator.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = self.xmlconnector.check_string(value.attrib["target_surface"])
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])
                    elif "shape" in value.attrib.keys():
                        shape = str(value.attrib["shape"])
                    elif "size_w" in value.attrib.keys():
                        size_w = int(value.attrib["size_w"])
                    elif "size_h" in value.attrib.keys():
                        size_h = int(value.attrib["size_h"])
                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                    elif "center_x" in value.attrib.keys():
                        center_x = int(value.attrib["center_x"])
                    elif "center_y" in value.attrib.keys():
                        center_y = int(value.attrib["center_y"])
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                    elif "freq" in value.attrib.keys():
                        freq = float(value.attrib["freq"])
                    elif "style" in value.attrib.keys():
                        style = str(value.attrib["style"])

                indicator = NNNode.NNNodeIndicator(target_surface,
                                                  name,
                                                  shape,
                                                  (position_x, position_y),
                                                  (center_x, center_y),
                                                  (size_w, size_h),
                                                  anim_duration,
                                                  anim_type,
                                                  anim_scaler_x,
                                                  anim_scaler_y,
                                                  (color_r, color_g, color_b, 200),
                                                  freq,
                                                  style)

                self.obj_manager.obj_list.append(indicator)



        # -------------------------------------------------------------------
        #
        # < LINES >
        #
        elem_lines = self.elem_scene.findall('line')

        # FOR ALL node_text
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


                # VALUE TAGS IN THE DRAWPAD ELEMENT
                for value in line.findall('value'):

                    if "target_surface" in value.attrib.keys():
                        # IF EVALUATION IS NEEDED, SEND THE VALUE TO XmlConnector !
                        target_surface = self.xmlconnector.check_string(value.attrib["target_surface"])
                    elif "name" in value.attrib.keys():
                        name = str(value.attrib["name"])

                    elif "type" in value.attrib.keys():
                        type = str(value.attrib["type"])
                    elif "vertices" in value.attrib.keys():
                        vert_str_list = value.attrib["vertices"].split("_")
                        vert_list = []
                        for vert in vert_str_list:
                            vert_list.append(vert.split(","))
                        nplist = list( numpy.array(vert_list).astype(numpy.int) )

                        vertices = []
                        for vert in nplist:
                            vertices.append(list(vert))

                    elif "anim_duration" in value.attrib.keys():
                        anim_duration = int(value.attrib["anim_duration"])
                    elif "anim_type" in value.attrib.keys():
                        anim_type = str(value.attrib["anim_type"])
                    elif "anim_scaler_x" in value.attrib.keys():
                        anim_scaler_x = float(value.attrib["anim_scaler_x"])
                    elif "anim_scaler_y" in value.attrib.keys():
                        anim_scaler_y = float(value.attrib["anim_scaler_y"])
                    elif "position_x" in value.attrib.keys():
                        position_x = int(value.attrib["position_x"])
                    elif "position_y" in value.attrib.keys():
                        position_y = int(value.attrib["position_y"])
                    elif "color_r" in value.attrib.keys():
                        color_r = int(value.attrib["color_r"])
                    elif "color_g" in value.attrib.keys():
                        color_g = int(value.attrib["color_g"])
                    elif "color_b" in value.attrib.keys():
                        color_b = int(value.attrib["color_b"])
                    elif "freq" in value.attrib.keys():
                        freq = float(value.attrib["freq"])
                    elif "style" in value.attrib.keys():
                        style = str(value.attrib["style"])
                    elif "view_cv" in value.attrib.keys():
                        view_cv = value.attrib["view_cv"]
                        if view_cv == "True":
                            view_cv = True
                        elif view_cv == "False":
                            view_cv = False

                    elif "arrow_scale" in value.attrib.keys():
                        arrow_scale = float(value.attrib["arrow_scale"])
                    elif "arrow_adjust" in value.attrib.keys():
                        arrow_adjust = float(value.attrib["arrow_adjust"])
                    elif "arrow_visible" in value.attrib.keys():
                        arrow_visible = value.attrib["arrow_visible"]
                        if arrow_visible == "True":
                            arrow_visible = True
                        elif arrow_visible == "False":
                            arrow_visible = False
                    elif "adding_direction_x" in value.attrib.keys():
                        adding_direction_x = float(value.attrib["adding_direction_x"])
                    elif "adding_direction_y" in value.attrib.keys():
                        adding_direction_y = float(value.attrib["adding_direction_y"])




                line_obj = NNNode.NNNodeLine(target_surface,
                                              vertices,
                                              name,
                                              type,
                                              (position_x, position_y),
                                              anim_duration,
                                              anim_type,
                                              anim_scaler_x,
                                              anim_scaler_y,
                                              (color_r, color_g, color_b, 200),
                                              freq,
                                              style,
                                              view_cv,
                                              arrow_scale,
                                              arrow_adjust,
                                              arrow_visible,
                                              (adding_direction_x, adding_direction_y)
                                              )

                self.obj_manager.obj_list.append(line_obj)



        # -------------------------------------------------------------------
        #
        # < NAVI BUTTONS >
        #
        # CREATING NAV BUTTON
        elem_nav_buttons = self.elem_scene.findall('nav_buttons')

        if NNGlobals.ALL_BUTTON_DISABLE == False:

            for nav_button in elem_nav_buttons:
                attrib = nav_button.attrib["mode"]
                #print(attrib)

                if attrib == 'Function':
                    # NAVI BUTTONS
                    self.create_nav_buttons()

                # BELOW IS FOR SCENE 1
                elif attrib == 'Manual':

                    # ----------------------------------------------------------------------------
                    # NAV BUTTON
                    width = 50
                    height = 50

                    self.create_nav_next_button('Btn_Next',
                                                (NNGlobals.SCREEN_WIDTH // 2, 770),
                                                width,
                                                height,
                                                self.start_button
                                                )



        # ==============================================================================================================



        # -------------------------------------------------------------------
        #
        # < LOADING NNModel NODES AND LAYERS >
        #

        # SWITCHING train_flag
        if self.scene_number >= 2 and \
                self.scene_number in self.display_nn_visuals["Weight_v_newtrain"] and \
                self.scene_number in self.display_nn_visuals["Weight_w_newtrain"] :
            self.train_flag = True

        # SETTING UP THE PARAMETERS FOR TRAINING
        if self.scene_number >= 2:

            # IF self.train_flag IS TRUE, WE NEED TO
            # PREPARE self.weight_v_new_train AND self.weight_w_new_train

            if self.train_flag:
                self.nnmodel.train_prepare()

                # WE NEED TO INITIALIZE BELOWS
                # BELOW WILL TRAIN ONCE
                # TO PREPARE THE DATA WE NEED TO CONTINUE THE TRAINING
                self.nnmodel.train_to_visualize_only()

                # TRAINING RESULT
                self.epoch = self.nnmodel.epoch
                self.loss = self.nnmodel.loss
                self.score = self.nnmodel.score
                self.weight_v_new_train = self.nnmodel.V
                self.weight_w_new_train = self.nnmodel.W


            # SETTING UP NN MODEL DATA
            self.all_nodes_layers_setup()

            # CREATE PIXEL ARRAY FOR NN DATA ONLY IF THE SCENE NUMBER IS IN THE DICTIONARY
            for key in self.display_nn_visuals:

                if self.scene_number in self.display_nn_visuals[key]:
                    self.nodes_layers_create_pixelarray(key)



        # -------------------------------------------------------------------
        #
        # < DISPLAYING SCENE INDEX NUMBER >
        #
        if self.scene_number >= 3:
            # DISPLAYING SCENE NUMBER
            self.create_scene_index()



        # -------------------------------------------------------------------
        #
        # < DISPLAYING RESULT NUMBERS 0 - 9 >
        if self.scene_number >= 4:
            self.display_result_categories()



        # -------------------------------------------------------------------
        # < DEMO MODE PROCESS >
        #
        # GLOBALLY, DISPLAYING THE NOTIFICATION TEXT IF WE ARE IN THE DEMO MODE
        #if NNGlobals.DEMO_MODE_NOW and self.scene_number >= 2:
        if NNGlobals.DEMO_MODE_NOW and self.scene_number >= 2:

            #####print("~~~ ENTERED THE SCENE WITH DEMO MODE ~~~")

            # AND SCENE NUMBER 2, WE GET THE DEMO INPUT VALUE FROM NN MODEL
            if self.scene_number == 2:
                #####print("~~~ GETTING DEMO INPUT DATA ~~~")

                # < INPUTTED VALUE MANAGEMENT >
                #
                # CONVERT the_value_dict DICTIONARY TO PROPER FORMAT LIST FOR OUR NNModel

                picked = random.choice(self.nnmodel.dataset_data).flatten()

                # INVERT 0 VLAUE TO 255 IN THE PICKED UP VALUE
                for i in range(len(picked)):
                    if picked[i] == 0:
                        picked[i] = 255

                # CONVERT TO NUMPY ARRAY AND TRANSPOSE TO INVERT ROW AND COLUMN
                picked_np = numpy.array(picked).reshape((10, 10))
                picked_np_t = picked_np.T


                # TODO :: FIX BELOW !
                #         TOO MANY PLACES !
                # REGISTER THE VALUE PICKED UP FROM TRAINSET TO - < 3 PLACES >
                # 1 - the_value_dict
                # 2 - obj_manager.the_value_dict
                # 3 - ACTUAL obj IN obj_manager.obj_list

                self.set_value_to_dicts_objs(picked_np_t)




            # DISPLAYING TEXT
            demo_text_1 = NNNode.NNNodeText(self.surface,
                                          'text_demo_mode_a_' + str(self.scene_number),
                                          "DEMO 中",
                                          (NNGlobals.SCREEN_WIDTH // 2 - 700, NNGlobals.SCREEN_HEIGHT // 2 - 490),
                                          (200, 50, 90),
                                          50,
                                          8000,
                                          "Fixed",
                                          0.5,
                                          300,
                                          True,
                                          "Center")

            self.obj_manager.obj_list.append(demo_text_1)


            demo_text_2 = NNNode.NNNodeText(self.surface,
                                          'text_demo_mode_b_' + str(self.scene_number),
                                          "カーソルを",
                                          (NNGlobals.SCREEN_WIDTH // 2 - 300, NNGlobals.SCREEN_HEIGHT // 2 - 490),
                                          (200, 50, 90),
                                          60,
                                          8000,
                                          "Fixed",
                                          0.5,
                                          300,
                                          True,
                                          "Center")

            self.obj_manager.obj_list.append(demo_text_2)

            demo_text_3 = NNNode.NNNodeText(self.surface,
                                          'text_demo_mode_c_' + str(self.scene_number),
                                          "動かして",
                                          (NNGlobals.SCREEN_WIDTH // 2 + 300, NNGlobals.SCREEN_HEIGHT // 2 - 490),
                                          (200, 50, 90),
                                          60,
                                          8000,
                                          "Fixed",
                                          0.5,
                                          300,
                                          True,
                                          "Center")

            self.obj_manager.obj_list.append(demo_text_3)

            demo_text_4 = NNNode.NNNodeText(self.surface,
                                          'text_demo_mode_d_' + str(self.scene_number),
                                          "ください",
                                          (NNGlobals.SCREEN_WIDTH // 2 + 700, NNGlobals.SCREEN_HEIGHT // 2 - 490),
                                          (200, 50, 90),
                                          60,
                                          8000,
                                          "Fixed",
                                          0.5,
                                          300,
                                          True,
                                          "Center")

            self.obj_manager.obj_list.append(demo_text_4)


        # BELOW IS FOR DISPLAYING MOUSE CURSOR POSITION
        if NNGlobals.MOUSECOORDS:
            coord = pygame.mouse.get_pos()
            self.mouse_coord = NNNode.NNNodeText(self.surface,
                                            "mouse_cursor_pos",
                                            str(coord),
                                            (200, 50),
                                            (255, 0, 0),
                                            30,
                                            8000,
                                            "Fixed",
                                            0.5,
                                            300,
                                            True,
                                            "Center")

            self.obj_manager.obj_list.append(self.mouse_coord)


        # CREATING TEXT TO DISPLAY THE TRAINING PHASE
        if self.train_flag and self.scene_number >= 2:
            if self.weight_v_new_train is not None and \
                    self.weight_w_new_train is not None:


                self.text_epoch = NNNode.NNNodeText(self.surface,
                                                     "text_epoch_now",
                                                     str(self.nnmodel.epoch),
                                                     (480, 535),
                                                     (55, 120, 180),
                                                     50,
                                                     8000,
                                                     "Fixed",
                                                     0.5,
                                                     300,
                                                     True,
                                                     "Center")

                self.obj_manager.obj_list.append(self.text_epoch)

                self.text_epoch_b = NNNode.NNNodeText(self.surface,
                                                     "text_epoch_now",
                                                     "回 訓練完了",
                                                     (670, 540),
                                                     (55, 120, 180),
                                                     50,
                                                     8000,
                                                     "Fixed",
                                                     0.5,
                                                     300,
                                                     True,
                                                     "Center")

                self.obj_manager.obj_list.append(self.text_epoch_b)

                val = format(self.nnmodel.loss, '.2f')

                self.text_loss = NNNode.NNNodeText(self.surface,
                                                     "text_loss_now",
                                                     str(val),
                                                     (1200, 535),
                                                     (220, 50, 35),
                                                     50,
                                                     8000,
                                                     "Fixed",
                                                     0.5,
                                                     300,
                                                     True,
                                                     "Center")

                self.obj_manager.obj_list.append(self.text_loss)

                self.text_loss_b = NNNode.NNNodeText(self.surface,
                                                     "text_loss_now",
                                                     "の誤差",
                                                     (1380, 540),
                                                     (220, 50, 35),
                                                     50,
                                                     8000,
                                                     "Fixed",
                                                     0.5,
                                                     300,
                                                     True,
                                                     "Center")

                self.obj_manager.obj_list.append(self.text_loss_b)

                val_b = self.nnmodel.score * 100
                val_b = format(val_b, '.2f')

                self.text_score = NNNode.NNNodeText(self.surface,
                                                     "text_score_now",
                                                     str(val_b),
                                                     (1800, 535),
                                                     (55, 120, 120),
                                                     50,
                                                     8000,
                                                     "Fixed",
                                                     0.5,
                                                     300,
                                                     True,
                                                     "Center")

                self.obj_manager.obj_list.append(self.text_score)

                self.text_score_b = NNNode.NNNodeText(self.surface,
                                                     "text_score_now",
                                                     "% の精度",
                                                     (2040, 540),
                                                     (55, 120, 120),
                                                     50,
                                                     8000,
                                                     "Fixed",
                                                     0.5,
                                                     300,
                                                     True,
                                                     "Center")

                self.obj_manager.obj_list.append(self.text_score_b)


        # ------------------------------------------------------------------------
        # IF ENTIRE FLOW IS RESETTED, OR ENTERED TO SCENE 1
        # RESET self.text_nn_result TO 0 AND self.nnmodel
        if self.scene_number == 1:

            # RESETTING PREDICTION TEXT
            self.nnmodel.prediction = 0
            self.text_nn_result.set_style("0", 140, self.textcolor_main)

            # RESETTING TRAINSET SURFACE
            self.surface_trainset = None
            self.surface_trainset_bg = pygame.Surface((self.surface_trainset_w, self.surface_trainset_h))
            self.surface_trainset_bg.fill(pygame.Color(255, 255, 255))

            # BELOW IS CRITICAL AFTER RESETTING DEMO MODE
            self.clear_value_dict()



        # FROM SCENE NUMBER 22,
        # DISPLAY CIRCLE TO PREDICTED NUMBER
        if self.scene_number >= 22:
            #####print("DISPLAY THE PREDICTED RESULT !!")

            NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(NNGlobals.USER_INPUT)
            #####print(NNGlobals.USER_RESULT)

            text_predicted = NNNode.NNNodeText(self.surface,
                                          'text_predicted',
                                          "○",
                                          (NNGlobals.SCREEN_WIDTH//2 - 900 + (200 * NNGlobals.USER_RESULT), NNGlobals.SCREEN_HEIGHT//2 - 390),
                                          (200, 50, 90),
                                          70,
                                          8000,
                                          "Fixed",
                                          0.5,
                                          300,
                                          True,
                                          "Center")

            self.obj_manager.obj_list.append(text_predicted)


        # TODO :: CLEAN UP BELOW
        #      :: THERE IS ANOTHER PARTS IN THE PARENT CLASS !
        # ADD THE DUMMY INPUT DATA 1.0 RECTANGLE
        if self.scene_number >= 2:
            self.obj_manager.obj_list.append(NNNode.NNNodeText(self.surface,
                                                               "input_dummy_t",
                                                               '1.0',
                                                               (28, NNGlobals.SCREEN_HEIGHT // 2 + 484),
                                                               self.textcolor_main,
                                                               14,
                                                               8000,
                                                               'Fixed',
                                                               0.5,
                                                               300,
                                                               True))



        # DISPLAYING MANY TRAINSETS
        if self.scene_number == 33:
            for i in range(len(self.disp_trainsets)):
                self.disp_trainsets[i] = self.get_random_trainset_surface(self.disp_trainsets[i].get_size())


        # DISPLAYING INPUTTED SURFACE
        if self.scene_number == 22 or self.scene_number == 60:
            self.userinput_surface = self.get_userinput_surface()


        # DISPLAYING TRAINSET (SPECIFIED)
        if self.scene_number == 36:
            self.disp_trainset_surface = self.get_specified_trainset_surface(self.disp_trainset_surface.get_size(), NNGlobals.USER_RESULT)
            self.disp_trainset_surface_2 = self.get_specified_trainset_surface(self.disp_trainset_surface.get_size(), NNGlobals.USER_RESULT)


        # DISPLAYING TRAINSET (SPECIFIED)
        if self.scene_number == 35 or self.scene_number == 40 or self.scene_number == 42:
            self.disp_trainset_surface = self.get_specified_trainset_surface(self.disp_trainset_surface.get_size(), NNGlobals.USER_RESULT)







    def update(self, elapsed_time):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_For_All::update() -- self.scene_number IS   {self.scene_number}")
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_For_All::update() -- elapsed_time IS   {elapsed_time}")
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNScene_For_All::update() -- NNGlobals.SCENE_INDEX IS   {NNGlobals.SCENE_INDEX}")

        # BELOW IS JUST FOR THE SCENE 1
        self.update_drawpad()
        self.display_closest_trainingset()


        super().update(elapsed_time)

        # FOR DEBUG ONLY
        if NNGlobals.MOUSECOORDS:
            coord = pygame.mouse.get_pos()
            self.mouse_coord.set_style(str(coord), 30, (255, 0, 0))


        # UPDATING VARIABLES FOR TRAINING PHASE
        if self.train_flag and self.scene_number >= 2:
            if self.weight_v_new_train is not None and \
                    self.weight_w_new_train is not None:

                self.text_epoch.set_style(str(self.nnmodel.epoch), 60, (55, 120, 180))
                val_a = format(self.nnmodel.loss, '.2f')
                self.text_loss.set_style(str(val_a), 60, (220, 50, 35))
                val_b = self.nnmodel.score * 100
                val_b = format(val_b, '.2f')
                self.text_score.set_style(str(val_b), 60, (55, 120, 120))



    def render(self):

        super().render()

        if self.scene_number == 1:
            self.surface.blit(self.surface_trainset_bg, (2100, 690))


        if self.surface_trainset:
            self.surface.blit(self.surface_trainset, (2100, 690))


        if self.scene_number == 22 or self.scene_number == 60:
            self.surface.blit(self.userinput_surface, (NNGlobals.SCREEN_WIDTH // 2 - self.userinput_surface.get_width()//2, NNGlobals.SCREEN_HEIGHT // 2 ))


        if self.scene_number == 33:
            for i in range(len(self.disp_trainsets)):
                self.surface.blit(self.disp_trainsets[i], (i * self.disp_trainsets[i].get_width(), 800))


        if self.scene_number == 36:
            self.surface.blit(self.disp_trainset_surface, (NNGlobals.SCREEN_WIDTH // 2 - self.disp_trainset_surface.get_width() // 2, NNGlobals.SCREEN_HEIGHT // 2 + 150))
            self.surface.blit(self.disp_trainset_surface_2, (NNGlobals.SCREEN_WIDTH // 2 - self.disp_trainset_surface.get_width()//2, NNGlobals.SCREEN_HEIGHT // 2 - 200))


        if self.scene_number == 35 or self.scene_number == 40 or self.scene_number == 42:
            self.surface.blit(self.disp_trainset_surface, (NNGlobals.SCREEN_WIDTH // 2 - self.disp_trainset_surface.get_width()//2, NNGlobals.SCREEN_HEIGHT // 2 + 150))






    def get_userinput_surface(self):
        surface_scaled = None

        if NNGlobals.DEMO_MODE_NOW:
            # GETTING USER INPUTTED ARRAY
            array_userinput = NNGlobals.USER_INPUT[1:]

            for i in range(len(array_userinput)):
                array_userinput[i] = int(array_userinput[i] * 255)

            array_pic = self.create_pixelarray_from_list(array_userinput)

            surface_scaled = self.get_scaled_surface_from_pixelarr(array_pic, (300, 300))


        else:
            # GETTING USER INPUTTED ARRAY
            array_userinput = NNGlobals.USER_INPUT[1:]

            for i in range(len(array_userinput)):
                array_userinput[i] = int(array_userinput[i] * 255)

            array_pic = self.create_pixelarray_from_list(array_userinput)

            surface_scaled = self.get_scaled_surface_from_pixelarr(array_pic, (300, 300))

        return surface_scaled



    def create_pixelarray_from_list(self, array):
        array_pic = []
        for value in array:
            array_pic.append((255 - value, 255 - value, 255 - value))

        array_pic = numpy.array(array_pic).reshape((10, 10, 3))

        return array_pic



    def get_scaled_surface_from_pixelarr(self, pixelarr, size):

        surface = pygame.surfarray.make_surface(pixelarr)
        surface = pygame.transform.flip(surface, True, False)
        surface = pygame.transform.rotate(surface, 90)

        surface_scaled = pygame.transform.scale(surface, size)

        return surface_scaled



    def get_specified_trainset_surface(self, size, answer):

        searched = [i for i, x in enumerate(list(self.nnmodel.dataset_label)) if x == str(answer)]

        random_array = numpy.array(self.nnmodel.dataset_data[random.choice(searched)]).flatten()

        array_pic = self.create_pixelarray_from_list(random_array)

        surface_scaled = self.get_scaled_surface_from_pixelarr(array_pic, size)

        return surface_scaled


    def get_random_trainset_surface(self, size):

        searched = [i for i, x in enumerate(list(self.nnmodel.dataset_label)) if x == str(random.randrange(10))]

        random_array = numpy.array(self.nnmodel.dataset_data[random.choice(searched)]).flatten()

        array_pic = self.create_pixelarray_from_list(random_array)

        surface_scaled = self.get_scaled_surface_from_pixelarr(array_pic, size)

        return surface_scaled



    def display_closest_trainingset(self):
        # IF THERE IS drawpad ELEMENT, RUN super().drawpad_create()
        elem_drawpad = self.elem_scene.find('drawpad')

        # TO DISPLAY THE CLOSEST RESULT IN THE TRAIN SET
        # BELOW IS FOR SCENE 1


        if elem_drawpad is not None and NNGlobals.SCENE_INDEX == 0:

            # TODO :: BELOW IS SHOULD BE INCLUDED TO DRAWPAD CLASS !
            # CHECK THE AREA OF DRAWPAD
            drawpad_pos = (NNGlobals.SCREEN_WIDTH // 2, NNGlobals.SCREEN_HEIGHT // 2)

            drawpad_area = { "N": drawpad_pos[1] - (30 * 5),
                             "W": drawpad_pos[0] - (30 * 5),
                             "S": drawpad_pos[1] + (30 * 5),
                             "E": drawpad_pos[0] + (30 * 5)
                            }

            # CHECK MOUSE CURSOR IS ON THE START BUTTON AREA
            if drawpad_area["W"] < pygame.mouse.get_pos()[0] < drawpad_area["E"] and \
                drawpad_area["N"] < pygame.mouse.get_pos()[1] < drawpad_area["S"]:


                # UPDATING THE COLOR AND PREDICT THE RESULT OF THE NEURAL NETWORK
                if self.click_left_occured is True or self.click_right_occured is True:

                    # GETTING CURRENT VALUES
                    current_user_pred = {"Prediction": NNGlobals.USER_RESULT, "Values": self.the_value_dict}

                    # GETTING TRAIN SETS
                    #print(self.nnmodel.dataset_data)
                    #print(self.nnmodel.dataset_label)

                    # TODO :: ARCHIVE BELOW !
                    # < GETTING ALL INDICES MATCHES TO VALUE ! >
                    # https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list

                    #searched = list(self.nnmodel.dataset_label).index(str(current_user_pred["Prediction"]))

                    # < ABOUT ENUMERATE >
                    # https://ja.foobarninja.com/python/enumerate/?gclid=CjwKCAiAxeX_BRASEiwAc1QdkYs5bf1PKq3CVcJorNqSjSz27Fy7n3tXZeCzotd3My8StkV8DChFuhoC2v4QAvD_BwE
                    searched = [i for i, x in enumerate(list(self.nnmodel.dataset_label)) if x == str(current_user_pred["Prediction"])]

                    # for answer_index in searched:
                    #     array = list(numpy.array(self.nnmodel.dataset_data[answer_index]).flat)
                    #     #print(array)

                    random_array = numpy.array(self.nnmodel.dataset_data[random.choice(searched)]).flatten()

                    array_pic = []
                    for value in random_array:
                        array_pic.append((255-value, 255-value, 255-value))

                    array_pic = numpy.array(array_pic).reshape((10, 10, 3))

                    surface = pygame.surfarray.make_surface(array_pic)
                    surface = pygame.transform.flip(surface, True, False)
                    surface = pygame.transform.rotate(surface, 90)

                    self.surface_trainset = pygame.transform.scale(surface, (self.surface_trainset_w, self.surface_trainset_h))


    # TODO :: MAYBE BELOW FUNCTION CANNOT BE USED
    #         IN NORMAL FLOW ! (ONLY DEMO MODE)
    #         BECAUSE OF APPLYING 4
    def set_value_to_dicts_objs(self, input):

        for key in sorted(self.the_value_dict.keys()):

            # RETRIVE THE INDICES
            row = int(key.split("_")[2])
            col = int(key.split("_")[1])

            # ---------------------------------------
            # APPLYING VALUE 1
            self.the_value_dict[key] = input[col][row]

            # ---------------------------------------
            # APPLYING VALUE 2
            self.obj_manager.the_value_dict[key] = input[col][row]

            # ---------------------------------------
            # APPLYING VALUE 3
            for obj in self.obj_manager.obj_list:

                id = "txt_obj" + "_" + str(col) + "_" + str(row)

                # APPLY TO NNObject OBJECTS
                if obj.obj_id == key:
                    obj.the_value = input[col][row]

                # APPLY TO NNTextNode OBJECTS
                if obj.obj_id == id:
                    obj.the_value = input[col][row]


        # ---------------------------------------
        # APPLYING VALUE 4
        # APPLYING TO NNGlobals.USER_INPUT
        input = self.the_value_dict.values()

        input_final = []

        input_final.append(1.0)

        # CONVERT TYPE TO FLOAT
        for elem in input:

            if elem != 255.0 and elem != 0.0:
                elem = float(elem) / 255.0

            elif elem == 0.0:
                elem = 255.0

            elif elem == 255.0:
                elem = 0.0

            input_final.append(elem)

        #input_numpy = numpy.array(input_final).T

        #NNGlobals.USER_INPUT = list(input_numpy)
        NNGlobals.USER_INPUT = input_final




    def update_drawpad(self):
        # IF THERE IS drawpad ELEMENT, RUN super().drawpad_create()
        elem_drawpad = self.elem_scene.find('drawpad')


        # BELOW IS FOR SCENE 1
        if elem_drawpad is not None and NNGlobals.SCENE_INDEX == 0:

            # BELOW IS IMPORTANT
            # STORE THE VALUES TO GLOBAL VARIABLE

            if not len(self.obj_manager.the_value_dict) == 0:
                self.the_value_dict = self.obj_manager.the_value_dict


            # < INPUTTED VALUE MANAGEMENT >
            #
            # CONVERT the_value_dict DICTIONARY TO PROPER FORMAT LIST FOR OUR NNModel
            input = self.the_value_dict.values()

            input_final = []

            input_final.append(1.0)

            # CONVERT TYPE TO FLOAT
            for elem in input:
                elem = (255.0 - float(elem)) / 255.0

                input_final.append(elem)

            NNGlobals.USER_INPUT = input_final


            # --------------------------------------------------------------------------------------
            #
            # < UPDATING THE COLOR AND PREDICT THE RESULT OF THE NEURAL NETWORK >

            # TODO :: BELOW IS SHOULD BE INCLUDED TO DRAWPAD CLASS !
            # CHECK THE AREA OF DRAWPAD
            drawpad_pos = (NNGlobals.SCREEN_WIDTH // 2, NNGlobals.SCREEN_HEIGHT // 2)

            drawpad_area = { "N": drawpad_pos[1] - (30 * 5),
                             "W": drawpad_pos[0] - (30 * 5),
                             "S": drawpad_pos[1] + (30 * 5),
                             "E": drawpad_pos[0] + (30 * 5)
                            }

            # CHECK MOUSE CURSOR IS ON THE START BUTTON AREA
            if drawpad_area["W"] < pygame.mouse.get_pos()[0] < drawpad_area["E"] and \
                drawpad_area["N"] < pygame.mouse.get_pos()[1] < drawpad_area["S"]:

                #print("MOUSE CURSOR IS ON THE START BUTTON !!!!")

                # THEN IF MOUSE BUTTON IS CLICKED...
                if self.click_left_occured is True or self.click_right_occured is True:
                    #print(self.obj_manager.the_value_dict)
                    #print(NNGlobals.USER_INPUT)

                    #print(f'====  INPUT FOR PREDICTION FUNCTION  --  {input_final}')
                    #print(len(input_final))

                    NNGlobals.USER_RESULT = self.nnmodel.get_final_prediction(input_final)
                    #print(f'***** USER\'S RESULT IS    {NNGlobals.USER_RESULT}')

                    self.text_nn_result.set_style(str(NNGlobals.USER_RESULT), 140, self.textcolor_main)

                    # RESETTING GLOBAL TIMER
                    NNGlobals.TIMER.reset()