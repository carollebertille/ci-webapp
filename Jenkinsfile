pipeline {
    agent any 
      environment {
       DOCKERHUB_ID = "edennolan2021"
       IMAGE_NAME = "helloworld"
       IMAGE_TAG = "v1"  
       CONTAINER_PORT = "8081"
       DOCKERHUB_CREDENTIALS = credentials('dockerhub')
      APP_PORT= "80"
     }

  stages {
      stage('login to docker repository') {
       when {
          expression { GIT_BRANCH == 'origin/main' }
        }
          steps {
             script {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
             }
          }
      }
       
      stage('SonarQube analysis') {
        when {
          expression { GIT_BRANCH == 'origin/main' }
         }
            agent {
                docker {
                  image 'edennolan2021/sonar-scanner-cli:4.8'
                }
               }
               environment {
        CI = 'true'
        scannerHome='/opt/sonar-scanner'
       }   
            steps{
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
         }

    
      stage("Build docker images") {
        when {
          expression { GIT_BRANCH == 'origin/main' }
        }
        steps {
            script {
               sh ' docker build -t ${DOCKERHUB_ID}/$IMAGE_NAME:$IMAGE_TAG . '
            }
        }
     }

    stage('push docker image') {
     when {
          expression { GIT_BRANCH == 'origin/main' }
        }
          steps {
             script {
               sh 'docker push $DOCKERHUB_ID/$IMAGE_NAME:$IMAGE_TAG '
             }
	  }
     }
    
      
 }
}
   
 
