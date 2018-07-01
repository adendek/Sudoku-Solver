from Common.Errors import SudokuFieldSizeError, InappropriateArgsError
from ImageProcessing.processSudokuField import ProcessSudokuField
from ImageProcessing.extractSudokuField import ExtractField
from Common.validationFunctions import Validator
from tkinter.filedialog import askopenfilename
import GUI.Framework.widgets as widgets
import GUI.Variables.variables as var
import GUI.Framework.mainTemplate
from GUI import askIfCorrectView
from tkinter import TclError
import PIL.ImageTk
import numpy as np
import PIL.Image
import tkinter
import imghdr
import cv2
import os


class CaptureImageView(GUI.Framework.mainTemplate.MainTemplate):
    def __init__(self):
        super().__init__("Exit", self._on_destroy, "Take Picture", self._take_picture)

        self.video = CaptureVideo()
        self.video_delay = 20  # ms - how often refreshes picture from the camera

        self.content_frame = widgets.Frame(self, row=2, padx=var.BORDER, pady=var.BORDER)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.content_frame, width=self.video.width, height=self.video.height)
        self.canvas.grid(row=2)
        self.label_text = "Show the picture of sudoku puzzle to the camera and press enter or click 'Take picture'.\n "\
                          "The picture should not be curved and the Sudoku field should be clearly visible."
        self.set_info_label(self.label_text)
        self.load_from_source_frame, self.vid_but, self.img_but = self._configure_load_from_source_frame()

        self.bind("<Return>", self._pressed_enter)  # take the picture when user press enter

        self.load_from_video = True

        self._update_video_frame()
        self._set_to_screen_center()

    def _configure_load_from_source_frame(self):
        frame = widgets.Frame(self.content_frame, row=1, sticky="ew", pady=var.BORDER, padx=2)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        vid_frame = widgets.Frame(frame, row=0, column=0, sticky="w")
        pic_frame = widgets.Frame(frame, row=0, column=1, sticky="e")
        vid = widgets.Button(vid_frame, "Take picture from the video", self.load_video)
        vid.config(width=22, state="disabled")
        pic = widgets.Button(pic_frame, "Load picture from source", self._load_picture)
        pic.config(width=22)
        return frame, vid, pic

    def _load_picture(self):
        filename = askopenfilename(parent=self)  # show an "Open" dialog box and return the path to the selected file
        if os.path.exists(filename) and imghdr.what(filename) is not None:  # imghdr returns none if file isn't an image
            self.vid_but.config(state="normal")
            self.video.video.release()
            self.img = self._change_img_size_if_to_big(PIL.Image.open(os.path.normpath(filename)))
            self.photo_img = PIL.ImageTk.PhotoImage(self.img)
            self._prepare_canvas(self.img.width, self.img.height)
            self.canvas.create_image((0, 0), image=self.photo_img, anchor='nw')
            self.load_from_video = False
        else:
            err_text = "Path to image is not valid or the file is not an image!"
            self.display_message(err_text, self.label_text, "red", 2)

    def _change_img_size_if_to_big(self, img):
        if not Validator.is_type(img, PIL.Image.Image):
            raise InappropriateArgsError("changing image size! arg: " + str(img))
        ratio = 2
        width, height = img.width, img.height
        max_width, max_height = self.winfo_screenwidth() / ratio, self.winfo_screenheight() / ratio
        if width >= max_width or height >= max_height:
            img.thumbnail((max_width, max_height), PIL.Image.ANTIALIAS)
        return img

    def _prepare_canvas(self, width, height):
        if Validator.is_positive_number([width, height]):
            self.canvas.delete("all")
            self.canvas.config(width=width, height=height)
            self._set_to_screen_center()
            return self.canvas
        raise InappropriateArgsError("preparing canvas")

    def load_video(self):
        self.vid_but.config(state="disabled")
        self.video = CaptureVideo()
        self._prepare_canvas(self.video.width, self.video.height)
        self.load_from_video = True
        return self.video

    def _get_image(self):
        if self.load_from_video:
            return self.video.get_image()
        else:
            return np.array(self.img)

    def _pressed_enter(self, event):
        self._take_picture()

    def _take_picture(self):
        msg = self.display_message("Processing image!", self.label_text, "green")
        image = self._get_image()
        try:
            field = ExtractField(image)
        except cv2.error:
            return self._handle_image_errors(msg)
        try:
            self.process = ProcessSudokuField(field.extract_sudoku_field())
            field = self.process.process_field_and_get_number_matrix()
        except (SudokuFieldSizeError, InappropriateArgsError) as e:
            return self._handle_errors_at_recognition(msg)
        self.withdraw()
        self.video.video.release()  # stop filming
        view = askIfCorrectView.AskIfCorrectView(field, self)
        try:
            view.iconbitmap(var.ICON_PATH)
        except tkinter.TclError:
            pass

    def _handle_image_errors(self, after_id):
        if not Validator.is_type(after_id, str):
            raise InappropriateArgsError("handling image_error")
        self.after_cancel(after_id)
        text = "There appears to be some problems with Sudoku field detection...\n" \
               "Make sure, that the lines, which outlines the field, are thick enough!"
        return self.display_message(text, self.label_text, "red", 6)

    def _handle_errors_at_recognition(self, after_id):
        if not Validator.is_type(after_id, str):
            raise InappropriateArgsError("handling error at recognition of the image")
        self.after_cancel(after_id)
        text = "Could not detect Sudoku field correctly! Put the picture closer to the camera\n" \
               "and make sure that the Sudoku field is curved as little as possible!"
        return self.display_message(text, self.label_text, "red", 6)

    def _update_video_frame(self):
        # Get a frame from the video source
        ret, frame = self.video.get_frame()
        if ret:
            try:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            except TclError:
                self.photo = None
        self.after(self.video_delay, self._update_video_frame)


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
