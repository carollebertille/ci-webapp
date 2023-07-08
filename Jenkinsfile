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
     
    
    
    stage('Run container based on builded image') {
      when {
          expression { GIT_BRANCH == 'origin/main' }
        }
            steps {
               script {
                 sh '''
                    echo "cleaning existing container if exist"
                    docker ps -a | grep -i $IMAGE_NAME && docker rm -f ${IMAGE_NAME}
                    docker run --name ${IMAGE_NAME} -d -p ${APP_PORT}:$CONTAINER_PORT ${DOCKERHUB_ID}/$IMAGE_NAME:$IMAGE_TAG 
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
                  curl -I -X GET http://localhost:${APP_PORT}/api/status | grep -i "200"

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
   
 
