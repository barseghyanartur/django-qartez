python setup.py install
mkdir -p example/db/ example/static/ example/tmp/ example/media/
python example/example/manage.py collectstatic --noinput