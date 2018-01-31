pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh 'virtualenv --python `which python3.5` .venv'
        sh 'source .venv/bin/activate'
      }
    }
  }
}