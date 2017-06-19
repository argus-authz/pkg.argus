pipeline {
  agent { label 'docker' }

  options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }
  
  parameters {
    string(name: 'COMPONENTS', defaultValue: 'pap pdp-pep-common pep-common pdp pep-server pep-api-c pep-api-java pepcli gsi-pep-callout metapackage')
    choice(name: 'PLATFORM', choices: 'centos6\ncentos7')
    string(name: 'PKG_BUILD_NUMBER', defaultValue: '', description: 'This is used to pass a custom build number that will be included in the package version.')
  }

  stages{
    stage('package') {
      environment {
        DATA_CONTAINER_NAME = "stage-area-pkg.argus-${env.BUILD_NUMBER}"
        PKG_TAG = "${env.BRANCH_NAME}"
        MVN_REPO_CONTAINER_NAME = "mvn_repo-pkg.argus-${env.BUILD_NUMBER}"
        PLATFORM = "${params.PLATFORM}"
        COMPONENTS = "${params.COMPONENTS}"
        PKG_BUILD_NUMBER = "${params.PKG_BUILD_NUMBER}"
        STAGE_ALL = '1'
      }
      
      steps {
        git(url: 'https://github.com/argus-authz/pkg.argus.git', branch: env.BRANCH_NAME)
        sh 'docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:${PLATFORM}'
        sh 'docker create -v /m2-repository --name ${MVN_REPO_CONTAINER_NAME} italiangrid/pkg.base:${PLATFORM}'
        sh '''
          pushd rpm 
          ls -al
          sh build.sh
          popd
        '''
        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area repo'
        sh 'docker rm -f ${DATA_CONTAINER_NAME} ${MVN_REPO_CONTAINER_NAME}'
        archiveArtifacts 'repo/**'
        
        script { currentBuild.result = 'SUCCESS' }
      }
    }
  }
  
  post {
    failure {
      slackSend color: 'danger', message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure (<${env.BUILD_URL}|Open>)"
    }
    changed {
      script{
        if('SUCCESS'.equals(currentBuild.result)) {
          slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Back to normal (<${env.BUILD_URL}|Open>)"
        }
      }
    }
  }
}
