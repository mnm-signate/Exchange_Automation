# coding=utf-8
import time

import ccxt
import numpy as np
import cbo_order_market
import cbo_order_stop
import line

# ロット #単位はドル
LOT = 5000
# 本番用(mex1)
bitmex = ccxt.bitmex({
    'apiKey': '自分のbitmex api キー',
    'secret': '自分のbitmex api シークレット',
    'enableRateLimit': True
})
bitmex.urls['api'] = bitmex.urls['www']

# 過去18時間のhigh_lowを取得
def high_low18(last,line_num):
    timest = bitmex.nonce()
    timest = timest - 1000 * 60 * 1140
    candles = bitmex.fetch_ohlcv('BTC/USD', timeframe='1h', since=timest)
    high = np.array([])
    low = np.array([])
    for i in candles:
        high = np.append(high, i[2])
        low = np.append(low, i[3])
    high_max = np.max(high[0:-1])
    low_min = np.min(low[0:-1])
    body = "過去 ： 高値 => " + str(high_max) + " 安値 => " + str(low_min)
    print(body)
    if line_num % 600 == 0:
        positions = bitmex.private_get_position()
        entry_price = positions[0]['avgEntryPrice']
        line.execute("[MEX_DTN生存確認]" + "現在価格：" + str(last) + " " + body + "保有vol：" + str(entry_price))
    if last > high_max:
        return "上昇ドテン",high_max,low_min
    elif last < low_min:
        return "下降ドテン",high_max,low_min
    else:
        return "",high_max,low_min


# 現状のポジションを確認
def check_position():
    positions = bitmex.private_get_position()
    position_volume = positions[0]['currentQty']
    if position_volume == 0:
        side = "NO POSITION"
    else:
        if position_volume > 0:
            side = "Buy"
            position_volume = positions[0]['currentQty']
        elif positions[0]['currentQty'] < 0:
            side = "Sell"
            position_volume = positions[0]['currentQty']
    print("現在の保有ポジション = " + str(side) + ":" + str(position_volume))
    return side

# ドテンタイミングの監視をスタート
line_num = 0
now_position = check_position()
status = ""
cur_high_max = 0
cur_low_min = 0
while True:
    try:
        now_position = check_position()
        last = (bitmex.fetch_order_book('BTC/USD')['bids'][0][0] + bitmex.fetch_order_book('BTC/USD')['bids'][0][0]) / 2
        print("MEX1現在価格：" + str(last))
        done = high_low18(last,line_num)
        line_num += 1

        if status != done[0]:
            print(done[0])
            if done[0] == "上昇ドテン" and (now_position == "Sell" or now_position == "NO POSITION"):
                order = cbo_order_market.execute('b', done[1], done[2],bitmex,LOT)
            elif done[0] == "下降ドテン" and (now_position == "Buy" or now_position == "NO POSITION"):
                order = cbo_order_market.execute('s', done[1], done[2],bitmex,LOT)
            if done[0] != "":
                status = done[0]
        orders = bitmex.fetch_open_orders()
        if (cur_low_min != 0 and cur_low_min != done[2] and now_position == 'Buy') or (cur_high_max != 0 and cur_high_max != done[1] and now_position == 'Sell') or (len(orders) == 0 and now_position != "NO POSITION"):
            print('stop価格の更新があったので、現在のorderをキャンセルして再注文')
            cbo_order_stop.update_only_stop(now_position, done[1], done[2],bitmex,LOT)

        cur_high_max = done[1]
        cur_low_min = done[2]
        time.sleep(10)
    except Exception as e:
        print("エラー:" + str(e))
        pass