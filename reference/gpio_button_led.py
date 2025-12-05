#!/usr/bin/env python3
"""
ボタンでLEDを制御するプログラム（gpiozero版）
Raspberry Pi上で動作します

接続方法:
  【LED】
  GPIO17 ---[330Ω抵抗]--- LED(+) --- LED(-) --- GND

  【ボタン】
  GPIO2 ---[ボタン]--- GND
  （内部プルアップ抵抗を使用）

動作:
  - ボタンを押すとLEDが点灯
  - ボタンを離すとLEDが消灯

使用方法:
  python3 gpio_button_led.py
"""

from gpiozero import LED, Button
from signal import pause
import sys

# 使用するGPIOピン番号
LED_PIN = 17
BUTTON_PIN = 2

def main():
    """メイン処理"""
    print("=" * 60)
    print("ボタンでLED制御プログラム")
    print("=" * 60)
    print(f"LED    : GPIO{LED_PIN}")
    print(f"ボタン : GPIO{BUTTON_PIN}")
    print("Ctrl+C で終了します\n")

    try:
        # LED と ボタンのオブジェクトを作成
        led = LED(LED_PIN)
        button = Button(BUTTON_PIN)

        # イベントハンドラを設定
        def on_button_pressed():
            """ボタンが押された時"""
            led.on()
            print("ボタン: 押された → LED ON")

        def on_button_released():
            """ボタンが離された時"""
            led.off()
            print("ボタン: 離された → LED OFF")

        # イベントにハンドラを登録
        button.when_pressed = on_button_pressed
        button.when_released = on_button_released

        print("準備完了。ボタンを押してください...\n")

        # イベント待機（無限ループ）
        pause()

    except KeyboardInterrupt:
        print("\n\nプログラムを終了します")
        led.off()
        sys.exit(0)

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("\n【トラブルシューティング】")
        print("1. gpiozeroがインストールされているか確認:")
        print("   sudo apt install python3-gpiozero")
        print("2. GPIOピンの接続を確認")
        print("3. Raspberry Pi上で実行しているか確認")
        sys.exit(1)


if __name__ == '__main__':
    main()
