#print('------------------ NNModel MODULE ENTERED')
import numpy as np
import os
import glob
import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from inspect import currentframe, getframeinfo, stack


# データ読み込み
# 評価処理 (戻り値は精度と損失関数)
from sklearn.metrics import accuracy_score
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# TO GENERATE THE IMAGE
from PIL import Image


# USING MATPLOTLIB
# WHEN YOU IMPORT MATPLOTLIB LIBRARY,
# YOU CREATE 'SUB-FOLDER' NAMED 'PYPLOT' AS 'SUB-PACKAGE'
import matplotlib.pyplot as plt


class NN(object):


    # TODO :: ** ARCHIVE THIS **
    #         IMPORTING MODULE WILL CAUSE RECURSIVE OBJECT WHEN MULTIPROCESSING !
    #         WHEN I USED 'GLOBAL-SCOPE' MODULE, AND MADE INSTANCE IN THAT
    #         I HAVE GOT SEVERAL EXECUTIONS OF THIS CLASS.
    #         ESPECIALLY, IN THE SITUATION OF 'MULTI-PROCESSING'
    #
    #         -> SO I CREATED NNModel INSTANCE IN SPECIFIC PLACE WHICH USES THIS OBJECT,
    #            THEN, MADE THIS OBJECT TO SINGLETON !


    # SINGLETON PATTERN
    # BECAUSE WE ARE CREATE THIS OBJECT IN THE GLOBAL MODULE FOR SAFETY
    # TODO :: FIX THIS !

    __instance = None

    @staticmethod
    def get_instance():
        if NN.__instance is None:
            NN.__instance = NN()


        #print(getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
        #print(NN.__instance)
        #print(f'PARENT PID --   {os.getppid()}')
        #print(f'PID --   {os.getpid()}')

        return NN.__instance


    def __init__(self):

        print('NN EXECUTED')



        # -----------------------------------------------------------------
        # < MAKING DATASETS >

        #self.preparing_geometry_data()

        #self.preparing_dataset()
        #self.preparing_dataset_original_size()



        # -----------------------------------------------------------------
        # FLAG FOR EXECUTION OF TRAINING OR NOT
        self.training_mode = False


        # -----------------------------------------------------------------
        # < LOADING DATA >


        # LOADING MODIFIED DATASET FROM PICKLE
        #self.dataset_data, self.dataset_label = self.proc_01_loading('geometry_10px.pickle', 'geometry_10px_labels.pickle')
        self.dataset_data, self.dataset_label = self.proc_01_loading('mnist_10px.pickle', 'mnist_10px_labels.pickle')
        #self.dataset_data, self.dataset_label = self.proc_01_loading('mnist_28px.pickle', 'mnist_28px_labels.pickle')

        # < CONVERT DATA TO NDARRAY TYPE OF NUMPY >
        self.x_org, self.y_org = self.proc_02_convert_10px(self.dataset_data, self.dataset_label)
        #self.x_org, self.y_org = self.proc_02_convert_28px(self.dataset_data, self.dataset_label)


        # < ADDING DUMMY DATA TO 'FIRST' PLACE IN THE INPUT DATA (X VALUE) >
        self.x_all = self.proc_03_add_dummy(self.x_org)

        # << PREPARING Y VALUE (TARGET VALUE) >>
        self.y_all_one = self.proc_04_prepare_y_value(self.y_org)

        # < SPLITTING THE DATASETS TO 2 GROUPS >
        # (SPLITTING TO 'TRAINING' AND 'TEST')
        self.x_train, self.x_test, self.y_train, self.y_test, self.y_train_one, self.y_test_one = self.proc_05_split_two_groups(self.x_all, self.y_org, self.y_all_one)


        # FOR FINAL PREDICTION
        self.b1_test = None
        self.yp_test_one = None
        self.yp_test = 0




        # -----------------------------------------------------------------
        # < PREPARING TRAINING >

        if self.training_mode:

            # THE COUNTS OF LAYERS OF 'HIDDEN-LAYER'
            # (WHICH IS VERTICALLY ALIGNED)
            self.H = self.proc_06_hidden_layer_count()

            # BELOW COUNTS IS FOR THE 'INPUT LAYER' BETWEEN THE
            # (OUTPUT LAYER OF HIDDEN LAYER) ~ (OUTPUT LAYER)
            self.H1 = self.proc_07_add_one_layer(self.H)

            # THE COUNTS OF DATASETS FOR TRAINING
            # 60000
            self.M = self.proc_08_add_one_layer(self.x_train)

            # THE DIMENSION OF INPUT DATA FOR TRAINING
            # 100
            self.D = self.proc_09_input_dimension(self.x_train)

            # HOW MANY CASES OF ANSWERS ?
            # 10 BECAUSE WE WANT TO CATEGORIZE DIGITS BETWEEN 0~9
            self.N = self.proc_10_categories_count(self.y_train_one)

            # LEARNING RATE
            self.alpha = self.proc_11_learning_rate()

            # HOW MANY TIMES WE TRAIN ? --> 100 TIMES IN THIS CASE
            self.nb_epoch = self.proc_12_epoch_count()

            # THE AMOUNT OF COUNT WE PICK UP RANDOMLY
            self.batch_size, self.B = self.proc_13_batch_size()

            # WEIGHTS BETWEEN 3 LAYERS
            self.V, self.W = self.proc_14_initial_weights(self.D, self.H, self.H1, self.N)

            # THIS IS FOR RECORD OF AMOUNT OF ACCURACY AND LOSS VALUES
            # THIS WILL BE USED 'WHEN WE PRINT THE RESULTS !'
            self.history3 = self.proc_15_initial_train_results()

            # BELOW IS FOR USING 'MINI-BATCH' METHOD
            #
            # < INDEX CLASS >
            # ( CUSTOM-MADE )
            # : THIS CLASS IS CONSTRUCTED WITH 2 PARAMETERS.
            #   PARAMETER 1 -- ENTIRE COUNTS OF INDEXES
            #   PARAMETER 2 -- SIZE OF MINI BATCHES
            #
            self.indexes = self.proc_16_initial_index(self.M, self.batch_size)

            # 繰り返し回数カウンタ初期化
            self.epoch = self.proc_17_initial_epoch()




        # -----------------------------------------------------------------
        # TRAINING


        if self.training_mode:

            # メイン処理 (シグモイド関数をLeRU関数に変更)
            while self.epoch < self.nb_epoch:

                # 学習対象の選択(ミニバッチ学習法)
                index, next_flag = self.indexes.next_index()
                x, yt = self.x_train[index], self.y_train_one[index]

                # 予測値計算 (順伝播)
                a = x @ self.V                                              # (10.6.3)
                b = self.ReLU(a)                                            # (10.6.4) ReLU化
                b1 = np.insert(b, 0, 1, axis=1)                             # ダミー変数の追加
                u = b1 @ self.W                                             # (10.6.5)
                yp = self.softmax(u)                                        # (10.6.6)

                # 誤差計算
                yd = yp - yt  # (10.6.7)
                bd = self.step(a) * (yd @ self.W[1:].T)                     # (10.6.8) ReLU化

                # 勾配計算
                self.W = self.W - self.alpha * (b1.T @ yd) / self.B         # (10.6.9)
                self.V = self.V - self.alpha * (x.T @ bd) / self.B          # (10.6.10)

                if next_flag:  # 1epoch 終了後の処理
                    score, loss = self.evaluate2(
                        self.x_test, self.y_test, self.y_test_one, self.V, self.W)
                    self.history3 = np.vstack((self.history3,
                                          np.array([self.epoch, loss, score])))
                    print("epoch = %d loss = %f score = %f"
                          % (self.epoch, loss, score))
                    self.epoch = self.epoch + 1

            # 損失関数値と精度の確認
            print('初期状態: 損失関数:%f 精度:%f'
                  % (self.history3[0, 1], self.history3[0, 2]))
            print('最終状態: 損失関数:%f 精度:%f'
                  % (self.history3[-1, 1], self.history3[-1, 2]))


            # 学習曲線の表示 (損失関数値)
            plt.plot(self.history3[:, 0], self.history3[:, 1])
            plt.ylim(0, 2.5)
            plt.xticks(size=14)
            plt.yticks(size=14)
            plt.grid(lw=2)
            plt.show()


            # 学習曲線の表示 (精度)
            plt.plot(self.history3[:, 0], self.history3[:, 2])
            plt.ylim(0, 1)
            plt.xticks(size=14)
            plt.yticks(size=14)
            plt.grid(lw=2)
            plt.show()




            # STORING V WEIGHT VALUES TO FILE

            # PREPARING ROWS FOR DATAFRAME IN PANDAS
            v_indices = []
            for row in range(self.V.shape[0]):
                v_indices.append('wght_V_input_' + str(row))

            # PREPARING COLUMNS FOR DATAFRAME IN PANDAS
            v_columns = []
            for col in range(self.V.shape[1]):
                v_columns.append('wght_V_layer_' + str(col))

            df_weight_V = pd.DataFrame(self.V, index=v_indices , columns=v_columns)
            df_weight_V.to_csv('weight_V.csv')




            # STORING W WEIGHT VALUES TO FILE

            # PREPARING ROWS FOR DATAFRAME IN PANDAS
            w_indices = []
            for row in range(self.W.shape[0]):
                w_indices.append('wght_W_input_' + str(row))

            # PREPARING COLUMNS FOR DATAFRAME IN PANDAS
            w_columns = []
            for col in range(self.W.shape[1]):
                w_columns.append('wght_W_layer_' + str(col))

            df_weight_W = pd.DataFrame(self.W, index=w_indices, columns=w_columns)
            df_weight_W.to_csv('weight_W.csv')





















        # -----------------------------------------------------------------
        # PREDICT


        # LOADING WEIGHT VALUES FROM FILE
        # < WEIGHT V >
        #
        weight_V = pd.read_csv('weight_V.csv')
        #print(weight_V)

        # < SELECTING 2D AREA IN THE PANDAS DATAFRAME AND NUMPY ARRAY >
        #
        # PANDAS DATAFRAME TO NUMPY ARRAY
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_numpy.html
        #
        np_weight_V = weight_V.to_numpy()
        rows_cnt = np_weight_V.shape[0]
        columns_cnt = np_weight_V.shape[1]

        # ADVANCED SLICING TO NUMPY ARRAY (2D)
        # https://www.w3schools.com/python/numpy_array_slicing.asp
        # https://www.w3schools.com/python/trypython.asp?filename=demo_numpy_array_slicing_2d
        #
        #
        #            *  *  *              ---> from '1:4'
        # arr = [[1, 2, 3, 4, 5],
        #        [6, 7, 8, 9, 10]]      * ---> from '1'
        #
        # arr[1, 1:4]
        #
        # OUTPUT == [7 8 9]
        #
        # : From the second element, slice elements from index 1 to index 4 (not included):
        #                                                                    ************
        weight_V_result = np_weight_V[0:rows_cnt, 1:columns_cnt]

        # CHANGING DTYPE
        #
        # astype() FUNCTION
        # https://www.geeksforgeeks.org/change-data-type-of-given-numpy-array/
        weight_V_result = weight_V_result.astype('float32')

        self.weight_V_result = weight_V_result



        #  -----------------------------------------------------------------
        # < WEIGHT W >
        #
        weight_W = pd.read_csv('weight_W.csv')
        #print(weight_W)


        np_weight_W = weight_W.to_numpy()
        rows_cnt = np_weight_W.shape[0]
        columns_cnt = np_weight_W.shape[1]

        weight_W_result = np_weight_W[0:rows_cnt, 1:columns_cnt]
        weight_W_result = weight_W_result.astype('float32')

        self.weight_W_result = weight_W_result




    # -------------------------------------------------------------------------------------------------------------------------------
    # < FUNCTIONS >

    def reset_prediction(self):
        self.b1_test = None
        self.yp_test_one = None
        self.yp_test = 0


    def proc_01_loading(self, path_datasets, path_labels):

        # -------------------------------------------------------------------------------------
        # < LOADING DATA >

        # LOADING MODIFIED DATASET FROM PICKLE
        # https://stackoverflow.com/questions/31791011/how-do-i-save-a-self-made-dataset-in-python-so-that-i-can-use-it-later
        dataset_data = []
        dataset_label = []

        # LOADING DATASETS FROM PICKLE DATA
        with open(path_datasets, 'rb') as data:
            dataset_data = pickle.load(data)

        with open(path_labels, 'rb') as data:
            dataset_label = pickle.load(data)

        #print(dataset_data)
        #print(dataset_label)

        return dataset_data, dataset_label



    def proc_02_convert_28px(self, dataset_data, dataset_label):
        # -------------------------------------------------------------------------------------
        # < CONVERT DATA TO NDARRAY TYPE OF NUMPY >

        # https://note.nkmk.me/en/python-numpy-list/
        dataset_data = np.array(dataset_data)
        dataset_label = np.array(dataset_label)

        # print(dataset_data.dtype)
        # print(dataset_label[0])

        # CASTING TYPE OF ndarray TO SPECIFIC TYPES WE WANT
        # https://note.nkmk.me/python-numpy-dtype-astype/
        x_org = dataset_data.astype(np.float32)
        y_org = dataset_label.astype(np.int32)


        # UNTIL NOW, THE DATASET IS (10 x 10) DATA AND 70000 COUNTS. (70000, 10, 10)
        # SO WE WILL CHANGE DIMENSION
        x_org = np.reshape(x_org, (70000, 784))



        # print('========= x_org =========')
        # print(x_org)
        # print('=========================')
        # print('========= x_org[0] =========')
        # print(x_org[0])
        # print('=========================')
        # print('========= x_org.shape =========')
        # print(x_org.shape)
        # print('=========================')
        #
        # print('========= y_org =========')
        # print(y_org)
        # print(y_org[0])
        # print('=========================')
        # print('========= y_org.shape =========')
        # print(y_org.shape)
        # print('=========================')
        #
        # print(f'x_org  -- dtype  -->   {x_org.dtype}')          # float32
        # print(f'y_org  -- dtype  -->   {y_org.dtype}')          # int32


        return x_org, y_org



    def proc_02_convert_10px(self, dataset_data, dataset_label):
        # -------------------------------------------------------------------------------------
        # < CONVERT DATA TO NDARRAY TYPE OF NUMPY >

        # https://note.nkmk.me/en/python-numpy-list/
        dataset_data = np.array(dataset_data)
        dataset_label = np.array(dataset_label)

        # print(dataset_data.dtype)
        # print(dataset_label[0])

        # CASTING TYPE OF ndarray TO SPECIFIC TYPES WE WANT
        # https://note.nkmk.me/python-numpy-dtype-astype/
        x_org = dataset_data.astype(np.float32)
        y_org = dataset_label.astype(np.int32)



        # UNTIL NOW, THE DATASET IS (10 x 10) DATA AND 70000 COUNTS. (70000, 10, 10)
        # SO WE WILL CHANGE DIMENSION
        x_org = np.reshape(x_org, (70000, 100))

        # x_org = np.reshape(x_org, (300, 100))

        # print('========= x_org =========')
        # print(x_org)
        # print('=========================')
        # print('========= x_org[0] =========')
        # print(x_org[0])
        # print('=========================')
        # print('========= x_org.shape =========')
        # print(x_org.shape)
        # print('=========================')
        #
        # print('========= y_org =========')
        # print(y_org)
        # print(y_org[0])
        # print('=========================')
        # print('========= y_org.shape =========')
        # print(y_org.shape)
        # print('=========================')
        #
        # print(f'x_org  -- dtype  -->   {x_org.dtype}')  # float32
        # print(f'y_org  -- dtype  -->   {y_org.dtype}')  # int32

        return x_org, y_org




    def proc_03_add_dummy(self, x_org):
        # -------------------------------------------------------------------------------------
        # < ADDING DUMMY DATA TO 'FIRST' PLACE IN THE INPUT DATA (X VALUE) >

        # BELOW IS 'NOT REQUIRED' BECAUSE
        # I CONVERTED TO BOOLEAN VALUE (0 OR 1)
        # step1 データ正規化 値の範囲を[0, 1]とする
        x_norm = x_org / 255.0

        # 先頭にダミー変数(1)を追加
        #x_all = np.insert(x_org, 0, 1, axis=1)

        # BELOW IS FOR GRAYSCALE IMAGE
        x_all = np.insert(x_norm, 0, 1, axis=1)


        #print(x_all)  # [0. 0. ... 0. 0. 0.] : 100 COUNTS -->>  [1. 0. 0. ... 0. 0. 0.] : 101 COUNTS
        #                                          *
        #print('ダミー変数追加後', x_all.shape)  # ダミー変数追加後 (70000, 101)

        return x_all



    def proc_04_prepare_y_value(self, y_org):
        # -------------------------------------------------------------------------------------
        # << PREPARING Y VALUE (TARGET VALUE) >>

        # THERE ARE 10 TARGET VALUE (ANSWERS)
        # 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9
        #
        # AND IF '5' IS THE ANSWER...
        #
        # [0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0]  -->>  THIS IS 'ONE-HOT-VECTOR' FORMAT DATA
        #print('=====================  CONVERTING y TO ONE-HOT-VECTOR  =====================')

        ohe = OneHotEncoder(sparse=False)
        y_all_one = ohe.fit_transform(np.c_[y_org])

        # print('========= y_all_one =========')
        # print(y_all_one)
        # print(y_all_one.shape)
        # print(y_all_one[0])
        # print('=========================')

        return y_all_one



    def proc_05_split_two_groups(self, x_all, y_org, y_all_one):
        # -------------------------------------------------------------------------------------
        # < SPLITTING THE DATASETS TO 2 GROUPS >
        # (SPLITTING TO 'TRAINING' AND 'TEST')

        # train_test_split() FUNCTION
        # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
        # : Split arrays or matrices into random train and test subsets

        # x_train :: INPUT DATA FOR TRAINING
        # x_test  :: INPUT DATA FOR TEST
        # y_train :: OUTPUTTED DATA FOR TRAINING
        # y_test  :: OUTPUTTED DATA FOR TEST
        # y_train_one ::
        # y_test_one  ::
        x_train, x_test, y_train, y_test, y_train_one, y_test_one = train_test_split(x_all,
                                                                                     y_org,
                                                                                     y_all_one,
                                                                                     train_size=60000,
                                                                                     test_size=10000,
                                                                                     shuffle=False)


        #print(x_train.shape, x_test.shape, y_train.shape, y_test.shape, y_train_one.shape, y_test_one.shape)
        #    (60000, 11, 10) (10000, 11, 10) (60000,)       (10000,)      (60000, 10)        (10000, 10)

        return x_train, x_test, y_train, y_test, y_train_one, y_test_one



    # -------------------------------------------------------------------------------------
    # < PREPARING TRAINING >


    def proc_06_hidden_layer_count(self):
        # THE COUNTS OF LAYERS OF 'HIDDEN-LAYER'
        # (WHICH IS VERTICALLY ALIGNED)
        H = 128

        return H


    def proc_07_add_one_layer(self, H):
        # BELOW COUNTS IS FOR THE 'INPUT LAYER' BETWEEN THE
        # (OUTPUT LAYER OF HIDDEN LAYER) ~ (OUTPUT LAYER)
        H1 = H + 1

        return H1



    def proc_08_add_one_layer(self, x_train):
        # THE COUNTS OF DATASETS FOR TRAINING
        # 60000
        M = x_train.shape[0]

        return M


    def proc_09_input_dimension(self, x_train):
        # THE DIMENSION OF INPUT DATA FOR TRAINING
        # 100
        D = x_train.shape[1]

        return D


    def proc_10_categories_count(self, y_train_one):
        # HOW MANY CASES OF ANSWERS ?
        # 10 BECAUSE WE WANT TO CATEGORIZE DIGITS BETWEEN 0~9
        N = y_train_one.shape[1]

        return N


    def proc_11_learning_rate(self):
        # LEARNING RATE
        alpha = 0.1
        #alpha = 0.0001


        return alpha


    def proc_12_epoch_count(self):
        # HOW MANY TIMES WE TRAIN ? --> 100 TIMES IN THIS CASE
        nb_epoch = 100
        #nb_epoch = 1000

        return nb_epoch


    def proc_13_batch_size(self):
        # THE AMOUNT OF COUNT WE PICK UP RANDOMLY
        batch_size = 512
        #batch_size = 256
        B = batch_size

        return batch_size, B


    def proc_14_initial_weights(self, D, H, H1, N):
        # WEIGHTS BETWEEN 3 LAYERS
        #
        #      I           H           O
        #      N           I           U
        #      P  -  V  -  D  -  W  -  T
        #      U           D           P
        #      T           E           U
        #                  N           T
        #
        # WEIGHT LAYER 'V' -- BETWEEN INPUT AND HIDDEN LAYERS
        # WEIGHT LAYER 'W' -- BETWEEN HIDDEN AND OUTPUT LAYERS
        #
        V = np.random.randn(D, H) / np.sqrt(D / 2)
        W = np.random.randn(H1, N) / np.sqrt(H1 / 2)

        return V, W



    def proc_15_initial_train_results(self):
        # THIS IS FOR RECORD OF AMOUNT OF ACCURACY AND LOSS VALUES
        # THIS WILL BE USED 'WHEN WE PRINT THE RESULTS !'
        history3 = np.zeros((0, 3))

        return history3


    def proc_16_initial_index(self, M, batch_size):
        # BELOW IS FOR USING 'MINI-BATCH' METHOD
        #
        # < INDEX CLASS >
        # ( CUSTOM-MADE )
        # : THIS CLASS IS CONSTRUCTED WITH 2 PARAMETERS.
        #   PARAMETER 1 -- ENTIRE COUNTS OF INDEXES
        #   PARAMETER 2 -- SIZE OF MINI BATCHES
        #
        indexes = Indexes(M, batch_size)

        return indexes


    def proc_17_initial_epoch(self):
        # 繰り返し回数カウンタ初期化
        epoch = 0

        return epoch




    # ------------------------------------------------------------------------------------------------------------------
    # BELOWS ARE USING IN THE ACTUAL REALTIME-PREDICTION

    def weight_v_dot_product(self, input):
        return input @ self.weight_V_result

    def hidden_relu(self, input):
        return self.ReLU(input)


    def insert_dummy_node(self, input):
        b1_test = np.insert(input, 0, 1)
        return b1_test


    def weight_w_dot_product(self, input):
        return input @ self.weight_W_result


    def get_output_with_softmax(self, input):
        return self.softmax(input)


    def find_max_value_in_result(self, input):
        return np.argmax(input)


    def get_final_prediction(self, input):
        # CALCULATING PREDICTION
        self.b1_test = self.insert_dummy_node(self.hidden_relu(self.weight_v_dot_product(input)))
        self.yp_test_one = self.get_output_with_softmax(self.weight_w_dot_product(self.b1_test))
        self.yp_test = self.find_max_value_in_result(self.yp_test_one)


        # DISPLAYING GRAPH
        #plt.figure(figsize=(10, 3))
        #ax = plt.subplot(2, 1 / 2, 1)
        #plt.imshow(input[1:].reshape(10, 10), cmap='gray_r')
        #ax.set_title('%d:%d' % (y_selected[i], yp_test[i]), fontsize=14)
        #ax.get_xaxis().set_visible(False)
        #ax.get_yaxis().set_visible(False)
        #plt.show()

        return self.yp_test



    # --------------------------------------------------------------------
    # FOR TRAINING

    def train_prepare(self):

        # THE COUNTS OF LAYERS OF 'HIDDEN-LAYER'
        # (WHICH IS VERTICALLY ALIGNED)
        self.H = self.proc_06_hidden_layer_count()

        # BELOW COUNTS IS FOR THE 'INPUT LAYER' BETWEEN THE
        # (OUTPUT LAYER OF HIDDEN LAYER) ~ (OUTPUT LAYER)
        self.H1 = self.proc_07_add_one_layer(self.H)

        # THE COUNTS OF DATASETS FOR TRAINING
        # 60000
        self.M = self.proc_08_add_one_layer(self.x_train)

        # THE DIMENSION OF INPUT DATA FOR TRAINING
        # 100
        self.D = self.proc_09_input_dimension(self.x_train)

        # HOW MANY CASES OF ANSWERS ?
        # 10 BECAUSE WE WANT TO CATEGORIZE DIGITS BETWEEN 0~9
        self.N = self.proc_10_categories_count(self.y_train_one)

        # LEARNING RATE
        self.alpha = self.proc_11_learning_rate()

        # HOW MANY TIMES WE TRAIN ? --> 100 TIMES IN THIS CASE
        self.nb_epoch = self.proc_12_epoch_count()

        # THE AMOUNT OF COUNT WE PICK UP RANDOMLY
        self.batch_size, self.B = self.proc_13_batch_size()

        # WEIGHTS BETWEEN 3 LAYERS
        self.V, self.W = self.proc_14_initial_weights(self.D, self.H, self.H1, self.N)

        # THIS IS FOR RECORD OF AMOUNT OF ACCURACY AND LOSS VALUES
        # THIS WILL BE USED 'WHEN WE PRINT THE RESULTS !'
        self.history3 = self.proc_15_initial_train_results()

        # BELOW IS FOR USING 'MINI-BATCH' METHOD
        #
        # < INDEX CLASS >
        # ( CUSTOM-MADE )
        # : THIS CLASS IS CONSTRUCTED WITH 2 PARAMETERS.
        #   PARAMETER 1 -- ENTIRE COUNTS OF INDEXES
        #   PARAMETER 2 -- SIZE OF MINI BATCHES
        #
        self.indexes = self.proc_16_initial_index(self.M, self.batch_size)

        # 繰り返し回数カウンタ初期化
        self.epoch = self.proc_17_initial_epoch()



    # -------------------------------------------------------------------------------------------



    def train_1_select_trainset(self):
        # 学習対象の選択(ミニバッチ学習法)
        self.index, self.next_flag = self.indexes.next_index()
        self.x, self.yt = self.x_train[self.index], self.y_train_one[self.index]


    def train_2_calculate_predict_yp(self):
        # 予測値計算 (順伝播)
        self.a = self.x @ self.V  # (10.6.3)
        self.b = self.ReLU(self.a)  # (10.6.4) ReLU化
        self.b1 = np.insert(self.b, 0, 1, axis=1)  # ダミー変数の追加
        self.u = self.b1 @ self.W  # (10.6.5)
        self.yp = self.softmax(self.u)  # (10.6.6)


    def train_3_calculate_differences(self):
        # 誤差計算
        self.yd = self.yp - self.yt  # (10.6.7)
        self.bd = self.step(self.a) * (self.yd @ self.W[1:].T)  # (10.6.8) ReLU化


    def train_4_gradient_descent(self):
        # 勾配計算
        self.W = self.W - self.alpha * (self.b1.T @ self.yd) / self.B  # (10.6.9)
        self.V = self.V - self.alpha * (self.x.T @ self.bd) / self.B  # (10.6.10)


    # ---------------------------------------------------------------------------------------


    def train_to_visualize_only(self):

        if self.epoch < self.nb_epoch:

            # # 学習対象の選択(ミニバッチ学習法)
            # index, next_flag = self.indexes.next_index()
            # x, yt = self.x_train[index], self.y_train_one[index]
            self.train_1_select_trainset()


            # # 予測値計算 (順伝播)
            # a = x @ self.V  # (10.6.3)
            # b = self.ReLU(a)  # (10.6.4) ReLU化
            # b1 = np.insert(b, 0, 1, axis=1)  # ダミー変数の追加
            # u = b1 @ self.W  # (10.6.5)
            # yp = self.softmax(u)  # (10.6.6)
            self.train_2_calculate_predict_yp()


            # # 誤差計算
            # yd = yp - yt  # (10.6.7)
            # bd = self.step(a) * (yd @ self.W[1:].T)  # (10.6.8) ReLU化
            self.train_3_calculate_differences()


            # # 勾配計算
            # self.W = self.W - self.alpha * (b1.T @ yd) / self.B  # (10.6.9)
            # self.V = self.V - self.alpha * (x.T @ bd) / self.B  # (10.6.10)
            self.train_4_gradient_descent()



            # DISPLAYING PROCESSES FOR TRAINING
            if self.next_flag:  # 1epoch 終了後の処理
                self.score, self.loss = self.evaluate2(self.x_test, self.y_test, self.y_test_one, self.V, self.W)

                self.history3 = np.vstack((self.history3, np.array([self.epoch, self.loss, self.score])))

                #print("epoch = %d loss = %f score = %f" % (self.epoch, loss, score))

                self.epoch = self.epoch + 1



        #         return (self.epoch, loss, score)
        #
        #     else:
        #         message = (-1, -1, -1)
        #         return message
        #
        # else:
        #     message = (-1, -1, -1)
        #     return message




        # 損失関数値と精度の確認
        # print('初期状態: 損失関数:%f 精度:%f'
        #       % (self.history3[0, 1], self.history3[0, 2]))
        # print('最終状態: 損失関数:%f 精度:%f'
        #       % (self.history3[-1, 1], self.history3[-1, 2]))





        # DISPLAYING AND EXPORTING WEIGHTS TO FILE IS NOT NECESSARY!


        #
        # # 学習曲線の表示 (損失関数値)
        # plt.plot(self.history3[:, 0], self.history3[:, 1])
        # plt.ylim(0, 2.5)
        # plt.xticks(size=14)
        # plt.yticks(size=14)
        # plt.grid(lw=2)
        # plt.show()
        #
        #
        # # 学習曲線の表示 (精度)
        # plt.plot(self.history3[:, 0], self.history3[:, 2])
        # plt.ylim(0, 1)
        # plt.xticks(size=14)
        # plt.yticks(size=14)
        # plt.grid(lw=2)
        # plt.show()



        #
        # # STORING V WEIGHT VALUES TO FILE
        #
        # # PREPARING ROWS FOR DATAFRAME IN PANDAS
        # v_indices = []
        # for row in range(self.V.shape[0]):
        #     v_indices.append('wght_V_input_' + str(row))
        #
        # # PREPARING COLUMNS FOR DATAFRAME IN PANDAS
        # v_columns = []
        # for col in range(self.V.shape[1]):
        #     v_columns.append('wght_V_layer_' + str(col))
        #
        # df_weight_V = pd.DataFrame(self.V, index=v_indices, columns=v_columns)
        # df_weight_V.to_csv('weight_V.csv')
        #
        # # STORING W WEIGHT VALUES TO FILE
        #
        # # PREPARING ROWS FOR DATAFRAME IN PANDAS
        # w_indices = []
        # for row in range(self.W.shape[0]):
        #     w_indices.append('wght_W_input_' + str(row))
        #
        # # PREPARING COLUMNS FOR DATAFRAME IN PANDAS
        # w_columns = []
        # for col in range(self.W.shape[1]):
        #     w_columns.append('wght_W_layer_' + str(col))
        #
        # df_weight_W = pd.DataFrame(self.W, index=w_indices, columns=w_columns)
        # df_weight_W.to_csv('weight_W.csv')
        #




    # ------------------------------------------------------------------------------------------------------------------
    # UTILITIES




    # シグモイド関数
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))



    # softmax関数
    def softmax(self, x):
        x = x.T
        x_max = x.max(axis=0)
        x = x - x_max
        w = np.exp(x)
        return (w / w.sum(axis=0)).T




    # 交差エントロピー関数
    def cross_entropy(self, yt, yp):
        return -np.mean(np.sum(yt * np.log(yp), axis=1))




    # ReLU関数
    def ReLU(self, x):
        return np.maximum(0, x)



    # step関数
    def step(self, x):
        return 1.0 * (x > 0)



    # EVALUATE WITH 'SIGMOID MODEL'
    def evaluate(self, x_test, y_test, y_test_one, V, W):
        b1_test = np.insert(self.sigmoid(x_test @ V), 0, 1, axis=1)
        yp_test_one = self.softmax(b1_test @ W)
        yp_test = np.argmax(yp_test_one, axis=1)
        loss = self.cross_entropy(y_test_one, yp_test_one)
        score = accuracy_score(y_test, yp_test)
        return score, loss



    # EVALUATE WITH 'RELU MODEL'
    def evaluate2(self, x_test, y_test, y_test_one, V, W):
        b1_test = np.insert(self.ReLU(x_test @ V), 0, 1, axis=1)
        yp_test_one = self.softmax(b1_test @ W)
        yp_test = np.argmax(yp_test_one, axis=1)

        # CALCULATING LOSS WITH CROSS ENTROPY
        loss = self.cross_entropy(y_test_one, yp_test_one)

        # accuracy_score() FUNCTION
        # IN sklearn.metrics.accuracy_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
        # : In multilabel classification, this function computes subset accuracy:
        #   the set of labels predicted for a sample must exactly match the
        #   corresponding set of labels in y_true.
        #
        score = accuracy_score(y_test, yp_test)

        return score, loss





    def modify_datasets(self, datasets, original_list_size, new_list_size, flag_to_bool):
        # RESULT DATASETS
        result_datasets = []

        #
        original_list_sqrt = int(np.sqrt(original_list_size))
        new_list_sqrt = int(np.sqrt(new_list_size))

        # FOR EVERY DATASETS
        for index in range(len(datasets)):

            # < CREATING PICTURE FROM MNIST DATA SET >
            #
            # https://thispointer.com/python-convert-a-1d-array-to-a-2d-numpy-array-or-matrix/
            # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
            # https://stackoverflow.com/questions/42353676/display-mnist-image-using-matplotlib

            # GETTING ONE IMAGE FROM DATASETS
            data = np.array(datasets[index], dtype='float32')

            # INVERT IT TO WHITE
            # for i in range(original_list_size):
            #     if data[i] == 0.0:
            #         data[i] = 1.0

            # RESHAPE IT TO SQUARE-ROOTED SIZE
            data = data.reshape(original_list_sqrt,
                                original_list_sqrt)


            #
            #img = Image.fromarray(np.uint8(data*255), 'L')
            img = Image.fromarray(np.uint8(data), 'L')
            #img.save('my.png')
            #img.show()

            # RESIZING AND CONVERT TO BOOL-IMAGE (True OR False)
            # https://note.nkmk.me/python-pillow-image-resize/
            img_resized = img.resize((new_list_sqrt, new_list_sqrt))
            #img_resized.save('my.png')
            #img_resized.show()


            # IF FLAG TO BOOL IS ON...
            if flag_to_bool:
                # CONVERTING TO BOOLEAN IMAGE
                img_resized = self.convert_to_bool_image(img_resized)



            #img_resized_booled = self.convert_to_bool_image(img_resized)
            #img_resized.save('my.png')
            #img_resized_booled.save('my_booled.png')
            #img_resized.show()



            # RETURN TO ARRAY FROM PICTURE
            # https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays
            array = np.asarray(img_resized)



            """
            # INVERTED ARRAY OF LIST
            # https://stackoverflow.com/questions/7030831/how-do-i-get-the-opposite-negation-of-a-boolean-in-python
            # https://docs.python.org/ja/3/library/operator.html
            # : BELOW IS RECOMMENDED WHEN WE USE NUMPY !
            #   BECAUSE BOOLEAN IS SUBCLASS OF INTEGER IN PYTHON,
            #   SO IT WILL PRINT ACTUAL VALUE IN SOME CASE.
            inverted_array = ~array

            #print(array)
            #print(array.shape)
            #print(inverted_array)
            #print(inverted_array.shape)

            result_datasets.append(inverted_array)
            """


            result_datasets.append(array)

        return result_datasets


    def convert_to_bool_image(self, image):

        # IMAGE SIZE
        # https://note.nkmk.me/en/python-opencv-pillow-image-size/
        width = image.width
        height = image.height

        curved_image_px_list = []

        # FOR EVERY PIXELS...
        for h in range(height):
            for w in range(width):
                # GETTING PIXEL
                # https://www.geeksforgeeks.org/python-pil-getpixel-method/
                pixel = image.getpixel((w,h))

                # PIXEL MANIPULATION
                # IN THIS CASE pixel IS 0-255 FLOAT32 TYPE VALUE
                # 0 -> BLACK
                # 1 -> WHITE
                if 20 < pixel < 255:
                    pixel = int(pixel * 0.5)

                # FIRST, STORE THE PIXEL TO LIST
                curved_image_px_list.append(np.array(pixel, dtype='float32'))

        #print( curved_image_px_list )


        # PREPARING THE CONTAINER OF CURVED IMAGE
        curved_image = np.reshape(curved_image_px_list, (width, height))

        #print( curved_image )

        image = Image.fromarray(np.uint8(curved_image), 'L')
        #image.show()

        bool_image = image.convert(mode="1", dither=Image.NONE)
        #bool_image = image.convert(mode="1", dither=Image.NONE)
        #bool_image.show()


        # greyscale_img.save('my_resized.png')
        # greyscale_img.show()

        return bool_image




    # -------------------------------------------------------------------------------------------------------------





    def preparing_dataset_original_size(self):

        # SETTING PATH
        mnist_file = 'mnist-original.mat'
        mnist_path = 'mldata'
        mnist_url = 'https://github.com/amplab/datascience-sp14/raw/master/lab7/mldata/mnist-original.mat'

        # ファイルの存在確認
        # CHECKING FILE IS EXISTED OR NOT
        mnist_fullpath = os.path.join('.', mnist_path, mnist_file)


        # IF THE FILE IS NOT EXISTED,
        # DOWNLOAD FROM INTERNET
        # if not os.path.isfile(mnist_fullpath):
        #     # データダウンロード
        #     mldir = os.path.join('.', 'mldata')
        #     os.makedirs(mldir, exist_ok=True)
        #     print("donwload %s started." % mnist_file)
        #     urllib.request.urlretrieve(mnist_url, mnist_fullpath)
        #     print("donwload %s finished." % mnist_file)


        mnist_X, mnist_y = fetch_openml('mnist_784', version=1, data_home=".", return_X_y=True)

        print(mnist_X)
        print(mnist_y)
        print(type(mnist_X))        # <class 'numpy.ndarray'>
        print(type(mnist_y))        # <class 'numpy.ndarray'>
        print(mnist_X.shape)        # (70000, 784) --> 70000 DATASETS OF 784 = 28px * 28px
        print(mnist_y.shape)        # (70000,)     --> LABELS



        # WRITE PICKLE DATA (DATASETS)
        with open('mnist_28px.pickle', 'wb') as output:
            pickle.dump(mnist_X, output)

        # WRITE PICKLE DATA (LABELS)
        with open('mnist_28px_labels.pickle', 'wb') as output:
            pickle.dump(mnist_y, output)



    # BELOW FUNCTION IS USED ONCE WHEN ORIGINAL MNIST DATASET SHOULD BE MODIFIED
    def preparing_dataset(self):

        # SETTING PATH
        mnist_file = 'mnist-original.mat'
        mnist_path = 'mldata'
        mnist_url = 'https://github.com/amplab/datascience-sp14/raw/master/lab7/mldata/mnist-original.mat'

        # ファイルの存在確認
        # CHECKING FILE IS EXISTED OR NOT
        mnist_fullpath = os.path.join('.', mnist_path, mnist_file)


        # IF THE FILE IS NOT EXISTED,
        # DOWNLOAD FROM INTERNET
        # if not os.path.isfile(mnist_fullpath):
        #     # データダウンロード
        #     mldir = os.path.join('.', 'mldata')
        #     os.makedirs(mldir, exist_ok=True)
        #     print("donwload %s started." % mnist_file)
        #     urllib.request.urlretrieve(mnist_url, mnist_fullpath)
        #     print("donwload %s finished." % mnist_file)


        mnist_X, mnist_y = fetch_openml('mnist_784', version=1, data_home=".", return_X_y=True)

        print(mnist_X)
        print(mnist_y)
        print(type(mnist_X))        # <class 'numpy.ndarray'>
        print(type(mnist_y))        # <class 'numpy.ndarray'>
        print(mnist_X.shape)        # (70000, 784) --> 70000 DATASETS OF 784 = 28px * 28px
        print(mnist_y.shape)        # (70000,)     --> LABELS

        #data[0:256, 0:256] = [255, 0, 0]  # red patch in upper left

        # RESIZE DATASETS AND CONVERT TO BOOLEAN DATA
        modified_mnist = self.modify_datasets( mnist_X, 784, 100, False)


        # WRITE PICKLE DATA (DATASETS)
        with open('mnist_10px.pickle', 'wb') as output:
            pickle.dump(modified_mnist, output)

        # WRITE PICKLE DATA (LABELS)
        with open('mnist_10px_labels.pickle', 'wb') as output:
            pickle.dump(mnist_y, output)



    def proc_18_training(self, training_mode, epoch, nb_epoch, indexes, x_train, y_train_one, V, W, alpha, B, x_test, y_test, y_test_one, history3):
        # -----------------------------------------------------------------
        # < TRAINING >

        # LOOP UNTIL THE COUNT OF nb_epoch
        # (100 TIMES IN THIS CASE)
        if training_mode:
            while epoch < nb_epoch:

                # < PICKING UP THE TARGET WE WANT TO TRAIN >
                # (FROM THE BOOK)
                # IN THIS CASE, OUR DATASETS ARE 70000 COUNTS.
                # IN THE CASE LIKE THIS, WE USUALLY USE 'MINI-BATCH' METHOD.
                # MINI BATCH METHOD PICKS UP THE DATA 'RANDOMLY' FROM DATASETS.
                #
                #
                # < MINI BATCH METHOD >
                # https://machinelearningmastery.com/gentle-introduction-mini-batch-gradient-descent-configure-batch-size
                # : Mini-batch gradient descent is a variation of the gradient descent algorithm
                #   that splits the training dataset into small batches that are used to
                #   calculate model error and update model coefficients.
                #
                #
                # next_index() FUNCTION
                # IN Index CLASS (CUSTOM-MADE)
                # : WITH THE BELOW DESCRIPTIONS, CUSTOM-MADE CLASS 'Index' AND THE MEMBER
                #   FUNCTION 'next_index()' WILL RETURN 'RANDOMLY PICKED UP' 512 INDICES
                #   BETWEEN THE VALUE 0 ~ 70000.
                #   (e.g. [ 33412, 3, 324, ... 55546, 23134, 334]  :: 512 COUNTS)
                #
                #   THEN, IT WILL REMOVE THE INDICES WE PICKED UP (IN THE next_index()
                #   FUNCTION). AND LOOP UNTIL THE next_flag TURNS INTO 'False'.
                #
                index, next_flag = indexes.next_index()
                #print(f'** TRAINING ** -- index --  {index} -- next_flag -- {next_flag}')

                # PICK UP ONE ELEMENT
                x, yt = x_train[index], y_train_one[index]


                # print('x -- INPUT DATA -- 100 LENGTH -- 1D LIST')
                # print(x)
                # print('x.shape')
                # print(x.shape)
                # print('V')
                # print(V)
                # print('V.shape')
                # print(V.shape)


                # < FEED-FORWARD NEURAL NETWORK >

                # 1 -- CALCULATION BETWEEN
                # INPUT ~ HIDDEN LAYER
                a = x @ V                                       # (10.6.3)

                # 2 -- APPLYING 'ACTIVATION FUNCTION' < ReLU MODEL >
                # :: ReLU MODEL IS THE ACTIVATION FUNCTION OF THE 'HIDDEN LAYER'.
                b = self.ReLU(a)

                # 3 -- PREPARING FOR CALCULATION
                #
                # BETWEEN
                # (OUTPUT LAYER OF 'HIDDEN' LAYER)
                # AND
                # (INPUT LAYER OF 'OUTPUT' LAYER)
                b1 = np.insert(b, 0, 1, axis=1)                     # ダミー変数の追加

                # 4 -- CALCULATION BETWEEN
                # HIDDEN ~ OUTPUT LAYER
                u = b1 @ W                                          # (10.6.5)

                # 5 -- APPLYING 'ACTIVATION FUNCTION' < SOFTMAX MODEL >
                # :: SOFTMAX MODEL IS THE ACTIVATION FUNCTION OF THE 'OUTPUT LAYER'.
                yp = self.softmax(u)                                # (10.6.6)

                # CALCULATION THE DIFFERENECE BETWEEN
                # PREDICTION AND TRUE(TARGET) VALUES
                yd = yp - yt                                        # (10.6.7)

                bd = self.step(a) * (yd @ W[1:].T)                  # (10.6.8) ReLU化
                                                                    # STEP FUNCTION IS DIFFERENTIATED FUNCTION OF ReLU FUNCTION

                # CALCULATING GRADIENT DESCENT
                W = W - alpha * (b1.T @ yd) / B                     # (10.6.9)
                V = V - alpha * (x.T @ bd) / B                      # (10.6.10)


                # IF THERE IS 'NEXT' EPOCH
                # (SO LOOP THE TRAINING AGAIN)
                if next_flag:                                                           # 1epoch 終了後の処理

                    score, loss = self.evaluate2(x_test, y_test, y_test_one, V, W)

                    history3 = np.vstack((history3, np.array([epoch, loss, score])))

                    print("epoch = %d loss = %f score = %f" % (epoch, loss, score))

                    # RE-COUNT THE EPOCHS
                    epoch = epoch + 1






            # -----------------------------------------------------------------
            # < PRINTING RESULT OF TRAINING >


            # PRINTING OUT THE PROCESSES OF TRAINING
            print('初期状態: 損失関数:%f 精度:%f' % (history3[0, 1], history3[0, 2]))
            print('最終状態: 損失関数:%f 精度:%f' % (history3[-1, 1], history3[-1, 2]))


            # PRINTING THE RESULT OF LOSS CURVE
            # LOSSES WILL BE DECREASED IF THE TRAINING IS DONE PROPERLY
            plt.plot(history3[:, 0], history3[:, 1])
            plt.ylim(0, 2.5)
            plt.xticks(size=14)
            plt.yticks(size=14)
            plt.grid(lw=2)
            plt.show()


            # PRINTING THE RESULT OF LEARNING CURVE
            # THE VALUE WILL BE INCREASED IF THE TRAINING IS DONE PROPERLY
            plt.plot(history3[:, 0], history3[:, 2])
            plt.ylim(0, 1)
            plt.xticks(size=14)
            plt.yticks(size=14)
            plt.grid(lw=2)
            plt.show()




    def proc_19_test_28px(self, y_test, x_test, V, W):
        # -----------------------------------------------------------------
        # < PRINTING RESULT OF TESTING >

        # TEST FOR 20 CASES
        N = 20

        # SETTING UP THE SEED VALUE FOR RANDOM FUNCTION
        # np.random.seed(123)
        #np.random.seed(22)

        # PICKING UP THE INDICES RANDOMLY
        indexes = np.random.choice(y_test.shape[0], N, replace=False)

        # PICKING UP THE ONE DATA FOR TESTING
        x_selected = x_test[indexes]
        #print(x_selected)

        y_selected = y_test[indexes]

        # CALCULATING PREDICTION
        b1_test = np.insert(self.ReLU(x_selected @ V), 0, 1, axis=1)
        yp_test_one = self.softmax(b1_test @ W)
        yp_test = np.argmax(yp_test_one, axis=1)

        # DISPLAYING GRAPH
        plt.figure(figsize=(10, 3))
        for i in range(N):
            ax = plt.subplot(2, N / 2, i + 1)
            plt.imshow(x_selected[i, 1:].reshape(28, 28), cmap='gray_r')
            ax.set_title('%d:%d' % (y_selected[i], yp_test[i]), fontsize=14)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        plt.show()




    def proc_19_test_10px(self, y_test, x_test, V, W):
        # -----------------------------------------------------------------
        # < PRINTING RESULT OF TESTING >

        # TEST FOR 20 CASES
        N = 20

        # SETTING UP THE SEED VALUE FOR RANDOM FUNCTION
        # np.random.seed(123)
        #np.random.seed(22)

        # PICKING UP THE INDICES RANDOMLY
        indexes = np.random.choice(y_test.shape[0], N, replace=False)

        # PICKING UP THE ONE DATA FOR TESTING
        x_selected = x_test[indexes]
        #print(x_selected)

        y_selected = y_test[indexes]

        # CALCULATING PREDICTION
        b1_test = np.insert(self.ReLU(x_selected @ V), 0, 1, axis=1)
        yp_test_one = self.softmax(b1_test @ W)
        yp_test = np.argmax(yp_test_one, axis=1)

        # DISPLAYING GRAPH
        plt.figure(figsize=(10, 3))
        for i in range(N):
            ax = plt.subplot(2, N / 2, i + 1)
            plt.imshow(x_selected[i, 1:].reshape(10, 10), cmap='gray_r')
            ax.set_title('%d:%d' % (y_selected[i], yp_test[i]), fontsize=14)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        plt.show()







    def preparing_geometry_data(self):

        # SETTING PATH
        image_list_circle = []  # DATA
        label_list_circle = []  # LABEL
        image_list_square = []
        label_list_square = []
        image_list_triangle = []
        label_list_triangle = []

        #
        # https://stackoverflow.com/questions/26392336/importing-images-from-a-directory-python-to-list-or-dictionary

        # FOR CIRCLES
        for filename in glob.glob('datasets/circles/*.png'):
            # CONVERTING IMAGE TO GRAYSCALE IMAGE
            # https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
            im = Image.open(filename).convert('L')
            # CONVERT TO ARRAY
            pixel = np.asarray(im)
             # SAVE
            image_list_circle.append(pixel)
            label_list_circle.append('circle')

        # FOR SQUARES
        for filename in glob.glob('datasets/squares/*.png'):
            im = Image.open(filename).convert('L')
            pixel = np.asarray(im)
            image_list_square.append(pixel)
            label_list_square.append('square')

        # FOR TRIANGLES
        for filename in glob.glob('datasets/triangles/*.png'):
            im = Image.open(filename).convert('L')
            pixel = np.asarray(im)
            image_list_triangle.append(pixel)
            label_list_triangle.append('triangle')


        #image_list_circle[0].show()


        print(image_list_circle)
        print(image_list_square)
        print(image_list_triangle)


        # CONCATENATE TO ONE LIST
        # https://www.w3schools.com/python/gloss_python_join_lists.asp
        image_datasets = image_list_circle + image_list_square + image_list_triangle
        label_list = label_list_circle + label_list_square + label_list_triangle

        print(image_datasets)
        print(label_list)

        print(image_datasets)
        print(label_list)

        # MAKING NUMPY ARRAY FROM LIST
        # https://note.nkmk.me/en/python-numpy-list/
        image_datasets = np.array(image_datasets, dtype='float32')

        # RESHAPING THE NUMPY ARRAY
        # https://note.nkmk.me/en/python-numpy-reshape-usage/
        image_datasets = image_datasets.reshape([300, 784])


        # ----------------------------------------------------------------------
        # MODIFYING IMAGES


        # RESIZE DATASETS AND CONVERT TO BOOLEAN DATA
        modified_geometry = self.modify_datasets( image_datasets, 784, 100, False)


        # WRITE PICKLE DATA (DATASETS)
        with open('geometry_10px.pickle', 'wb') as output:
            pickle.dump(modified_geometry, output)

        # WRITE PICKLE DATA (LABELS)
        with open('geometry_10px_labels.pickle', 'wb') as output:
            pickle.dump(label_list, output)




