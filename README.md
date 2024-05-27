# 特定のページが更新されたら通知する仕組みを作ってみた

## 公開情報

[特定のページが更新されたら通知する仕組みを作ってみた](https://qiita.com/UniKawazoe/items/0e631e92476dffb41a0d)

## 構成図

![サイト更新検知_アーキテクチャー図.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3747609/5f88df9f-278a-83a6-5239-260f116b5b98.jpeg)

## 展開方法

1. CloudFormation.ymlを、AWSアカウントのバージニアリージョンに展開する
2. パラメータに指定する
3. AWSSNSからメールが来るため、サブスクライブする

### CloudFormation.yml内のパラメータについて

- EmailAddress
更新されたことを通知するメールアドレス

- DiscordWebhookURL
発行したDiscordWebhookURL

- ScheduleInterval
更新確認頻度(デフォルトでは12時間)

- MonitoringURLs
更新情報をキャッチアップしたいURL(複数設定可)