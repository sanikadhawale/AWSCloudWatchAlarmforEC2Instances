# AWSCloudWatchAlarmforEC2Instances
>Developed a AWS Lambda microservice to create a CloudWatch Alarm using Python 3.10 boto3 library to create a CloudWatch Alarm.
>The Alarm will triggered when the EC2 instance metric CPUUtilization surpasses a certain threshold, the EC2 metric are fetch from CloudWatch Metrics.
>Created another Lambda function that will be invoked, when the CloudWatch Alarm goes off, which will send the Alarm and EC2 details like alarm state, timestamp, EC2 instance name and id to DynamoDB Table.
