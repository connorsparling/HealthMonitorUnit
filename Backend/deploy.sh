#!/bin/bash
set -e

gcloud builds submit --tag gcr.io/healthmonitorunit-backend/hmu-backend
gcloud run deploy --image gcr.io/healthmonitorunit-backend/hmu-backend --platform managed
firebase deploy