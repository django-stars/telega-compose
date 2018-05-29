telega-compose
--------------

.. image:: https://travis-ci.org/django-stars/telega-compose.svg?branch=master
    :target: https://travis-ci.org/django-stars/telega-compose

.. image:: https://codecov.io/gh/django-stars/telega-compose/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/django-stars/telega-compose

.. image:: https://badge.fury.io/py/telega-compose.svg
    :target: https://badge.fury.io/py/telega-compose

This is a wrapper on `docker-compose`_, which extends `compose file`_ syntax to keep several configurations (states) of your services in one file, with similar to docker-compose file syntax using native YAML `anchors and aliases`_.

How it works:
=============

- Render in-memory docker-compose file for required state from states file.
- Call docker-compose app with rendered file (state) and apply required docker-compose command on it.

States file reference:
======================

It's a YAML file with two required sections: **compose** and **states**.

Section **compose** is regular docker-compose config excluding `services`_ section:

.. code-block:: yaml

    compose:
      version: '3.4'
      configs:
        my_config:
          file: ./my_config.txt
        my_other_config:
          external: true
      secrets:
        my_secret:
          file: ./my_secret.txt
        my_other_secret:
          external: true
      volumes:
        data:
        media:


Section **states** is a list of states with description of `services`_ section for each state:

.. code-block:: yaml

    states:
      live:
        services:
          backend: *backend_service
          database: *database_service
          webserver: *webserver_service

You can describe service in separate section or inside **states** section. Also, you can inherit early described service and override some parameters in place:

.. code-block:: yaml

    states:
      local:
        services:
          database: &database_local_service
            <<: *database_service
            ports:
              - "127.0.0.1:5432:5432"


The rest of the sections you can use for you own purposes. For example to configure logging for all services:

.. code-block:: yaml

    ---
    compose:
      ...

    config:
      logging: &logging_config
        driver: "json-file"
        options:
          max-size: 50m

    components:

      backend: &backend_service
        ...
        logging: *logging_config

      database: &database_service
        ...
        logging: *logging_config

      webserver: &webserver_service
        ...
        logging: *logging_config

    states:

      live:
        services:
          backend: *backend_service
          database: *database_service
          webserver: *webserver_service

CLI usage:
==========

.. code-block:: bash

    tcompose [-h] [-f FILE] state [docker-compose parameters]

Positional arguments:

- *state* - state to render docker-compose file
- *docker-compose parameters* - any `command and its parameters accepted by docker-compose`_ except parameter for docker-compose file (*-f*, *--file*)

Optional arguments:

- *-h*, *--help* - to show help message
- *-f FILE*, *--file FILE* - path to states file, by default: *states.yml*

Examples:

.. code-block:: bash

     tcompose local_dev config
     tcompose live -f /path/to/my-custom-states.yml up -d
     tcompose qa -f /path/to/states.yml --project-name acme up

.. _docker-compose: https://docs.docker.com/compose/
.. _compose file: https://docs.docker.com/compose/compose-file/
.. _command and its parameters accepted by docker-compose: https://docs.docker.com/compose/reference/
.. _anchors and aliases: http://www.yaml.org/spec/1.2/spec.html#id2760395
.. _services: https://docs.docker.com/compose/compose-file/#service-configuration-reference
