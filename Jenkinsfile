pipeline{
  agent any
  stages {
    stage('Build Flask twitter search engine App'){
      steps{
        sh 'docker build -t alex_caroline/myflaskapp:1.0 .'
      }
    }
    stage('Run docker images'){

        stage('Run Flask twitter search engine App'){
          steps{
            sh 'docker run -d -p 5000:5000 --name myflaskapp_c alex_caroline/myflaskapp:1.0'
          }

      }
    }
    stage('Testing'){
      steps{
        sh 'python test_app.py'
      }
    }
    stage('Docker images down'){
      steps{
        sh 'docker rm -f myflaskapp_c'
        sh 'docker rmi -f alex_caroline/myflaskapp:1.0'
      }
    }
  }
}
