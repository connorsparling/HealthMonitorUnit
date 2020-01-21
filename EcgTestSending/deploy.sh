#!/bin/bash
set -e

gcloud config set project healthmonitorunit-ecgsending
gcloud builds submit --tag gcr.io/healthmonitorunit-ecgsending/hmu-ecgsending
gcloud run deploy --image gcr.io/healthmonitorunit-ecgsending/hmu-ecgsending --platform managed
firebase deploy