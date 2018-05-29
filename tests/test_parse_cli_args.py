import pytest

from telega_compose.main import parse_cli_args


@pytest.mark.parametrize(
    'input_args, arg_file, arg_state, compose_args',
    [
        (['local'], None, 'local', []),
        (['local', 'up'], None, 'local', ['up']),
        (['local', 'up', '-d'], None, 'local', ['up', '-d']),
        (['live', '-f', '/path/to/states.yml'], '/path/to/states.yml', 'live', []),
        (['live', '-f', '/path/to/states.yml', 'config'], '/path/to/states.yml', 'live', ['config']),
        (['live', '-f', '/path/to/states.yml', 'run', 'database'], '/path/to/states.yml', 'live', ['run', 'database']),
    ]
)
def test_parse_cli_args(input_args, arg_file, arg_state, compose_args):
    result_args, result_compose_args = parse_cli_args(input_args)
    assert result_args.file == arg_file
    assert result_args.state == arg_state
    assert result_compose_args == compose_args
