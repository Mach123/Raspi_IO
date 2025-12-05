# Raspberry Pi GPIO制御ガイド

Raspberry Pi Bullseye/Bookworm上でのGPIO制御プログラム集です。

## 概要

このディレクトリには、Raspberry PiのGPIOを使用してLEDやボタンを制御するサンプルプログラムが含まれています。

## プログラム一覧

### 🔴 LED制御

| ファイル名 | ライブラリ | 説明 |
|-----------|----------|------|
| `gpio_led_blink.py` | gpiozero | LED点滅（推奨） |
| `gpio_led_blink_rpigpio.py` | RPi.GPIO | LED点滅（互換性重視） |
| `gpio_pwm_led.py` | gpiozero | PWMでLEDの明るさ制御 |

### 🔵 ボタン制御

| ファイル名 | ライブラリ | 説明 |
|-----------|----------|------|
| `gpio_button_led.py` | gpiozero | ボタンでLED制御（イベント駆動） |

## 必要な環境

### ハードウェア
- Raspberry Pi（任意のモデル）
- LED（赤色推奨）
- 抵抗 330Ω
- タクトスイッチ（プッシュボタン）
- ブレッドボード
- ジャンパーワイヤ

### ソフトウェア
- Raspberry Pi OS Bullseye/Bookworm
- Python 3.7以上

## インストール

### 推奨: gpiozero（最も簡単）

```bash
# 通常はプリインストールされています
sudo apt update
sudo apt install python3-gpiozero
```

### RPi.GPIO（互換性重視）

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```

### 権限設定

```bash
# ユーザーをgpioグループに追加（必要に応じて）
sudo usermod -a -G gpio $USER

# 再ログインが必要
```

## ハードウェア接続

### LED接続

```
Raspberry Pi                        LED
┌─────────────┐
│             │
│   GPIO17 ○──┼──[330Ω抵抗]───●──┤ LED ├──●── GND
│             │                   長い足  短い足
│      GND ○──┼─────────────────────────────┘
│             │
└─────────────┘

注意:
- LEDの長い足（アノード+）を抵抗側に接続
- LEDの短い足（カソード-）をGNDに接続
- 抵抗は330Ω（オレンジ・オレンジ・茶）を使用
```

### ボタン接続

```
Raspberry Pi              ボタン
┌─────────────┐
│             │
│    GPIO2 ○──┼──┬─[ボタン]─┐
│             │  │          │
│      GND ○──┼──┴──────────┘
│             │
└─────────────┘

注意:
- 内部プルアップ抵抗を使用（外部抵抗不要）
- ボタンを押すとGPIO2がGNDに接続される
```

### GPIO番号の確認

```bash
# GPIO配置を確認
pinout

# または
gpio readall
```

## 使用方法

### 1. LED点滅（gpiozero版 - 推奨）

```bash
python3 gpio_led_blink.py
```

**機能:**
- GPIO17のLEDが1秒間隔で点滅
- Ctrl+Cで終了

### 2. LED点滅（RPi.GPIO版）

```bash
python3 gpio_led_blink_rpigpio.py
```

**機能:**
- 従来のRPi.GPIOライブラリを使用
- 動作は gpiozero版と同じ

### 3. PWMでLED制御

```bash
python3 gpio_pwm_led.py
```

**機能:**
- LEDが呼吸するように明るさが変化
- 2つの制御方法を実演
  1. `pulse()` メソッド（自動）
  2. 手動でPWM値を変化

### 4. ボタンでLED制御

```bash
python3 gpio_button_led.py
```

**機能:**
- ボタンを押すとLED点灯
- ボタンを離すとLED消灯
- イベント駆動方式

## GPIO制御ライブラリの比較

### gpiozero（推奨）

**メリット:**
- シンプルで直感的なAPI
- 高レベルで使いやすい
- Bullseye以降で推奨
- 豊富なドキュメント

**デメリット:**
- 低レベル制御には不向き

**使用例:**
```python
from gpiozero import LED
led = LED(17)
led.on()
```

### RPi.GPIO（互換性重視）

**メリット:**
- 最も広く使われている
- 多くのチュートリアルで使用
- 豊富なサンプルコード

**デメリット:**
- 将来的には非推奨の可能性
- やや複雑なAPI

**使用例:**
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
```

### lgpio（新しい方法）

**メリット:**
- 新しいカーネルAPIを使用
- root権限不要
- 将来性あり

**デメリット:**
- ドキュメントが少ない
- サンプルコードが少ない

**使用例:**
```python
import lgpio
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, 17)
lgpio.gpio_write(h, 17, 1)
```

## GPIO番号の指定方法

### BCM vs BOARD

