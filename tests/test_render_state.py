import pytest
import sys

from telega_compose.main import render_state


if sys.version_info[0] < 3:
    MOCK_OPEN = '__builtin__.open'
else:
    MOCK_OPEN = 'builtins.open'


yml_data = """---
compose:
  version: '3.3'

components:

  app: &app_service
    image: test/app
    depends_on:
      - database

  database: &database_service
    image: test/database

  webserver: &webserver_service
    image: test/webserver
    depends_on:
      - app

states:

  live:
    services:
      app: *app_service
      database: *database_service
      webserver: *webserver_service

  local:
    services:
      app: &app_local_service
        <<: *app_service
        command: ./app --develop

      database: &database_local_service
        <<: *database_service
        ports:
          - "127.0.0.1:5432:5432"
"""

live_state = """services:
  app:
    depends_on:
    - database
    image: test/app
  database:
    image: test/database
  webserver:
    depends_on:
    - app
    image: test/webserver
version: '3.3'
"""

local_state = """services:
  app:
    command: ./app --develop
    depends_on:
    - database
    image: test/app
  database:
    image: test/database
    ports:
    - 127.0.0.1:5432:5432
version: '3.3'
"""


@pytest.mark.parametrize(
    'state_name, rendered_state',
    [
        ('live', live_state,),
        ('local', local_state,),
    ]
)
def test_render_state_success(mocker, state_name, rendered_state):
    mock_os_path_exists = mocker.patch('os.path.exists')
    mock_os_path_exists.return_value = True
    mocker.patch(MOCK_OPEN, mocker.mock_open(read_data=yml_data))

    result = render_state(state_name, 'filename')
    assert result == rendered_state


def test_file_does_not_exists_fail(mocker):
    mock_os_path_exists = mocker.patch('os.path.exists')
    mock_os_path_exists.return_value = False

    with pytest.raises(Exception) as exception:
        render_state('local', 'filename')
    assert 'States file filename not found' in str(exception)


def test_state_not_fail(mocker):
    mock_os_path_exists = mocker.patch('os.path.exists')
    mock_os_path_exists.return_value = True
    mocker.patch(MOCK_OPEN, mocker.mock_open(read_data=yml_data))

    with pytest.raises(Exception) as exception:
        render_state('non-existing', 'filename')
    assert 'Unknown state non-existing' in str(exception)
