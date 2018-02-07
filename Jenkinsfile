pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    stages {

        stage('dev') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }
            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                DEV_SECURITY = credentials('DEV_SECURITY')
                CF_USER = credentials('CF_USER')
            }
            steps {
                sh "cf login -a https://${env.CLOUDFOUNDRY_API} --skip-ssl-validation -u ${CF_USER_USR} -p ${CF_USER_PSW} -o rmras -s dev"
                sh 'cf push --no-start ras-frontstage-api-dev'
                sh 'cf set-env ras-frontstage-api-dev ONS_ENV dev'
                sh "cf set-env ras-frontstage-api-dev SECURITY_USER_NAME ${env.DEV_SECURITY_USR}"
                sh "cf set-env ras-frontstage-api-dev SECURITY_USER_PASSWORD ${env.DEV_SECURITY_PSW}"
                sh "cf set-env ras-frontstage-api-dev DJANGO_CLIENT_ID ons@ons.gov"
                sh "cf set-env ras-frontstage-api-dev DJANGO_CLIENT_SECRET password"

                sh "cf set-env ras-frontstage-api-dev RAS_SECURE_MESSAGE_SERVICE_HOST ras-secure-messaging-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_SECURE_MESSAGE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_CASE_SERVICE_HOST casesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_CASE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_PARTY_SERVICE_HOST ras-party-service-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_PARTY_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_OAUTH_SERVICE_HOST ras-django-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_OAUTH_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_COLLECTION_EXERCISE_SERVICE_HOST collectionexercisesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_COLLECTION_EXERCISE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_SURVEY_SERVICE_HOST surveysvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_SURVEY_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_IAC_SERVICE_HOST iacsvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_IAC_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_COLLECTION_INSTRUMENT_SERVICE_HOST ras-collection-instrument-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_COLLECTION_INSTRUMENT_SERVICE_PORT 80"

                sh 'cf start ras-frontstage-api-dev'
            }
        }

        stage('ci?') {
            agent none
            steps {
                script {
                    try {
                        timeout(time: 60, unit: 'SECONDS') {
                            script {
                                env.deploy_ci = input message: 'Deploy to CI?', id: 'deploy_ci', parameters: [choice(name: 'Deploy to CI', choices: 'no\nyes', description: 'Choose "yes" if you want to deploy to CI')]
                            }
                        }
                    } catch (ignored) {
                        echo 'Skipping ci deployment'
                    }
                }
            }
        }

        stage('ci') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }

            }
            when {
                environment name: 'deploy_ci', value: 'yes'
            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                CI_SECURITY = credentials('CI_SECURITY')
                CF_USER = credentials('CF_USER')

                RAS_NOTIFY_EMAIL_VERIFICATION_TEMPLATE = credentials('RAS_NOTIFY_EMAIL_VERIFICATION_TEMPLATE')
                RAS_NOTIFY_REQUEST_PASSWORD_CHANGE_TEMPLATE = credentials('RAS_NOTIFY_REQUEST_PASSWORD_CHANGE_TEMPLATE')
                RAS_NOTIFY_CONFIRM_PASSWORD_CHANGE_TEMPLATE = credentials('RAS_NOTIFY_CONFIRM_PASSWORD_CHANGE_TEMPLATE')
            }
            steps {
                sh "cf login -a https://${env.CLOUDFOUNDRY_API} --skip-ssl-validation -u ${CF_USER_USR} -p ${CF_USER_PSW} -o rmras -s ci"
                sh 'cf push --no-start ras-frontstage-api-ci'
                sh "cf set-env ras-frontstage-api-dev SECURITY_USER_NAME ${env.DEV_SECURITY_USR}"
                sh "cf set-env ras-frontstage-api-dev SECURITY_USER_PASSWORD ${env.DEV_SECURITY_PSW}"
                sh "cf set-env ras-frontstage-api-dev DJANGO_CLIENT_ID ons@ons.gov"
                sh "cf set-env ras-frontstage-api-dev DJANGO_CLIENT_SECRET password"

                sh "cf set-env ras-frontstage-api-dev RAS_SECURE_MESSAGE_SERVICE_HOST ras-secure-messaging-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_SECURE_MESSAGE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_CASE_SERVICE_HOST casesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_CASE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_PARTY_SERVICE_HOST ras-party-service-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_PARTY_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_OAUTH_SERVICE_HOST ras-django-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_OAUTH_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_COLLECTION_EXERCISE_SERVICE_HOST collectionexercisesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_COLLECTION_EXERCISE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_SURVEY_SERVICE_HOST surveysvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_SURVEY_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_IAC_SERVICE_HOST iacsvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_IAC_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_COLLECTION_INSTRUMENT_SERVICE_HOST ras-collection-instrument-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_COLLECTION_INSTRUMENT_SERVICE_PORT 80"

                sh 'cf start ras-frontstage-api-ci'
            }
        }

        stage('release?') {
            agent none
            steps {
                script {
                    try {
                        timeout(time: 60, unit: 'SECONDS') {
                            script {
                                env.do_release = input message: 'Do a release?', id: 'do_release', parameters: [choice(name: 'Deploy to test', choices: 'no\nyes', description: 'Choose "yes" if you want to create a tag')]
                            }
                        }
                    } catch (ignored) {
                        echo 'Skipping test deployment'
                    }
                }
            }
        }

        stage('release') {
            agent {
                docker {
                    image 'node'
                    args '-u root'
                }

            }
            environment {
                GITHUB_API_KEY = credentials('GITHUB_API_KEY')
            }
            when {
                environment name: 'do_release', value: 'yes'
            }
            steps {
                // Prune any local tags created by any other builds
                sh "git tag -l | xargs git tag -d && git fetch -t"
                sh "git remote set-url origin https://ons-sdc:${GITHUB_API_KEY}@github.com/ONSdigital/ras-collection-instrument.git"
                sh "npm install -g bmpr"
                sh "bmpr patch|xargs git push origin"
            }
        }

        stage('test') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }

            }
            when {
                environment name: 'do_release', value: 'yes'
            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                TEST_SECURITY = credentials('TEST_SECURITY')
                CF_USER = credentials('CF_USER')

                RAS_NOTIFY_EMAIL_VERIFICATION_TEMPLATE = credentials('RAS_NOTIFY_EMAIL_VERIFICATION_TEMPLATE')
                RAS_NOTIFY_REQUEST_PASSWORD_CHANGE_TEMPLATE = credentials('RAS_NOTIFY_REQUEST_PASSWORD_CHANGE_TEMPLATE')
                RAS_NOTIFY_CONFIRM_PASSWORD_CHANGE_TEMPLATE = credentials('RAS_NOTIFY_CONFIRM_PASSWORD_CHANGE_TEMPLATE')
            }
            steps {
                sh "cf login -a https://${env.CLOUDFOUNDRY_API} --skip-ssl-validation -u ${CF_USER_USR} -p ${CF_USER_PSW} -o rmras -s test"
                sh 'cf push --no-start ras-frontstage-api-test'
                sh 'cf set-env ras-frontstage-api-test ONS_ENV test'
                sh "cf set-env ras-frontstage-api-dev SECURITY_USER_NAME ${env.DEV_SECURITY_USR}"
                sh "cf set-env ras-frontstage-api-dev SECURITY_USER_PASSWORD ${env.DEV_SECURITY_PSW}"
                sh "cf set-env ras-frontstage-api-dev DJANGO_CLIENT_ID ons@ons.gov"
                sh "cf set-env ras-frontstage-api-dev DJANGO_CLIENT_SECRET password"

                sh "cf set-env ras-frontstage-api-dev RAS_SECURE_MESSAGE_SERVICE_HOST ras-secure-messaging-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_SECURE_MESSAGE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_CASE_SERVICE_HOST casesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_CASE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_PARTY_SERVICE_HOST ras-party-service-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_PARTY_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_OAUTH_SERVICE_HOST ras-django-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_OAUTH_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_COLLECTION_EXERCISE_SERVICE_HOST collectionexercisesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_COLLECTION_EXERCISE_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_SURVEY_SERVICE_HOST surveysvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_SURVEY_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RM_IAC_SERVICE_HOST iacsvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RM_IAC_SERVICE_PORT 80"

                sh "cf set-env ras-frontstage-api-dev RAS_COLLECTION_INSTRUMENT_SERVICE_HOST ras-collection-instrument-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-frontstage-api-dev RAS_COLLECTION_INSTRUMENT_SERVICE_PORT 80"
                
                sh 'cf start ras-frontstage-api-test'
            }
        }
    }

    post {
        always {
            cleanWs()
            dir('${env.WORKSPACE}@tmp') {
                deleteDir()
            }
            dir('${env.WORKSPACE}@script') {
                deleteDir()
            }
            dir('${env.WORKSPACE}@script@tmp') {
                deleteDir()
            }
        }
    }
}