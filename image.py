import numpy as np

from pathlib import Path
from PIL import Image as PILImage

from palette import Palette
from color_tools import ColorTools


# increase if colors in pattern are too similar
METHOD_TO_COLOR_THRESHOLD = {
    'euclidean': 30,
    'compuphase': 30,
    'de76': 10,
    'de00': 10,
}
BACKGROUND_INDEX = 255  # must be between n_colors and 255 inclusive since pattern is uint8
background_code = 'B5200'
ignore_background = True  # bg is set white with no symbol and not shown in legend

class Image:

    def __init__(self, show_colors: bool=True, show_symbols: bool=True) -> None:
        """Init object"""
        self.show_colors = show_colors
        self.show_symbols = show_symbols
        self.method = None
        self.palette = None
        self.pil_image = None
        self.base_rgb_image = None

    @property
    def width(self) -> int:
        """Return image width"""
        return self.pil_image.size[0]
    
    @property
    def height(self) -> int:
        """Return image height"""
        return self.pil_image.size[1]

    def _import_image(self, img_file: Path) -> None:
        """Read image as (cols,rows,rgb)"""
        if not img_file.exists():
            raise FileNotFoundError(f'File \'{img_file}\' not found')
        self.pil_image = PILImage.open(img_file).convert('RGB')  # make sure to read it in RGB mode

    def _resize(self, stitches_per_row: int) -> None:
        """Resize image so each pixel is a stitch (equivalent to pixelate), 
        output image is (stitches_cols, stitches_rows, rgb)"""
        pixel_size = self.width / stitches_per_row
        stitches_per_col = round(self.height / pixel_size)
        self.pil_image = self.pil_image.resize(
            (stitches_per_row, stitches_per_col),
            resample=PILImage.Resampling.NEAREST,  # or LANCZOS
        )
        self.base_rgb_image = self.pil_image

    def _quantize(self) -> None:
        """Assign a color index to each pixel, only n colors are used, 
        output image is (stitches_cols, stitches_rows) where each element is a color index"""
        palette_1d = [coord for color in self.palette for coord in color.dmc_rgb]
        palette_img = PILImage.new("P", (1, 1))  # create an image 1x1 just to put the palette on
        palette_img.putpalette(palette_1d)
        self.pil_image = self.pil_image.quantize(
            palette=palette_img,
            dither=PILImage.Dither.NONE,
        )

    def _set_dmc_palette(self, n_colors: int, method: str):
        """Get a list of dmc colors most used in image"""
        self.palette = Palette(method)
        predominant_rgbs = self._get_predominant_colors(n_colors, method)
        for c_idx, rgb in enumerate(predominant_rgbs):
            self.palette.add_color_by_rgb(c_idx, rgb)
            if self.show_symbols:
                self.palette.add_symbols()

    def _get_predominant_colors(self, n_colors: int, method: str) -> list[tuple[int]]:
        """Get a list of colors most used in image"""
        count_rgbs = self.pil_image.getcolors(maxcolors=self.width*self.height)
        count_rgbs.sort(reverse=True) # sort by count
        img_rgbs = [c_rgb[1] for c_rgb in count_rgbs]
        output_rgbs = []
        for base_rgb in img_rgbs:
            if all(
                ColorTools.compute_color_distance(base_rgb, rgb, method) >= METHOD_TO_COLOR_THRESHOLD[method]
                for rgb in output_rgbs
            ):
                output_rgbs.append(base_rgb)
        return output_rgbs[:n_colors]  # return only the n most predominant colors

    def process(self, img_file: Path, n_colors: int, stitches_per_row: int, method: str) -> tuple[Palette, np.ndarray[int]]:
        """Process image:
        1. Resize image to be stitches_per_row x stitches_per_column, this shape is not changed anymore
        2. Compute the dmc palette based on the predominant image colors
        3. Quantize the image with n dmc colors
        4. Convert the image to a np array"""
        self._import_image(img_file)  # pil_image is always width,height / cols,rows / x,y
        self._resize(stitches_per_row)
        n_colors += 1 if ignore_background is True else 0  # add 1 color because bg color wont be shown in legend
        self._set_dmc_palette(n_colors, method)
        self._quantize()
        if self.show_colors is False:
            self.palette.replace_all_colors_by_code(background_code)
