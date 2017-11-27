#!/usr/bin/env bash
reset
#./scripts/uninstall.sh
#./scripts/install.sh
python examples/example/manage.py test qartez --traceback -v 3
