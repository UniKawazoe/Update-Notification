import json
import hashlib
import requests
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
TABLE_NAME = 'website-monitor'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456781234:website-monitor'

URLS = ["https://xxx","https://yyy","https://zzz",]

def lambda_handler(event, context):
    changes_detected = []
    for URL in URLS:
        # URLからコンテンツを取得
        response = requests.get(URL)
        content = response.text
        # コンテンツをハッシュ化
        current_hash = hashlib.sha256(content.encode()).hexdigest()
        # DynamoDBから前回のハッシュを取得
        table = dynamodb.Table(TABLE_NAME)
        try:
            response = table.get_item(Key={'URL': URL})
            previous_hash = response['Item']['hash'] if 'Item' in response else None
        except ClientError as e:
            print(e.response['Error']['Message'])
            previous_hash = None
        # ハッシュを比較
        print("Hashed:", current_hash, previous_hash)
        if current_hash != previous_hash:

            url = "https://discord.com/api/webhooks/1234567890123456789/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # URLを入力する

            # response = requests.post(url, data=json.dumps(payload), headers=headers)
            MESSAGE_CONTENT = f"ページが更新されています。\n確認しましょう。\n{URL}"
            REQUEST_BODY = {"content": MESSAGE_CONTENT}
            response = requests.post(url, json=REQUEST_BODY)

            if response.status_code == 204:
                print("Webhook送信に成功しました。")
            else:
                print(f"Webhook送信に失敗しました。ステータスコード: {response.status_code}")


            # ハッシュが異なる場合は、SNSに通知
            message = f'Website content at {URL} has changed.'
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)
            # 新しいハッシュをDynamoDBに保存
            table.put_item(Item={'URL': URL, 'hash': current_hash})
            changes_detected.append(URL)
    if changes_detected:
        return {
            'statusCode': 200,
            'body': json.dumps(f'Changes detected in: {", ".join(changes_detected)}; notifications sent.')
        }
    else:
        # ハッシュが同じ場合は何もしない
        return {
            'statusCode': 200,
            'body': json.dumps('No change in website content for all URLs.')
        }
