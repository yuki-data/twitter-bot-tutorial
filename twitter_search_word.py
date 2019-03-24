import os
import time
import tweepy

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

if not CONSUMER_KEY:
    raise NameError("API key is not provided")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

user = api.me()
initial_message = "動作するボットアカウントは、{0}({1})です"
print(initial_message.format(user.name, user.screen_name))


def retweet_and_follow(search_word="#検索するハッシュタグ"):
    statuses = api.search(search_word, count=100)

    print("検索でヒットしたのは、{}件です。".format(len(statuses)))

    tweet_ids_ignored = []
    for status in statuses:
        if search_word not in status.text:
            # 正確に検索ワードが入っているもの以外除外
            tweet_ids_ignored.append(status.id)
            continue
        if status.author.screen_name == api.me().screen_name:
            # ボット自身のツイートを除外
            tweet_ids_ignored.append(status.id)
            if hasattr(status, "retweeted_status"):
                # すでにリツイートしたものを除外
                tweet_ids_ignored.append(status.retweeted_status.id)

    print("リツイートするのは、{}件です。".format(len(statuses) - len(tweet_ids_ignored)))

    for status in statuses:
        if status.id not in tweet_ids_ignored:
            try:
                status.retweet()
            except tweepy.TweepError as e:
                # ignore error if the error message is 'tweet is already retweeted'
                # searchのインターバルが長ければstatus.retweeted_status.id経由で除外できる
                # インターバルが短いとリツイート状態の反映が遅れるため327エラーが出る
                if e.api_code == 327:
                    print("already retweeted")
                    print(status.created_at, status.text[:20], status.lang, status.author.screen_name, status.retweeted, status.id)
                else:
                    raise e
            else:
                print(status.created_at, status.text[:20], status.lang, status.author.screen_name, status.retweeted, status.id)
            # error handling is unnecessary if already following
            status.author.follow()


if __name__ == "__main__":
    while True:
        retweet_and_follow("#検索するハッシュタグ")
        time.sleep(10)
