import math

from skimage.color import rgb2lab, deltaE_cie76, deltaE_ciede2000


class ColorTools:

    @staticmethod
    def _euclidean_distance(c1: tuple[int], c2: tuple[int]) -> float:
        """Compute euclidean distance between two colors'"""
        return math.dist(c1, c2)

    @classmethod
    def _deltae76_distance(cls, c1: tuple[int], c2: tuple[int]) -> float:
        """
        Compute euclidean distance between two LAB colors
        deltaE is a measure of human perception in color difference
        """
        c1 = cls.rgb_to_lab(c1)
        c2 = cls.rgb_to_lab(c2)
        return deltaE_cie76(c1, c2)

    @classmethod
    def _deltae00_distance(cls, c1: tuple[int], c2: tuple[int]) -> float:
        """
        Compute CIEDE2000 distance between two LAB colors
        deltaE is a measure of human perception in color difference
        CIEDE2000 adjusts the distance specially for blues and purples
        """
        c1 = cls.rgb_to_lab(c1)
        c2 = cls.rgb_to_lab(c2)
        return deltaE_ciede2000(c1, c2)

    @staticmethod
    def rgb_to_lab(rgb: tuple[int]) -> tuple[float]:
        """Convert RGB to LAB coords"""
        norm_rgb = tuple(coord/255 for coord in rgb)  # normalize to 1
        return tuple(rgb2lab(norm_rgb))

    @classmethod
    def compute_color_distance(cls, c1: tuple[int], c2: tuple[int], method: str='de2000') -> float:
        """Compute color distance based on method"""
        dist_method = None
        if method == 'euclidean':
            dist_method = cls._euclidean_distance
        elif method == 'de76':
            dist_method = cls._deltae76_distance
        elif method == 'de00':
            dist_method = cls._deltae00_distance
        else:
            raise ValueError(f'Distance method \'{method}\' not allowed')
        return dist_method(c1, c2)

    @classmethod
    def compute_color_mse(cls, pattern, method: str, color_idx: int) -> float:
        """Compute MSE between DMC color and real color (method is used to compute yi-ŷi)"""
        count, mse = 0, 0
        color = pattern.palette.get_color_by_idx(color_idx)
        for r, row in enumerate(pattern.array):
            for c, c_idx in enumerate(row):
                if c_idx == color_idx:
                    base_rgb = tuple(pattern.base_rgb_array[r, c])
                    error = cls.compute_color_distance(base_rgb, color.dmc_rgb, method)
                    mse = error**2
                    count += 1
        return mse/count if count > 0 else 0.0

    @staticmethod
    def inverse_rgb(rgb: tuple[int]) -> tuple[int]:
        """Get inverse color from RGB"""
        return tuple(255 - coord for coord in rgb)