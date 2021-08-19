from datetime import datetime, timedelta, timezone
import pprint
import json
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
 
#DynamoDBオブジェクトを取得
dynamodb = boto3.resource('dynamodb')
 
#Lambdaのメイン関数
def lambda_handler(event, context):
    
    #テーブル名を指定
    table_name = "YoppyServings"
 
    #float型をdecimal型に変換
    payload = {
        key: val 
        if type(val) != float 
        else decimal.Decimal(str(val)) 
            for key, val in event.items()
    }
    
    #DynamoDBテーブルのオブジェクトを取得
    dynamotable = dynamodb.Table(table_name)
    
    #mail_adressとused_atを連結してidを作成
    id = event['mail_address']+event['used_at']
    
    #payloadにid_keyとid_valをappend
    payload['id'] = id
    
    #東京の現在時刻をcreated_atに代入
    JST = timezone(timedelta(hours=+9), 'JST')
    current_time = datetime.now(JST)
    
    #時刻のformatを修正 
    created_at=current_time.strftime("%Y-%m-%dT%H:%M:%S")+"+09:00"
    
    #created_atをpayloadに追加
    payload['created_at'] = created_at
    
    try:
        #DynamoDBへのデータ登録
        res = dynamotable.put_item(
            Item = payload
        )
        
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
