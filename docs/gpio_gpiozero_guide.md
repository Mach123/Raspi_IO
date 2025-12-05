# gpiozero 詳細ガイド

## gpiozeroとは

**gpiozero** は、Raspberry Pi財団が開発した、GPIO制御のためのPythonライブラリです。シンプルで直感的なAPIにより、初心者から上級者まで使いやすい設計になっています。

## インストール

### Raspberry Pi OS

通常、Raspberry Pi OSにはプリインストールされています。

```bash
# バージョン確認
python3 -c "import gpiozero; print(gpiozero.__version__)"
```

### インストールが必要な場合

```bash
sudo apt update
sudo apt install python3-gpiozero
```

### pipでインストール

```bash
pip3 install gpiozero
```

## 基本概念

### デバイスクラス

gpiozeroは、各電子部品を「デバイス」として抽象化します。

```python
from gpiozero import LED, Button, Motor

led = LED(17)        # LEDデバイス
button = Button(2)   # ボタンデバイス
motor = Motor(4, 5)  # モーターデバイス
```

### ピン番号

**gpiozeroは常にBCM番号を使用します。**

```python
# GPIO17を使用（物理ピン11番）
led = LED(17)
```

## 出力デバイス

### LED - 基本的なLED制御

#### 基本操作

```python
from gpiozero import LED

led = LED(17)

# ON/OFF
led.on()
led.off()

# トグル
led.toggle()

# 状態確認
if led.is_lit:
    print("LEDは点灯中")
```

#### 点滅

```python
from gpiozero import LED

led = LED(17)

# 1秒間隔で点滅（ブロッキング）
led.blink()

# カスタム間隔
led.blink(on_time=2, off_time=0.5)  # 2秒ON、0.5秒OFF

# バックグラウンドで点滅
led.blink(on_time=1, off_time=1, n=10, background=False)  # 10回点滅
```

#### コンテキストマネージャ

```python
from gpiozero import LED

with LED(17) as led:
    led.on()
    input("Enterで終了...")
# 自動的にクリーンアップ
```

### PWMLED - PWM制御LED

#### 明るさ制御

```python
from gpiozero import PWMLED

led = PWMLED(17)

# 明るさを設定（0.0 ～ 1.0）
led.value = 0.5  # 50%の明るさ

# 完全にON/OFF
led.on()    # value = 1.0
led.off()   # value = 0.0
```

#### 呼吸するLED（パルス）

```python
from gpiozero import PWMLED

led = PWMLED(17)

# 呼吸するように点滅
led.pulse(fade_in_time=2, fade_out_time=2)

# カスタマイズ
led.pulse(
    fade_in_time=1,    # 1秒かけて明るく
    fade_out_time=1,   # 1秒かけて暗く
    n=5,               # 5回繰り返し
    background=True    # バックグラウンドで実行
)
```

#### 手動でフェード

```python
from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

# 徐々に明るく
for brightness in range(0, 101, 5):
    led.value = brightness / 100
    sleep(0.05)

# 徐々に暗く
for brightness in range(100, -1, -5):
    led.value = brightness / 100
    sleep(0.05)
```

### RGBLED - RGB LED制御

```python
from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=9, green=10, blue=11)

# 基本色
led.red = 1      # 赤
led.green = 1    # 緑
led.blue = 1     # 青

# カスタムカラー（0.0 ～ 1.0）
led.color = (0, 1, 0)      # 緑
led.color = (1, 0, 1)      # マゼンタ
led.color = (0.5, 0.5, 0)  # 黄色（暗め）

# パルス（色が変化）
led.pulse(fade_in_time=1, fade_out_time=1)
```

### Buzzer - ブザー制御

```python
from gpiozero import Buzzer

buzzer = Buzzer(17)

# ON/OFF
buzzer.on()
buzzer.off()

# ビープ音
buzzer.beep(on_time=0.5, off_time=0.5, n=3)  # 3回ビープ
```

### Motor - DCモーター制御

```python
from gpiozero import Motor

motor = Motor(forward=4, backward=14)

# 前進
motor.forward(speed=0.5)  # 50%の速度で前進

# 後退
motor.backward(speed=1)   # 100%の速度で後退

# 停止
motor.stop()

# 反転
motor.reverse()
```

### Servo - サーボモーター制御

```python
from gpiozero import Servo
from time import sleep

servo = Servo(17)

# 位置指定（-1 ～ 1）
servo.min()     # -1: 最小角度
servo.mid()     #  0: 中央
servo.max()     #  1: 最大角度

# カスタム位置
servo.value = 0.5  # 中央と最大の中間

# スイープ
servo.min()
sleep(1)
servo.mid()
sleep(1)
servo.max()
```

## 入力デバイス

### Button - ボタン入力

#### 基本操作

```python
from gpiozero import Button

button = Button(2)

# ポーリング方式
while True:
    if button.is_pressed:
        print("押されています")
    else:
        print("離されています")
```

#### イベント駆動

```python
from gpiozero import Button
from signal import pause

button = Button(2)

# イベントハンドラを設定
def on_pressed():
    print("ボタンが押されました！")

def on_released():
    print("ボタンが離されました！")

button.when_pressed = on_pressed
button.when_released = on_released

pause()  # イベント待機
```

