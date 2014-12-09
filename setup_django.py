import time

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SetupDjango(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Installing nginx and supervisor")
        master.ssh.execute('apt-get -y update')
        master.ssh.execute('apt-get -y install nginx supervisor')

        log.info("Cloning Staphopia.com")
        master.ssh.execute('git clone git@bitbucket.org:staphopia/staphopia.com.git /home/staphopia/staphopia.com')
        master.ssh.execute('ln -s /etc/staphopia/private.py /home/staphopia/staphopia.com/staphopia/settings/private.py')
        master.ssh.execute('chown -R staphopia /home/staphopia/staphopia.com')
        master.ssh.execute('chgrp -R staphopia /home/staphopia/staphopia.com')

        log.info("Installing Python libraries")
        master.ssh.execute('pip install -r /home/staphopia/staphopia.com/requirements.txt')

        log.info("Migrating Django DB")
        master.ssh.execute('python /home/staphopia/staphopia.com/manage.py syncdb --settings="staphopia.settings.dev"')
        master.ssh.execute('python /home/staphopia/staphopia.com/manage.py migrate --settings="staphopia.settings.dev"')

        log.info("Setting up nginx static file proxy")
        master.ssh.execute('rm /etc/nginx/sites-enabled/default')
        master.ssh.execute('ln -s /home/staphopia/staphopia.com/config/nginx_static.conf /etc/nginx/sites-enabled/staphopia')
        master.ssh.execute('service nginx restart')

        log.info("Setting up gunicorn and supervisor")
        master.ssh.execute('pip install gunicorn')
        master.ssh.execute('ln -s /home/staphopia/staphopia.com/config/supervisor.gunicorn.conf /etc/supervisor/conf.d/supervisor.gunicorn.conf')
        master.ssh.execute('supervisorctl reread')
        master.ssh.execute('supervisorctl update')
        master.ssh.execute('service supervisor stop')
        time.sleep(5)
        master.ssh.execute('service supervisor start')
