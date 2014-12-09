from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class UpdateDjango(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Updating Staphopia.com")
        master.ssh.execute('cd /home/staphopia/staphopia.com && git pull')
        master.ssh.execute('chown -R staphopia /home/staphopia/staphopia.com')
        master.ssh.execute('chgrp -R staphopia /home/staphopia/staphopia.com')

        log.info("Installing Python libraries")
        master.ssh.execute('pip install -r /home/staphopia/staphopia.com/requirements.txt')

        log.info("Migrating Django DB")
        master.ssh.execute('python /home/staphopia/staphopia.com/manage.py syncdb --settings="staphopia.settings.dev"')
        master.ssh.execute('python /home/staphopia/staphopia.com/manage.py migrate --settings="staphopia.settings.dev"')
