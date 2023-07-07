pipeline {
    agent any 
      environment {
       DOCKERHUB_ID = "edennolan2021"
       IMAGE_NAME = "helloworld"
       IMAGE_TAG = "v1"  
       CONTAINER_PORT = "8081"
       DOCKERHUB = credentials('dockerhub')
       HOST_PORT = "80"
     }
  stages {
      stage('login to docker repository') {
       when {
          expression { GIT_BRANCH == 'origin/main' }
        }
          steps {
             script {
               sh 'echo $DOCKERHUB | docker login -u $DOCKERHUB_ID --password-stdin'
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
     stage("scan docker images") {
        when {
          expression { GIT_BRANCH == 'origin/main' }
        }
      environment{
          SNYK_TOKEN = credentials('snyktoken')
       }
       steps{
         sh '''
          echo "starting image scan ..."
           SCAN_RESULT-$(docker run --rm -e SNYK_TOKEN=$SNYK_TOKEN -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/app snyk/snyk:docker snyk test --docker ${DOCKERHUB_ID}/$IMAGE_NAME:$IMAGE_TAG --json
            echo"scan ended"
         '''
        }
    }
    
    stage('Run container based on builded image') {
      when {
          expression { GIT_BRANCH == 'origin/main' }
        }
            steps {
               script {
                 sh '''
                    echo "cleaning existing container if exist
                    docker ps -a | grep -i $IMAGE_NAME && docker rm -f ${IMAGE_NAME}
                    docker run --name ${IMAGE_NAME} -d -p ${APP_PORT}:CONTAINER_PORT ${DOCKERHUB_ID}/$IMAGE_NAME:$IMAGE_TAG 
                    sleep 5
                 '''
               }
            }
       }
  stage('Test image') {
      when {
          expression { GIT_BRANCH == 'origin/main' }
        }
           steps {
              script {
                sh '''
                    curl -I http://${HOST_IP}:${APP_PORT} | grep -i "200"
                '''
              }
           }
      }
    stage('Clean Container') {
          when {
          expression { GIT_BRANCH == 'origin/main' }
             }
          steps {
             script {
               sh '''
                 docker stop $IMAGE_NAME
                 docker rm $IMAGE_NAME
               '''
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
    stage("Deploy app in Pre-production Environment") {
        when {
          expression { GIT_BRANCH == 'origin/dev' }
            }
            steps {
                withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'gke_credential', namespace: '', serverUrl: '') {
                 sh "kubectl apply -f deployment.yml"
                }
            }
        }
	     
      
    stage("Deploy app in production Environment") {
       when {
          expression { GIT_BRANCH == 'origin/main' }
            }
            steps {
                withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'gke_credential', namespace: '', serverUrl: '') {
                 sh "kubectl apply -f deployment.yml"
                }
            }
          }
      
 }
}
   
 
