# Description
This folder contains the code for the backend server hosted on http://backend.healthmonitor.dev

# Environment Setup
- Ensure you are in the correct `/Backend` folder from https://console.firebase.google.com

## Anaconda Setup (Optional)
- Download and Install Anaconda following instructions at https://docs.anaconda.com/anaconda/install/
> Create a conda environment with node.js and npm installed
```shell
$ conda create -n <NAME> node.js
```
> Activate your conda environment
```shell
$ conda activate <NAME>
```

## Firebase and Google Cloud Setup
- Make sure you have access to the firebase and google cloud project
- Download and install Google Cloud SDK following instructions at https://cloud.google.com/sdk/docs/quickstarts
- Download and install Node.js and npm from https://nodejs.org/en/ (if not setup from conda environment)
> Install firebase tools globally
```shell
$ npm install -g firebase-tools
```
> Login to Firebase 
```shell
$ firebase login
```
> Setup google cloud 
```shell
$ gcloud init
```

# Run and Deploy
## Running Locally
> To run the server locally use
```shell
$ npm start
```

## Deploy to Cloud
> To deploy the server to Google Cloud and Firebase use
```shell
$ npm run deploy
```