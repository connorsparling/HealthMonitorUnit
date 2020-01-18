#!/bin/bash
set -e

gcloud builds submit --tag gcr.io/healthmonitorunit-ecgsending/hmu-ecgsending
gcloud run deploy --image gcr.io/healthmonitorunit-ecgsending/hmu-ecgsending --platform managed
firebase deploy