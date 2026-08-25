import math
import numpy as np

from pathlib import Path
from tabulate import tabulate

from chart import Chart
from color_tools import ColorTools


TABLE_HEADER = [
    'DMC code',
    'DMC color',
    'DMC RGB',
    'Stitches',
    'Length (m)',
    'Skeins',
    'MSE'
]
TABLE_FORMAT = 'simple'
FABRIC_COUNT_TO_STITCH_LENGTH = {
    11: 2.10,  # number of squares (or stitches) per inch, thread length in cm
    14: 1.80,
    16: 1.60,
    18: 1.45,
    20: 1.30,
}
SKEIN_LENGTH = 8  # m
STRANDS_PER_SKEIN = 6  # strands in a skein
CM_PER_INCH = 2.54  # cm/inch
# skein: madeja  (EN to SP)
# strand: hebra


class InfoFile:

    def __init__(self, fabric_count: int, strands_for_stitching: int) -> None:
        """Init object"""
        self.fabric_count = fabric_count  # number of squares (or stitches) per inch
        self.strands_for_stitching = strands_for_stitching
        self.pattern_size = {}
        self.thread_info = {
            'code': [],
            'name': [],
            'rgb': [],
            'stitches': [],
            'length': [],
            'skeins': [],
            'error': [],
        }
        if fabric_count not in FABRIC_COUNT_TO_STITCH_LENGTH:
            raise ValueError(f'Allowed values for \'thread_count\' parameters are: {", ".join(FABRIC_COUNT_TO_STITCH_LENGTH.keys())}')
        self.length_per_stitch = FABRIC_COUNT_TO_STITCH_LENGTH[fabric_count]

    def import_chart(self, chart: Chart, method: str):
        """Import pattern"""
        self.pattern_size = {
            'width': chart.pattern.width,
            'height': chart.pattern.height,
            'inch': (
                chart.pattern.width / self.fabric_count,  # squares / squares*inch = inch
                chart.pattern.height / self.fabric_count,
            ),
            'cm': (
                chart.pattern.width / self.fabric_count * CM_PER_INCH,  # squares / squares*inch * cm/inch = cm
                chart.pattern.height / self.fabric_count * CM_PER_INCH,
            ),
        }
        for color in chart.pattern.palette:
            if color.show_in_legend is True:
                stitches = np.sum(chart.pattern.array == color.idx)    # len([idx for row in pattern.dmc_pattern for idx in row if c_idx == idx])
                length = stitches * self.length_per_stitch / 100  # m
                skeins = math.ceil(length / (SKEIN_LENGTH*STRANDS_PER_SKEIN/self.strands_for_stitching))
                error = ColorTools.compute_color_mse(chart.pattern, method, color.idx)
                self.thread_info['code'].append(color.dmc_code)
                self.thread_info['name'].append(color.dmc_name)
                self.thread_info['rgb'].append(color.get_dmc_rgb_as_str())
                self.thread_info['stitches'].append(stitches)
                self.thread_info['length'].append(length)
                self.thread_info['skeins'].append(skeins)
                self.thread_info['error'].append(error)

    def _write_design_info(self, f):
        """Write design info"""
        f.write('Design information:\n')
        f.write('\n')
        f.write(f'  Fabric count or Aida count: {self.fabric_count} (ct or stitches per inch)\n')
        f.write(f'  Strands for stitching: {self.strands_for_stitching} strands\n')
        f.write(
            f'  Size (width x height): {self.pattern_size["cm"][0]:.2f}x{self.pattern_size["cm"][1]:.2f} (cm) or '
            f'{self.pattern_size["inch"][0]:.2f}x{self.pattern_size["inch"][1]:.2f} (\'\')\n'
        )
        f.write(f'  Stitches (width x height): {self.pattern_size["width"]}x{self.pattern_size["height"]}\n')
        f.write('\n')

    def _write_thread_info(self, f):
        """Write thread info"""
        f.write('Thread information:\n')
        f.write('\n')
        f.write(tabulate(self.thread_info, headers=TABLE_HEADER, tablefmt=TABLE_FORMAT, floatfmt=('','','','','.2f','','.4f')))
        f.write('\n')

    def save(self, file: Path):
        """Write design and thread info into file"""
        with open(file, 'w') as f:
            self._write_design_info(f)
            self._write_thread_info(f)