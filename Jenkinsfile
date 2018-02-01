pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh '''#!/bin/bash
            virtualenv --python `which python3.5` .venv
            source .venv/bin/activate
            pip install -r dependencies/requirements.txt
        '''
      }
    }
    stage('Test') {
      steps {
        sh '''#!/bin/bash
            source .venv/bin/activate
            python ACM_General/manage.py test
        '''
      }
    }
  }
}
