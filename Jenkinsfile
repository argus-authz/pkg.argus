def platform2Dir = [
  "centos7" : 'rpm',
  "centos6" : 'rpm'
]

def buildPackages(platform, platform2Dir) {
  return {
    unstash "source"

    def platformDir = platform2Dir[platform]

    if (!platformDir) {
      error("Unknown platform: ${platform}")
    }

    dir(platformDir) {
      sh "PLATFORM=${platform} pkg-build.sh"
    }
  }
}

pipeline {

  agent { label 'docker' }

  options {
    timeout(time: 3, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  environment {
    PKG_TAG = "${env.BRANCH_NAME}"
    PACKAGES_VOLUME = "pkg-vol-${env.BUILD_TAG}"
    STAGE_AREA_VOLUME = "sa-vol-${env.BUILD_TAG}"
    PLATFORMS = "centos6 centos7"
    DOCKER_REGISTRY_HOST = "${env.DOCKER_REGISTRY_HOST}"
    DOCKER_ARGS = "--rm -v /opt/cnafsd/helper-scripts/scripts/:/usr/local/bin"
  }

  stages {
    stage('checkout') {
      steps {
        deleteDir()
        checkout scm
        stash name: "source", includes: "**"
      }
    }
    stage('setup-volumes') {
      steps {
        sh 'pwd && ls -lR'
        sh 'rm -rf artifacts && mkdir -p artifacts'
        sh './setup-volumes.sh'
      }
    }
    stage('package') {
      steps {
        script {
          def buildStages = PLATFORMS.split(' ').collectEntries {
            [ "${it} build packages" : buildPackages(it, platform2Dir) ]
          }
          parallel buildStages
        }
      }
    }
    stage('archive-artifacts') {
      steps {
        sh './copy-artifacts.sh'
        archiveArtifacts "artifacts/**"
        stash name: "packages", includes: "artifacts/packages/**"
      }
    }
    stage('cleanup') {
      steps {
          sh 'docker volume rm ${PACKAGES_VOLUME} ${STAGE_AREA_VOLUME} || echo Volume removal failed'
      }
    }
  }
  
  post {
    failure {
      slackSend color: 'danger', message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure (<${env.BUILD_URL}|Open>)"
    }
    changed {
      script {
        if ('SUCCESS'.equals(currentBuild.result)) {
          slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Back to normal (<${env.BUILD_URL}|Open>)"
        }
      }
    }
  }
}
