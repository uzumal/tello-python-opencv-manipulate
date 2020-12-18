#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello            # tello.pyをインポート
import time           # time.sleepを使いたいので
from kbhit import *   # kbhit.pyをインポート
import socket

HOST = '172.20.72.28'
# HOST = '172.20.71.48'
# HOST = '192.168.10.100'
# HOST = '127.0.0.1'
PORT = 4602

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = "null"

# メイン関数本体
def main():
    # kbhitのためのおまじない
    atexit.register(set_normal_term)
    set_curses_term()

    global name
    pre_name = "null"

    # Telloクラスを使って，droneというインスタンス(実体)を作る
    drone = tello.Tello('', 8889) 

    current_time = time.time()  # 現在時刻の保存変数
    pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数

    #Ctrl+cが押されるまでループ
    try:
        while True:
            name = "null"

            # 5秒おきに'command'を送って、Telloが自動終了しないようにする
            current_time = time.time()  # 現在時刻を取得
            # if current_time - pre_time > 1.0 :  # 前回時刻から5秒以上経過しているか？
            pre_name = drone.send_command('attitude?')   # 'command'送信
            if len(pre_name) > 13:
                name = pre_name
            time.sleep(0.3) # 適度にウェイトを入れてCPU負荷を下げる
            pre_name = drone.send_command('command')   # 'command'送信
            if len(pre_name) > 13:
                name = pre_name
            pre_time = current_time         # 前回時刻を更新

            if kbhit():     # 何かキーが押されるのを待つ
                key = getch()   # 1文字取得
                # キーに応じた処理
                if key == 't':      # 離陸
                    name = 'takeoff'
                    drone.takeoff()
                elif key == 'l':    # 着陸
                    name = 'land'
                    drone.land()
                elif key == 'w':    # 前進
                    name = 'forward'
                    drone.move_forward(0.3) # 0.3mなので30cm動く
                    # print("speed:" + str(drone.get_speed()))
                elif key == 's':    # 後進
                    name = 'backward'
                    drone.move_backward(0.3)
                elif key == 'a':    # 左移動
                    name = 'left'
                    drone.move_left(0.3)
                elif key == 'd':    # 右移動
                    name = 'right'
                    drone.move_right(0.3)
                elif key == 'q':    # 左旋回
                    name = 'rotate_left'
                    drone.rotate_ccw(20)    # 20度旋回
                elif key == 'e':    # 右旋回
                    name = 'rotate_right'
                    drone.rotate_cw(20)
                elif key == 'r':    # 上昇
                    name = 'up'
                    drone.move_up(0.3)
                elif key == 'f':    # 下降
                    name = 'down'
                    drone.move_down(0.3)
                elif key == 'n':    #stop
                    client.close()
            
            #UDP通信
            result = str(name)
            print(name)
            # print(result)
            client.sendto(result.encode('utf-8'),(HOST,PORT))

            # time.sleep(0.3) # 適度にウェイトを入れてCPU負荷を下げる
            

    except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
        print( "SIGINTを検知" )

    # telloクラスを削除
    del drone

def check():
    global name
    print(name)
    return name

# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると"__main__"は入らないので，実行かimportかを判断できる．
    main()    # メイン関数を実行
