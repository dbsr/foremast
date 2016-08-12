import boto3
import logging

LOG = logging.getLogger(__name__)


class SNSTopicNotFound(Exception):
    pass


def get_sns_topic_arn(topic_name, account, region):
    """ Get SNS topic ARN

    Args:
        topic_name (str): Name of the topic to lookup.
        account (str): Environment, e.g. dev
        region (str): Region name, e.g. us-east-1

    Returns:
        str: ARN for requested topic name
    """
    session = boto3.Session(profile_name=account, region_name=region)
    sns_client = session.client('sns')

    topics = sns_client.list_topics()['Topics']

    for topic in topics:
        topic_arn = topic['TopicArn']
        if topic_name == topic_arn.split(':')[-1]:
            return topic_arn
    else:
        LOG.critical("No topic with name %s found.", topic_name)
        raise SNSTopicNotFound('No topic with name {0} found'.format(topic_name))