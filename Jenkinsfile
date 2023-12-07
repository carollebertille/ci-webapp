pipeline {
    agent any 
      environment { 
	registry = '792069373652.dkr.ecr.us-east-2.amazonaws.com/carolle'
        dockerimage = '' 
     }

  stages {
      
      stage('SonarQube analysis') {
        when {
          expression { GIT_BRANCH == 'origin/main' }
         }
            agent {
                docker {
                  image 'edennolan2021/sonar-scanner-cli'
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
        steps{
                script {
                    dockerImage = docker.build registry
                }
            }
     }
    stage('Pushing to ECR') {
            steps{
                script {
                    sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 792069373652.dkr.ecr.us-east-1.amazonaws.com'
                    sh 'docker push 792069373652.dkr.ecr.us-east-1.amazonaws.com/carolle'
                }
            }
        }  
 }
}
   
 
