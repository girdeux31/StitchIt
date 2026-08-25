import numpy as np

from image import Image
from PIL import Image as PILImage

from backstitch_detector import BackstitchDetector
from confetti_cleaner import ConfettiCleaner


BACKGROUND_INDEX = 99  # must be between n_colors and 255 inclusive since pattern is uint8
BACKGROUND_CODE = 'B5200'
IGNORE_BACKGROUND = True  # bg is set white with no symbol and not shown in legend
BACKSTITCH = True

class Pattern:

    def __init__(self, show_colors: bool=True):
        """Init object"""
        self.show_colors = show_colors
        self.array = None
        self.width = None
        self.height = None
        self.bg_idx = None
        self.palette = None
        self.backstitches = []

    def _extract_array_from_image(self, image: PILImage) -> np.ndarray[int]:
        """Convert image into a np array"""
        return np.array(image)

    def _change_background_index(self) -> None:
        """Set color index of background to special index"""
        self.bg_idx = self._get_background_idx()
        if IGNORE_BACKGROUND is True:
            self.array[self.array==self.bg_idx] = BACKGROUND_INDEX  # change idx in pattern
            self.palette.remove_color_by_idx(self.bg_idx)  # remove old bg color
            self.palette.add_color_by_code(BACKGROUND_INDEX, BACKGROUND_CODE, show_in_legend=False)  # add bg color
            self.bg_idx = BACKGROUND_INDEX  # change bg idx

    def _get_background_idx(self) -> int:
        """Get index representing background (mode of outer rim)"""
        rim = np.concatenate(
            [
                self.array[0, :],  # top
                self.array[-1, :],  # bottom
                self.array[1:-1, 0],  # left
                self.array[1:-1, -1],  # right
            ]
        )
        values, counts = np.unique(rim, return_counts=True)
        return values[np.argmax(counts)]

    def _set_backstitches(self) -> None:
        """Detect backstitches"""
        backstitch_detector = BackstitchDetector(self)
        self.backstitches = backstitch_detector.detect()
    
    def process_from_image(self, image: Image) -> None:
        self.palette = image.palette
        self.array = self._extract_array_from_image(image.pil_image)
        self.base_rgb_array = self._extract_array_from_image(image.base_rgb_image)
        self.width = self.array.shape[1]
        self.height = self.array.shape[0]

        cleaner = ConfettiCleaner()
        cleaner.clean_confetti(self)

        self._change_background_index()
        if BACKSTITCH:
            self._set_backstitches()
