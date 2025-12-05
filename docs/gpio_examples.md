# gpiozero 実装例集

このドキュメントでは、gpiozeroを使用した実践的なGPIO制御の実装例を紹介します。

## 基本例

### LED点滅

最もシンプルなLED制御の例です。

```python
#!/usr/bin/env python3
"""
LED点滅（基本）
GPIO17にLEDを接続（330Ω抵抗経由）
"""

from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    print("LED ON")
    sleep(1)

    led.off()
    print("LED OFF")
    sleep(1)
```

### より簡潔な点滅

```python
from gpiozero import LED

led = LED(17)
led.blink()  # 1秒間隔でデフォルト点滅

input("Enterで終了...")
```

### カスタム点滅パターン

```python
from gpiozero import LED

led = LED(17)

# 2秒ON、0.5秒OFFで点滅
led.blink(on_time=2, off_time=0.5)

input("Enterで終了...")
```

## ボタン制御

### ボタンでLED制御（基本）

```python
#!/usr/bin/env python3
"""
ボタンを押すとLED点灯、離すと消灯
"""

from gpiozero import Button, LED
from signal import pause

button = Button(2)
led = LED(17)

button.when_pressed = led.on
button.when_released = led.off

print("ボタンでLEDを制御します（Ctrl+Cで終了）")
pause()
```

### ボタンでLEDトグル

```python
#!/usr/bin/env python3
"""
ボタンを押すたびにLEDのON/OFFを切り替え
"""

from gpiozero import Button, LED
from signal import pause

button = Button(2)
led = LED(17)

button.when_pressed = led.toggle

print("ボタンを押すとLEDが切り替わります（Ctrl+Cで終了）")
pause()
```

### 長押し検出

```python
#!/usr/bin/env python3
"""
ボタンの長押しを検出
"""

from gpiozero import Button
from signal import pause

button = Button(2, hold_time=2)  # 2秒で長押し判定

def on_pressed():
    print("ボタンが押されました")

def on_held():
    print("ボタンが長押しされました！")

button.when_pressed = on_pressed
button.when_held = on_held

print("ボタンを押してみてください（Ctrl+Cで終了）")
pause()
```

## PWM制御

### 呼吸するLED

```python
#!/usr/bin/env python3
"""
LEDが呼吸するように明るさが変化
"""

from gpiozero import PWMLED

led = PWMLED(17)

# 1秒かけて明るく、1秒かけて暗く
led.pulse(fade_in_time=1, fade_out_time=1)

input("Enterで終了...")
```

### 手動PWM制御

```python
#!/usr/bin/env python3
"""
PWMでLEDの明るさを手動制御
"""

from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

print("明るくなります...")
for brightness in range(0, 101, 5):
    led.value = brightness / 100
    print(f"明るさ: {brightness}%")
    sleep(0.1)

sleep(1)

print("暗くなります...")
for brightness in range(100, -1, -5):
    led.value = brightness / 100
    print(f"明るさ: {brightness}%")
    sleep(0.1)

led.off()
```

### 可変抵抗でLED明るさ制御

```python
#!/usr/bin/env python3
"""
可変抵抗（ポテンショメーター）でLEDの明るさを制御
MCP3008 ADCを使用
"""

from gpiozero import MCP3008, PWMLED

pot = MCP3008(channel=0)  # 可変抵抗をCH0に接続
led = PWMLED(17)

# 可変抵抗の値でLEDの明るさを制御
led.source = pot.values

input("可変抵抗を回してください。Enterで終了...")
```

## RGB LED制御

### RGB LEDで色を変化

```python
#!/usr/bin/env python3
"""
RGB LEDで様々な色を表示
"""

from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=9, green=10, blue=11)

print("RGB LEDのカラーデモ")

colors = [
    ("赤", (1, 0, 0)),
    ("緑", (0, 1, 0)),
    ("青", (0, 0, 1)),
    ("黄", (1, 1, 0)),
    ("シアン", (0, 1, 1)),
    ("マゼンタ", (1, 0, 1)),
    ("白", (1, 1, 1)),
]

while True:
    for name, color in colors:
        print(f"{name}: {color}")
        led.color = color
        sleep(1)
```

### RGB LEDパルス

```python
#!/usr/bin/env python3
"""
RGB LEDが呼吸するように変化
"""

from gpiozero import RGBLED

led = RGBLED(red=9, green=10, blue=11)

# 赤で呼吸
led.color = (1, 0, 0)
led.pulse(fade_in_time=1, fade_out_time=1)

input("Enterで終了...")
```

## 複数LED制御

### LEDチェイサー

```python
#!/usr/bin/env python3
"""
LEDが順番に点灯するチェイサー効果
"""

from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(17, 27, 22, 23, 24)

print("LEDチェイサー（Ctrl+Cで終了）")

while True:
    for led in leds:
        led.on()
        sleep(0.2)
        led.off()
```

