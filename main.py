from GUI.capureImageView import CaptureImageView
from GUI.Variables.variables import ICON_PATH

if __name__ == '__main__':
    main_view = CaptureImageView()
    main_view.iconbitmap(ICON_PATH)
    main_view.mainloop()
    exit(0)
