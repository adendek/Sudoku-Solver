import tkinter
import GUI.captureVideo
import PIL.ImageTk
import PIL.Image
import GUI.Framework.main_template
import GUI.Framework.widgets as widgets
import GUI.variables.variables as var
from tkinter import TclError


class CaptureImageView(GUI.Framework.main_template.MainTemplate):
    def __init__(self):
        super().__init__("Exit", self._exit, "Take Picture", self._take_picture)
        self.video = GUI.captureVideo.CaptureVideo(self)
        self.video_delay = 20  # ms - how often refreshes picture from the camera

        self.content_frame = widgets.Frame(self, row=2, padx=var.BORDER, pady=var.BORDER)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.content_frame, width=self.video.width, height=self.video.height)
        self.canvas.pack()

        self._update()

        self._set_to_screen_center()

        self.mainloop()

    def _take_picture(self):
        print("taking picture")
        pass

    def _exit(self):
        self.destroy()
        exit(0)

    def _on_destroy(self):
        self.destroy()
        exit(0)

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


if __name__ == '__main__':
    CaptureImageView()
