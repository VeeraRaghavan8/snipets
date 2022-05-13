
# AWS

## S3

```sh
aws s3api list-object-versions --bucket bucket-name --prefix Prod/filename.txt
aws s3api get-bucket-notification-configuration --bucket bucket-name

CODE_PATH="/path/to/code/"
S3_PATH="s3://bucket-name/path/to/code/"
aws s3 sync $CODE_PATH $S3_PATH --sse --delete --dryrun
```

## Lambda

```sh
aws lambda update-function-code --function-name fn_name --zip-file fileb://mdl.zip

aws lambda update-function-code --function-name fn_name --s3-bucket <bucket> --s3-key <key/to/code> --region us-east-1

aws lambda publish-version --function-name $function-name --region us-east-1

Version_Number=`aws lambda list-versions-by-function --function-name  $function-name --region us-east-1 --o table | grep "Version"  | sed 's/ //g' | sed 's/|//g' | grep -Eo '[0-9]+$' | sort -nrk1,1 | head -1`

aws lambda update-alias --function-name $function-name --function-version $Version_Number --name dev --region us-east-1

aws lambda get-function-configuration --function-name $function-name
```

## EMR
```sh


aws emr add-steps --cluster-id j-3FT7KWNMRN3KH --steps Type=CUSTOM_JAR,Name="RUN_CODE_1",Jar="command-runner.jar",ActionOnFailure=CONTINUE,Args=[bash, -c,"aws s3 cp s3://bucket/path/to/code/ /home/hadoop/ --recursive;cd  /home/hadoop/;spark-submit code.py DEV COMPANY;"]
```

## Batch

```sh
date_epoch=date -d '2021-10-19 21:59:20' +"%s%3N"

aws batch list-jobs --output json --job-status FAILED --job-queue ao-algorithm-dev | jq '.jobSummaryList | .[] | select(.createdAt>=1634695160000)'

aws batch list-jobs --output json --job-status FAILED --job-queue ao-algorithm-dev | jq '.jobSummaryList | .[] | select(.createdAt>=1634695160000) | select(.container.exitCode!=null)'

aws batch list-jobs --output json --job-status SUCCEEDED --job-queue=ao-algorithm-dev --region us-east-1 | jq '.[] | map(select( .createdAt >= 1642564800000)) | .[].jobName'
```