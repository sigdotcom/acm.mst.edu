pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh '''#!/bin/bash
            virtualenv --python `which python3.5` .venv
            source .venv/bin/activate
        '''
        sh 'pip3 install -r dependencies/requirements.txt'
      }
    }
  }
}