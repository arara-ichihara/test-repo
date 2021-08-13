# coding: utf-8
 
# ①ライブラリのimport
import datetime
import pprint
import json
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
 
# ②Functionのロードをログに出力
print('Loading function')
 
# ③DynamoDBオブジェクトを取得
dynamodb = boto3.resource('dynamodb')
 
# ④Lambdaのメイン関数
def lambda_handler(event, context):
    
    # ⑤テーブル名を指定
    table_name = "set_usage_confirmation"
 
    # ⑦float型をdecimal型に変換
    payload = {
        key: val 
        if type(val) != float 
        else decimal.Decimal(str(val)) 
            for key, val in event.items()
    }
    
    # ⑧DynamoDBテーブルのオブジェクトを取得
    dynamotable = dynamodb.Table(table_name)
    
    # mail_adressとused_atを連結してidを作成
    id = event["mail_address"]+event["used_at"]
    
    #payloadにid_keyとid_valをappend
    payload['id'] = id
    
    try:
        # ⑨DynamoDBへのデータ登録
        res = dynamotable.put_item(
            Item = payload
        )
        print("Succeeded.")
        
        pprint.pprint(event)
        pprint.pprint(payload)
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    
    except Exception as e:
        print("Failed.")
        print(e)
        return
