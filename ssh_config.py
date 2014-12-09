from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SSHConfig(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info('SSH allow passwords, fix timeout')
            node.ssh.execute("sed -i 's/^PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config")
            node.ssh.execute('echo ClientAliveInterval 60 >> /etc/ssh/sshd_config && service ssh restart')

            log.info('Setting system wide SSH key for git')
            node.ssh.execute('echo "Host github.com" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    HostName github.com" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    User git" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    IdentityFile /etc/ssh/id_rsa.git" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    IdentitiesOnly yes" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "Host bitbucket.org" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    HostName bitbucket.org" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    User git" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    IdentityFile /etc/ssh/id_rsa.git" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    IdentitiesOnly yes" >> /etc/ssh/ssh_config')
            node.ssh.execute('echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config')
            node.ssh.execute('service ssh restart')
