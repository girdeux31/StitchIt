import csv

from color_tools import ColorTools


class DMC:

    csv_file = 'dmc_colors.csv'
    
    def __init__(self):
        """Init object"""
        self.dmc_dict = self._read_info_from_csv(self.csv_file)

    def _read_info_from_csv(self, csv_file: str) -> dict[str, dict[str, tuple | str]]:
        """Read CSV file with DMC info"""
        dmc_dict = {}
        with open(csv_file, mode='r') as f:

            reader = csv.reader(f)
            for row in reader:
                if len(row) != 5:
                    raise ValueError(f'Bad format while reading \'{self.csv_file}\' file')
                
                code = row[0]
                rgb = (int(row[1]), int(row[2]), int(row[3]))
                name = row[4]
                dmc_dict[code] = {'rgb': rgb, 'name': name}

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
