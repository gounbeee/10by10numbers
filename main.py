
#from threading import Thread
# https://qiita.com/__init__/items/74b36eba31ccbc0364ed



import TenByTenNumbers_main




# https://stackoverflow.com/questions/25477470/how-can-i-restrict-the-scope-of-a-multiprocessing-process
#
#  Because of the nature of os.fork(), any variables in the global
#  namespace of your __main__ module will be inherited by the child
#  processes (assuming you're on a Posix platform), so you'll see
#  the memory usage in the children reflect that as soon as they're
#  created. I'm not sure if all that memory is really being allocated
#  though, as far as I know that memory is shared until you actually
#  try to change it in the child, at which point a new copy is made.
#  Windows, on the other hand, doesn't use os.fork() - it re-imports
#  the main module in each child, and pickles any local variables you
#  want sent to the children. So, using Windows you can actually avoid
#  the large global ending up copied in the child by only defining it
#  inside an if __name__ == "__main__": guard, because everything
#  inside that guard will only run in the parent process:


# https://stackoverflow.com/questions/29203108/what-happens-to-imports-when-a-new-process-is-spawned
#
# On Linux, fork will be used to spawn the child, so anything in the global scope of the parent will
# also be available in the child, with copy-on-write semantics.
#
# On Windows, anything you import at the module-level in the __main__ module of the parent process
# will get re-imported in the child.
#
# This means that if you have a parent module (let's call it someModule) like this:






# TODO :: MAKE THIS PROGRAM TO NETWORK !
# https://stackoverflow.com/questions/9961752/basic-networking-with-pygame


# https://stackoverflow.com/questions/61277742/how-to-guard-python-multiprocessing-on-windows-from-unwanted-recursion


def main():

    # TODO :: MULTI PROCESS MADE FREEZE WHEN SEVERAL HIGH-SPEED GAME LOOPS !!!!!
    #         5, 6 COUNTS ? THEN FREEZED

    # PIPE TO COMMUNICATE EACH PROCESSES !
    
    #p_send_main_to_sub , p_receive_main_to_sub = Pipe()
    #p_send_sub_to_main, p_receive_sub_to_main = Pipe()

    #process_sub = Process(target=TenByTenNumbers_sub.TenByTenNumbers_sub, args=(p_receive_main_to_sub, p_send_sub_to_main, ))
    #process_sub.start()


    #process_main = Process(target=TenByTenNumbers_main.TenByTenNumbers_main, args=(p_send_main_to_sub, p_receive_sub_to_main, ))
    #process_main.start()



    #process_sub.join()
    #process_main.join()
    pass

if __name__ == '__main__':
    #main()
    prg = TenByTenNumbers_main.TenByTenNumbers_main()
