pipeline {
    agent {
        kubernetes {
            cloud 'rsys-devel'
            defaultContainer 'pip'
            inheritFrom 'pip'
        }
    }
    stages {
        stage("install") {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage("build") {
            steps {
                sh "python -m build"
            }
        }
        stage("test installation") {
            steps {
                sh "pip install dist/*.whl"
                sh "csvbyname -h"
            }
        }
        stage("archive") {
            steps {
                archiveArtifacts artifacts: 'dist/*.tar.gz, dist/*.whl', fingerprint: true, followSymlinks: false, onlyIfSuccessful: true
            }
        }
        stage("publish package") {
            when {
                branch '**/main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: '4d6f64be-d26d-4f95-8de3-b6a9b0beb311', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "python -m twine upload --repository-url https://git.reslate.systems/api/packages/${USER}/pypi -u ${USER} -p ${PASS} --non-interactive --disable-progress-bar --verbose dist/*"
                }
            }
        }
    }
}