### ナイトライダー効果

```python
#!/usr/bin/env python3
"""
LEDが往復するナイトライダー効果
"""

from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(17, 27, 22, 23, 24)

def knight_rider():
    # 右へ
    for led in leds:
        led.on()
        sleep(0.1)
        led.off()

    # 左へ
    for led in reversed(leds):
        led.on()
        sleep(0.1)
        led.off()

print("ナイトライダー効果（Ctrl+Cで終了）")

while True:
    knight_rider()
```

### LEDバーグラフ

```python
#!/usr/bin/env python3
"""
値に応じてLEDバーグラフを表示
"""

from gpiozero import LEDBarGraph
from time import sleep

graph = LEDBarGraph(5, 6, 13, 19, 26)

print("LEDバーグラフデモ")

# 0%から100%まで
for value in range(0, 11):
    graph.value = value / 10
    print(f"値: {value * 10}%")
    sleep(0.5)

sleep(1)

# 100%から0%まで
for value in range(10, -1, -1):
    graph.value = value / 10
    print(f"値: {value * 10}%")
    sleep(0.5)
```

## トラフィックライト

### 基本的な信号機

```python
#!/usr/bin/env python3
"""
トラフィックライト（信号機）シミュレーション
"""

from gpiozero import LEDBoard
from time import sleep

lights = LEDBoard(red=17, yellow=27, green=22)

def traffic_light_sequence():
    # 赤信号
    lights.red.on()
    lights.yellow.off()
    lights.green.off()
    print("🔴 赤信号")
    sleep(3)

    # 黄信号
    lights.red.off()
    lights.yellow.on()
    lights.green.off()
    print("🟡 黄信号")
    sleep(1)

    # 青信号
    lights.red.off()
    lights.yellow.off()
    lights.green.on()
    print("🟢 青信号")
    sleep(3)

    # 青点滅
    print("🟢 青点滅")
    for _ in range(3):
        lights.green.off()
        sleep(0.3)
        lights.green.on()
        sleep(0.3)

print("トラフィックライト（Ctrl+Cで終了）")

try:
    while True:
        traffic_light_sequence()
except KeyboardInterrupt:
    lights.off()
    print("\n信号機を停止しました")
```

### 歩行者用信号機

```python
#!/usr/bin/env python3
"""
ボタンを押すと歩行者用信号が青になる
"""

from gpiozero import Button, LEDBoard
from time import sleep

button = Button(2)
car_lights = LEDBoard(red=17, yellow=27, green=22)
pedestrian_lights = LEDBoard(red=23, green=24)

def pedestrian_crossing():
    print("横断開始シーケンス")

    # 車: 青→黄
    car_lights.green.off()
    car_lights.yellow.on()
    sleep(2)

    # 車: 赤、歩行者: 青
    car_lights.yellow.off()
    car_lights.red.on()
    pedestrian_lights.red.off()
    pedestrian_lights.green.on()
    print("🚶 横断してください")
    sleep(5)

    # 歩行者: 青点滅
    for _ in range(5):
        pedestrian_lights.green.toggle()
        sleep(0.3)

    # 歩行者: 赤
    pedestrian_lights.green.off()
    pedestrian_lights.red.on()
    print("⛔ 横断禁止")
    sleep(1)

    # 車: 青
    car_lights.red.off()
    car_lights.green.on()

# 初期状態
car_lights.green.on()
pedestrian_lights.red.on()

button.when_pressed = pedestrian_crossing

print("ボタンを押すと横断できます（Ctrl+Cで終了）")

try:
    from signal import pause
    pause()
except KeyboardInterrupt:
    car_lights.off()
    pedestrian_lights.off()
```

## センサー連動

### モーションセンサーでLED点灯

```python
#!/usr/bin/env python3
"""
動きを検知するとLEDが点灯
"""

from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(4)
led = LED(17)

def motion_detected():
    print("🔴 動きを検知！LED点灯")
    led.on()

def no_motion():
    print("⚫ 動きなし。LED消灯")
    led.off()

pir.when_motion = motion_detected
pir.when_no_motion = no_motion

print("モーションセンサー監視中（Ctrl+Cで終了）")
pause()
```

### 距離センサーで警告

