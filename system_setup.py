from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SystemInstaller(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing required packages")
            master.ssh.execute('apt-get -y update')
            node.ssh.execute('apt-get -y install libmysqlclient-dev libpq-dev')

            log.info("Updating PIP and setuptools")
            node.ssh.execute('pip install --upgrade pip')
            node.ssh.execute('curl https://bootstrap.pypa.io/ez_setup.py | python')

            log.info("Installing Python libraries")
            node.ssh.execute('echo "biopython==1.64" > /tmp/requirements.txt')
            node.ssh.execute('echo "PyVCF==0.6.7" >> /tmp/requirements.txt')
            node.ssh.execute('echo "ruffus==2.5" >> /tmp/requirements.txt')
            node.ssh.execute('pip install -r /tmp/requirements.txt')

            log.info('Installing R, ggplot2')
            node.ssh.execute('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9')
            node.ssh.execute('echo deb http://ftp.osuosl.org/pub/cran/bin/linux/ubuntu precise/ >> /etc/apt/sources.list')
            node.ssh.execute('apt-get -y update')
            node.ssh.execute('apt-get -y install r-base r-base-dev')
            node.ssh.execute('echo "install.packages(\"ggplot2\", repos=\"http://cran.fhcrc.org\")" >> /tmp/install_ggplot2.Rscript')

            log.info('SSH allow passwords, fix timeout')
            node.ssh.execute("sed -i 's/^PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config")
            node.ssh.execute('echo ClientAliveInterval 60 >> /etc/ssh/sshd_config && service ssh restart')

            log.info('Setting system wide SSH key for git')
            node.ssh.execute('echo "Host github.com" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    IdentityFile /mnt/ebs/staphopia/id_rsa.git" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "Host bitbucket.org" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    IdentityFile /mnt/ebs/staphopia/id_rsa.git" >> /etc/ssh/ssh_config')
            node.ssh.execute('service ssh restart')
