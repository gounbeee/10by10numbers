import time
import numpy as np
from threading import Thread
#from multiprocessing import Process

class NNPixelArray(object):


    def __init__(self, dict):

        # INPUT
        self.dict_data = dict

        # -----------------------------------
        # RESULT DATA

        # PIXEL ARRAYS
        self.pixel_array_weight_v = []
        self.pixel_array_weight_w = []
        self.pixel_array_hidden_a = []
        self.pixel_array_hidden_relu = []
        self.pixel_array_hidden_b = []
        self.pixel_array_output_u = []
        self.pixel_array_softmax = []

        self.pixel_array_weight_v_newtrain = []
        self.pixel_array_weight_w_newtrain = []


        # POSITIONS OF NODES AND LAYERS
        self.start_pos_weight_v = ()
        self.start_pos_weight_w = ()
        self.start_pos_hidden_a = ()
        self.start_pos_hidden_relu = ()
        self.start_pos_hidden_b = ()
        self.start_pos_output_u = ()
        self.start_pos_softmax = ()

        self.start_pos_weight_v_newtrain = ()
        self.start_pos_weight_w_newtrain = ()



    def all_nodes_layers_create_pixelarray(self):
        self.create_pixels_array_weight_v(self.dict_data["weight_v"])
        self.create_pixels_array_weight_w(self.dict_data["weight_w"])
        self.create_pixels_array_hidden_a(self.dict_data["hidden_a"])
        self.create_pixels_array_hidden_relu(self.dict_data["hidden_relu"])
        self.create_pixels_array_hidden_b(self.dict_data["hidden_b"])
        self.create_pixels_array_output_u(self.dict_data["output_u"])
        self.create_pixels_array_softmax(self.dict_data["softmax"])

        self.create_pixel_array_weight_v_newtrain(self.dict_data["weight_v_newtrain"])
        self.create_pixel_array_weight_w_newtrain(self.dict_data["weight_w_newtrain"])



    def nodes_layers_create_pixelarray(self, category):
        if category == "Weight_V":

            self.create_pixels_array_weight_v(self.dict_data["weight_v"])
        elif category == "Hidden_A":
            self.create_pixels_array_hidden_a(self.dict_data["hidden_a"])
        elif category == "Hidden_Relu":
            self.create_pixels_array_hidden_relu(self.dict_data["hidden_relu"])
        elif category == "Hidden_B":
            self.create_pixels_array_hidden_b(self.dict_data["hidden_b"])
        elif category == "Weight_W":
            self.create_pixels_array_weight_w(self.dict_data["weight_w"])
        elif category == "Output_U":
            self.create_pixels_array_output_u(self.dict_data["output_u"])
        elif category == "Softmax":
            self.create_pixels_array_softmax(self.dict_data["softmax"])
        elif category == "Weight_v_newtrain":
            self.create_pixel_array_weight_v_newtrain(self.dict_data["weight_v_newtrain"])
        elif category == "Weight_w_newtrain":
            self.create_pixel_array_weight_w_newtrain(self.dict_data["weight_w_newtrain"])



    def all_nodes_layers_create_pixelarray_threads(self):

        # MULTIPROCESSING OR MULTITHREADING IS USED BELOW !!
        # https://www.udemy.com/course/mastering-python-3-programming/learn/lecture/15194624#overview

        process_weight_v = Thread(target=self.create_pixels_array_weight_v, args=(self.dict_data["weight_v"], ))
        process_weight_w = Thread(target=self.create_pixels_array_weight_w, args=(self.dict_data["weight_w"], ))
        process_hidden_a = Thread(target=self.create_pixels_array_hidden_a, args=(self.dict_data["hidden_a"], ))
        process_hidden_relu = Thread(target=self.create_pixels_array_hidden_relu, args=(self.dict_data["hidden_relu"], ))
        process_hidden_b = Thread(target=self.create_pixels_array_hidden_b, args=(self.dict_data["hidden_b"], ))
        process_output_u = Thread(target=self.create_pixels_array_output_u, args=(self.dict_data["output_u"], ))
        process_softmax = Thread(target=self.create_pixels_array_softmax, args=(self.dict_data["softmax"], ))



        process_weight_v.start()
        process_weight_w.start()
        process_hidden_a.start()
        process_hidden_relu.start()
        process_hidden_b.start()
        process_output_u.start()
        process_softmax.start()

        process_weight_v.join()
        process_weight_w.join()
        process_hidden_a.join()
        process_hidden_relu.join()
        process_hidden_b.join()
        process_output_u.join()
        process_softmax.join()






    # -------------------------------------------------------------------------------

    # TODO :: ARCHIVE BELOW !
    # BECAUSE MULTIPROCESSING USES 'PICKLING THE OBJECT' BUT OUR PYGAME SURFACE CANNOT BE PICKLED,
    # SO WE NEED TO SEPERATE THE < PIXEL-ARRAY-MAKING > AND < GETTING-SURFACE > FROM IT
    #
    # https://www.reddit.com/r/pygame/comments/az2y4b/how_to_use_multiprocessing_with_pygame/

    def create_pixels_array_weight_v(self, result_dict_from_update):
        self.pixel_array_weight_v, self.start_pos_weight_v = self.create_pixels_array(result_dict_from_update)

    def create_pixels_array_weight_w(self, result_dict_from_update):
        self.pixel_array_weight_w, self.start_pos_weight_w = self.create_pixels_array(result_dict_from_update)

    def create_pixels_array_hidden_a(self, result_dict_from_update):
        self.pixel_array_hidden_a, self.start_pos_hidden_a  = self.create_pixels_array(result_dict_from_update)

    def create_pixels_array_hidden_relu(self, result_dict_from_update):
        self.pixel_array_hidden_relu, self.start_pos_hidden_relu = self.create_pixels_array(result_dict_from_update)

    def create_pixels_array_hidden_b(self, result_dict_from_update):
        self.pixel_array_hidden_b, self.start_pos_hidden_b = self.create_pixels_array(result_dict_from_update)

    def create_pixels_array_output_u(self, result_dict_from_update):
        self.pixel_array_output_u, self.start_pos_output_u = self.create_pixels_array(result_dict_from_update)

    def create_pixels_array_softmax(self, result_dict_from_update):
        self.pixel_array_softmax, self.start_pos_softmax = self.create_pixels_array(result_dict_from_update)


    def create_pixel_array_weight_v_newtrain(self, result_dict_from_update):
        self.pixel_array_weight_v_newtrain, self.start_pos_weight_v_newtrain = self.create_pixels_array(result_dict_from_update)

    def create_pixel_array_weight_w_newtrain(self, result_dict_from_update):
        self.pixel_array_weight_w_newtrain, self.start_pos_weight_w_newtrain = self.create_pixels_array(result_dict_from_update)



    # -------------------------------------------------------------------------------
    # < MAKING PIXEL ARRAY FROM DATA >
    # < SHARING FUNCTION >

    def create_pixels_array(self, result_dict_from_update):

        pos_diff_from_center_x = result_dict_from_update["pos_diff_from_center_x"]
        pos_diff_from_center_y = result_dict_from_update["pos_diff_from_center_y"]
        count_width = result_dict_from_update["countWidth"]
        count_height = result_dict_from_update["countHeight"]
        width = result_dict_from_update["unitWidth"]
        height = result_dict_from_update["unitHeight"]
        margin_w = result_dict_from_update["marginWidth"]
        margin_h = result_dict_from_update["marginHeight"]
        color = result_dict_from_update["Color"]
        value = result_dict_from_update["ResultValue"]


        #   TODO :: ARCHIVE BELOW
        # ---------------------------------------------------

        # << DIRECT NUMPY ARRAY >>
        # CHANGE METHOD TO USE RAW ARRAY OF PIXELS

        # ---------------------------------------------------

        # < GETTING COLOR >

        color_array = []

        # < SPEEDING UP WITH LIST ! >
        # https://stackoverflow.com/questions/54945933/performance-of-numpy-insert-dependant-from-array-size-workaround


        # < CREATING ARRAY WITH TUPLE >
        # https://stackoverflow.com/questions/40709519/initialize-64-by-64-numpy-of-0-0-tuples-in-python
        # a = np.empty((64, 64), dtype=object)
        # for y in range(64):
        #     for x in range(64):
        #         a[y, x] = (255, 255, 255)



        #starttime = time.time()
        #print(f"PROFILING < GETTING COLOR >... STARTED ...")



        for hcnt_index in range(count_height):
                for wcnt_index in range(count_width):

                    # COLOR ADJUSTING WITH WEIGHT VALUE
                    if count_height == 1:
                        color_with_value_r = color[0] - value[wcnt_index] * 255
                        color_with_value_g = color[1] - value[wcnt_index] * 255
                        color_with_value_b = color[2] - value[wcnt_index] * 255
                    else:
                        color_with_value_r = color[0] - value[wcnt_index][hcnt_index] * 255
                        color_with_value_g = color[1] - value[wcnt_index][hcnt_index] * 255
                        color_with_value_b = color[2] - value[wcnt_index][hcnt_index] * 255

                    # COLOR VALUE CLAMPING
                    if color_with_value_r <= 0:
                        color_with_value_r = 1
                    elif color_with_value_r > 255:
                        color_with_value_r = 255

                    if color_with_value_g <= 0:
                        color_with_value_g = 1
                    elif color_with_value_g > 255:
                        color_with_value_g = 255

                    if color_with_value_b <= 0:
                        color_with_value_b = 1
                    elif color_with_value_b > 255:
                        color_with_value_b = 255

                    # GETTING COLORS
                    the_color = (int(color_with_value_r), int(color_with_value_g), int(color_with_value_b))

                    # SAVE THE COLOR TO ARRAY
                    color_array.append(the_color)



        #endtime = time.time()
        #print(f"         ... ENDED : ELAPSED --> {endtime - starttime}")




        # BELOW IS FOR TESTING
        # color_array = [
        #     [[10,10,10], [30,30,30], [60,60,60], [120,120,120], [150,150,150], [180,180,180], [200,200,200], [210,210,210], [230,230,230], [244,0,244]],
        #     [[20,10,10], [30,30,30], [60,60,60], [120,120,120], [150,150,150], [180,180,180], [200,200,200], [210,210,210], [230,230,230], [244,244,0]],
        #     [[30,10,10], [30,30,30], [60,60,60], [120,120,120], [150,150,150], [180,180,180], [200,200,200], [210,210,210], [230,230,230], [0,244,244]],
        #     [[40,10,10], [30,30,30], [60,60,60], [120,120,120], [150,150,150], [180,180,180], [200,200,200], [210,210,210], [230,230,230], [244,0,244]],
        # ]

        color_array = np.array(color_array)
        color_array = np.reshape(color_array, (count_height, count_width, 3))

        # < FILL RECTS AREA WITH COLOR >
        #
        # ** (NOT INCLUDING MARGINS) **
        #                                  260                        400
        pixel_array = np.zeros((int(height) * count_height, int(width) * count_width, 3), dtype=float)



        #starttime = time.time()
        #print(f"PROFILING < APPLYING COLOR >... STARTED ...")


        # FOR ALL PIXELS...
        # h WILL GO TO 0 - 260
        # w WILL GO TO 0 - 400
        for h_c in range(count_height):                               # 4
            for w_c in range(count_width):                            # 10
                for h_px in range(int(height)):                       # 65
                    for w_px in range(int(width)):                    # 40

                        # BELOW'S INDEX 'SHIFTS' TO NEXT ROWS  AND COLUMNS
                        pixel_array[h_px + int(height) * h_c][w_px + int(width) * w_c] = color_array[h_c][w_c]


        #endtime = time.time()
        #print(f"         ... ENDED : ELAPSED --> {endtime - starttime}")



        # < INSERTING MARGINS >
        # < USING numpy.insert() >
        #

        # ---------------------------------------------------------------------
        # TODO :: ARCHIVE BELOW !
        # I USED 'REVERSED ORDER' FOR INDEX
        # BECAUSE I JUST ITERATED AT THE BELOW,
        # SO THE RESULT ARRAY WILL BE CHANGED IF I STARTED FROM THE LOWER INDEX !
        # ---------------------------------------------------------------------

        # https://stackoverflow.com/questions/7286365/print-a-list-in-reverse-order-with-range


        #starttime = time.time()
        #print(f"PROFILING < CREATING MARGINS >... STARTED ...")

        #print(pixel_array)

        pixel_array = list(pixel_array)




        #
        # # CREATING VERTICAL MARGIN AREA
        # for hcnt_index in reversed(range(count_height)):
        #     # SKIP 0 INDEX
        #     if hcnt_index is not 0:
        #
        #         # SIMPLE-ITERATING FOR CREATING MARGINAL BAND
        #         # INSERTING 0 COLUMNS DURING THE LENGTH OF HORIZONTAL-MARGIN
        #         for h_margin in range(margin_h):
        #             pixel_array = np.insert(pixel_array, int(height) * (hcnt_index), (0, 0, 0), axis=0)
        #
        #
        #
        #
        #
        # # CREATING HORIZONTAL MARGIN AREA
        # for wcnt_index in reversed(range(count_width)):
        #     # SKIP 0 INDEX
        #     if wcnt_index is not 0:
        #
        #         # SIMPLE-ITERATING FOR CREATING MARGINAL BAND
        #         # INSERTING 0 COLUMNS DURING THE LENGTH OF HORIZONTAL-MARGIN
        #         for w_margin in range(margin_w):
        #             pixel_array = np.insert(pixel_array, int(width) * (wcnt_index), (0, 0, 0), axis=1)
        #
        #             # LIST VERSION TO SPEED UP
        #             #pixel_array.insert(int(width) * (wcnt_index), (0, 0, 0))
        #







        #endtime = time.time()
        #print(f"         ... ENDED : ELAPSED --> {endtime - starttime}")


        # < TRANSPOSE THE MATRIX ! >
        # : BECAUSE THE HEIGHT AND WIDTH WAS INVERTED, SO WE NEEDED TO TRANSPOSE THE MATRIX.
        #
        #   TODO :: BELOW IS CRITICAL !!
        #   https://note.nkmk.me/en/python-numpy-transpose/
        #   transpose() is useful, for example, when a 3D array is a group of 2D arrays.
        #   If the data of matrices are stored as a 3D array of shape (n, row, column),
        #   all matrices can be transposed as follows.
        #
        #   EXAMPLE:
        #
        #   print(a_3d)
        # [[[ 0  1  2  3]
        #   [ 4  5  6  7]
        #   [ 8  9 10 11]]
        #
        #  [[12 13 14 15]
        #   [16 17 18 19]
        #   [20 21 22 23]]]
        #
        # print(a_3d.shape)
        # (2, 3, 4)
        #
        # ---------------------------------
        #                       TODO :: BELOW IS CRITICAL !!!
        #                       v-- THIS MEANS THAT THE INDEX NUMBER OF DIMENSION  OF MULTI-DIMENSION VECTOR !!!
        #                                  :: IN THIS CASE, THE FIRST DIMENSION (0) WILL BE KEPT AS SAME !!!
        # print(a_3d.transpose( 0, 2, 1))
        #  [[[ 0  4  8]
        #    [ 1  5  9]
        #    [ 2  6 10]
        #    [ 3  7 11]]
        #
        #   [[12 16 20]
        #    [13 17 21]
        #    [14 18 22]
        #    [15 19 23]]]
        #
        # print(a_3d.transpose(0, 2, 1).shape)
        # (2, 4, 3)


        pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))

        # POSITION OF THE AREA
        position_center_x = self.dict_data["screen_width"] // 2
        position_center_y = self.dict_data["screen_height"] // 2

        start_position_to_draw_x = position_center_x - pixel_array.shape[0] // 2 + pos_diff_from_center_x
        start_position_to_draw_y = position_center_y - pixel_array.shape[1] // 2 + pos_diff_from_center_y


        return pixel_array, (start_position_to_draw_x, start_position_to_draw_y)




