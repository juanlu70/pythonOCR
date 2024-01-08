#!/usr/bin/env python3
import os
import sys
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import text_processing
import ia_process


tp = text_processing.TextProcessing()
ia = ia_process.IAProcess()


class MyHandler(FileSystemEventHandler):
    def __init__(self):

        return

    # -- create an event handler for file creation and execute process for every event --
    def on_created(self, event):
        time.sleep(1)
        print("on_created", event.src_path)
        # -- temporary download file, don't process it --
        if "crdownload" in event.src_path:
            time.sleep(2)
            return

        # -- process downloaded image --
        if os.path.isfile(event.src_path):
            text = tp.tesseract_ocr(event.src_path)
            print("--------- QUERY ----------------")
            print(tp.main(text))
            print("--------------------------------")

        return

    # -- process arguments --
    def process_arguments(self) -> str:
        """
        Function to process arguments from command-line

        :param self:
        :return: dict
        """
        proc_args = {}
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--image", type=str, default='',
                            help="Full path of image file, or path for image creation events.")
        parser.add_argument("-s", "--solution", type=str, default='', help="Full path of solution file")
        parser.add_argument("-v", "--verbose", action="count", default=0, help="Be verbose")
        args = parser.parse_args()

        tp.solution_file = args.solution
        tp.verbose = args.verbose

        return args.image


if __name__ == "__main__":
    verbose = 0
    event_handler = MyHandler()

    # -- manage arguments --
    path_image = event_handler.process_arguments()
    # if len(sys.argv) > 1:
    #     name = sys.argv[1]
    # else:
    #     print("A filename or watchdog directory is needed!")
    #     print("USE: "+sys.argv[0]+" [filename|directory]")
    #     sys.exit()

    # -- add verbose mode --
    # if len(sys.argv) > 2:
    #     if sys.argv[2] == "-v":
    #         tp.verbose = 1
    #     else:
    #         tp.solution_file = sys.argv[2]

    # -- load solutions file --
    if tp.solution_file != "":
        fp = open(tp.solution_file, "r")
        tp.solution_text = fp.read()
        fp.close()
        tp.process_solutions()

    # -- get question text and get answer or begin event driven loop to get captured images --
    if os.path.isfile(path_image):
        query = tp.tesseract_ocr(path_image)
        text = tp.main(query)
    else:
        print("Program started, waiting images to be created...")
        observer = Observer()
        observer.schedule(event_handler, path=path_image, recursive=True)
        observer.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

    # -- this is for isolated files as input --
    print("QUERY:")
    print(text)
    print("-------------------------------------")