#### ラムダ式で簡潔に

```python
from gpiozero import Button
from signal import pause

button = Button(2)

button.when_pressed = lambda: print("押された！")
button.when_released = lambda: print("離された！")

pause()
```

#### プルアップ/プルダウン

```python
from gpiozero import Button

# プルアップ（デフォルト）
button = Button(2, pull_up=True)

# プルダウン
button = Button(2, pull_up=False)

# 外部プルアップ/ダウン使用時
button = Button(2, pull_up=None)
```

#### チャタリング対策

```python
from gpiozero import Button

# バウンスタイム設定（デフォルト: 10ms）
button = Button(2, bounce_time=0.05)  # 50ms
```

#### 長押し検出

```python
from gpiozero import Button
from signal import pause

button = Button(2, hold_time=2)  # 2秒で長押し判定

button.when_pressed = lambda: print("押された")
button.when_held = lambda: print("長押しされました！")

pause()
```

### MotionSensor - PIRセンサー

```python
from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(4)

pir.when_motion = lambda: print("動きを検知！")
pir.when_no_motion = lambda: print("動きなし")

pause()
```

### LightSensor - 光センサー（LDR）

```python
from gpiozero import LightSensor

ldr = LightSensor(18)

# 明るさ判定
if ldr.light_detected:
    print("明るい")
else:
    print("暗い")

# イベント駆動
ldr.when_light = lambda: print("明るくなった")
ldr.when_dark = lambda: print("暗くなった")
```

### DistanceSensor - 超音波距離センサー（HC-SR04）

```python
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=18, trigger=17)

while True:
    distance_cm = sensor.distance * 100
    print(f"距離: {distance_cm:.1f} cm")
    sleep(1)
```

## 複合デバイス

### LEDBoard - 複数LED制御

```python
from gpiozero import LEDBoard
from time import sleep

# 複数LEDをまとめて管理
leds = LEDBoard(17, 27, 22)

# 全点灯/全消灯
leds.on()
leds.off()

# 個別制御
leds[0].on()   # 最初のLED
leds[1].on()   # 2番目のLED

# 順番に点灯
for led in leds:
    led.on()
    sleep(0.5)
    led.off()
```

#### 名前付きLED

```python
from gpiozero import LEDBoard

leds = LEDBoard(red=17, yellow=27, green=22)

# 名前でアクセス
leds.red.on()
leds.yellow.on()
leds.green.on()

# 複数同時
leds.on()
leds.off()
```

### LEDBarGraph - LEDバーグラフ

```python
from gpiozero import LEDBarGraph

graph = LEDBarGraph(5, 6, 13, 19, 26)

# 値を設定（0.0 ～ 1.0）
graph.value = 0.5   # 半分点灯

# 1/5刻みで点灯
graph.value = 2/5   # 5本中2本点灯
```

### Robot - ロボット制御

```python
from gpiozero import Robot

# 左モーター: GPIO4, 14
# 右モーター: GPIO17, 18
robot = Robot(left=(4, 14), right=(17, 18))

# 前進
robot.forward(speed=0.5)

# 後退
robot.backward()

# 左回転
robot.left()

# 右回転
robot.right()

# 停止
robot.stop()
```

## デバイス間の連携

### 値の接続（values）

```python
from gpiozero import MCP3008, PWMLED

# アナログ入力（可変抵抗など）
pot = MCP3008(channel=0)

# PWM LED
led = PWMLED(17)

# 可変抵抗の値でLEDの明るさを制御
led.source = pot.values
```

### ソース/バリュー

```python
from gpiozero import Button, LED

button = Button(2)
led = LED(17)

# ボタンの状態をLEDに連動
led.source = button.values
# ボタンを押すとLED点灯、離すと消灯
```

### 複雑な連携

```python
from gpiozero import Button, LED
from gpiozero.tools import negated

button = Button(2)
led = LED(17)

# ボタンの状態を反転してLEDに連動
led.source = negated(button.values)
# ボタンを押すとLED消灯、離すと点灯
```

## イベント駆動プログラミング

### when_* イベント

gpiozeroの多くのデバイスは `when_*` 属性をサポートします。

```python
from gpiozero import Button, LED
from signal import pause

button = Button(2)
led = LED(17)

# 単純な関数
def button_pressed():
    led.toggle()

button.when_pressed = button_pressed

# またはラムダ式
button.when_pressed = lambda: led.toggle()

pause()
```

### 利用可能なイベント

| デバイス | イベント |
|---------|---------|
| Button | `when_pressed`, `when_released`, `when_held` |
| MotionSensor | `when_motion`, `when_no_motion` |
| LightSensor | `when_light`, `when_dark` |
| DistanceSensor | `when_in_range`, `when_out_of_range` |

### pause() - イベント待機

```python
from signal import pause

# プログラムを終了させずにイベントを待機
pause()
```

## ピンファクトリー

gpiozeroは、バックエンドとして異なる「ピンファクトリー」を使用できます。

