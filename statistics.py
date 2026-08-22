import math
from tabulate import tabulate

from pattern import Pattern


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


class Statistics:

    def __init__(self, fabric_count: int, strands_for_stitching: int) -> None:
        """Init object"""
        self.fabric_count = fabric_count  # number of squares (or stitches) per inch
        self.strands_for_stitching = strands_for_stitching
        self.pattern_size = {}
        self.thread_info = {
            'code': [],
            'name': [],
            'stitches': [],
            'length': [],
            'skeins': [],
        }
        if fabric_count not in FABRIC_COUNT_TO_STITCH_LENGTH:
            raise ValueError(f'Allowed values for \'thread_count\' parameters are: {", ".join(FABRIC_COUNT_TO_STITCH_LENGTH.keys())}')
        self.length_per_stitch = FABRIC_COUNT_TO_STITCH_LENGTH[fabric_count]

    def import_pattern(self, pattern: Pattern, method: str):
        """Import pattern"""
        self.pattern_size = {
            'stitches': (pattern.width, pattern.height),
            'inch': (
                pattern.width / self.fabric_count,  # squares / squares*inch = inch
                pattern.height / self.fabric_count,
            ),
            'cm': (
                pattern.width / self.fabric_count * CM_PER_INCH,  # squares / squares*inch * cm/inch = cm
                pattern.height / self.fabric_count * CM_PER_INCH,
            ),
        }
        for c_idx, c_info in pattern.dmc_palette.items():
            stitches = len([idx for row in pattern.dmc_pattern for idx in row if c_idx == idx])
            length = stitches * self.length_per_stitch / 100  # m
            skeins = math.ceil(length / (SKEIN_LENGTH*STRANDS_PER_SKEIN/self.strands_for_stitching))
            self.thread_info['code'].append(c_info['code'])
            self.thread_info['name'].append(c_info['name'])
            self.thread_info['stitches'].append(stitches)
            self.thread_info['length'].append(length)
            self.thread_info['skeins'].append(skeins)

    def print_info(self) -> None:
        """Print design and thread info"""
        self._print_design_info()
        self._print_thread_info()

    def _print_design_info(self):
        """Print design info"""
        print('Design information:')
        print('')
        print(f'  Fabric count or Aida count: {self.fabric_count} (ct or stitches per inch)')
        print(f'  Strands for stitching: {self.strands_for_stitching} strands')
        print(
            f'  Size (width x height): {self.pattern_size["cm"][0]:.2f}x{self.pattern_size["cm"][1]:.2f} (cm) or '
            f'{self.pattern_size["inch"][0]:.2f}x{self.pattern_size["inch"][1]:.2f} (\'\')'
        )
        print(f'  Stitches (width x height): {self.pattern_size["stitches"][0]}x{self.pattern_size["stitches"][1]}')
        print('')

    def _print_thread_info(self):
        """Print thread info"""
        headers = [
            'DMC code',
            'DMC color',
            'Stitches',
            'Length (m)',
            'Skeins',
        ]
        print('Thread information:')
        print('')
        print(tabulate(self.thread_info, headers=headers, tablefmt='simple'))
        print('')
