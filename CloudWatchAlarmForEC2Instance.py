import boto3

def create_cloudwatch_alarm(instance_id, threshold):
    client = boto3.client('cloudwatch')
    
    alarm_name = f"CPUUtilizationAlarm_i-04bd6c3c94932cf0c"
    alarm_description = "Alarm triggered when CPU utilization surpasses a certain threshold."
    metric_name = 'CPUUtilization'
    namespace = 'AWS/EC2'
    statistic = 'Average'
    comparison_operator = 'GreaterThanThreshold'
    evaluation_periods = 1
    period = 60
    threshold_value = threshold
    alarm_actions = [f'arn:aws:automate:us-east-2:ec2:stop']
    dimensions = [{'Name': 'InstanceId', 'Value': instance_id}]
    
    response = client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=alarm_description,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic=statistic,
        ComparisonOperator=comparison_operator,
        EvaluationPeriods=evaluation_periods,
        Period=period,
        Threshold=threshold_value,
        AlarmActions=alarm_actions,
        Dimensions=dimensions
    )
    print(response)
    
    print(f"Alarm created successfully.")

def lambda_handler(event, context):
    instance_id = 'i-04bd6c3c94932cf0c'
    threshold = 50  # Set the threshold value as per your requirement
    create_cloudwatch_alarm(instance_id, threshold)

