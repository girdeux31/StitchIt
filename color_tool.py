import math
from skimage.color import rgb2lab, deltaE_cie76, deltaE_ciede2000


class ColorTool:

    @staticmethod
    def _euclidean_distance(c1: tuple[int], c2: tuple[int]) -> float:
        """Compute euclidean distance between two colors'"""
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        return math.sqrt(((r1-r2)**2) + ((g1-g2)**2) + ((b1-b2)**2))

    @staticmethod
    def _compuphase_distance(c1: tuple[int], c2: tuple[int]) -> float:
        """Compute the compuphase distance between two RGB colors (like euclidian but with weighting factors depending on red)"""
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        rmean = (r1 + r2) / 2
        mr = (512 + rmean) / 256
        mg = 4
        mb = (767 - rmean) / 256

        return math.sqrt(mr*((r1-r2)**2) + mg*((g1-g2)**2) + mb*((b1-b2)**2))

    @classmethod
    def _deltae76_distance(cls, c1: tuple[int], c2: tuple[int]) -> float:
        """Compute euclidian distance between two LAB colors"""
        lab_1 = rgb2lab(cls._normalize_rgb_color(c1))
        lab_2 = rgb2lab(cls._normalize_rgb_color(c2))
        return deltaE_cie76(lab_1, lab_2)

    @classmethod
    def _deltae00_distance(cls, c1: tuple[int], c2: tuple[int]) -> float:
        """Compute CIEDE2000 distance between two LAB colors"""
        lab_1 = rgb2lab(cls._normalize_rgb_color(c1))
        lab_2 = rgb2lab(cls._normalize_rgb_color(c2))
        return deltaE_ciede2000(lab_1, lab_2)

    @staticmethod
    def _normalize_rgb_color(color: tuple[int]) -> tuple[float]:
        """Normalize rgb color to 1"""
        return tuple(rgb/255 for rgb in color)

    @classmethod
    def compute_color_distance(cls, c1: tuple[int], c2: tuple[int], method: str='de2000') -> float:
        """Compute color distance based on method"""
        dist_method = None
        if method == 'euclidian':
            dist_method = cls._euclidean_distance
        elif method == 'compuphase':
            dist_method = cls._compuphase_distance
        elif method == 'de76':
            dist_method = cls._deltae76_distance
        elif method == 'de00':
            dist_method = cls._deltae00_distance
        return dist_method(c1, c2)
