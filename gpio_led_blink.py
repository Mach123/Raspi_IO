#!/usr/bin/env python3
"""
LED点滅プログラム（gpiozero版）
Raspberry Pi上で動作します

接続方法:
  GPIO17 ---[330Ω抵抗]--- LED(+) --- LED(-) --- GND

使用方法:
  python3 gpio_led_blink.py
"""

from gpiozero import LED
from time import sleep
import sys

# 使用するGPIOピン番号
LED_PIN = 17

# 点滅間隔（秒）
BLINK_INTERVAL = 1.0

def main():
    """メイン処理"""
    print("=" * 60)
    print("LED点滅プログラム")
    print("=" * 60)
    print(f"GPIO{LED_PIN}を使用します")
    print(f"点滅間隔: {BLINK_INTERVAL}秒")
    print("Ctrl+C で終了します\n")

    try:
        # LEDオブジェクトを作成
        led = LED(LED_PIN)

        # 無限ループで点滅
        while True:
            led.on()
            print(f"LED ON  (GPIO{LED_PIN})")
            sleep(BLINK_INTERVAL)

            led.off()
            print(f"LED OFF (GPIO{LED_PIN})")
            sleep(BLINK_INTERVAL)

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
