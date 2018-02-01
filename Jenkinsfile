pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh '''#!/bin/bash
            echo $PATH
            echo $WORKSPACE
            virtualenv --python `which python3.5` .venv
            source .venv/bin/activate
        '''
      }
    }
  }
  environment {
    PATH = 'PATH+EXTRA=WORKSPACE/.venv/bin'
  }
}
