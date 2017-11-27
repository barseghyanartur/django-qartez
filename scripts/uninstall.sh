#!/usr/bin/env bash
pip uninstall django-qartez -y
rm build -rf
rm dist -rf
rm examples/static -rf
rm src/django_qartez.egg-info -rf
rm builddocs.zip