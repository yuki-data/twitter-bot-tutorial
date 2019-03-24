# Herokuで稼動するツイッターボット
指定したキーワード(ハッシュタグなど)を含むツイートを自動でリツイートし、
ツイートした人を自動フォローするツイッターボットです。

使用には、ツイッターのAPIキーが必要です。

Heroku上で常時可動させることを前提に、必要ファイル(Procfile, requirements.txt)を含んでいます。


# HerokuでのAPIキーの設定

heroku config:set CONSUMER_KEY=""
heroku config:set CONSUMER_SECRET=""
heroku config:set ACCESS_TOKEN=""
heroku config:set ACCESS_SECRET=""