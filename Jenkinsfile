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
            virtualenv --python `which python3.5` .venv
            source .venv/bin/activate
            pip install -r dependencies/requirements.txt
        '''
      }
    }
  }
}