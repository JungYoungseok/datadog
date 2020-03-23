#!/bin/bash

result=$(curl https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu/latest)
curl -X POST "https://http-intake.logs.datadoghq.com/v1/input/{API-KEY}?service=covid19-puller&ddsource=aws_bash_crawler&ddtags=operator:jacky.jung,datasource:wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai,report_type:latest" -H "Content-Type: application/json" -d "$result"


result=$(curl -X GET "https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu/brief" -H "accept: application/json")
curl -X POST "https://http-intake.logs.datadoghq.com/v1/input/{APK-KEY}?service=covid19-puller&ddsourc=aws_bash_crawler&ddtags=operator:jacky.jung,datasource:wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai,report_type:brief" -H "Content-Type: application/json" -d "$result"

