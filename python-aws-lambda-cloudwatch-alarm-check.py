import boto3

def lambda_handler(event, context):
    # リージョンを取得
    client = boto3.client('cloudwatch', event['Region'])
    sns = boto3.client('sns')

    # リージョン内のアラーム一覧を取得
    responce = client.describe_alarms()
    all_list = []
    alarm_list = []

    for metricalarm in responce['MetricAlarms']:
        # 全てのアラーム名をリストに追加
        all_list.append(metricalarm['AlarmName'])
        
        if metricalarm['StateValue'] == 'ALARM':
            # StateValueがALARMなアラーム名をリストに追加
            alarm_list.append(metricalarm['AlarmName'])

            # StateValueがALARMなアラームに対して、SNSから再送する。
            for alarmaction in metricalarm['AlarmActions']:
                responce2 = sns.publish(
                    TopicArn=alarmaction,
                    Subject='reALARM: "' + metricalarm['AlarmName'] + '"',
                    Message=metricalarm['AlarmName']
                )

    # print(all_list)
    # print(alarm_list)
