pipeline {
  agent { label 'docker' }

  options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }

  stages{
    stage('package el6') {
      environment {
        DATA_CONTAINER_NAME = 'stage-area-pkg.argus-el6-${BUILD_NUMBER}'
      }
      steps {
        git(url: 'https://github.com/argus-authz/pkg.argus.git', branch: env.BRANCH_NAME)
        sh 'docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:centos6'
        sh '''
        pushd rpm 
        ls -al
        sh build.sh
        popd
        '''
        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area repo'
        sh 'docker rm -f ${DATA_CONTAINER_NAME}'
//        archiveArtifacts 'repo/**'
        sh "rsync -avu repo/ admin@packages.default.svc.cluster.local:/srv/packages/repo/argus/centos6/"
      }
    }
    
    stage('package el7') {
      environment {
        DATA_CONTAINER_NAME = 'stage-area-pkg.argus-el7-${BUILD_NUMBER}'
      }
      steps {
        git(url: 'https://github.com/argus-authz/pkg.argus.git', branch: env.BRANCH_NAME)
        sh 'docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:centos7'
        sh '''
        pushd rpm 
        ls -al
        sh build.sh
        popd
        '''
        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area repo'
        sh 'docker rm -f ${DATA_CONTAINER_NAME}'
        //        archiveArtifacts 'repo/**'
        sh "rsync -avu repo/ admin@packages.default.svc.cluster.local:/srv/packages/repo/argus/centos7/"
      }
    }
  }
}
