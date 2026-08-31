from pathlib import Path
from src.stitchit import stitchit

from base_test import assert_output, setup_method


INP_NAME = Path('einstain.jpg')
DEFAULT_N_COLORS = 5
DEFAULT_STITCHES_PER_ROW = 80

def test_default_values(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
    }
    ref_file, tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_method_euclidean(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'method': 'euclidean',
    }
    ref_file, tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(ref_file, tmp_file)

def test_method_de76(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'method': 'de76',
    }
    ref_file, tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(ref_file, tmp_file)