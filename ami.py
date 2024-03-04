import boto3
import sys

def delete_amis(access_key_id, secret_access_key, region):
    # Create EC2 client using provided credentials and region
    client = boto3.client(
        'ec2',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region
    )
    
    # Describe instances
    instances = client.describe_instances()
    used_amis = []

    # Collect used AMIs from instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            used_amis.append(instance['ImageId'])

    print("Used AMIs:", used_amis)

    # Remove duplicate AMIs
    def remove_duplicates(amis):
        unique_amis = []
        for ami in amis:
            if ami not in unique_amis:
                unique_amis.append(ami)
        return unique_amis

    unique_amis = remove_duplicates(used_amis)
    print("Unique AMIs:", unique_amis)

    # Get custom AMIs from the account
    custom_images = client.describe_images(
        Filters=[
            {
                'Name': 'state',
                'Values': [
                    'available'
                ]
            },
        ],
        Owners=['self']
    )

    custom_amis_list = []

    # Collect custom AMIs
    for image in custom_images['Images']:
        custom_amis_list.append(image['ImageId'])

    # Deregister custom AMIs not in use
    for custom_ami in custom_amis_list:
        if custom_ami not in used_amis:
            print(f"Deregistering AMI: {custom_ami}")
            client.deregister_image(ImageId=custom_ami)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ami.py <access_key_id> <secret_access_key> <region>")
        sys.exit(1)

    access_key_id = sys.argv[1]
    secret_access_key = sys.argv[2]
    region = sys.argv[3]

    delete_amis(access_key_id, secret_access_key, region)  

