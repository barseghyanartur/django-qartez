#!/usr/bin/env bash
python setup.py develop
mkdir -p examples/db/ examples/static/ examples/tmp/ examples/media/
python examples/example/manage.py collectstatic --noinput
