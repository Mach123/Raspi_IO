#!/usr/bin/env python3
"""
PWMでLEDの明るさを制御するプログラム（gpiozero版）
Raspberry Pi上で動作します

接続方法:
  GPIO17 ---[330Ω抵抗]--- LED(+) --- LED(-) --- GND

動作:
  LEDが呼吸するように、ゆっくり明るくなり、ゆっくり暗くなります

使用方法:
  python3 gpio_pwm_led.py
"""

from gpiozero import PWMLED
from time import sleep
import sys

# 使用するGPIOピン番号
LED_PIN = 17

# フェード時間（秒）
FADE_TIME = 2.0

def main():
    """メイン処理"""
    print("=" * 60)
    print("PWM LED制御プログラム（呼吸するLED）")
    print("=" * 60)
    print(f"GPIO{LED_PIN}を使用します")
    print(f"フェード時間: {FADE_TIME}秒")
    print("Ctrl+C で終了します\n")

    try:
        # PWM LEDオブジェクトを作成
        led = PWMLED(LED_PIN)

        print("方法1: pulse()メソッドを使用")
        print("LEDが呼吸を始めます...\n")

        # 自動的に呼吸するように点滅
        led.pulse(fade_in_time=FADE_TIME, fade_out_time=FADE_TIME)

        # 終了待機
        input("Enterキーで次のデモへ...")

        # 一旦停止
        led.off()
        print("\n方法2: 手動でPWM値を変化させる")
        sleep(1)

        # 手動でPWM制御
        while True:
            # 徐々に明るく（0% → 100%）
            print("明るくなります...")
            for brightness in range(0, 101, 5):
                led.value = brightness / 100.0
                print(f"  明るさ: {brightness}%", end='\r')
                sleep(0.1)
            print()  # 改行

            sleep(0.5)

            # 徐々に暗く（100% → 0%）
            print("暗くなります...")
            for brightness in range(100, -1, -5):
                led.value = brightness / 100.0
                print(f"  明るさ: {brightness}%", end='\r')
                sleep(0.1)
            print()  # 改行

            sleep(0.5)

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
