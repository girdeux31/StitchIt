import numpy as np

from data_classes import OtherConfig


class ConfettiCleaner:

    def __init__(self, other_config: OtherConfig):
        """Init object"""
        self.other_config = other_config
        self.pattern = None

    def clean_confetti(self, pattern) -> None:
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
        self.pattern = pattern
        org_array = pattern.array
        for col in range(0, self.pattern.width):
            for row in range(0, self.pattern.height):
                if self.other_config.clean_confetti_wout_neighbors is True:
                    self._clean_pixel_if_no_neighbors(row, col, org_array)
                if self.other_config.clean_confetti_w1_diagonal_neighbor is True:
                    self._clean_pixel_if_only_one_diagonal_neighbor(row, col, org_array)

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
        """Replace current pixel by mode in neighbors"""
        mode = int(max(neighbors, key=neighbors.count))
        self.pattern.array [row, col] = mode
