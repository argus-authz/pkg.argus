def platform2Dir = [
  "centos7" : 'rpm',
  "centos6" : 'rpm'
]

def buildPackages(platform, platform2Dir, includeBuildNumber) {
  return {
    unstash "source"

    def platformDir = platform2Dir[platform]

    if (!platformDir) {
      error("Unknown platform: ${platform}")
    }

    def includeEnv = ""
    if (includeBuildNumber) {
      includeEnv = "INCLUDE_BUILD_NUMBER=1"
    }

    dir(platformDir) {
      sh "PLATFORM=${platform} ${includeEnv} pkg-build.sh"
    }
  }
}

pipeline {

  agent { label 'docker' }

  options {
    timeout(time: 3, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }
  
  parameters {
    booleanParam(name: 'INCLUDE_BUILD_NUMBER', defaultValue: true, description: 'Include build number into rpm name')

    string(name: 'PKG_BUILD_NUMBER', defaultValue: '', description: 'This is used to pass a custom build number that will be included in the package version.')
    string(name: 'COMPONENT_LIST', defaultValue: '', description: 'List of components to build')
    string(name: 'USE_DOCKER_REGISTRY', defaultValue: '1', description: 'Pull image from private registry; empty is false')
  }

  stages{
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
            [ "${it} build packages" : buildPackages(it, platform2Dir, "${params.INCLUDE_BUILD_NUMBER}" ) ]
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
