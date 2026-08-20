import csv

from color_tool import ColorTool


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

    def get_most_similar_code_by_rgb(self, rgb: tuple[int], method: str) -> str:
        """Get DMC color code from an RGB tuple. To get the code, the closest rgb is chosen from the list,
        correction to the distance can be applied with corrected bool argument"""
        temp_dist = 99999999
        for code, info in self.dmc_dict.items():
            dist = ColorTool.compute_color_distance(info['rgb'], rgb, method)
            if dist < temp_dist:
                temp_dist = dist
                new_code = code

        return new_code
    
    def get_color_name_by_code(self, code: str) -> str:
        """Get the exact color name by code"""
        if code not in self.dmc_dict:
            raise KeyError(f'Code {code} not found in \'{self.csv_file}\' file')
        return self.dmc_dict[code]['name']
    
    def get_most_similar_rgb_by_rgb(self, rgb: tuple[int], method: str) -> tuple[int]:
        """"""
        code = self.get_most_similar_code_by_rgb(rgb, method=method)
        return self.dmc_dict[code]['rgb']
