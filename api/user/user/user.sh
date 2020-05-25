#! /bin/sh
echo "Making migrations..."
python user/manage.py makemigrtions
echo "Migrating..."
python user/manage.py migrate
echo "Done Migrating. Collecting static..."
python user/manage.py collectstatic
echo "Done collecting static. Copying static..."
cp user/static/ /shared/ -r
echo "Installing requirements..."
apt-get install nano
pip install gunicorn
gunicorn --chdir user/ user.wsgi --bind 0.0.0.0:8000 -w 2 --daemon
echo "Started gunicorn on port 8000."
