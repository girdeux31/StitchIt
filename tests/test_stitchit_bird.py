from pathlib import Path
from src.stitchit import stitchit

from base_test import assert_output, setup_method


INP_NAME = Path('bird.jpg')
DEFAULT_N_COLORS = 3
DEFAULT_STITCHES_PER_ROW = 60

def test_default_values(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_no_colors(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'no_colors': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_no_symbols(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'no_symbols': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_no_legend(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'no_legend': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_all_false(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'no_colors': None,
        'no_symbols': None,
        'no_legend': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_show_background(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'show_background': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_backstitch_constant(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'backstitch_option': "constant",
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_min_values(request):
    args = {
        'n_colors': 2,
        'stitches_per_row': 10,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)