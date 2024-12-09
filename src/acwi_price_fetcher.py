from price_fetcher import FetchBasePrice

url = "https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=20331418A&int_fd=fund:psearch:search_result"
acwi_price = FetchBasePrice(url)
print(f"The Base Price of ACWI is: {acwi_price}")
