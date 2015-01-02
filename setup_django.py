import time

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SetupDjango(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            if node.alias == "master":
                log.info("Installing nginx and supervisor")
                master.ssh.execute('apt-get -y update')
                master.ssh.execute('apt-get -y install nginx supervisor')

                log.info("Cloning Staphopia.com")
                master.ssh.execute('rm -rf /staphopia/ebs/staphopia.com')
                master.ssh.execute('git clone git@bitbucket.org:staphopia/staphopia.com.git /staphopia/ebs/staphopia.com')
                master.ssh.execute('ln -s /etc/staphopia/private.py /staphopia/ebs/staphopia.com/staphopia/settings/private.py')
                master.ssh.execute('chown -R staphopia /staphopia/ebs/staphopia.com')
                master.ssh.execute('chgrp -R staphopia /staphopia/ebs/staphopia.com')

                log.info("Installing Python libraries")
                master.ssh.execute('curl https://bootstrap.pypa.io/ez_setup.py | python')
                master.ssh.execute('pip install -r /staphopia/ebs/staphopia.com/requirements.txt')

                log.info("Migrating Django DB")
                master.ssh.execute('python /staphopia/ebs/staphopia.com/manage.py syncdb --settings="staphopia.settings.dev"')
                master.ssh.execute('python /staphopia/ebs/staphopia.com/manage.py migrate --settings="staphopia.settings.dev"')

                log.info("Setting up nginx static file proxy")
                master.ssh.execute('rm /etc/nginx/sites-enabled/default')
                master.ssh.execute('ln -s /staphopia/ebs/staphopia.com/config/nginx_static.conf /etc/nginx/sites-enabled/staphopia')
                master.ssh.execute('service nginx restart')

                log.info("Setting up gunicorn and supervisor")
                master.ssh.execute('pip install gunicorn')
                master.ssh.execute('ln -s /staphopia/ebs/staphopia.com/config/supervisor.gunicorn.conf /etc/supervisor/conf.d/supervisor.gunicorn.conf')
                master.ssh.execute('supervisorctl reread')
                master.ssh.execute('supervisorctl update')
                master.ssh.execute('service supervisor stop')
                time.sleep(10)
                master.ssh.execute('service supervisor start')
            else:
                log.info("Installing Django related libraries")
                node.ssh.execute('curl https://bootstrap.pypa.io/ez_setup.py | python')
                node.ssh.execute('pip install -r /staphopia/ebs/staphopia.com/requirements.txt')

    def on_add_node(self, node, nodes, master, user, user_shell, volumes):
        if node.alias == "master":
            log.info("Master node, not doing anything.")
        else:
            log.info("Installing Django related libraries")
            node.ssh.execute('curl https://bootstrap.pypa.io/ez_setup.py | python')
            node.ssh.execute('pip install -r /staphopia/ebs/staphopia.com/requirements.txt')
