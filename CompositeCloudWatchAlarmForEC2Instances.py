import boto3
import json

def create_composite_alarm(instance_ids, threshold):
    client = boto3.client('cloudwatch')

    composite_alarm_name = 'CompositeCPUUtilizationAlarm'
    alarm_description = 'Composite alarm triggered when CPU utilization surpasses a certain threshold for multiple instances'
    metric_name = 'CPUUtilization'
    namespace = 'AWS/EC2'
    period = 60
    evaluation_periods = 1
    comparison_operator = 'GreaterThanThreshold'
    threshold_value = threshold
    alarm_actions = ['arn:aws:automate:us-east-2:ec2:stop']

    dimensions = [{'Name': 'InstanceId', 'Value': instance_id} for instance_id in instance_ids]

    composite_alarm_rule = dict(
    And=[
        dict(
            Dimensions=dimensions,
            MetricName=metric_name,
            Namespace=namespace,
            ComparisonOperator=comparison_operator,
            Threshold=threshold_value,
            Period=period,
            EvaluationPeriods=evaluation_periods
            )
        ]
    )

    response = client.put_composite_alarm(
        AlarmName=composite_alarm_name,
        AlarmDescription=alarm_description,
        ActionsEnabled=True,
        AlarmRule=json.dumps(composite_alarm_rule),
    )

    print(f"Composite alarm {response['CompositeAlarmArn']} created successfully.")

def lambda_handler(event, context):
    instance_ids = ['i-04bd6c3c94932cf0c', 'i-0c7f831c5f650bd78']  # Sending the list of Instance IDs for which the CloudWatch Alarm is to be set.
    threshold = 50  # Set the threshold value as per your requirement

    create_composite_alarm(instance_ids, threshold)
