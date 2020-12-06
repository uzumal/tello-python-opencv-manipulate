#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello            # tello.pyをインポート
import time           # time.sleepを使いたいので
from kbhit import *   # kbhit.pyをインポート
import socket

HOST = '172.20.70.39'
PORT = 4602

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = "null"
# メイン関数本体
def main():
    # kbhitのためのおまじない
    atexit.register(set_normal_term)
    set_curses_term()

    global name

    # Telloクラスを使って，droneというインスタンス(実体)を作る
    drone = tello.Tello('', 8889) 

    current_time = time.time()  # 現在時刻の保存変数
    pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数

    #Ctrl+cが押されるまでループ
    try:
        while True:
            name = "null"
            # frame = drone.read()
            # if frame is None or frame.size == 0:    # 中身がおかしかったら無視
            #     continue 
            # # (B)ここから画像処理
            # image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)      # OpenCV用のカラー並びに変換する
            # small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを半分に変更
            # # (X)ウィンドウに表示
            # cv2.imshow('OpenCV Window', small_image)    # ウィンドウに表示するイメージを変えれば色々表示できる

            #　キー操作
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
                elif key == 'b':
                    drone.send_command("speed?")
                elif key == 'n':
                    drone.send_command("attitude?")
            #UDP通信
            result = str(name)
            print(result)
            client.sendto(result.encode('utf-8'),(HOST,PORT))


            time.sleep(0.3) # 適度にウェイトを入れてCPU負荷を下げる

            # 5秒おきに'command'を送って、Telloが自動終了しないようにする
            current_time = time.time()  # 現在時刻を取得
            if current_time - pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか？
                drone.send_command('command')   # 'command'送信
                pre_time = current_time         # 前回時刻を更新

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
