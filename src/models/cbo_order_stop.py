# coding=utf-8
import time

import ccxt

import line
def create_ifd_order(oposit_side, size, stop_price, bitmex):
    uniq_id = time.time()
    bitmex.create_order('BTC/USD', type='stop', side=oposit_side, amount=size, params={
        'stopPx': stop_price,
        'execInst': "LastPrice,ReduceOnly",
        'contingencyType': 'OneTriggersTheOther',
        'clOrdLinkID': uniq_id,
    })
    bitmex.create_order('BTC/USD', type='market', side=oposit_side, amount=size, params={
        'clOrdLinkID': uniq_id,
    })

# ストップ指値からの成行（IFDON）
def create_ifd_limit_order(oposit_side, size, stop_price, bitmex):
    uniq_id = time.time()
    if oposit_side == "sell":
        trigger_diff = 5
    else:
        trigger_diff = -5

    bitmex.create_order('BTC/USD', type='StopLimit', side=oposit_side, amount=size, params={
        'stopPx': stop_price + trigger_diff,
        'price': stop_price,
        'execInst': "LastPrice,ReduceOnly",
        'contingencyType': 'OneTriggersTheOther',
        'clOrdLinkID': uniq_id,
    })
    bitmex.create_order('BTC/USD', type='market', side=oposit_side, amount=size, params={
        'clOrdLinkID': uniq_id,
    })

def update_only_stop(judge, high_max, low_min, bitmex,lot):
    print('stop情報が更新されているので現在のstopを解消し、新規発注します。')
    orders = bitmex.fetch_open_orders()
    if len(orders) != 0:
        for o in orders:
            id = o['id']
            cancel = bitmex.cancel_order(id)
            print("未実行の注文が存在したのでキャンセル:" + cancel['status'] + ' ' + cancel['id'])
    if judge == 'Buy':
        oposit_order = create_ifd_limit_order('sell', lot, low_min, bitmex)
    elif judge == "Sell":
        oposit_order = create_ifd_limit_order('buy', lot, high_max, bitmex)
    time.sleep(10)
    body = "stop成行をupdateしました。"
    print(body)
    line.execute("[MEX_DTNstop成行更新]" + body)
