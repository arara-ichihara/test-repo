import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('I am tuan!')
    }
