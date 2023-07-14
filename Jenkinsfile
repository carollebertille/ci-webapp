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
    stage("scan docker images") {
        when {
          expression { GIT_BRANCH == 'origin/main' }
        }
      environment{
          SNYK_TOKEN = credentials('SNYK')
       }
       steps{
        script {
         sh '''
          echo "starting image scan ..."
          SCAN_RESULT=$(docker run --rm -e $SNYK_TOKEN -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/app snyk/snyk:docker snyk test --docker ${DOCKERHUB_ID}/$IMAGE_NAME:$IMAGE_TAG --json 
          echo"scan ended"
         '''
        }
       }
    }
      
 }
}
   
 
