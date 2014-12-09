from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SystemInstaller(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing required packages")
            node.ssh.execute('apt-get -y update')
            node.ssh.execute('apt-get -y install libmysqlclient-dev libpq-dev')

            log.info("Updating PIP and setuptools")
            node.ssh.execute('pip install --upgrade pip')
            node.ssh.execute('curl https://bootstrap.pypa.io/ez_setup.py | python')

            log.info("Installing Python libraries")
            node.ssh.execute('echo "biopython==1.64" > /tmp/requirements.txt')
            node.ssh.execute('echo "PyVCF==0.6.7" >> /tmp/requirements.txt')
            node.ssh.execute('echo "ruffus==2.5" >> /tmp/requirements.txt')
            node.ssh.execute('echo "Django==1.7" >> /tmp/master_requirements.txt')
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

            log.info('Installing R, ggplot2')
            node.ssh.execute('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9')
            node.ssh.execute('echo deb http://ftp.osuosl.org/pub/cran/bin/linux/ubuntu precise/ >> /etc/apt/sources.list')
            node.ssh.execute('apt-get -y update')
            node.ssh.execute('apt-get -y install r-base r-base-dev')
            node.ssh.execute('echo "install.packages(\"ggplot2\", repos=\"http://cran.fhcrc.org\")" >> /tmp/install_ggplot2.Rscript')

            log.info('Remove Apache2')
            node.ssh.execute('service apache2 stop')
            node.ssh.execute('apt-get -y --purge remove apache2*')
            node.ssh.execute('apt-get -y autoremove')
