
from multiprocessing import Process



if __name__ == '__main__':
    process_main = Process(target=TenByTenNumbers_main.TenByTenNumbers_main().run)

    process_main.start()

    process_main.join()

