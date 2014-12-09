from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SetupPipeline(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Pulling analysis-pipeline")
        master.ssh.execute('git clone git@bitbucket.org:staphopia/analysis-pipeline.git /staphopia/ebs/analysis-pipeline')

        log.info("Building packages")
        master.ssh.execute('cd /staphopia/ebs/analysis-pipeline && make')

        log.info("Giving ownership to staphopia")
        master.ssh.execute('chown -R staphopia /staphopia/ebs/analysis-pipeline')
        master.ssh.execute('chgrp -R staphopia /staphopia/ebs/analysis-pipeline')

