import numpy as np

from PIL import Image as PILImage

from src.palette import Palette
from src.color_tools import ColorTools
from src.data_classes import GeneralConfig, OtherConfig
from src.constants import METHOD_TO_COLOR_THRESHOLD


class Image:

    def __init__(self, general_config: GeneralConfig, other_config: OtherConfig) -> None:
        """Init object"""
        self.general_config = general_config
        self.other_config = other_config
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

    def _import_image(self) -> None:
        """Read image as (cols,rows,rgb)"""
        if not self.general_config.input_file.exists():
            raise FileNotFoundError(f'File \'{self.general_config.input_file}\' not found')
        self.pil_image = PILImage.open(self.general_config.input_file).convert('RGB')  # make sure to read it in RGB mode

    def _resize(self) -> None:
        """Resize image so each pixel is a stitch (equivalent to pixelate), 
        output image is (stitches_cols, stitches_rows, rgb)"""
        pixel_size = self.width / self.general_config.stitches_per_row
        stitches_per_col = round(self.height / pixel_size)
        self.pil_image = self.pil_image.resize(
            (self.general_config.stitches_per_row, stitches_per_col),
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

    def _set_dmc_palette(self):
        """Get a list of dmc colors most used in image"""
        self.palette = Palette(self.other_config.method)
        predominant_rgbs = self._get_predominant_colors()
        for c_idx, rgb in enumerate(predominant_rgbs):
            self.palette.add_color_by_rgb(c_idx, rgb)
            if self.general_config.show_symbols:
                self.palette.add_symbols()

    def _get_predominant_colors(self) -> list[tuple[int]]:
        """Get a list of colors most used in image"""
        count_rgbs = self.pil_image.getcolors(maxcolors=self.width*self.height)
        count_rgbs.sort(reverse=True) # sort by count
        img_rgbs = [c_rgb[1] for c_rgb in count_rgbs]
        output_rgbs = []
        for base_rgb in img_rgbs:
            if all(
                ColorTools.compute_color_distance(base_rgb, rgb, self.other_config.method) >= METHOD_TO_COLOR_THRESHOLD[self.other_config.method]
                for rgb in output_rgbs
            ):
                output_rgbs.append(base_rgb)
        return output_rgbs[:self.general_config.n_colors]  # return only the n most predominant colors

    def process(self) -> tuple[Palette, np.ndarray[int]]:
        """Process image:
        1. Resize image to be stitches_per_row x stitches_per_column, this shape is not changed anymore
        2. Compute the dmc palette based on the predominant image colors
        3. Quantize the image with n dmc colors
        4. Convert the image to a np array"""
        self._import_image()  # pil_image is always width,height / cols,rows / x,y
        self._resize()
        self.general_config.n_colors += 1 if self.general_config.show_aida is True else 0  # add 1 color because aida color wont be shown in legend
        self._set_dmc_palette()
        self._quantize()
        if self.general_config.show_colors is False:
            self.palette.replace_all_colors_by_rgb(self.other_config.aida_color)
