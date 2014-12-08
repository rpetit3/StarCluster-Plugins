from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SystemInstaller(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing Python libraries")
            node.ssh.execute('echo "Django==1.7" > /tmp/master_requirements.txt')
            node.ssh.execute('echo "MySQL-python==1.2.5" >> /tmp/requirements.txt')
            node.ssh.execute('echo "git+git://github.com/macropin/django-registration" >> /tmp/requirements.txt')
            node.ssh.execute('echo "django-crispy-forms==1.4.0" >> /tmp/requirements.txt')
            node.ssh.execute('echo "python-magic==0.4.6" >> /tmp/requirements.txt')
            node.ssh.execute('echo "django-datatables-view==1.12" >> /tmp/requirements.txt')
            node.ssh.execute('echo "psycopg2==2.5.4" >> /tmp/requirements.txt')
            node.ssh.execute('echo "django-email-changer==0.1.2" >> /tmp/requirements.txt')
            node.ssh.execute('echo "django-storages==1.1.8" >> /tmp/requirements.txt')
            node.ssh.execute('echo "boto==2.32.1" >> /tmp/requirements.txt')
            node.ssh.execute('pip install -r /tmp/requirements.txt')
