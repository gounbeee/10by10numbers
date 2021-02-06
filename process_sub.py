

if __name__ == '__main__':
    # process_main = Process(target=TenByTenNumbers_main.TenByTenNumbers_main().run)
    process_sub = Process(target=TenByTenNumbers_sub.TenByTenNumbers_sub().run)

    # process_main.start()
    process_sub.start()

    # process_main.join()
    process_sub.join()