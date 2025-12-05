#!/usr/bin/env python3
"""
LED点滅プログラム（RPi.GPIO版）
Raspberry Pi上で動作します

接続方法:
  GPIO17 ---[330Ω抵抗]--- LED(+) --- LED(-) --- GND

使用方法:
  python3 gpio_led_blink_rpigpio.py

注意:
  RPi.GPIOは古い方法ですが、最も互換性が高いです。
  Bullseye以降では gpiozero または lgpio の使用を推奨します。
"""

import RPi.GPIO as GPIO
import time
import sys

# 使用するGPIOピン番号
LED_PIN = 17

# 点滅間隔（秒）
BLINK_INTERVAL = 1.0

def main():
    """メイン処理"""
    print("=" * 60)
    print("LED点滅プログラム（RPi.GPIO版）")
    print("=" * 60)
    print(f"GPIO{LED_PIN}を使用します")
    print(f"点滅間隔: {BLINK_INTERVAL}秒")
    print("Ctrl+C で終了します\n")

    try:
        # GPIO番号の指定方法を設定（BCM番号で指定）
        GPIO.setmode(GPIO.BCM)

        # 警告を非表示（既に使用中の警告を抑制）
        GPIO.setwarnings(False)

        # GPIOピンを出力に設定
        GPIO.setup(LED_PIN, GPIO.OUT)

        print("LEDが点滅を始めます...\n")

        # 無限ループで点滅
        count = 0
        while True:
            count += 1

            # LED ON
            GPIO.output(LED_PIN, GPIO.HIGH)
            print(f"[{count:4d}] LED ON  (GPIO{LED_PIN} = HIGH)")
            time.sleep(BLINK_INTERVAL)

            # LED OFF
            GPIO.output(LED_PIN, GPIO.LOW)
            print(f"[{count:4d}] LED OFF (GPIO{LED_PIN} = LOW)")
            time.sleep(BLINK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nプログラムを終了します")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("\n【トラブルシューティング】")
        print("1. RPi.GPIOがインストールされているか確認:")
        print("   sudo apt install python3-rpi.gpio")
        print("2. GPIOピンの接続を確認")
        print("3. Raspberry Pi上で実行しているか確認")

    finally:
        # GPIOクリーンアップ
        GPIO.cleanup()
        print("GPIO cleanup完了")


if __name__ == '__main__':
    main()
