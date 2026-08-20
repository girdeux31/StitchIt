from math import dist
from pathlib import Path

import numpy as np
from PIL import Image as PILImage

from dmc import DMC

RESIZE_WIDTH  = 1000
MASK_SIZE = 3
SIMILAR_COLOR_THRESHOLD = 30
DEBUG = False

if DEBUG:
    import matplotlib.pyplot as plt


class Image:

    def __init__(self, img_file: Path) -> None:
        """Init object"""
        self.img_file = img_file
        self.dmc_palette = None
        self.dmc_pattern = None
        self.pil_image = self._import_image(img_file)  # pil_image is always width,height / cols,rows / x,y

    @property
    def width(self) -> int:
        """Return image width"""
        return self.pil_image.size[0]
    
    @property
    def height(self) -> int:
        """Return image height"""
        return self.pil_image.size[1]

    @staticmethod
    def _import_image(img_file: Path) -> PILImage:
        """Read image as (cols,rows,rgb)"""
        if not img_file.exists():
            raise FileNotFoundError(f'File \'{img_file}\' not found')
        return PILImage.open(img_file).convert('RGB')  # make sure to read it in RGB mode

    def _resize(self, stitches_per_row: int) -> None:
        """Resize image so each pixel is a stitch (equivalent to pixelate), 
        output image is (stitches_cols, stitches_rows, rgb)"""
        pixel_size = self.width // stitches_per_row
        stitches_per_col = self.height // pixel_size
        self.pil_image = self.pil_image.resize(
            (stitches_per_row, stitches_per_col),
            resample=PILImage.Resampling.NEAREST,  # or LANCZOS
        )

    def _quantize(self, dmc_palette_2d: list[tuple[int]]) -> None:
        """Assign a color index to each pixel, only n colors are used, 
        output image is (stitches_cols, stitches_rows) where each element is a color index"""
        dmc_palette_1d = [value for rgb in dmc_palette_2d for value in rgb]
        dmc_palette_img = PILImage.new("P", (1, 1))  # create an image 1x1 just to put the palette on
        dmc_palette_img.putpalette(dmc_palette_1d)
        self.pil_image = self.pil_image.quantize(
            palette=dmc_palette_img,
            dither=PILImage.Dither.NONE,
        )

    def _get_dmc_palette(self, n_colors: int, method: str) -> list[tuple[int]]:
        """Get a list of dmc colors most used in image"""
        dmc = DMC()
        dmc_palette = []
        predominant_rgbs = self._get_predominant_colors(n_colors)
        for rgb in predominant_rgbs:
            dmc_rgb = dmc.get_most_similar_rgb_by_rgb(rgb, method)
            dmc_palette.append(dmc_rgb)
        return dmc_palette

    def _get_predominant_colors(self, n_colors: int) -> list[tuple[int]]:
        """Get a list of colors most used in image"""
        count_rgbs = self.pil_image.getcolors(maxcolors=self.width*self.height)
        # TODO change RGB to LAB if method is 76 or 00
        count_rgbs.sort(reverse=True) # sort by count
        img_rbgs = [c_rgb[1] for c_rgb in count_rgbs]
        output_rgbs = []
        for base_rgb in img_rbgs:
            if all(dist(base_rgb, rgb) >= SIMILAR_COLOR_THRESHOLD for rgb in output_rgbs):
                output_rgbs.append(base_rgb)
        return output_rgbs[:n_colors]  # return only the n most predominant colors

    def _get_dmc_pattern(self) -> np.ndarray[int]:
        """Convert the image into a np array"""
        return np.array(self.pil_image)

    def _clean(self) -> None:
        """Remove isolated pixels and replace by majority neighborhood color,
        output image is (stitches_cols, stitches_rows) where each element is a color index"""
        pattern = self._get_dmc_pattern()

        for x in range(0, self.width):
            for y in range(0, self.height):
                neighbors = self._get_neighbors_in_coords((y, x), pattern)
                if pattern[y, x] not in neighbors:
                    mode = int(max(neighbors, key=neighbors.count))
                    self.pil_image.putpixel((x,y), mode)

    @staticmethod
    def _get_neighbors_in_coords(coords: tuple[int], array: np.ndarray[int]) -> list[int]:
        neighbors = []
        rows = array.shape[0]
        cols = array.shape[1]
        mask_half_width = int(MASK_SIZE/2)
        for i in range(max(0, coords[0] - mask_half_width), min(rows, coords[0] + mask_half_width + 1)):
            for j in range(max(0, coords[1] - mask_half_width), min(cols, coords[1] + mask_half_width + 1)):
                if i != coords[0] or j != coords[1]:
                    neighbors.append(array[i, j])

        return neighbors

    def process(self, n_colors: int, stitches_per_row: int, method: str):
        """Process image:
        1. Resize image to be stitches_per_row x stitches_per_column, this shape is not changed anymore
        2. Compute the dmc palette based on the predominant image colors
        3. Quantize the image with n dmc colors
        4. Convert the image to a np array"""
        self._resize(stitches_per_row)
        if DEBUG:
            self.show('After resize')
        dmc_palette = self._get_dmc_palette(n_colors, method)
        self._quantize(dmc_palette)
        if DEBUG:
            self.show('After quantize')
        self._clean()
        if DEBUG:
            self.show('After clean')
        dcm_pattern = self._get_dmc_pattern()

        return dmc_palette, dcm_pattern

    def show(self, title):
        """Show PIL Image in screen"""
        data = np.array(self.pil_image)
        plt.title(title)
        plt.imshow(data)
        plt.show()