```python
# BCM番号（GPIO番号）- 推奨
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # GPIO17

# BOARD番号（物理ピン番号）
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # 物理ピン11番 = GPIO17
```

**推奨**: BCM番号を使用（gpiozeroは常にBCM番号）

## 主要なGPIOピン配置（Raspberry Pi 4の例）

```
     3.3V  (1) (2)  5V
    GPIO2  (3) (4)  5V
    GPIO3  (5) (6)  GND
    GPIO4  (7) (8)  GPIO14
      GND  (9) (10) GPIO15
   GPIO17 (11) (12) GPIO18
   GPIO27 (13) (14) GND
   GPIO22 (15) (16) GPIO23
     3.3V (17) (18) GPIO24
   GPIO10 (19) (20) GND
    GPIO9 (21) (22) GPIO25
   GPIO11 (23) (24) GPIO8
      GND (25) (26) GPIO7
    GPIO0 (27) (28) GPIO1
    GPIO5 (29) (30) GND
    GPIO6 (31) (32) GPIO12
   GPIO13 (33) (34) GND
   GPIO19 (35) (36) GPIO16
   GPIO26 (37) (38) GPIO20
      GND (39) (40) GPIO21
```

**よく使用するピン:**
- GPIO17 (ピン11) - LED制御
- GPIO27 (ピン13) - LED制御
- GPIO22 (ピン15) - LED制御
- GPIO2 (ピン3) - ボタン入力（I2C共用）
- GPIO3 (ピン5) - ボタン入力（I2C共用）

## トラブルシューティング

### エラー: ModuleNotFoundError

**症状:**
```
ModuleNotFoundError: No module named 'gpiozero'
```

**対処法:**
```bash
sudo apt install python3-gpiozero
```

### エラー: 権限エラー

**症状:**
```
PermissionError: [Errno 13] Permission denied: '/dev/gpiomem'
```

**対処法:**
```bash
# ユーザーをgpioグループに追加
sudo usermod -a -G gpio $USER

# 再ログイン
logout
```

### 警告: GPIO already in use

**症状:**
```
RuntimeWarning: This channel is already in use
```

**対処法:**
```python
# 警告を無視（RPi.GPIOの場合）
GPIO.setwarnings(False)

# または、GPIOクリーンアップ
GPIO.cleanup()
```

### LEDが点灯しない

**確認事項:**
1. LEDの向きは正しいか（長い足がGPIO側）
2. 抵抗は接続されているか
3. GNDに接続されているか
4. GPIO番号は正しいか
5. プログラムはエラーなく動作しているか

### ボタンが反応しない

**確認事項:**
1. ボタンの接続は正しいか
2. GNDに接続されているか
3. GPIO番号は正しいか
4. 内部プルアップが有効か（gpiozeroは自動）

## 安全上の注意

### ⚠️ 重要な注意事項

1. **電圧に注意**
   - GPIOピンは3.3Vです（5Vではありません）
   - 5Vをかけると破損します

2. **電流制限**
   - 1ピンあたり最大16mA
   - 全ピン合計で最大50mA
   - **必ず抵抗を使用してください**

3. **ショートに注意**
   - GPIO同士をショートさせない
   - GNDと3.3V/5Vをショートさせない

4. **静電気対策**
   - 触る前に金属に触れて放電
   - 乾燥した環境では特に注意

## 参考資料

### 公式ドキュメント

- [gpiozero Documentation](https://gpiozero.readthedocs.io/)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)

### チュートリアル

- [Raspberry Pi GPIO入門](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header)
- [gpiozero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html)

### オンラインツール

- [GPIO Pinout (Interactive)](https://pinout.xyz/)
- [GPIO Simulator](https://gpiozero.readthedocs.io/en/stable/remote_gpio.html)

## 発展的な使い方

### 複数のLEDを制御

```python
from gpiozero import LED
from time import sleep

leds = [LED(17), LED(27), LED(22)]

# 順番に点灯
for led in leds:
    led.on()
    sleep(0.5)
    led.off()
```

### PWMでサーボモーター制御

```python
from gpiozero import Servo
from time import sleep

servo = Servo(17)

servo.min()   # 最小角度
sleep(1)
servo.mid()   # 中央
sleep(1)
servo.max()   # 最大角度
```

### 距離センサー（HC-SR04）

```python
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=17, trigger=4)

while True:
    print(f'Distance: {sensor.distance * 100:.1f} cm')
    sleep(1)
```

## ライセンス

このサンプルコードは教育・研究目的で自由に使用できます。

## 作成情報

- **作成日:** 2025-12-05
- **対象環境:** Raspberry Pi OS Bullseye/Bookworm
- **推奨ライブラリ:** gpiozero

---

**Note:** これらのプログラムは実際のRaspberry Piハードウェア上でのみ動作します。