```python
#!/usr/bin/env python3
"""
距離に応じてLEDの点滅速度を変化
"""

from gpiozero import DistanceSensor, LED
from time import sleep

sensor = DistanceSensor(echo=18, trigger=17)
led = LED(22)

print("距離センサー駐車アシスト（Ctrl+Cで終了）")

try:
    while True:
        distance = sensor.distance * 100  # cm

        if distance < 10:
            # 非常に近い: 高速点滅
            led.blink(on_time=0.1, off_time=0.1)
            print(f"⚠️  危険！ {distance:.1f} cm")
        elif distance < 30:
            # 近い: 通常点滅
            led.blink(on_time=0.5, off_time=0.5)
            print(f"⚠️  注意 {distance:.1f} cm")
        elif distance < 50:
            # やや近い: ゆっくり点滅
            led.blink(on_time=1, off_time=1)
            print(f"ℹ️  {distance:.1f} cm")
        else:
            # 安全距離
            led.off()
            print(f"✅ 安全 {distance:.1f} cm")

        sleep(0.5)

except KeyboardInterrupt:
    led.off()
    print("\n終了")
```

### 明るさセンサーで自動点灯

```python
#!/usr/bin/env python3
"""
暗くなるとLEDが自動点灯
"""

from gpiozero import LightSensor, LED
from signal import pause

ldr = LightSensor(18)
led = LED(17)

# 暗くなったらLED点灯
ldr.when_dark = lambda: (led.on(), print("💡 暗いのでLED点灯"))
ldr.when_light = lambda: (led.off(), print("☀️  明るいのでLED消灯"))

print("明るさセンサー監視中（Ctrl+Cで終了）")
pause()
```

## ブザー制御

### アラームシステム

```python
#!/usr/bin/env python3
"""
ボタンでアラームのON/OFF、モーションセンサーで警報
"""

from gpiozero import Button, MotionSensor, Buzzer, LED
from signal import pause

button = Button(2)
pir = MotionSensor(4)
buzzer = Buzzer(17)
led = LED(27)

armed = False

def toggle_alarm():
    global armed
    armed = not armed

    if armed:
        print("🔒 アラームON")
        led.blink(on_time=0.5, off_time=0.5)
    else:
        print("🔓 アラームOFF")
        led.off()
        buzzer.off()

def intruder_detected():
    if armed:
        print("⚠️  侵入者検知！警報！")
        buzzer.beep(on_time=0.3, off_time=0.3, n=10)
        led.on()

button.when_pressed = toggle_alarm
pir.when_motion = intruder_detected

print("アラームシステム（ボタンでON/OFF、Ctrl+Cで終了）")
pause()
```

## モーター制御

### DCモーター基本制御

```python
#!/usr/bin/env python3
"""
ボタンでDCモーターを制御
"""

from gpiozero import Motor, Button
from time import sleep

motor = Motor(forward=4, backward=14)
forward_button = Button(2)
backward_button = Button(3)

def start_forward():
    print("⏩ 前進")
    motor.forward(speed=0.7)

def start_backward():
    print("⏪ 後退")
    motor.backward(speed=0.7)

def stop_motor():
    print("⏹️  停止")
    motor.stop()

forward_button.when_pressed = start_forward
forward_button.when_released = stop_motor

backward_button.when_pressed = start_backward
backward_button.when_released = stop_motor

print("ボタンでモーター制御（Ctrl+Cで終了）")

try:
    from signal import pause
    pause()
except KeyboardInterrupt:
    motor.stop()
```

### サーボモータースイープ

```python
#!/usr/bin/env python3
"""
サーボモーターを左右にスイープ
"""

from gpiozero import Servo
from time import sleep

servo = Servo(17)

print("サーボモータースイープ（Ctrl+Cで終了）")

try:
    while True:
        print("← 最小角度")
        servo.min()
        sleep(1)

        print("→ 最大角度")
        servo.max()
        sleep(1)

        print("| 中央")
        servo.mid()
        sleep(1)

except KeyboardInterrupt:
    servo.mid()
    print("\n終了")
```

## 実用的なアプリケーション

### 温度アラート（DHT22センサー）

```python
#!/usr/bin/env python3
"""
温度が閾値を超えるとLEDとブザーで警告
"""

import Adafruit_DHT
from gpiozero import LED, Buzzer
from time import sleep

sensor = Adafruit_DHT.DHT22
pin = 4
led = LED(17)
buzzer = Buzzer(27)

TEMP_THRESHOLD = 30  # 30°C以上で警告

print(f"温度監視中（閾値: {TEMP_THRESHOLD}°C、Ctrl+Cで終了）")

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if temperature is not None:
            print(f"温度: {temperature:.1f}°C, 湿度: {humidity:.1f}%")

            if temperature > TEMP_THRESHOLD:
                print(f"⚠️  警告: 温度が高すぎます！")
                led.blink(on_time=0.3, off_time=0.3)
                buzzer.beep(on_time=0.2, off_time=0.2, n=3, background=True)
            else:
                led.off()

        sleep(2)

except KeyboardInterrupt:
    led.off()
    buzzer.off()
    print("\n終了")
```

### セキュリティシステム