### デフォルト動作

```python
from gpiozero import LED

# 自動的に利用可能なピンファクトリーを選択
led = LED(17)
```

### 明示的に指定

```python
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device, LED

# lgpioを使用
Device.pin_factory = LGPIOFactory()

led = LED(17)
```

### 利用可能なピンファクトリー

| ファクトリー | 説明 | 推奨度 |
|------------|------|--------|
| lgpio | 新しいGPIOライブラリ | ⭐⭐⭐⭐⭐ |
| RPi.GPIO | 従来のライブラリ | ⭐⭐⭐ |
| pigpio | リモートGPIO対応 | ⭐⭐⭐⭐ |
| native | gpiozero組み込み | ⭐⭐⭐ |

### 環境変数で指定

```bash
# lgpioを使用
export GPIOZERO_PIN_FACTORY=lgpio

# RPi.GPIOを使用
export GPIOZERO_PIN_FACTORY=rpigpio

# pigpioを使用
export GPIOZERO_PIN_FACTORY=pigpio
```

## ベストプラクティス

### 1. コンテキストマネージャを使用

```python
from gpiozero import LED

with LED(17) as led:
    led.blink()
    input("Enterで終了...")
# 自動的にクリーンアップ
```

### 2. イベント駆動を活用

```python
# ❌ 非推奨: ポーリング
while True:
    if button.is_pressed:
        led.on()
    sleep(0.01)

# ✅ 推奨: イベント駆動
button.when_pressed = led.on
button.when_released = led.off
pause()
```

### 3. デバイス連携を活用

```python
# ❌ 冗長
button.when_pressed = lambda: led.on()
button.when_released = lambda: led.off()

# ✅ シンプル
led.source = button.values
```

### 4. 適切なプルアップ/ダウン

```python
# ボタンはデフォルトでプルアップ
button = Button(2)  # pull_up=True

# 必要に応じて変更
button = Button(2, pull_up=False)  # プルダウン
```

### 5. チャタリング対策

```python
# bounce_timeを適切に設定
button = Button(2, bounce_time=0.05)  # 50ms
```

### 6. リソース管理

```python
# プログラム終了時に適切にクリーンアップ
import atexit
from gpiozero import LED

led = LED(17)

def cleanup():
    led.close()

atexit.register(cleanup)
```

## よくあるパターン

### ボタンでLEDトグル

```python
from gpiozero import Button, LED
from signal import pause

button = Button(2)
led = LED(17)

button.when_pressed = led.toggle

pause()
```

### トラフィックライト

```python
from gpiozero import LEDBoard
from time import sleep

lights = LEDBoard(red=17, yellow=27, green=22)

while True:
    lights.red.on()
    sleep(3)
    lights.red.off()

    lights.yellow.on()
    sleep(1)
    lights.yellow.off()

    lights.green.on()
    sleep(3)
    lights.green.off()
```

### 距離によるLED警告

```python
from gpiozero import DistanceSensor, LED
from time import sleep

sensor = DistanceSensor(echo=18, trigger=17)
led = LED(22)

while True:
    distance = sensor.distance * 100  # cm

    if distance < 10:
        led.blink(on_time=0.1, off_time=0.1)  # 高速点滅
    elif distance < 30:
        led.blink(on_time=0.5, off_time=0.5)  # 通常点滅
    else:
        led.off()

    sleep(0.1)
```

### 明るさ自動調整

```python
from gpiozero import LightSensor, PWMLED

ldr = LightSensor(18)
led = PWMLED(17)

# 暗いほどLEDを明るく
led.source = negated(ldr.values)
```

## デバッグとテスト

### ピン情報の確認

```python
from gpiozero import LED

led = LED(17)

print(f"Pin: {led.pin}")
print(f"Is active: {led.is_active}")
print(f"Is lit: {led.is_lit}")
```

### モックピン（テスト用）

```python
from gpiozero.pins.mock import MockFactory
from gpiozero import Device, LED

# モックピンファクトリーを使用
Device.pin_factory = MockFactory()

led = LED(17)
led.on()

# 状態確認（実際のハードウェアなしでテスト可能）
print(led.pin.state)  # 1 (ON)
```

## 参考資料

### 公式ドキュメント

- [gpiozero API Documentation](https://gpiozero.readthedocs.io/en/stable/api.html)
- [gpiozero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html)
- [gpiozero Source/Values](https://gpiozero.readthedocs.io/en/stable/api_boards.html#source-values)

### チュートリアル

- [Getting Started with gpiozero](https://projects.raspberrypi.org/en/projects/physical-computing)
- [gpiozero Basic Recipes](https://gpiozero.readthedocs.io/en/stable/recipes_basic.html)
- [gpiozero Advanced Recipes](https://gpiozero.readthedocs.io/en/stable/recipes_advanced.html)

## 次のステップ

- **[ハードウェア接続ガイド](./gpio_hardware_connection.md)** で安全な接続方法を学ぶ
- **[実装例集](./gpio_examples.md)** で実践的なサンプルを試す
- **[トラブルシューティング](./gpio_troubleshooting.md)** で問題解決方法を確認
