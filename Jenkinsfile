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
    stage("Deploy app in Pre-production Environment") {
        when {
          expression { GIT_BRANCH == 'origin/dev' }
            }
            steps {
                withKubeConfig(caCertificate: '', clusterName: 'gke_helloworld-391505_us-west1-a_helloworld-391505-gke', contextName: 'gke_helloworld-391505_us-west1-a_helloworld-391505-gke', credentialsId: 'gke-credential', namespace: 'helloworld', serverUrl: 'https://34.83.83.200') {
                 sh "kubectl apply -f deployment.yml"
                }
            }
        }
	     
      
    stage("Deploy app in production Environment") {
       when {
          expression { GIT_BRANCH == 'origin/main' }
            }
            steps {
                withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'gke_credential', namespace: '', serverUrl: 'https://34.83.83.200') {
                 sh "kubectl apply -f deployment.yml"
                }
            }
          }
      
 }
}
   
 
