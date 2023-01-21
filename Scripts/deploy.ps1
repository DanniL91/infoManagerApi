gcloud run deploy info-manager-api \
--image gcr.io/voltaic-quest-341402/info-api \
--platform managed \
--region southamerica-west1 \
--allow-unauthenticated \
--project voltaic-quest-341402 \
--service-account serverless-django@voltaic-quest-341402.iam.gserviceaccount.com 