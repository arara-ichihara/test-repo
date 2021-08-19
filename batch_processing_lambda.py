import json
import boto3
from datetime import datetime, timedelta, timezone
import pprint
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import numpy as np

#dynamodb指定
DYNAMO_TABLE_NAME = 'yoppy-test-db2'
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table(DYNAMO_TABLE_NAME)
#s3指定
s3_resource = boto3.resource('s3')
OUTPUT_BUCKET = 'log-yoppy-csv'
#日付取得
JST = timezone(timedelta(hours=+9), 'JST')
today = datetime.now(JST)
lastmonth = datetime(today.year, today.month-1,1)
lastmonth_str=lastmonth.strftime("%Y-%m")
year_only_str=lastmonth.strftime("%Y")
month_only_str=lastmonth.strftime("%m")
#s3にエクスポート
TEMP_FILENAME = '/tmp/食堂利用情報_' + year_only_str + '_' + month_only_str + '.csv'   #/tmp/のパスが必要
LATEST_OUTPUT_KEY = 'latest/食堂利用情報_' + year_only_str + '_' + month_only_str + '.csv'    #上書きされる
LAST_MONTH_OUTPUT_KEY =  year_only_str + '/' + month_only_str + '/食堂利用情報_' + year_only_str + '_' + month_only_str + '.csv'   #2021/07/export.csv

def lambda_handler(event, context):
print("")
#確認用
print(table)
print(today)
print(lastmonth_str," ",year_only_str," ",month_only_str)

options = {
'FilterExpression': Attr('used_at_date').contains(lastmonth_str),
'ProjectionExpression' : 'mail_address,used_at_date,used_in,reservation_num'
}
response=table.scan(**options)
#確認用
#pprint.pprint(response)
print("--------------")
#dynamoDBからアイテムを取得
df = pd.DataFrame(response['Items'])
#確認用
print(df.to_string())
#金額とゲスト有無のカラムを追加
df2 = df.assign(利用金額=lambda x: (x['reservation_num']*200))
df2 = df2.assign(ゲスト有無=lambda x: np.where((x['reservation_num']>1),'1','0'))
#確認用
print(df2.to_string())
df2 = df2.rename(columns={'mail_address':'利用者','used_at_date':'利用日','used_in':'利用場所','reservation_num':'利用人数'})
#csvファイルにエクスポート
df2.to_csv(TEMP_FILENAME, index=False, header=True)
#s3にアップロード
s3_resource.Bucket(OUTPUT_BUCKET).upload_file(TEMP_FILENAME, LATEST_OUTPUT_KEY)
s3_resource.Bucket(OUTPUT_BUCKET).upload_file(TEMP_FILENAME, LAST_MONTH_OUTPUT_KEY)

return 0