```python
#!/usr/bin/env python3
"""
総合セキュリティシステム
- PIRセンサー: 動き検知
- ドアセンサー（ボタン）: 開閉検知
- LED: 状態表示
- ブザー: 警報
"""

from gpiozero import MotionSensor, Button, LED, Buzzer, LEDBoard
from signal import pause
from datetime import datetime

# デバイス
pir = MotionSensor(4)
door = Button(2)  # ドアセンサー（常時閉）
arm_button = Button(3)

status_led = LEDBoard(armed=17, motion=27, door_open=22)
buzzer = Buzzer(18)

armed = False
alarm_active = False

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def toggle_arm():
    global armed, alarm_active
    armed = not armed
    alarm_active = False

    if armed:
        log("🔒 システム起動")
        status_led.armed.on()
        buzzer.beep(on_time=0.1, off_time=0.1, n=2)
    else:
        log("🔓 システム解除")
        status_led.armed.off()
        status_led.motion.off()
        buzzer.off()

def motion_detected():
    if armed:
        global alarm_active
        alarm_active = True
        log("⚠️  動き検知！")
        status_led.motion.blink(on_time=0.2, off_time=0.2)
        buzzer.beep(on_time=0.5, off_time=0.5, n=10, background=True)

def door_opened():
    if armed:
        log("🚪 ドアが開きました！")
        status_led.door_open.on()
        buzzer.beep(on_time=0.3, off_time=0.3, n=5, background=True)

def door_closed():
    log("🚪 ドアが閉まりました")
    status_led.door_open.off()

# イベント登録
arm_button.when_pressed = toggle_arm
pir.when_motion = motion_detected
door.when_released = door_opened  # ボタンが離される=ドアが開く
door.when_pressed = door_closed

log("セキュリティシステム起動")
pause()
```

## ゲーム

### 反応速度測定

```python
#!/usr/bin/env python3
"""
LEDが点灯したらボタンを押す反応速度ゲーム
"""

from gpiozero import LED, Button
from time import sleep, time
from random import uniform

led = LED(17)
button = Button(2)

print("=== 反応速度測定ゲーム ===")
print("LEDが点灯したら素早くボタンを押してください")

for round in range(5):
    print(f"\nラウンド {round + 1}/5")
    print("待機中...")

    # ランダムな時間待機
    sleep(uniform(2, 5))

    # LED点灯
    led.on()
    start_time = time()

    # ボタンが押されるまで待機
    button.wait_for_press()

    # 反応時間計算
    reaction_time = time() - start_time
    led.off()

    print(f"反応時間: {reaction_time * 1000:.0f} ms")

    sleep(1)

print("\nゲーム終了！")
```

### サイモンゲーム

```python
#!/usr/bin/env python3
"""
シンプルなサイモンゲーム（記憶ゲーム）
"""

from gpiozero import LEDBoard, Button
from time import sleep
from random import choice

leds = LEDBoard(red=17, green=27, blue=22, yellow=23)
buttons = {
    'red': Button(2),
    'green': Button(3),
    'blue': Button(4),
    'yellow': Button(14)
}

sequence = []
colors = ['red', 'green', 'blue', 'yellow']

def show_sequence():
    """シーケンスを表示"""
    sleep(1)
    for color in sequence:
        led = getattr(leds, color)
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.2)

def get_player_input():
    """プレイヤーの入力を取得"""
    for color in sequence:
        # ボタンが押されるまで待機
        pressed = None
        while pressed is None:
            for button_color, button in buttons.items():
                if button.is_pressed:
                    pressed = button_color
                    # LED点灯でフィードバック
                    led = getattr(leds, pressed)
                    led.on()
                    sleep(0.3)
                    led.off()
                    button.wait_for_release()
                    break
            sleep(0.01)

        # 正誤判定
        if pressed != color:
            return False

    return True

print("=== サイモンゲーム ===")
print("LEDの順序を記憶してボタンを押してください")

level = 1
while True:
    print(f"\nレベル {level}")

    # シーケンスに1色追加
    sequence.append(choice(colors))

    # シーケンスを表示
    show_sequence()

    # プレイヤー入力
    print("入力してください...")
    if get_player_input():
        print("正解！")
        level += 1
        sleep(1)
    else:
        print(f"不正解！スコア: {level - 1}")
        # 全LED点滅
        for _ in range(3):
            leds.on()
            sleep(0.2)
            leds.off()
            sleep(0.2)
        break
```

## まとめ

これらの例を参考に、gpiozeroを使ったGPIO制御の理解を深めてください。

### さらに学ぶには

- **[gpiozero詳細ガイド](./gpio_gpiozero_guide.md)** でAPIの詳細を確認
- **[トラブルシューティング](./gpio_troubleshooting.md)** で問題解決方法を学ぶ
- **[gpiozero公式Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html)** でさらなる例を探す
