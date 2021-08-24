import PySimpleGUI as sg
import glob
import os
from FileParser import FileParser

class Window(object):

    def __init__(self):
        pass

    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    layout = [
        [
            sg.Column(file_list_column),
        ]
    ]

    def event_loop_listen(self):
        window = sg.Window("Image Viewer", self.layout)

        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            if event == "-FOLDER-":
                folder = values["-FOLDER-"]
                try:
                    # Get list of files in folder
                    file_list = os.listdir(folder)
                    path = glob.glob(folder + '/**/*.*', recursive=True)
                    parser = FileParser()
                    for file in path:
                        if os.path.isfile(file) and parser.isImage(file):
                            parser.save_image(file)
                except ValueError:
                    print(ValueError)
                    file_list = []

                fnames = [
                    f
                    for f in file_list
                    if os.path.isfile(os.path.join(folder, f))
                       and f.lower().endswith((".png", ".gif"))
                ]

                window["-FILE LIST-"].update(fnames)

            elif event == "-FILE LIST-":  # A file was chosen from the listbox
                try:
                    filename = os.path.join(
                        values["-FOLDER-"], values["-FILE LIST-"][0]
                    )
                    window["-TOUT-"].update(filename)
                    window["-IMAGE-"].update(filename=filename)

                except:
                    pass
                window.close()
