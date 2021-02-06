import pygame
import pygame.gfxdraw
import NNAnim
import math
import Timer
import numpy
import NNGlobals

from inspect import currentframe, getframeinfo, stack



# ------------------------------------------------
# BASE CLASS FOR NNNode
class NNNode(object):

    def __init__(self, id="objNone", animation_type="", duration=0,  xscaler=0, yscaler=0, the_value=0, freq=0):
        # DEFINE OBJECT'S ATTRIBUTES
        self.obj_id = id
        self.animation_type = animation_type
        self.duration = duration
        self.xscaler = xscaler
        self.yscaler = yscaler

        # INITIALIZATION FOR FREQUENCY FOR LOOPING ANIMATION
        self.freq = None
        if freq is not 0:
            self.freq = freq
        else:
            self.freq = 0

        # CREATING NNAnim OBEJCT TO ANIMATE
        self.anim = NNAnim.NNAnim(self.duration , self.animation_type, self.xscaler, self.yscaler, self.freq)

        # PHYSICS DATA
        self.animation_value_last = self.anim.result_value
        self.animation_value_new = self.anim.result_value

        # ANIMATED VALUE FROM NNAnim ENGINE
        self.animation_value_delta = None

        if type(self.animation_value_new) is list and len(self.animation_value_new) == 2:
            self.animation_value_delta = []
        elif type(self.animation_value_new) is float or type(self.animation_value_new) is int:
            self.animation_value_delta = 0

        # THE VALUE FOR NEURAL NETWORK
        self.the_value = the_value

        # FOR MOUSE CLICK DETECTION
        self.clicked = False

        # DEFAULT MAIN TEXT COLOR
        self.textcolor_main = (160, 50, 90)




    def update(self):

        # GETTING NEWLY ANIMATED VALUE FROM NNAnim ENGINE
        ##print(self.anim.update())

        # < GETTING UPDATED VALUES WITH NNAnim ENGINE >
        # : BELOW OUTPUT DEPENDS ON THE NNAnim'S update() FUNCTION
        self.animation_value_new = self.anim.update()


        # UPDATE FOR Circular, Fixed ANIMATION TYPES
        if (self.animation_type == "Circular" or self.animation_type == "Fixed") and \
                type(self.animation_value_new) is list and len(self.animation_value_new) == 2:

            #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNode::update_with_type() --2D VALUE IS NOW ANIMATING...! ")

            # CALCULATING VELOCITY WITH DELTA VALUE
            self.animation_value_delta = [self.animation_value_new[0] - self.animation_value_last[0],
                                          self.animation_value_new[1] - self.animation_value_last[1]]

            # ACTUAL ANIMATING
            self.position = [self.position[0] + self.animation_value_delta[0], self.position[1] + self.animation_value_delta[1]]

            # UPDATING LAST-ANIMATED VALUE
            # < BUILDING NEW PAST DATA >
            self.animation_value_last = [self.animation_value_new[0], self.animation_value_new[1]]



    # RENDERING
    def render(self):
        pass


    @property
    def the_value(self):
        return self.__the_value

    @the_value.setter
    def the_value(self, value):
        self.__the_value = value




