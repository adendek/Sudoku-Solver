import cv2


class CaptureVideo:
    def __init__(self, parent_window):
        self.video_source = 0  # 0 is for web cam
        self.parent_window = parent_window
        self.video = cv2.VideoCapture(self.video_source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

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
