pipeline {
    agent any
    stages {
        stage("clean") {
            steps {
                sh 'rm -rf ./dist/*'
            }
        }
        stage("install") {
            steps {
                sh 'mamba env update --file environment.yml --prefix ./env || mamba env create --force --file environment.yml --prefix ./env'
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
                withCredentials([usernamePassword(credentialsId: 'rs-git-package-registry-ydeng', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "python -m twine upload --repository-url https://git.reslate.systems/api/packages/${USER}/pypi -u ${USER} -p ${PASS} --non-interactive --disable-progress-bar --verbose dist/*"
                }
            }
        }
    }
}