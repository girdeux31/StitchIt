import math
import numpy as np

from pathlib import Path
from tabulate import tabulate

from src.chart import Chart
from src.color_tools import ColorTools
from src.data_classes import OtherConfig, ThreadConfig
from src.constants import TABLE_HEADER, TABLE_FORMAT, FABRIC_COUNT_TO_STITCH_LENGTH, CM_PER_INCH


class InfoFile:

    def __init__(self, other_config: OtherConfig, thread_config: ThreadConfig) -> None:
        """Init object"""
        self.other_config = other_config
        self.thread_config = thread_config
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
        self.length_per_stitch = FABRIC_COUNT_TO_STITCH_LENGTH[self.thread_config.fabric_count]

    def import_chart(self, chart: Chart):
        """Import pattern"""
        self.pattern_size = {
            'width': chart.pattern.width,
            'height': chart.pattern.height,
            'inch': (
                chart.pattern.width / self.thread_config.fabric_count,  # squares / squares*inch = inch
                chart.pattern.height / self.thread_config.fabric_count,
            ),
            'cm': (
                chart.pattern.width / self.thread_config.fabric_count * CM_PER_INCH,  # squares / squares*inch * cm/inch = cm
                chart.pattern.height / self.thread_config.fabric_count * CM_PER_INCH,
            ),
        }
        for color in chart.pattern.palette:
            if color.show_in_legend is True:
                stitches = np.sum(chart.pattern.array == color.idx)    # len([idx for row in pattern.dmc_pattern for idx in row if c_idx == idx])
                length = stitches * self.length_per_stitch / 100  # m
                skeins = math.ceil(length / (self.thread_config.skein_length*self.thread_config.strands_per_skein/self.thread_config.strands))
                error = ColorTools.compute_color_mse(chart.pattern, self.other_config.method, color.idx)
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
        f.write(f'  Fabric count or Aida count: {self.thread_config.fabric_count} (ct or stitches per inch)\n')
        f.write(f'  Strands for stitching: {self.thread_config.strands} strands\n')
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