# -------------------------------------------------------------------------------------------------------------





class Indexes(object):

    # CONSTRUCTOR
    def __init__(self, total, size):
        # TOTAL SIZE OF INDICES
        self.total = total
        # SIZE OF BATCH
        self.size = size
        # INITIALIZATION WITH ZERO
        self.indexes = np.zeros(0)


    # THE FUNCTION FOR GETTING INDEX
    def next_index(self):
        # INITIALIZATION THE NEXT FLAG TO 'FALSE'
        next_flag = False

        # bacthサイズより作業用Indexesが小さい場合はindexes再生成

        # THEN, BELOW IS THE CASE THAT THERE IS 'NEXT' PICKUP.
        #
        # CONDITION :: DETERMINE THAT THERE IS NEXT CALCULATION OR NOT
        #
        # IF
        if len(self.indexes) < self.size:
            # PICKING UP RANDOMLY
            #
            # numpy.random.choice(a, size=None, replace=True, p=None)
            # https://docs.scipy.org/doc//numpy-1.10.4/reference/generated/numpy.random.choice.html
            # : Generates a random sample from a given 1-D array.
            #
            # Parameters:
            # a : 1-D array-like or int
            #     If an ndarray, a random sample is generated from its elements.
            #     If an int, the random sample is generated as if a was np.arange(n)
            #
            # size : int or tuple of ints, optional
            #        Output shape. If the given shape is, e.g.,
            #        (m, n, k), then m * n * k samples are drawn.
            #        Default is None, in which case a single value is returned.
            #
            # replace : boolean, optional
            #           Whether the sample is with or without replacement
            #
            # p : 1-D array-like, optional
            #     The 'probabilities' associated with each entry in a.
            #     If not given the sample assumes a uniform distribution
            #     over all entries in a.
            #
            #     EXAMPLE >
            #              np.random.choice(5, 3, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
            #                    ABOVE WILL PICKUP 3, IN THE 0 ~ 4 (5 ELEMENTS),
            #                    WHERE THE PROBABILITIES IS LIST 'p' (THE WEIGHTS AMONG THE ELEMENTS)
            #                    p=[0.1, 0, 0.3, 0.6, 0]
            #                        0   1   2    3   4
            #              OUTPUT:
            #              array([2, 3, 0])     --> SO WE ARE GETTING THE RESULT WHICH INCLUDES 3,2 AND 0 !
            #
            #
            # Returns:
            # samples : 1-D ndarray, shape (size,)
            #           The generated random samples
            #
            # Raises: ValueError
            #         If a is an int and less than zero, if a or p are
            #         not 1-dimensional, if a is an array-like of size 0,
            #         if p is not a vector of probabilities, if a and p have
            #         different lengths, or if replace=False and the sample
            #         size is greater than the population size
            #
            self.indexes = np.random.choice(self.total, self.total, replace=False)

            # CHANGE THE NEXT-FLAG TO 'TRUE' HERE
            next_flag = True

        # 'PICKING UP' THE EXACT SIZE OF INDICES FROM ENTIRE LIST
        index = self.indexes[:self.size]

        # UPDATING THE INDEX LIST WITH 'CUTTING OFF ALREADY PICKED UP'
        # STORING THE LIST 'EXACTLY SAME COUNTS AFTER' THE SIZE OF WE PICKED UP ABOVE.
        self.indexes = self.indexes[self.size:]

        return index, next_flag



