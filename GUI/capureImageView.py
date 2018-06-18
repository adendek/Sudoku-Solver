import GUI.Framework.mainTemplate
import GUI.Framework.widgets as widgets
import GUI.variables.variables as var
from tkinter import TclError
from GUI import askIfCorrectView
from ImageProcessing.processImage import ProcessImage
import tkinter
import PIL.ImageTk
import PIL.Image
import cv2


class CaptureImageView(GUI.Framework.mainTemplate.MainTemplate):
    def __init__(self):
        super().__init__("Exit", self._on_destroy, "Take Picture", self._take_picture)
        self.video = CaptureVideo()
        self.video_delay = 20  # ms - how often refreshes picture from the camera

        self.content_frame = widgets.Frame(self, row=2, padx=var.BORDER, pady=var.BORDER)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.content_frame, width=self.video.width, height=self.video.height)
        self.canvas.pack()
        self.set_info_label("Show the picture of sudoku puzzle to the camera and press enter or click 'Take picture'.\n"
                            "Watch out that there will be a good light and try to have steady hand :)")

        self.bind("<Return>", self._pressed_enter)  # take the picture when user press enter

        self._update()

        self._set_to_screen_center()

        self.mainloop()

    def _pressed_enter(self, event):
        self._take_picture()

    def renew_video(self):
        self.video = CaptureVideo()

    def _take_picture(self):
        image = self.video.get_image()
        field = ProcessImage(image).get_field_matrix()
        self.withdraw()
        self.video.video.release()  # stop filming
        askIfCorrectView.AskIfCorrectView(field, self)

    def _update(self):
        # Get a frame from the video source
        ret, frame = self.video.get_frame()
        if ret:
            try:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            except TclError:
                self.photo = None
        self.after(self.video_delay, self._update)


class CaptureVideo:  # set video for tkinter
    def __init__(self):
        self.video_source = 0  # 0 is for web cam
        self.video = cv2.VideoCapture(self.video_source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_image(self):
        if self.video.isOpened():
            success, image = self.video.read()
            if success:
                return image
        return None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return None, None
