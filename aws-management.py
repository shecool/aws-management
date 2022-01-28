import boto3
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-a", "--action", dest="action", help="Specify the action you want to take. Options include: start, stop, and status.")
    parser.add_option("-r", "--region", dest="aws_region", help="Define AWS region e.g. us-west-1")
    parser.add_option("-o", "--owner", dest="owner_tag", help="Define the owner tagged to the instances.")

    # Future Use
    parser.add_option("-d", "--demo", dest="demo_tag", help="Define Demo tag.")

    (options, arguments) = parser.parse_args()

    # Check if user inputted a start or stop action
    # If not exit
    if options.action != "start" and options.action != "stop" and options.action != "status":
        parser.error("[!] Please specify an action. Use --help for more info.")
 
    return options

def get_name(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']

def eval_action(action, aws_region, aws_owner):
    ec2 = boto3.resource('ec2', region_name=aws_region)

    print('#############################################################################')
    print('AWS Region: ', aws_region)
    print('Instance(s) Owner: ', aws_owner)

    # Start running instances
    if action == "start":
        instances = ec2.instances.filter(Filters=[{'Name': 'tag:Owner','Values': [aws_owner]}, {'Name': 'instance-state-name', 'Values': ['stopped']}])
        for instance in instances:
            instance.start()
            instance_name = get_name(instance)
            print('Started instance: ', instance.id,  '|| Name: ', instance_name)

    # Stop running instances
    if action == "stop":
        instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:Owner','Values': [aws_owner]}, {'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            instance.stop()
            instance_name = get_name(instance)
            print('Stopped instance: ', instance.id,  '|| Name: ', instance_name)

    # Get status of all instances
    if action == "status":
        instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:Owner','Values': [aws_owner]}])
        for instance in instances:
            instance_name = get_name(instance)
            print('Instance ID: ', instance.id, '|| Status: ', instance.state['Name'],  '|| Name: ', instance_name)

def main():
    options = get_arguments()

    # Check if user specified a region - If not default to us-west-1
    if options.aws_region:
        aws_region = options.aws_region
    else:
        aws_region = "us-west-1"

    # Check if user specified an owner tag - If not default to SY
    if options.owner_tag:
        aws_owner = options.owner_tag
    else:
        aws_owner = "SY"

    # Evaluate the requested action
    eval_action(options.action, aws_region, aws_owner)



if __name__ == "__main__":
    main()





