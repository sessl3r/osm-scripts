#!/bin/bash

AUTH_ENDPOINT=$(curl --silent https://www.openstreetmap.org/.well-known/oauth-authorization-server | jq --raw-output '.authorization_endpoint')
TOKEN_ENDPOINT=$(curl --silent https://www.openstreetmap.org/.well-known/oauth-authorization-server | jq --raw-output '.token_endpoint')

echo $AUTH_ENDPOINT

read -p "Enter the code from $AUTH_ENDPOINT?response_type=code&client_id=$OSM_CLIENT_ID&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=write_api" CODE

export OSM_TOKEN=$(curl --silent  -X POST -d "grant_type=authorization_code&client_id=$OSM_CLIENT_ID&client_secret=$OSM_CLIENT_SECRET&code=$CODE&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob" "$TOKEN_ENDPOINT" | jq --raw-output '.access_token')
echo $OSM_TOKEN

