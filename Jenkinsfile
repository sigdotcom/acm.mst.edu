pipeline {
  agent any
  stages {
    stage('Setup') {
      agent any
      environment {
        PATH = 'PATH+Extra=.venv/bin'
      }
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
}