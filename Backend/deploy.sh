#!/bin/bash
set -e

gcloud config set project healthmonitorunit-backend
gcloud builds submit --tag gcr.io/healthmonitorunit-backend/hmu-backend
gcloud run deploy --image gcr.io/healthmonitorunit-backend/hmu-backend --platform managed --region us-central1
firebase deploy