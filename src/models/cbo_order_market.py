# coding=utf-8
import time

import ccxt

import line


def execute(judge, high_max, low_min,bitmex,lot):
    # ストップ成行からの成行（IFDON）
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

    # NO.1：成り行き注文の開始（スクリプトの引数によって動作を変化）
    def order_and_stop(judge, high_max, low_min):
        print('orderとstopと次回のドテンをポジションをオーダーします')
        if judge == 'b':
            order = market('buy', lot)
            oposit_order = create_ifd_limit_order('sell', lot, low_min, bitmex)
        elif judge == "s":
            order = market('sell', lot)
            oposit_order = create_ifd_limit_order('buy', lot, high_max, bitmex)
        time.sleep(10)
        body = order['info']['ordType'] + ' ' + order['info']['side'] + ': ' + str(
            order['info']['orderQty']) + ' @ ' + str(order['info']['price']) + ' / ' + order[
                   'id'] + "参考値 ： 高値 => " + str(high_max) + " 安値 => " + str(low_min)
        print(body)
        line.execute("[MEX_DTN売買実行]" + body)

    def only_stop(judge, high_max, low_min):
        print('stopと次回のドテンをポジションをオーダーします。stop情報が更新されている場合はpriceを更新')
        if judge == 'b':
            oposit_order = create_ifd_limit_order('sell', lot, low_min, bitmex)
        elif judge == "s":
            oposit_order = create_ifd_limit_order('buy', lot, high_max, bitmex)
        time.sleep(10)
        body = "stop成行"
        print(body)
        line.execute("[MEX_DTNstop成行実行]" + body)

        # 成行

    def market(side, size):
        return bitmex.create_order('BTC/USD', type='market', side=side, amount=size)

    # NO.0：リトライ処理の際に一度現在のポジションを整理する
    orders = bitmex.fetch_open_orders()
    if len(orders) != 0:
        for o in orders:
            id = o['id']
            cancel = bitmex.cancel_order(id)
            print("未実行の注文が存在したのでキャンセル:" + cancel['status'] + ' ' + cancel['id'])
    positions = bitmex.private_get_position()
    if positions[0]['currentQty'] == 0:
        print('ポジション保有なしなので新規発注します')
        order_and_stop(judge, high_max, low_min)
        print('stopが入っているか確認して、発注')
        orders = bitmex.fetch_open_orders()
        if len(orders) == 0:
            only_stop(judge, high_max, low_min)

    elif (positions[0]['currentQty'] > 0 and judge == 'b') or (positions[0]['currentQty'] < 0 and judge == 's'):
        print('すでに狙っていたポジションがあります')
        print('stopが入っているか確認して、発注')
        orders = bitmex.fetch_open_orders()
        if len(orders) == 0:
            only_stop(judge, high_max, low_min)

    elif len(orders) == 0 and ((positions[0]['currentQty'] > 0 and judge == 's') or (positions[0]['currentQty'] < 0 and judge == 'b')):
        print('異常事態発生。一旦ポジションを清算して、再発注')
        if positions[0]['currentQty'] > 0:
            market('sell',lot)
        elif positions[0]['currentQty'] < 0:
            market('buy', lot)
        print('ポジション保有なしなので新規発注します')
        order_and_stop(judge, high_max, low_min)
        print('stopが入っているか確認して、発注')
        orders = bitmex.fetch_open_orders()
        if len(orders) == 0:
            only_stop(judge, high_max, low_min)
