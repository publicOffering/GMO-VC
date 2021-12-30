import common_func as gmo_vc
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#定期的に現在レートを取得し、過去3回分をDynamoDBに保存。騰落傾向を記録する
def lambda_handler(event, context):
    print("monitor_rate_tendency hander was called")
    logger.info("monitor_rate_tendency hander was called")

    current_rate_dict = gmo_vc.get_current_rate_from_market()

    #BTC_RATE_1_TIMES_BEFORE
    #BTC_rate_2_times_before
    #BTC_rate_3_times_before