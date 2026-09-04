from pathlib import Path

from base_test import assert_output, setup_method

from src.stitchit.cli import main

INP_NAME = Path('bird.jpg')
DEFAULT_N_COLORS = 3
DEFAULT_STITCHES_PER_ROW = 60


def test_default_values(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_no_colors(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'no-colors': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_no_symbols(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'no-symbols': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_no_legend(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'no-legend': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_all_false(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'no-colors': None,
        'no-symbols': None,
        'no-legend': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_no_aida(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'no-aida': None,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_backstitch_constant(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'backstitch-option': 'constant',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_backstitch_inverse(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'backstitch-option': 'inverse',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_min_values(request):
    args = {
        'n-colors': 2,
        'stitches-per-row': 10,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_cleaner_moderate(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'cleaner-option': 'moderate',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)

def test_cleaner_none(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'cleaner-option': 'none',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    main()
    assert_output(INP_NAME, tmp_file)