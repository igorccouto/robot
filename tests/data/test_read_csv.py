import mock
from io import StringIO
from mock import mock_open
from robot.data import loader


in_mem_csv = ("col1;col2;col3\n"
                "1;3;foo\n"
                "2;5;bar\n"
                "-1;7;baz\n")

def test_returns_list():
    with mock.patch("builtins.open", mock_open(read_data=in_mem_csv)) as mock_file:
        data = loader.read_csv('ANY CSV FILE')
        assert isinstance(data, list), 'return value isn\'t a list.'
        assert len(data) == 3, 'not all rows were read.'

def test_reads_all_columns():
    with mock.patch("builtins.open", mock_open(read_data=in_mem_csv)) as mock_file:
        data = loader.read_csv('ANY CSV FILE')
        for d in data:
            assert isinstance(d, dict), 'return value isn\'t a list of dictionary.'
            assert len(d) == 3, 'not all columns were read.'
