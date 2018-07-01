from GUI.capureImageView import CaptureImageView
from GUI.Variables.variables import ICON_PATH
from tkinter import TclError

if __name__ == '__main__':
    main_view = CaptureImageView()
    try:
        main_view.iconbitmap(ICON_PATH)
    except TclError:
        pass
    main_view.mainloop()
    exit(0)
