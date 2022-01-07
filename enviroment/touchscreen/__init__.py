class TouchRecoder:
    def __init__(self):
        self.Touch = 0
        self.TouchGestureId = 0
        self.TouchCount = 0

        self.TouchEvenId = [0, 1, 2, 3, 4]
        self.X = [0, 1, 2, 3, 4]
        self.Y = [0, 1, 2, 3, 4]
        self.P = [0, 1, 2, 3, 4]


class Clicked:  # call the function when the object is clicked.
    def __init__(self, area=(0, 0, 0, 0), func=lambda: None, *arg, **kwargs):
        self.area = area
        self._temp_location = (0, 0)
        self.func = func
        self.active = False
        self.args = arg
        self.kwargs = kwargs

    @property
    def temp_location(self):
        return self._temp_location

    @temp_location.setter
    def temp_location(self, value):
        self._temp_location = value
        self.active = True


class Slide:
    def __init__(self):
        self.area = (0, 0, 0, 0)  # (x1, x2, y1, y2)
        self._temp_location = (0, 0)
        self.active = False
        self.func = None

    @property
    def temp_location(self):
        return self._temp_location

    @temp_location.setter
    def temp_location(self, value):
        self._temp_location = value
        self.active = True


class SlideX(Slide):
    pass


class SlideY(Slide):
    pass


class SlideB(Slide):
    def __init__(self):
        super().__init__()
        self._active = False
        self.showed = False

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if not value:
            self.showed = False
        self._active = value
