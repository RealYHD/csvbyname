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
                sh 'mamba env update --file environment.yml'
                sh 'echo "mamba activate csvbyname" >> ~/.bashrc'
            }
        }
        stage("build") {
            steps {
                sh "python -m build"
            }
        }
        stage("test") {
            steps {
                sh "pip install dist/*.whl"
            }
        }
        stage("publish") {
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