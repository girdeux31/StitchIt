import csv
from pathlib import Path

from PIL import ImageColor

from src.stitchit.color_tools import ColorTools
from src.stitchit.constants import CSV_REL_PATH


class DMCDB:
    
    def __init__(self):
        """Init object"""
        csv_file = Path(__file__).parent / CSV_REL_PATH
        self.dmc_dict = self._read_info_from_csv(csv_file)

    def _read_info_from_csv(self, csv_file: str) -> dict[str, dict[str, tuple | str]]:
        """Read CSV file with DMC info"""
        dmc_dict = {}
        with open(csv_file, mode='r') as f:

            reader = csv.reader(f)
            for row in reader:
                if len(row) != 3:
                    raise ValueError(f'Bad format while reading \'{self.csv_file}\' file')
                
                dmc_code = row[0]
                dmc_name = row[1]
                hex_code = row[2]
                rgb = ImageColor.getrgb(hex_code)
                dmc_dict[dmc_code] = {'rgb': rgb, 'name': dmc_name}

        return dmc_dict

    def get_most_similar_color(self, rgb: tuple[int], method: str) -> dict[str, str | tuple]:
        """
        Get DMC color info from an RGB tuple. To get the code, the closest rgb is chosen from the list
        using method to calculate distance
        """
        tmp_dist = 99999999
        for c_code, c_info in self.dmc_dict.items():
            dist = ColorTools.compute_color_distance(c_info['rgb'], rgb, method)
            if dist < tmp_dist:
                tmp_dist = dist
                new_code = c_code
        color_info = self.dmc_dict[new_code] | {'code': new_code}
        return color_info

    def get_color_by_code(self, code: str | int) -> dict[str, str | tuple]:
        """Get DMC color info from code"""
        code = str(code)
        if code not in self.dmc_dict:
            raise ValueError(f'Code \'{code}\' not found in DMC database')
        color_info = self.dmc_dict[code] | {'code': code}
        return color_info
