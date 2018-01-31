pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        bash 'virtualenv --python `which python3.5` .venv'
        bash 'source .venv/bin/activate'
      }
    }
  }
}
