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
BACKGROUND_CODE = 'B5200'

class Image:

    clean_pixels_wo_neighbors = True
    clean_pixels_w1_diagonal_neighbor = True

    def __init__(self, img_file: Path, show_colors: bool=True, show_symbols: bool=True) -> None:
        """Init object"""
        self.img_file = img_file
        self.show_colors = show_colors
        self.show_symbols = show_symbols
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
        pixel_size = self.width / stitches_per_row
        stitches_per_col = round(self.height / pixel_size)
        self.pil_image = self.pil_image.resize(
            (stitches_per_row, stitches_per_col),
            resample=PILImage.Resampling.NEAREST,  # or LANCZOS
        )

    def _quantize(self, palette: Palette) -> None:
        """Assign a color index to each pixel, only n colors are used, 
        output image is (stitches_cols, stitches_rows) where each element is a color index"""
        palette_1d = [coord for color in palette for coord in color.dmc_rgb]
        palette_img = PILImage.new("P", (1, 1))  # create an image 1x1 just to put the palette on
        palette_img.putpalette(palette_1d)
        self.pil_image = self.pil_image.quantize(
            palette=palette_img,
            dither=PILImage.Dither.NONE,
        )

    def _get_dmc_palette(self, n_colors: int, method: str) -> Palette:
        """Get a list of dmc colors most used in image"""
        dmc_palette = Palette(method)
        predominant_rgbs = self._get_predominant_colors(n_colors, method)
        for c_idx, rgb in enumerate(predominant_rgbs):
            if self.show_colors:
                dmc_palette.add_color_by_rgb(c_idx, rgb)
            else:
                dmc_palette.add_color_by_code(c_idx, BACKGROUND_CODE)
            if self.show_symbols:
                dmc_palette.add_symbol(c_idx)
        return dmc_palette

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

    def _get_dmc_pattern(self) -> np.ndarray[int]:
        """Convert the image into a np array"""
        return np.array(self.pil_image)

    def _clean(self) -> None:
        """
        Two options to clean 'confetti':
        1. Pixels that all neighbors are different color, example: B will be converted to A
            A A A
            A B A
            A A A
        2. Pixels that has one neighbor in any diagonal with same color, example: center B will be converted to A
            A A A
            A B A
            A A B
        if so, replace pixel by majority neighborhood color,
        output image is (stitches_cols, stitches_rows) where each element is a color index
        """
        pattern = self._get_dmc_pattern()
        for col in range(0, self.width):
            for row in range(0, self.height):
                if self.clean_pixels_wo_neighbors is True:
                    self._clean_pixel_if_no_neighbors(row, col, pattern)
                if self.clean_pixels_w1_diagonal_neighbor is True:
                    self._clean_pixel_if_only_one_diagonal_neighbor(row, col, pattern)

    def _clean_pixel_if_no_neighbors(self, row: int, col: int, array: np.ndarray[int]) -> None:
        """Clean 'bad' pixel only if all neighbors are different color"""
        current_pixel = int(array[row, col])
        neighbors = self._get_neighbor_values(row, col, array)
        if neighbors.count(current_pixel) == 0:
            self._replace_pixel_by_mode(row, col, neighbors)

    def _clean_pixel_if_only_one_diagonal_neighbor(self, row: int, col: int, array: np.ndarray[int]) -> None:
        """Clean 'bad' pixel only if there is just one same color neighbor in any diagonal"""
        current_pixel = int(array[row, col])
        neighbors = self._get_neighbor_values(row, col, array)
        diagonal_neighbors = self._get_neighbor_values(row, col, array, only_diagonals=True)
        if neighbors.count(current_pixel) == 1 and diagonal_neighbors.count(current_pixel) == 1:
            self._replace_pixel_by_mode(row, col, neighbors)

    def _get_neighbor_values(self, row: int, col: int, array: np.ndarray[int], only_diagonals: bool=False) -> list[int]:
        """Get neighbor values (color indexes) in a specific coordinate (max length is 8)"""
        values = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue  # don't include pixel at row, col (itself)
                if only_diagonals and (dr == 0 or dc == 0):
                    continue  # only include diagonal pixels
                r = row + dr
                c = col + dc
                if 0 <= r < array.shape[0] and 0 <= c < array.shape[1]:
                    values.append(array[r, c])
        return values

    def _replace_pixel_by_mode(self, row: int, col: int, neighbors: list[int]) -> None:
            mode = int(max(neighbors, key=neighbors.count))
            self.pil_image.putpixel((col, row), mode)

    def process(self, n_colors: int, stitches_per_row: int, method: str) -> tuple[Palette, np.ndarray[int]]:
        """Process image:
        1. Resize image to be stitches_per_row x stitches_per_column, this shape is not changed anymore
        2. Compute the dmc palette based on the predominant image colors
        3. Quantize the image with n dmc colors
        4. Convert the image to a np array"""
        self._resize(stitches_per_row)
        base_rgb_pattern = self._get_dmc_pattern()
        dmc_palette = self._get_dmc_palette(n_colors, method)
        self._quantize(dmc_palette)
        self._clean()
        dmc_pattern = self._get_dmc_pattern()

        return dmc_palette, dmc_pattern, base_rgb_pattern