# ------------------------------------------------
# ACTUAL CLASS FOR NODE OBJECT
class NNNodeObject(NNNode):

    # CONSTRUCTOR
    def __init__(self, surface, id='objNone', shape='Rectangle',position=(0, 0), center=(0, 0), size=30, duration=1000, animation_type='Fixed', xscaler=0.005, yscaler= 300, clickable=False, the_value=0):
        super().__init__(id, animation_type, duration, xscaler, yscaler, the_value)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # STORING POSITION AS INITIALIZATION
        self.position = position

        # STORING SHAPE
        self.shape = shape

        # COLOR PALLETE
        self.color_default = (200, 200, 200)
        self.color_selected = (0, 0, 0)
        self.color_hover = (255, 20, 10)

        # SETTING DEFAULT COLOR
        self.set_color_with_the_value(self.the_value)

        # SETTING CENTER
        self.center = center

        # SETTING SIZE
        self.size = (size, size)

        # MOUSE CLICK FLAG
        self.clickable = clickable


        self.the_value = 255



    # UPDATING
    def update(self):

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeObject::update() -- {self.obj_id}")

        # < MOUSE CURSOR WITH COLOR >
        #
        # IF THE FLAG FOR CLICKABLE IS True...
        if self.clickable:
            area = NNRegion([self.position[0] - self.size[0] // 2, self.position[1] - self.size[1] // 2],             # VERTEX OF TOP-LEFT
                            [self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2],             # VERTEX OF TOP-RIGHT
                            [self.position[0] - self.size[0] // 2, self.position[1] - self.size[1] // 2],             # VERTEX OF BOTTOM-LEFT
                            [self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2]              # VERTEX OF BOTTOM-RIGHT
                            )

            # COLLISION TEST
            # MOUSE POSITION EVENT

            if area.is_colliding( pygame.mouse.get_pos() ):

                # COLOR OF CURSOR
                self.color = self.color_hover

                # < VALUE SETTING FOR NEURAL NETWORK >
                # GETTING MOUSE CURSOR POSITION
                check_leftbutton_clicked = pygame.mouse.get_pressed(3)[0]
                check_rightbutton_clicked = pygame.mouse.get_pressed(3)[2]

                # TESTING WITH ASSERTION
                # https://qiita.com/nannoki/items/15004992b6bb5637a9cd
                #
                #assert not check_rightbutton_clicked, 'RIGHT MOUSE BUTTON WAS CLICKED'

                # < MOUSE BUTTON EVENT HANDLING >
                # IF LEFT MOUSE BUTTON WAS PRESSED...
                if check_leftbutton_clicked:

                    the_value_old = self.the_value

                    # SET THE the_value BE TOGGLED
                    self.clicked = True


                    # SETTING COLOR WITH DISTANCE BETWEEN CENTER POINT OF THIS NODE

                    the_value_new = self.set_color_with_grayscale()

                    if the_value_new < the_value_old:
                        self.the_value = the_value_new


                    self.set_color_with_the_value(self.the_value)


                # IF RIGHT MOUSE BUTTON WAS PRESSED...
                elif check_rightbutton_clicked:
                    # SET THE the_value TO 0
                    self.the_value = 255.0

                    # SET THE TILE'S COLOR TO DEFAULT COLOR
                    self.set_color_with_the_value(self.the_value)

                    self.clicked = True

            else:
                # IF THE VALUE IS NOT SETTED...

                if self.the_value == 255.0:
                    # IT WILL USE DEFAULT COLOR
                    self.set_color_with_the_value(self.the_value)


                else:
                    # OR, IT WILL USE BLACK
                    self.set_color_with_the_value(self.the_value)


                # DEFAULT VALUE OF clicked VARIABLE
                self.clicked = False

        else:

            # DEFAULT COLOR
            #self.set_color_with_the_value(self.the_value)
            pass


        # UPDATING THIS OBJECT
        super().update()



    def toggle_color(self):
        if self.color == self.color_default:
            self.color = self.color_selected
        elif self.color == self.color_selected:
            self.color = self.color_default



    def set_color_with_grayscale(self):

        # GETTING MOUSE CURSOR POINT
        mouse_postiion = pygame.mouse.get_pos()

        # GETTING CENTER POINT OF THIS NODE
        center_point = [self.position[0], self.position[1]]

        # CALCULATION THE DISTANCE BETWEEN THE ABOVE TWO POINTS
        distance = math.sqrt((mouse_postiion[0] - center_point[0])**2 + (mouse_postiion[1] - center_point[1])**2 )

        # GETTING MAX VALUE OF DISTANCE WITH NODE'S SIZE
        max_dist = math.sqrt((self.size[0]//2)**2 + (self.size[1]//2)**2)

        # MAPPING COLOR WITH 0 - max_dist VALUE TO 0 - 255 VALUE FOR GRAYSCALE COLOR
        mapped = 255 - int(((distance - 0.0) / (max_dist - 0.0)) * (255.0 - 0.0) + 0.0)

        new_color = self.color[0] - mapped

        return new_color





    def set_color_with_the_value(self, the_value):
        # COLOR SETTING BASED ON THE the_value

        self.color = (the_value, the_value, the_value)



    def set_default_color_tuple_3(self, tp):
        # COLOR SETTING BASED ON THE the_value

        self.color = self.color_default = (tp[0], tp[1], tp[2])



    def set_default_color_tuple_4(self, tp):
        # COLOR SETTING BASED ON THE the_value

        self.color = self.color_default = (tp[0], tp[1], tp[2], tp[3])


    # RENDERING
    def render(self):
        #frameinfo = getframeinfo(currentframe())
        #print(f"{frameinfo.filename} -- {frameinfo.lineno}  NNNodeObject::render() -- {self.obj_id}")

        # DRAWING CIRCLE IN PYGAME
        # https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/drawing-circles/

        if self.shape == 'Rectangle':
            pygame.draw.rect(self.surface, self.color, pygame.Rect((self.position[0]-self.size[0]//2, self.position[1]-self.size[1]//2), (self.size[0], self.size[1])))
        elif self.shape == 'Circle':
            pygame.draw.circle(self.surface, self.color, self.position, self.size[0])



    # < GETTING AND SETTING ATTRIBUTES >
    #
    # BELOW IS GOOD REFERENCE !
    # https://www.datacamp.com/community/tutorials/property-getters-setters
    #
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color



# ------------------------------------------------
# ACTUAL CLASS FOR NODE OBJECT



class NNNodeIndicator(NNNode):

    # CONSTRUCTOR
    def __init__(self, surface, id='objNone', shape='Rectangle', position=(0, 0), center=(0, 0), size=(100,40), duration=1000, animation_type='Fixed', xscaler=1.0, yscaler=1.0, color=(200,10,50), freq=1, style='Line_NoFill_10_5'):
        super().__init__(id, animation_type, duration, xscaler, yscaler, -1, freq)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # STORING POSITION AS INITIALIZATION
        self.position = position

        # STORING SHAPE
        self.shape = shape

        # SETTING COLOR (0 - 255 RANGE)
        self.color = color                  # TUPLE
        self.initial_alpha = color[3]

        # SETTING CENTER
        self.center = center

        # SETTING SIZE
        # (TUPLE TYPE FOR WIDTH AND HEIGHT) ***
        self.size = size

        # SETTING STYLE OF THIS OBJECT
        self.style = style

        self.line_width = None
        self.line_radius = None

        self.set_style(self.style)



    # UPDATING
    def update(self):
        # UPDATING THIS OBJECT
        super().update()

        # < UPDATING COLOR >
        # IF ANIMATION TYPE IS 'Sine_0_255'...
        if self.animation_type == "Sine_0_255":
            animating_alpha = self.anim.get_result()

            self.color = (self.color[0], self.color[1], self.color[2], animating_alpha)

        elif self.animation_type == "Cosine_0_255":
            animating_alpha = self.anim.get_result()

            self.color = (self.color[0], self.color[1], self.color[2], animating_alpha)




    # RENDERING
    def render(self):

        modified_for_centering = (self.position[0]-self.size[0]//2, self.position[1]-self.size[1]//2)

        # DRAWING CIRCLE IN PYGAME
        # https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/drawing-circles/

        if self.shape == 'Rectangle':
            # < DRAWING TRANSPARENT GRAPHICS >
            # https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame

            #surface = pygame.Surface(pygame.Rect((self.position[0]-self.size[0]//2, self.position[1]-self.size[1]//2), self.size).size)
            #surface.fill((0, 255, 0, 255))
            #surface.set_colorkey((0, 255, 0))
            # graphics_area = pygame.draw.rect(self.surface,
            #                                  self.color,
            #                                  pygame.Rect((self.position[0]-self.size[0]//2, self.position[1]-self.size[1]//2), self.size),
            #                                  self.line_width,          # LINE WIDTH
            #                                  self.line_radius          # BORDER RADIUS
            #                                  )
            # NEW SURFACE FOR ALPHA BLENDING
            #surface.set_alpha(self.color_alpha)
            #self.surface.blit(surface, self.position)

            # TODO :: BE NOTED THE BELOW API IS EXPERIMENTAL !
            # < USING gfxdraw API >
            # https://www.pygame.org/docs/ref/gfxdraw.html#pygame.gfxdraw.rectangle
            # https://stackoverflow.com/questions/13026887/transparent-rectangle-in-pygame
            #
            if self.line_width is not None:
                for i in range(self.line_width):
                    pygame.gfxdraw.rectangle(self.surface,
                                             pygame.Rect((modified_for_centering[0]+i, modified_for_centering[1]+i),
                                                         (self.size[0]-i*2, self.size[1]-i*2)),
                                                         self.color
                                             )

        elif self.shape == 'Circle':

            if self.line_width is not None:
                for i in range(self.line_width):
                    pygame.gfxdraw.circle(self.surface,
                                           self.position[0],
                                           self.position[1],
                                           self.size[0] - i,
                                           self.color
                                           )


        elif self.shape == 'Ellipse':

            if self.line_width is not None:
                for i in range(self.line_width):
                    pygame.gfxdraw.ellipse(self.surface,
                                           self.position[0],
                                           self.position[1],
                                           self.size[0] - i,
                                           self.size[1] - i,
                                           self.color
                                           )



    # SETTING STYLE OF THIS INDICATOR
    def set_style(self, style):

        # SETTING STYLE WITH STRING
        if style == "Line_NoFill_5_5":
            self.line_width = 5
            self.line_radius = 5
        elif style == "Line_NoFill_10_5":
            self.line_width = 10
            self.line_radius = 5
        elif style == "Line_NoFill_15_5":
            self.line_width = 15
            self.line_radius = 5
        elif style == "Line_NoFill_20_5":
            self.line_width = 20
            self.line_radius = 5
        elif style == "Line_NoFill_25_5":
            self.line_width = 25
            self.line_radius = 5


    # < GETTING AND SETTING ATTRIBUTES >
    #
    # BELOW IS GOOD REFERENCE !
    # https://www.datacamp.com/community/tutorials/property-getters-setters
    #
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color



# ------------------------------------------------
# ACTUAL CLASS FOR NODE OBJECT
class NNNodeButton(NNNode):

    # CONSTRUCTOR

    # < REGISTERING FUNCTION TO FUNCTION'S PARAMETER >
    # https://www.programiz.com/python-programming/function-argument
    # : ONCE WE DEFINED 'DEFAULT VALUE' TO PARAMETER, (LIKE position=(0, 0))
    #   AFTER THAT DEFINITION, WE HAVE TO DEFINE DEFAULT VALUE !
    #
    #   THAT IS WHY, 'callback' PARAMETER IS PLACED TO 3RD POSITION
    def __init__(self,
                 surface,
                 callback,
                 id='objNone',
                 shape='Rectangle',
                 position=(0, 0),
                 center=(0, 0),
                 size_w=30,
                 size_h=30,
                 duration=1000,
                 animation_type='Fixed',
                 xscaler=0.005,
                 yscaler= 300,
                 clickable= False,
                 the_value= 0
                 ):

        super().__init__(id, animation_type, duration, xscaler, yscaler, -1)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # STORING POSITION AS INITIALIZATION
        self.position = position

        # STORING SHAPE
        self.shape = shape

        # COLOR PALLETE
        self.color_default = self.textcolor_main
        self.color_selected = (0, 0, 0)
        self.color_hover = (235, 20, 10)

        self.color = self.color_default

        if "Btn_Reset" in id:
            self.color_default = (130, 130, 130)
            self.color = self.color_default
            self.color_hover = (190, 190, 190)

        # SETTING CENTER
        self.center = center

        # SETTING SIZE
        self.size_w = size_w
        self.size_h = size_h

        # MOUSE CLICK FLAG
        self.clickable = clickable


        # SETTING VALUE TO -1 BECAUSE WE DO NOT WANT TO BE USED AS DRAWPAD PIXEL
        self.the_value = -1


        # Timer FOR RECOVERING 'CLICKABLE'
        self.recoverduration = 600

        self.recovertimer = Timer.Timer([self.recoverduration])


        # REGISTERING CALLBACK FUNCTION

        self.callback_function = callback



    # UPDATING
    def update(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeObject::update() -- {self.obj_id}")

        # < MOUSE CURSOR WITH COLOR >
        #
        # IF THE FLAG FOR CLICKABLE IS True...
        if self.clickable:
            area = NNRegion([self.position[0] - self.size_w // 2, self.position[1] - self.size_h // 2],             # VERTEX OF TOP-LEFT
                            [self.position[0] + self.size_w // 2, self.position[1] + self.size_h // 2],             # VERTEX OF TOP-RIGHT
                            [self.position[0] - self.size_w // 2, self.position[1] - self.size_h // 2],             # VERTEX OF BOTTOM-LEFT
                            [self.position[0] + self.size_w // 2, self.position[1] + self.size_h // 2]              # VERTEX OF BOTTOM-RIGHT
                            )


            # COLLISION TEST
            # MOUSE POSITION EVENT
            if area.is_colliding( pygame.mouse.get_pos() ):

                # COLOR OF CURSOR
                self.color = self.color_hover

                # < VALUE SETTING FOR NEURAL NETWORK >
                # GETTING MOUSE CURSOR POSITION
                check_leftbutton_clicked = pygame.mouse.get_pressed(3)[0]

                # < MOUSE BUTTON EVENT HANDLING >
                # IF LEFT MOUSE BUTTON WAS PRESSED...
                if check_leftbutton_clicked:

                    # SET THE the_value BE TOGGLED
                    self.clicked = True

                    # IF THE TIMER FOR RECOVERING CLICKABLE WAS FULFILLED,
                    # YOU CAN EXECUTE CALLBACK FUNCTION AGAIN !
                    if self.recovertimer.get_result()["time_elapsed"] == -1:

                        # EXECUTE CALLBACK FUNCTION
                        self.callback_function()

                        # RE-NEW THE TIMER
                        self.recovertimer = None
                        self.recovertimer = Timer.Timer([self.recoverduration])

            else:
                # IF THE VALUE IS NOT SETTED...
                # DEFAULT COLOR
                self.color = self.color_default

                # DEFAULT VALUE OF clicked VARIABLE
                self.clicked = False

            # NO MATTER WHAT THIS NODE HAS the_value, THE TIMER WILL FLOW
            self.recovertimer.timer_tick()


        # IF THERE IS NO NEED TO CLICK...
        else:
            # DEFAULT COLOR
            self.color = self.color_default

            # TIMER TURN OFF
            self.recovertimer = None



        # UPDATING THIS OBJECT
        super().update()




    def toggle_color(self):
        if self.color == self.color_default:
            self.color = self.color_selected
        elif self.color == self.color_selected:
            self.color = self.color_default




    # RENDERING
    def render(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeObject::render() -- {self.obj_id}")

        # DRAWING CIRCLE IN PYGAME
        # https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/drawing-circles/

        if self.shape == 'Rectangle':
            pygame.draw.rect(self.surface, self.color, pygame.Rect((self.position[0] - self.size_w // 2, self.position[1] - self.size_h // 2), (self.size_w, self.size_h)))
        elif self.shape == 'Circle':
            pygame.draw.circle(self.surface, self.color, self.position, self.size_w)
        elif self.shape == "Left_Triangle":
            pygame.draw.polygon(self.surface, self.color, [(self.position[0] - self.size_w // 2, self.position[1]), (self.position[0]+self.size_w - self.size_w // 2, self.position[1]-self.size_h), (self.position[0]+self.size_w - self.size_w // 2, self.position[1]+self.size_h)])
        elif self.shape == "Right_Triangle":
            pygame.draw.polygon(self.surface, self.color, [(self.position[0] + self.size_w // 2, self.position[1]), (self.position[0]-self.size_w + self.size_w // 2, self.position[1]-self.size_h), (self.position[0]-self.size_w + self.size_w // 2, self.position[1]+self.size_h)])



    # < GETTING AND SETTING ATTRIBUTES >
    #
    # BELOW IS GOOD REFERENCE !
    # https://www.datacamp.com/community/tutorials/property-getters-setters
    #
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color



# --------------------------------------------------------------------------------------------------------------


# CLASS FOR TEXT
class NNNodeText(NNNode):

    # CONSTRUCTOR
    def __init__ (self, surface, id='objNone', text='OK', position=(0, 0), text_color=(160, 50, 90), text_size=50, duration=1000, animation_type='Fixed', xscaler=0.005, yscaler= 300, visible=False, align='Center'):
        super().__init__(id, animation_type, duration, xscaler, yscaler, -1, 0)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # TEXT SIZE
        self.text_size = text_size

        # TEXT TO BE DISPLAYED
        self.text = text

        # VISIBILITY
        self.visible = visible

        # FONT NAME
        self.font_name = 'GenEiChikugoMin2-R.ttf'

        # FONT SETTING
        # pygame.font.Font CLASS
        # https://www.pygame.org/docs/ref/font.html#pygame.font.Font
        # : create a new Font object from a file
        #
        # SO, BELOW WILL CREATE THE FONT OBJECT
        self.textStyle = pygame.font.Font(self.font_name, self.text_size)

        # DEFAULT STYLE WITH PYGAME COLOR
        self.color = pygame.Color(text_color)
        #self.color = pygame.Color((160, 50, 90))

        # TEXT OBJECT CREATION USING CUSTOM MADE FUNCTION 'text_objects'
        self.TextSurf, self.TextRect = self.createText(self.text, self.textStyle, self.color)

        # < ALPHA COLOR TO TEXT OBJECT >
        # IF animation_type IS 'SequentialText' WE NEED ALPHA IMAGE
        # https://stackoverflow.com/questions/49594895/render-anti-aliased-transparent-text-in-pygame
        # https://github.com/pygame/pygame/issues/1413
        # https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        self.alpha_image = None

        if animation_type == "SequentialText":
            # PREPARING ALPHA IMAGE SURFACE
            self.alpha_image = pygame.Surface(self.TextSurf.get_size(), flags=pygame.SRCALPHA)

            # SET THE ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value ))

            # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
            self.alpha_image.blit(self.TextSurf, self.TextRect, special_flags=pygame.BLEND_RGBA_MULT)

        else:
            self.alpha_image = None


        # STORING POSITION AS INITIALIZATION
        self.position = position

        # ALIGNING FLAG
        self.align_flag = align


        # ALIGNED POSITION
        #
        # < ABOUT ERROR 'TypeError: 'tuple' object does not support item assignment' >
        # https://stackoverflow.com/questions/7735838/typeerror-tuple-object-does-not-support-item-assignment-when-swapping-values
        # : Evaluating "1,2,3" results in (1, 2, 3), a tuple. As you've discovered, tuples are immutable. Convert to a list before processing.
        #
        # CONVERTING LIST TO TUPLE
        # https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/
        #
        aligned_position = list(self.position)

        if self.align_flag == "Center":
            aligned_position = [aligned_position[0] - self.TextSurf.get_width() // 2, aligned_position[1] - self.TextSurf.get_height() // 2]
        elif self.align_flag == "Left":
            aligned_position = [aligned_position[0], aligned_position[1] - self.TextSurf.get_height() // 2]

        self.position = tuple(aligned_position)



    def update(self):
        super().update()

        # < UPDATING TEXT WITH PROPER ALPHA VALUE >
        # : HERE, WE BASICALLY APPLY TEXT SURFACE TO APLHA IMAGE
        #
        # IF ANIMATION TYPE IS SequentialText...
        if self.animation_type == "SequentialText":
            # TEXT OBJECT CREATION USING CUSTOM MADE FUNCTION 'text_objects'
            self.TextSurf, self.TextRect = self.createText(self.text, self.textStyle, self.color)

            # UPDATING ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value))

            # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
            self.alpha_image.blit(self.TextSurf, self.TextRect, special_flags=pygame.BLEND_RGBA_MULT)

        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeText::update() -- {self.obj_id}   {self.anim.result_value}")




    def render(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeText::render() -- {self.obj_id}")


        # blit() FUNCTION
        # http://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
        # : Draws a source Surface onto this Surface.
        #
        # FORMAT :
        # blit(source, dest, area=None, special_flags=0)

        # ONLY RENDER IF visible FLAG IS True
        if self.visible:

            if self.animation_type == "SequentialText":
                self.surface.blit(self.alpha_image, self.position)

            else:
                self.surface.blit(self.TextSurf, self.position)



    def createText(self, text, font, color):

        textSurface = font.render(text, True, color)
        #textRect = textSurface.get_rect(center=(textSurface.get_width() // 2, textSurface.get_height() // 2))
        textRect = textSurface.get_rect()


        # get_rect() FUNCTION
        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_rect
        # : Getting the rectangular area of the Surface.
        #   An example would be mysurf.get_rect(center=(100, 100)) to create a
        #   rectangle for the Surface centered at a given position.
        #
        #
        # FORMAT
        # : get_rect(**kwargs) -> Rect
        #   Returns a new rectangle covering the entire surface. This rectangle
        #   will always start at (0, 0) with a width and height the same size as
        #   the image.
        #
        return textSurface, textRect



    def set_style(self, text, size, color):
        self.text = text
        self.text_size = size
        self.textStyle = pygame.font.Font(self.font_name, self.text_size)
        self.color = pygame.Color(color)

        # UPDATE TEXT OBJECT USING CUSTOM MADE FUNCTION 'text_objects'
        self.TextSurf, self.TextRect = self.createText(self.text, self.textStyle, self.color)



    # GETTING AND SETTING ATTRIBUTES
    # POSITION
    #
    # BELOW IS GOOD REFERENCE !
    # https://www.datacamp.com/community/tutorials/property-getters-setters
    #
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position
        # < ADDING ADDITIONAL PROCESS WHEN WE ACCESS TO POSITION OUT OF THIS OBJECT >
        #
        # TODO :: BELOW IS CRITICAL !
        #
        # SO, HERE WE NEED TO WRITE POSITION VALUE TO 'TextRect.center'
        # BUT, OUTSIDE OF THIS OBJECT (TEXT), THE 'POSITION' VALUE IS USING.
        # --> THAT MEANS, EVEN IF WE UPDATE THE POSITION, WE CAN NOT UPDATE 'self.TextRect.center'
        #
        #     SO, WE MADE 'GETTER & SETTER' FUNCTIONS WE ADDED 'SOME ADDITIONAL PROCESS' !
        #self.TextRect.center = self.__position


    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        self.__visible = visible



# --------------------------------------------------------------------------------------------------------------


# TODO :: SHOULD BELOW CLASS BE THE CHILD CLASS FROM NodeText ?

# CLASS FOR MULTI-TEXTS
class NNNodeMultiText(NNNode):

    # CONSTRUCTOR
    def __init__ (self, surface, id='objNone', text='OK', position=(0, 0), text_color=(160, 50, 90), text_size=50, duration=1000, animation_type='Fixed', xscaler=0.005, yscaler= 300, visible=False, align='Center', line_margin=20, text_align="Left", rotation=0):

        super().__init__(id, animation_type, duration, xscaler, yscaler, -1, 0)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # TEXT SIZE
        self.text_size = text_size

        # TEXT TO BE DISPLAYED
        self.text = text

        # VISIBILITY
        self.visible = visible

        # STORING POSITION AS INITIALIZATION
        self.position = position

        # ALIGNING FLAG
        self.align_flag = align

        # FONT NAME
        self.font_name = 'GenEiChikugoMin2-R.ttf'

        # FONT SETTING
        # pygame.font.Font CLASS
        # https://www.pygame.org/docs/ref/font.html#pygame.font.Font
        # : create a new Font object from a file
        #
        # SO, BELOW WILL CREATE THE FONT OBJECT
        self.textStyle = pygame.font.Font(self.font_name, self.text_size)

        # DEFAULT STYLE WITH PYGAME COLOR
        self.color = pygame.Color(text_color)
        # self.color = pygame.Color((160, 50, 90))

        # MARGIN WIDTH OF LINE
        self.line_margin = line_margin

        # ALIGNING LINES
        self.text_align = text_align

        # ROTATION VARIABLE
        self.rotation = rotation

        #self.text_multiline = text.splitlines()
        self.text_multiline = self.text.split("\\n")

        self.textsurf_list = []
        self.textrect_list = []


        # SETUP
        self.setup()



    def setup(self):

        text_count = 0

        for text in self.text_multiline:
            # TEXT OBJECT CREATION USING CUSTOM MADE FUNCTION 'text_objects'
            textSurf, textRect = self.createText(text, self.textStyle, self.color)

            self.textsurf_list.append(textSurf)

            textRect.y += text_count * textRect.height + text_count * self.line_margin
            self.textrect_list.append(textRect)

            text_count += 1


        # < MAKING ONE SURFACE >
        # IF animation_type IS 'SequentialText' WE NEED ALPHA IMAGE
        # https://stackoverflow.com/questions/49594895/render-anti-aliased-transparent-text-in-pygame
        # https://github.com/pygame/pygame/issues/1413
        # https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        self.alpha_image = None
        self.alpha_image_size = [0, 0]

        if self.animation_type == "SequentialText":

            # PREPARING ALPHA IMAGE SURFACE
            past_rectsize_width = 0

            # CALCULATING SIZE ACCUMULATING EVERY SURFACES
            for textrect in self.textrect_list:

                # FINDING WIDEST RECT
                if list(textrect)[2] >= past_rectsize_width:
                    self.alpha_image_size[0] = list(textrect)[2]

                    # STORING WIDTH SIZE
                    past_rectsize_width = list(textrect)[2]
                else:
                    self.alpha_image_size[0] = self.alpha_image_size[0]

                    # STORING WIDTH SIZE
                    past_rectsize_width = self.alpha_image_size[0]

                # GATHERING HEIGHTS FOR HEIGHT OF THE SURFACE
                self.alpha_image_size[1] += list(textrect)[3] + self.line_margin

            # CREATING MAIN SURFACE TO STORE THE RECTS
            self.alpha_image = pygame.Surface(self.alpha_image_size, flags=pygame.SRCALPHA)

            # SET THE ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value))


            # ------------------------------------------------------------------------------------------
            # < BLITTING TEXT SURFACE TO MAIN SURFACE >
            # :: WE WILL DO THAT WITH THE text_align SETTINGS

            if self.text_align == "Left":

                # RE-POSITIONING THE RECT IN self.textrect_list
                #
                # MOVING THE RECTS WHICH IS NOT THE WIDEST ONE

                widest_rect, widest_index = self.get_widest_rect(self.textrect_list)

                for index in range(len(self.textrect_list)):
                    # EXCLUDING THE WIDEST RECT USING THE INDEX WE GOT ABOVE
                    if index != widest_index:

                        # RE-POSITION IT

                        # RE-APPLYING NEW POSITION TO THAT RECT
                        self.textrect_list[index][0] = 0

                    self.alpha_image.blit(self.textsurf_list[index], self.textrect_list[index], special_flags=pygame.BLEND_RGBA_MULT)


            elif self.text_align == "Center":

                # RE-POSITIONING THE RECT IN self.textrect_list
                #
                # MOVING THE RECTS WHICH IS NOT THE WIDEST ONE

                widest_rect, widest_index = self.get_widest_rect(self.textrect_list)

                for index in range(len(self.textrect_list)):
                    # EXCLUDING THE WIDEST RECT USING THE INDEX WE GOT ABOVE
                    if index != widest_index:

                        # RE-POSITION IT

                        # CENTER X POSITION SHOULD BE THE HALF-WIDTH OF THE WIDEST RECT
                        center = widest_rect[2] // 2

                        # AND EVERY OTHER RECTS SHOULD BE POSITIONED
                        # AT THE HALF-LENGTH POSITION FROM ITS OWN WIDTH
                        new_position_x = center - (self.textrect_list[index][2] // 2)

                        # RE-APPLYING NEW POSITION TO THAT RECT
                        self.textrect_list[index][0] = new_position_x

                    self.alpha_image.blit(self.textsurf_list[index], self.textrect_list[index], special_flags=pygame.BLEND_RGBA_MULT)

            elif self.text_align == "Right":

                # RE-POSITIONING THE RECT IN self.textrect_list
                #
                # MOVING THE RECTS WHICH IS NOT THE WIDEST ONE

                widest_rect, widest_index = self.get_widest_rect(self.textrect_list)

                for index in range(len(self.textrect_list)):
                    # EXCLUDING THE WIDEST RECT USING THE INDEX WE GOT ABOVE
                    if index != widest_index:

                        # RE-POSITION IT

                        # THE ZERO POINT TO REPOSITION SHOULD BE
                        #
                        right = widest_rect[2]

                        # AND EVERY OTHER RECTS SHOULD BE POSITIONED
                        # AT THE PLACE THE SUBTRACTED VALUE WITH ITS OWN WIDTH
                        new_position_x = right - self.textrect_list[index][2]

                        # RE-APPLYING NEW POSITION TO THAT RECT
                        self.textrect_list[index][0] = new_position_x

                    self.alpha_image.blit(self.textsurf_list[index], self.textrect_list[index], special_flags=pygame.BLEND_RGBA_MULT)


        else:
            self.alpha_image = None


        # < CENTERING POSITION WITH CONVERTING TUPLE TO LIST TEMPORALILY >
        #
        # < ABOUT ERROR 'TypeError: 'tuple' object does not support item assignment' >
        # https://stackoverflow.com/questions/7735838/typeerror-tuple-object-does-not-support-item-assignment-when-swapping-values
        # : Evaluating "1,2,3" results in (1, 2, 3), a tuple. As you've discovered, tuples are immutable. Convert to a list before processing.
        #
        # CONVERTING LIST TO TUPLE
        # https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/
        #
        aligned_position = list(self.position)

        if self.alpha_image:

            if self.align_flag == "Center":

                aligned_position = [aligned_position[0] - self.alpha_image.get_width() // 2,
                                    aligned_position[1] - self.alpha_image.get_height() // 2]

            elif self.align_flag == "Left":

                aligned_position = [aligned_position[0],
                                    aligned_position[1] - self.alpha_image.get_height() // 2]

        self.position = tuple(aligned_position)





    def update(self):
        super().update()

        #self.setup()

        if self.animation_type == "SequentialText":

            # FIRST PREPARING THE SURFACE
            self.alpha_image = pygame.Surface(self.alpha_image_size, flags=pygame.SRCALPHA)

            # UPDATING ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value))

            # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
            for index in range(len(self.text_multiline)):
                self.alpha_image.blit(self.textsurf_list[index], self.textrect_list[index], special_flags=pygame.BLEND_RGBA_MULT)


        else:
            self.alpha_image = None




    def render(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeText::render() -- {self.obj_id}")

        # ONLY RENDER IF visible FLAG IS True
        if self.visible:

            if self.animation_type == "SequentialText":

                # ROTATION
                surf = pygame.transform.rotate(self.alpha_image, self.rotation)

                # TODO :: CONSIDERING AA TO ROTATED TEXT !
                # surf_smoothed = pygame.transform.smoothscale(surf,
                #                                              (int(surf.get_size()[0] * 0.95), int(surf.get_size()[1] * 0.95))
                #                                              )
                # surf_smoothed.set_colorkey((255, 255, 255))

                surf.set_colorkey((255, 255, 255))
                self.surface.blit(surf, self.position)

            else:
                self.surface.blit(self.textsurf_list[0], self.position)



    def createText(self, text, font, color):

        textSurface = font.render(text, True, color)
        #textRect = textSurface.get_rect(center=(textSurface.get_width() // 2, textSurface.get_height() // 2))
        textRect = textSurface.get_rect()

        return textSurface, textRect



    def set_style(self, text, size, color):
        self.text = text

        self.text_size = size
        self.textStyle = pygame.font.Font(self.font_name, self.text_size)
        self.color = pygame.Color(color)

        self.text_multiline = text.splitlines()

        self.textsurf_list = []
        self.textrect_list = []

        text_count = 0

        for text in self.text_multiline:
            # TEXT OBJECT CREATION USING CUSTOM MADE FUNCTION 'text_objects'
            textSurf, textRect = self.createText(text, self.textStyle, self.color)

            self.textsurf_list.append(textSurf)

            textRect.y += text_count * textRect.height + text_count * self.line_margin
            self.textrect_list.append(textRect)

            text_count += 1


        # < MAKING ONE SURFACE >
        # IF animation_type IS 'SequentialText' WE NEED ALPHA IMAGE
        # https://stackoverflow.com/questions/49594895/render-anti-aliased-transparent-text-in-pygame
        # https://github.com/pygame/pygame/issues/1413
        # https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        self.alpha_image = None

        alpha_image_size = [0, 0]

        if self.animation_type == "SequentialText":
            # PREPARING ALPHA IMAGE SURFACE
            past_rectsize_width = 0

            # CALCULATING SIZE ACCUMULATING EVERY SURFACES
            for textrect in self.textrect_list:

                if list(textrect)[2] >= past_rectsize_width:
                    alpha_image_size[0] = list(textrect)[2]
                else:
                    alpha_image_size[0] = alpha_image_size[0]

                alpha_image_size[1] += list(textrect)[3] + self.line_margin


            self.alpha_image = pygame.Surface(alpha_image_size, flags=pygame.SRCALPHA)

            # SET THE ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value))

            # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
            for index in range(len(self.text_multiline)):
                self.alpha_image.blit(self.textsurf_list[index], self.textrect_list[index], special_flags=pygame.BLEND_RGBA_MULT)

        else:
            self.alpha_image = None


    # GETTING AND SETTING ATTRIBUTES
    # POSITION
    #
    # BELOW IS GOOD REFERENCE !
    # https://www.datacamp.com/community/tutorials/property-getters-setters
    #
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position
        # < ADDING ADDITIONAL PROCESS WHEN WE ACCESS TO POSITION OUT OF THIS OBJECT >
        #
        # TODO :: BELOW IS CRITICAL !
        #
        # SO, HERE WE NEED TO WRITE POSITION VALUE TO 'TextRect.center'
        # BUT, OUTSIDE OF THIS OBJECT (TEXT), THE 'POSITION' VALUE IS USING.
        # --> THAT MEANS, EVEN IF WE UPDATE THE POSITION, WE CAN NOT UPDATE 'self.TextRect.center'
        #
        #     SO, WE MADE 'GETTER & SETTER' FUNCTIONS WE ADDED 'SOME ADDITIONAL PROCESS' !
        #self.TextRect.center = self.__position


    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        self.__visible = visible


    # TODO :: MOVE TO THE PARENT CLASS
    #
    # https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame/54714144
    def get_rect_rotated(self, rect, pos, originPos, angle):

        # calcaulate the axis aligned bounding box of the rotated image
        w, h = rect.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(rect, angle)

        return rotated_image, origin



    def get_widest_rect(self, rect_list):

        widest_width = 0
        widest_rect_index = -1

        if rect_list and len(rect_list) > 0:
            for index in range(len(rect_list)):
                if rect_list[index].width > widest_width:
                    # UPDATING TO NEW VALUE (DATA FOR COMPARE, INDEX)
                    widest_width = rect_list[index].width
                    widest_rect_index = index
                else:
                    # EVERYTHINGS SAME
                    widest_width = widest_width
                    widest_rect_index = widest_rect_index

            return (rect_list[widest_rect_index], widest_rect_index)



# --------------------------------------------------------------



# CLASS FOR PICTURE
class NNNodePic(NNNode):

    # CONSTRUCTOR
    def __init__ (self, surface, id='objNone', pic_file='PATH', position=(0, 0), pic_size=50, duration=1000, animation_type='Fixed', xscaler=0.005, yscaler= 300, visible=False, rotation = 0, align='Left_Up'):
        super().__init__(id, animation_type, duration, xscaler, yscaler, -1, 0)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # TEXT SIZE
        self.pic_size = pic_size

        # FILE PATH
        self.pic_file_path = pic_file

        # PYGAME IMAGE OBJECT
        self.pic_obj = pygame.image.load(self.pic_file_path)
        self.size_w, self.size_h = self.pic_obj.get_size()

        # STORING POSITION AS INITIALIZATION
        self.position = position
        self.rotation = rotation

        # VISIBILITY
        self.visible = visible



        # < ALPHA COLOR TO TEXT OBJECT >
        # IF animation_type IS 'SequentialText' WE NEED ALPHA IMAGE
        # https://stackoverflow.com/questions/49594895/render-anti-aliased-transparent-text-in-pygame
        # https://github.com/pygame/pygame/issues/1413
        # https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        self.alpha_image = None

        if animation_type == "SequentialPic":
            # PREPARING ALPHA IMAGE SURFACE
            self.alpha_image = pygame.Surface(self.pic_obj.get_size(), flags=pygame.SRCALPHA)

            # SET THE ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value ))

            # CREATING PYGAME PICTURE OBJECT
            self.pic_surface, self.pic_origin = self.get_image_rotated( self.pic_obj, self.position,
                                                                       (self.size_w // 2, self.size_h // 2),
                                                                        self.rotation)

            # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
            self.alpha_image.blit(self.pic_surface, self.pic_surface.get_rect(), special_flags=pygame.BLEND_RGBA_MULT)

        else:
            self.alpha_image = None





    def update(self):
        super().update()

        # < UPDATING TEXT WITH PROPER ALPHA VALUE >
        # : HERE, WE BASICALLY APPLY TEXT SURFACE TO APLHA IMAGE
        #
        # IF ANIMATION TYPE IS SequentialText...
        if self.animation_type == "SequentialPic":

            # CREATING PYGAME PICTURE OBJECT
            self.pic_surface, self.pic_origin = self.get_image_rotated( self.pic_obj,
                                                                        self.position,
                                                                       (self.size_w // 2, self.size_h // 2),
                                                                        self.rotation)


            # PREPARING ALPHA IMAGE SURFACE
            self.alpha_image = pygame.Surface(self.pic_surface.get_size(), flags=pygame.SRCALPHA)


            # UPDATING ALPHA VALUE
            self.alpha_image.fill(pygame.Color(255, 255, 255, self.anim.result_value))


            # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
            rect = self.pic_surface.get_rect()
            self.alpha_image.blit(self.pic_surface, rect, special_flags=pygame.BLEND_RGBA_MULT)


        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeText::update() -- {self.obj_id}   {self.anim.result_value}")




    def render(self):
        #print(f"{getframeinfo(currentframe()).filename} -- {getframeinfo(currentframe()).lineno}  NNNodeText::render() -- {self.obj_id}")

        #ONLY RENDER IF visible FLAG IS True
        if self.visible:

            if self.animation_type == "SequentialPic":
                # rotate and blit the image
                self.surface.blit(self.alpha_image, self.pic_origin)

                # draw rectangle around the image
                #pygame.draw.rect(self.surface, (255, 0, 0), (*self.pic_origin, *self.pic_surface.get_size()), 2)
            else:
                self.surface.blit(self.pic_surface, self.pic_origin)


    # ----------------------------------------------------------------------------------------------------------------


    #
    # https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame/54714144
    def get_image_rotated(self, image, pos, originPos, angle):

        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        return rotated_image, origin



    def get_image_rotated_2(self, surf, image, topleft, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect.topleft)
        pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)



    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position


    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        self.__visible = visible




# ------------------------------------------------
# LINE OBJECT

class NNNodeLine(NNNode):

    # CONSTRUCTOR
    def __init__(self, surface, vertices, id='objNone', type='Straight', position=(0, 0), duration=1000, animation_type='Fixed', xscaler=1.0, yscaler=1.0, color=(200,10,50), freq=1, style='Line_NoFill_10_5', view_cv = False, arrow_scale=70.0, arrow_adjust=40.0, arrow_visible=True, adding_direction=(0.0, 1.0)):
        super().__init__(id, animation_type, duration, xscaler, yscaler, -1, freq)

        # SURFACE TO BE DRAWN
        self.surface = surface

        # VERTICES TO DRAW
        self.vertices = vertices

        # STORING POSITION AS INITIALIZATION
        self.position = position

        # STORING SHAPE
        self.type = type

        # SETTING COLOR (0 - 255 RANGE)
        self.color = color                  # TUPLE
        self.initial_alpha = color[3]

        # SETTING STYLE OF THIS OBJECT
        self.style = style

        self.line_width = None
        self.line_radius = None

        # SET THE INITIAL COLOR AND TEXT
        self.set_style(self.style)

        # FOR DISPLAYING CONTROL VERTICES
        self.view_cv = view_cv

        # HOW LARGE ARROW HEAD IS ?
        self.arrow_scale = arrow_scale
        self.arrow_adjust = arrow_adjust
        self.arrow_visible = arrow_visible

        # DIRECTION TO EXPAND
        self.adding_direction = list(adding_direction)



    # UPDATING
    def update(self):
        # UPDATING THIS OBJECT
        super().update()

        # < UPDATING COLOR >
        # IF ANIMATION TYPE IS 'Sine_0_255'...
        if self.animation_type == "Sine_0_255":
            animating_alpha = self.anim.get_result()

            self.color = (self.color[0], self.color[1], self.color[2], animating_alpha)

        elif self.animation_type == "Cosine_0_255":
            animating_alpha = self.anim.get_result()

            self.color = (self.color[0], self.color[1], self.color[2], animating_alpha)


    # RENDERING
    def render(self):

        if self.type == 'Straight':

            pygame.draw.lines(self.surface,
                              self.color,
                              False,
                              self.vertices,
                              self.line_width  # LINE WIDTH
                              )

            # DRAW TRIANGLE

            # CALCULATING VECTOR
            base_vertice = [self.vertices[-1][0], self.vertices[-1][1]]
            vertice_one_before = [self.vertices[-2][0], self.vertices[-2][1]]

            vector = [base_vertice[0] - vertice_one_before[0], base_vertice[1] - vertice_one_before[1]]
            norm = numpy.sqrt(vector[0] ** 2 + vector[1] ** 2)
            vector_norm = [vector[0] / norm, vector[1] / norm]

            # SLIDE LITTLE ALONG THE NORMALIZED AXIS
            base_vertice = [base_vertice[0] + vector_norm[0] * 40, base_vertice[1] + vector_norm[1] * 40]

            # CALCULATING ROTATION TO SPECIFY THE OTHER TWO POINTS
            arrow_height = 50.0
            arrow_theta_a = math.radians(225)
            arrow_theta_b = math.radians(135)

            point_a = [vector_norm[0] * math.cos(arrow_theta_a) - vector_norm[1] * math.sin(arrow_theta_a),
                       vector_norm[0] * math.sin(arrow_theta_a) + vector_norm[1] * math.cos(arrow_theta_a)]

            point_b = [vector_norm[0] * math.cos(arrow_theta_b) - vector_norm[1] * math.sin(arrow_theta_b),
                       vector_norm[0] * math.sin(arrow_theta_b) + vector_norm[1] * math.cos(arrow_theta_b)]

            pygame.gfxdraw.filled_trigon(self.surface,
                                         int(base_vertice[0]), int(base_vertice[1]),
                                         int(base_vertice[0] + point_a[0] * arrow_height),
                                         int(base_vertice[1] + point_a[1] * arrow_height),
                                         int(base_vertice[0] + point_b[0] * arrow_height),
                                         int(base_vertice[1] + point_b[1] * arrow_height),
                                         self.color
                                         )

            # IF self.view_cv IS True, DISPLAY ALL CONTROL VERTICES
            if self.view_cv:
                for vert in self.vertices:
                    pygame.gfxdraw.filled_circle(self.surface,
                                                 vert[0],
                                                 vert[1],
                                                 5,
                                                 (255, 0, 0)
                                                 )



        elif self.type == 'Curve':
            if self.line_width is not None:

                # CREATING MULTIPLE VERTICES ALONG WITH THE WIDTH
                slide_nparray = numpy.ones((len(self.vertices), 2))
                #adding = [0.0, 1.0]
                adding = self.adding_direction

                # MULTIPLING ONE-HOT VECTOR TO SELECT THE DIRECTION TO EXPAND
                slide_nparray = numpy.multiply(slide_nparray, numpy.array(adding))


                # -----------------------------------------------------------------------------------------
                # DRAW BEZIER LINE

                # LINE MAKING TO POSITIVE DIRECTION
                for i in range(self.line_width // 2):
                    input_nparray = numpy.array(self.vertices)

                    # IF THE WIDTH IS 2, BELOW WILL BE [0, 0], [1, 1]
                    index = [i, i]

                    # ([0, 0], [1, 1]) x [1, 1] THEN 'PLUS' TO input_nparray
                    added_nparray = numpy.add(input_nparray, numpy.multiply(slide_nparray, numpy.array(index)))

                    pygame.gfxdraw.bezier(self.surface, added_nparray, 5, self.color)


                # LINE MAKING TO NEGATIVE DIRECTION
                for i in range(self.line_width // 2):
                    input_nparray = numpy.array(self.vertices)

                    # IF THE WIDTH IS 2, BELOW WILL BE [0, 0], [1, 1]
                    index = [i, i]

                    # ([0, 0], [1, 1]) x [1, 1] THEN 'PLUS' TO input_nparray
                    added_nparray = numpy.subtract(input_nparray, numpy.multiply(slide_nparray, numpy.array(index)))

                    pygame.gfxdraw.bezier(self.surface, added_nparray, 5, self.color)




                # -----------------------------------------------------------------------------------------
                # DRAW TRIANGLE

                # CALCULATING VECTOR (DIRECTION OF ARROW)
                base_vertice = [self.vertices[-1][0], self.vertices[-1][1]]
                vertice_one_before = [self.vertices[-2][0], self.vertices[-2][1]]

                vector = [base_vertice[0] - vertice_one_before[0], base_vertice[1] - vertice_one_before[1]]
                norm = numpy.sqrt(vector[0]**2 + vector[1]**2)
                vector_norm = [vector[0] / norm, vector[1] / norm]

                # SLIDE LITTLE ALONG THE NORMALIZED AXIS
                base_vertice = [base_vertice[0] + vector_norm[0] * self.arrow_adjust, base_vertice[1] + vector_norm[1] * self.arrow_adjust]


                # CALCULATING ROTATION TO SPECIFY THE OTHER TWO POINTS
                #arrow_height = 70.0
                arrow_height = self.arrow_scale
                arrow_theta_a = math.radians(210)
                arrow_theta_b = math.radians(150)


                point_a = [vector_norm[0] * math.cos(arrow_theta_a) - vector_norm[1] * math.sin(arrow_theta_a),
                           vector_norm[0] * math.sin(arrow_theta_a) + vector_norm[1] * math.cos(arrow_theta_a)]

                point_b = [vector_norm[0] * math.cos(arrow_theta_b) - vector_norm[1] * math.sin(arrow_theta_b),
                           vector_norm[0] * math.sin(arrow_theta_b) + vector_norm[1] * math.cos(arrow_theta_b)]


                if self.arrow_visible:

                    pygame.gfxdraw.filled_trigon(self.surface,
                                                 int(base_vertice[0]), int(base_vertice[1]),
                                                 int(base_vertice[0] + point_a[0]*arrow_height), int(base_vertice[1] + point_a[1]*arrow_height),
                                                 int(base_vertice[0] + point_b[0]*arrow_height), int(base_vertice[1] + point_b[1]*arrow_height),
                                                 self.color
                                                 )


                # ----------------------------------------------------------------
                # IF self.view_cv IS True, DISPLAY ALL CONTROL VERTICES
                if self.view_cv:
                    for vert in self.vertices:
                        pygame.gfxdraw.filled_circle(self.surface,
                                                      vert[0],
                                                      vert[1],
                                                      5,
                                                      (255, 0, 0)
                                                      )







    # SETTING STYLE OF THIS INDICATOR
    def set_style(self, style):

        # SETTING STYLE WITH STRING
        if style == "Line_NoFill_5_5":
            self.line_width = 5
            self.line_radius = 5
        elif style == "Line_NoFill_10_5":
            self.line_width = 10
            self.line_radius = 5
        elif style == "Line_NoFill_15_5":
            self.line_width = 15
            self.line_radius = 5
        elif style == "Line_NoFill_20_5":
            self.line_width = 20
            self.line_radius = 5
        elif style == "Line_NoFill_25_5":
            self.line_width = 25
            self.line_radius = 5
        elif style == "Line_NoFill_2_5":
            self.line_width = 2
            self.line_radius = 5


    # < GETTING AND SETTING ATTRIBUTES >
    #
    # BELOW IS GOOD REFERENCE !
    # https://www.datacamp.com/community/tutorials/property-getters-setters
    #
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color



# --------------------------------------------------------------



class NNRectRoundedAliased(object):

    def __init__(self):
        pass

    #
    # https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
    def AAfilledRoundedRect(self, surface, rect, color, radius=0.4):
        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """

        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        return surface.blit(rectangle, pos)










# ------------------------------------------------
# CLASS FOR DEFINITION OF 'REGION'
class NNRegion(object):

    def __init__(self, vertex_top_left, vertex_top_right, vertex_bottom_left, vertex_bottom_right):

        self.vertex_top_left = vertex_top_left
        self.vertex_top_right = vertex_top_right
        self.vertex_bottom_left = vertex_bottom_left
        self.vertex_bottom_right = vertex_bottom_right

    def is_colliding(self, position):

        # CHECK X POSITION
        if self.vertex_top_left[0] <= position[0] <= self.vertex_top_right[0] and \
                self.vertex_bottom_left[0] <= position[0] <= self.vertex_bottom_right[0]:

            # CHECK Y POSITION
            if self.vertex_top_left[1] <= position[1] <= self.vertex_top_right[1] and \
                    self.vertex_bottom_left[1] <= position[1] <= self.vertex_bottom_right[1]:
                return True
            else:
                return False
        else:
            return False




