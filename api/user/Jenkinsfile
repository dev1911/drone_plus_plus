node{
	def app

	stage ('Clone repository'){
		checkout scm
	}

	stage('Build image'){
		app = docker.build('$()env.BUILD_NUMBER',"-f ${shlokashah/user_web/api/user}/${Dockerfile} ${shlokashah/user_web/api/user}")
	}

	stage('Test image'){
		app.inside{
			sh 'echo "Tests Passes"'
		}
	}

	stage('Push image'){
		docker.withRegistry('https://registry.hub.docker.com','docker-hub-credentials'){
			app.push('$()env.BUILD_NUMBER')
			app.push("latest")
		}
	}
}