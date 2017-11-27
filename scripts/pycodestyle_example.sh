#!/usr/bin/env bash
reset
pycodestyle examples/example/ --exclude examples/example/wsgi.py,examples/example/foo/migrations/,examples/example/foo/tests/,
