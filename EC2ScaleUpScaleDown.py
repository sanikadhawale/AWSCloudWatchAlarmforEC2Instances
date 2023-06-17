import boto3

def lambda_handler(event, context):
    asg_name = 'your-auto-scaling-group-name'
    region = 'your-aws-region'
    cpu_threshold = 80
    network_threshold = 50000000  # Adjust this threshold as per your requirements (in bytes)

    cloudwatch = boto3.client('cloudwatch', region_name=region)
    autoscaling = boto3.client('autoscaling', region_name=region)

    # Retrieve the CPU utilization metric data
    cpu_response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': asg_name
            },
        ],
        StartTime=(datetime.datetime.now() - datetime.timedelta(minutes=5)),
        EndTime=datetime.datetime.now(),
        Period=300,
        Statistics=['Average']
    )

    # Retrieve the network traffic metric data
    network_response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='NetworkPacketsIn',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': asg_name
            },
        ],
        StartTime=(datetime.datetime.now() - datetime.timedelta(minutes=5)),
        EndTime=datetime.datetime.now(),
        Period=300,
        Statistics=['Average']
    )

    # Calculate the average CPU utilization over the last 5 minutes
    average_cpu = cpu_response['Datapoints'][0]['Average']
    print('Average CPU utilization:', average_cpu)

    # Calculate the average network traffic over the last 5 minutes
    average_network = network_response['Datapoints'][0]['Average']
    print('Average network traffic:', average_network)

    # Check if either CPU or network traffic exceeds the thresholds
    if average_cpu > cpu_threshold or average_network > network_threshold:
        # Scale up the Auto Scaling Group
        autoscaling.set_desired_capacity(
            AutoScalingGroupName=asg_name,
            DesiredCapacity=2  # Adjust the desired capacity as needed
        )
        print('Scaled up the Auto Scaling Group.')
    else:
        # Scale down the Auto Scaling Group
        autoscaling.set_desired_capacity(
            AutoScalingGroupName=asg_name,
            DesiredCapacity=1  # Adjust the desired capacity as needed
        )
        print('Scaled down the Auto Scaling Group.')
