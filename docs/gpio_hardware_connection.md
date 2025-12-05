# GPIO ハードウェア接続ガイド

## 安全な接続のための基礎知識

### ⚠️ 重要な注意事項

1. **GPIOは3.3V動作**
   - 絶対に5Vを接続しない
   - 3.3V以上の電圧で破損

2. **電流制限を守る**
   - 1ピンあたり最大16mA
   - 全ピン合計で最大50mA

3. **必ず抵抗を使用**
   - LEDには必ず抵抗を直列接続
   - 推奨: 330Ω ～ 1kΩ

4. **ショートさせない**
   - GPIO同士
   - GPIOとGND/電源

5. **静電気対策**
   - 触る前に金属に触れて放電

## 必要な部品

### 基本セット

| 部品 | 数量 | 説明 |
|------|------|------|
| Raspberry Pi | 1 | 任意のモデル |
| ブレッドボード | 1 | 半型または全型 |
| ジャンパーワイヤ（オス-メス） | 10本 | Raspberry Pi接続用 |
| ジャンパーワイヤ（オス-オス） | 20本 | ブレッドボード用 |

### LED制御用

| 部品 | 数量 | 説明 |
|------|------|------|
| LED（赤、緑、黄など） | 5個 | 3mm または 5mm |
| 抵抗 330Ω | 5個 | カラーコード: オレンジ・オレンジ・茶 |
| 抵抗 1kΩ | 5個 | カラーコード: 茶・黒・赤 |

### ボタン入力用

| 部品 | 数量 | 説明 |
|------|------|------|
| タクトスイッチ | 3個 | プッシュボタン |
| 抵抗 10kΩ（オプション） | 3個 | 外部プルアップ/ダウン用 |

### その他

| 部品 | 数量 | 説明 |
|------|------|------|
| ブザー | 1個 | アクティブまたはパッシブ |
| PIRセンサー | 1個 | HC-SR501など |
| 超音波センサー | 1個 | HC-SR04 |

## 抵抗値の選び方

### LED用抵抗

**計算式:**
```
抵抗値 = (電源電圧 - LED順方向電圧) / LED電流

例: (3.3V - 2.0V) / 0.01A = 130Ω
```

**推奨値:**

| LED色 | 順方向電圧 | 推奨抵抗 | 実際の電流 |
|-------|-----------|---------|-----------|
| 赤 | 1.8～2.0V | 330Ω | 約4mA |
| 黄/緑 | 2.0～2.2V | 330Ω | 約3～4mA |
| 青/白 | 3.0～3.3V | 330Ω | 約1mA |

**安全な抵抗値:**
- **330Ω**: 最も一般的、安全
- **470Ω**: さらに安全、やや暗い
- **1kΩ**: 非常に安全、かなり暗い

### プルアップ/ダウン抵抗

| 用途 | 推奨値 |
|------|--------|
| ボタンプルアップ | 10kΩ |
| ボタンプルダウン | 10kΩ |
| I2Cプルアップ | 4.7kΩ |

**注意:** gpiozeroでは内部プルアップ/ダウン抵抗を使用できるため、通常は外部抵抗不要。

## LED接続

### 基本的なLED接続

```
Raspberry Pi                           LED
┌──────────────┐
│              │
│   GPIO17 ○───┼───[330Ω]───┬──●──┤ LED ├──●─┐
│              │             │     長い足 短い足│
│      GND ○───┼─────────────┴────────────────┘
│              │
└──────────────┘
```

**接続手順:**

1. **LEDの向きを確認**
   - 長い足（アノード+）を抵抗側に
   - 短い足（カソード-）をGND側に

2. **抵抗を接続**
   - GPIO17と330Ω抵抗を接続
   - 抵抗とLEDの長い足（+）を接続

3. **GNDに接続**
   - LEDの短い足（-）をGNDに接続

**gpiozeroコード:**
```python
from gpiozero import LED

led = LED(17)
led.on()
```

### 複数LED接続

```
Raspberry Pi
┌──────────────┐
│   GPIO17 ○───┼───[330Ω]───LED1─── GND
│   GPIO27 ○───┼───[330Ω]───LED2─── GND
│   GPIO22 ○───┼───[330Ω]───LED3─── GND
│              │
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import LEDBoard

leds = LEDBoard(17, 27, 22)
leds.on()
```

### RGB LED接続

#### 共通カソード（-）型

```
Raspberry Pi                    RGB LED
┌──────────────┐
│    GPIO9 ○───┼───[330Ω]───R(赤)  ───┐
│   GPIO10 ○───┼───[330Ω]───G(緑)  ───┤
│   GPIO11 ○───┼───[330Ω]───B(青)  ───┤
│              │                      │
│      GND ○───┼──────────────────────┘
│              │        共通カソード(-)
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import RGBLED

led = RGBLED(red=9, green=10, blue=11)
led.color = (1, 0, 0)  # 赤
```

#### 共通アノード（+）型

```
Raspberry Pi                    RGB LED
┌──────────────┐
│   3.3V   ○───┼──────────────────────┐
│              │         共通アノード(+)│
│    GPIO9 ○───┼───[330Ω]───R(赤)  ───┤
│   GPIO10 ○───┼───[330Ω]───G(緑)  ───┤
│   GPIO11 ○───┼───[330Ω]───B(青)  ───┘
│              │
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import RGBLED

# 共通アノード型は active_high=False
led = RGBLED(red=9, green=10, blue=11, active_high=False)
led.color = (1, 0, 0)  # 赤
```

## ボタン接続

### 内部プルアップ使用（推奨）

```
Raspberry Pi
┌──────────────┐
│    GPIO2 ○───┼───┬─[ボタン]─┐
│              │   │          │
│      GND ○───┼───┴──────────┘
│              │
└──────────────┘
```

**説明:**
- ボタンを押すとGPIO2がGNDに接続
- 内部プルアップ抵抗により、通常時はHIGH
- 押下時はLOW

**gpiozeroコード:**
```python
from gpiozero import Button

# デフォルトで内部プルアップ使用
button = Button(2)

if button.is_pressed:
    print("押されています")
```

### 内部プルダウン使用

```
Raspberry Pi
┌──────────────┐
│   3.3V   ○───┼───┬─[ボタン]─┐
│              │   │          │
│    GPIO2 ○───┼───┴──────────┘
│              │
└──────────────┘
```

**説明:**
- ボタンを押すとGPIO2が3.3Vに接続
- 内部プルダウン抵抗により、通常時はLOW
- 押下時はHIGH

**gpiozeroコード:**
```python
from gpiozero import Button

# 内部プルダウン使用
button = Button(2, pull_up=False)

if button.is_pressed:
    print("押されています")
```

### 外部プルアップ抵抗使用

```
Raspberry Pi
┌──────────────┐
│   3.3V   ○───┼───[10kΩ]───┬─────GPIO2
│              │             │
│              │         [ボタン]
│              │             │
│      GND ○───┼─────────────┘
│              │
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import Button

# 外部プルアップ使用時
button = Button(2, pull_up=None)
```

## センサー接続

### PIRモーションセンサー（HC-SR501）

```
Raspberry Pi              PIR Sensor
┌──────────────┐         ┌─────────┐
│      5V  ○───┼─────────┤ VCC     │
│              │         │         │
│    GPIO4 ○───┼─────────┤ OUT     │
│              │         │         │
│      GND ○───┼─────────┤ GND     │
│              │         └─────────┘
└──────────────┘
```

**注意:**
- PIRセンサーは5V電源が必要
- 出力は3.3V互換（GPIO直結可能）

**gpiozeroコード:**
```python
from gpiozero import MotionSensor

pir = MotionSensor(4)

pir.when_motion = lambda: print("動きを検知！")
```

### 超音波距離センサー（HC-SR04）

```
Raspberry Pi              HC-SR04
┌──────────────┐         ┌─────────┐
│      5V  ○───┼─────────┤ VCC     │
│              │         │         │
│   GPIO17 ○───┼─────────┤ Trig    │
│              │         │         │
│              │    ┌────┤ Echo    │
│   GPIO18 ○───┼────┤1kΩ │         │
│              │    │    │         │
│      GND ○───┼────┴────┤ GND     │
│              │         └─────────┘
└──────────────┘
```

**注意:**
- Echo出力は5V→分圧が必要
- または5V tolerant GPIOを使用

**簡易接続（5V tolerant GPIOの場合）:**
```
Raspberry Pi              HC-SR04
┌──────────────┐         ┌─────────┐
│      5V  ○───┼─────────┤ VCC     │
│   GPIO17 ○───┼─────────┤ Trig    │
│   GPIO18 ○───┼─────────┤ Echo    │
│      GND ○───┼─────────┤ GND     │
└──────────────┘         └─────────┘
```

**gpiozeroコード:**
```python
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=18, trigger=17)

print(f"距離: {sensor.distance * 100:.1f} cm")
```

### LDR（光センサー）

LDRはアナログセンサーなので、ADC（MCP3008等）が必要です。

```
                          MCP3008
Raspberry Pi             ┌──────┐
┌──────────────┐         │      │
│   3.3V   ○───┼────┬────┤VDD   │
│              │    │    │      │
│              │  [LDR]  │CH0   │
│              │    │    │      │
│              │  [10kΩ] │      │
│              │    │    │      │
│      GND ○───┼────┴────┤VSS   │
│              │         │      │
│   GPIO10 ○───┼─────────┤MOSI  │
│    GPIO9 ○───┼─────────┤MISO  │
│   GPIO11 ○───┼─────────┤SCLK  │
│    GPIO8 ○───┼─────────┤CS/SS │
│              │         └──────┘
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import MCP3008, LightSensor

# MCP3008のチャンネル0にLDR接続
ldr = LightSensor(18)  # 簡易版

# または直接MCP3008を使用
pot = MCP3008(channel=0)
print(pot.value)
```

## モーター接続

### DCモーター（L293Dモータードライバ使用）

```
Raspberry Pi              L293D              Motor
┌──────────────┐         ┌─────┐
│    GPIO4 ○───┼─────────┤IN1  │
│              │         │     ├───┐
│   GPIO14 ○───┼─────────┤IN2  │   │    ┌───┐
│              │         │     │   ├────┤ M │
│      5V  ○───┼─────────┤VCC1 │   │    └───┘
│              │         │     ├───┘
│              │  外部12V┤VCC2 │
│              │         │     │
│      GND ○───┼─────────┤GND  │
│              │         └─────┘
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import Motor

motor = Motor(forward=4, backward=14)

motor.forward(speed=0.5)  # 50%で前進
motor.backward()          # 後退
motor.stop()              # 停止
```

### サーボモーター

```
Raspberry Pi              Servo
┌──────────────┐         ┌─────┐
│      5V  ○───┼─────────┤赤    │
│              │         │      │
│   GPIO17 ○───┼─────────┤橙    │
│              │         │(信号)│
│      GND ○───┼─────────┤茶    │
│              │         └─────┘
└──────────────┘
```

**注意:**
- サーボは5V電源が必要
- 大型サーボは外部電源推奨

**gpiozeroコード:**
```python
from gpiozero import Servo

servo = Servo(17)

servo.min()   # 最小角度
servo.mid()   # 中央
servo.max()   # 最大角度
```

## ブザー接続

### パッシブブザー

```
Raspberry Pi              Buzzer
┌──────────────┐
│   GPIO17 ○───┼─────────┬──●──[Buzzer]──●─┐
│              │         │      (+)     (-) │
│      GND ○───┼─────────┴─────────────────┘
│              │
└──────────────┘
```

**gpiozeroコード:**
```python
from gpiozero import Buzzer

buzzer = Buzzer(17)

buzzer.on()
buzzer.off()
buzzer.beep(on_time=0.5, off_time=0.5, n=3)  # 3回ビープ
```

### アクティブブザー（推奨）

アクティブブザーはパッシブと同じ接続ですが、ON/OFFのみで音が鳴ります。

```python
from gpiozero import Buzzer

buzzer = Buzzer(17)
buzzer.on()   # 音が鳴る
buzzer.off()  # 停止
```

## トラブルシューティング

### LEDが点灯しない

**確認事項:**

1. **LEDの向き**
   - 長い足（+）がGPIO側
   - 短い足（-）がGND側

2. **抵抗の接続**
   - 330Ω抵抗が直列に接続されているか
   - 抵抗値が適切か（330Ω～1kΩ）

3. **電源**
   - GNDに正しく接続されているか
   - GPIOピンから電圧が出力されているか

4. **コード**
   - `led.on()` が実行されているか
   - GPIO番号は正しいか

**デバッグ:**
```python
from gpiozero import LED

led = LED(17)
led.on()

print(f"LED is lit: {led.is_lit}")
print(f"Pin value: {led.pin.state}")
```

### ボタンが反応しない

**確認事項:**

1. **接続**
   - ボタンがGPIOとGNDに接続されているか
   - 接続が緩くないか

2. **プルアップ/ダウン**
   - 内部プルアップが有効か（デフォルトで有効）
   - 外部抵抗使用時は `pull_up=None`

3. **ボタンの動作**
   - ボタン自体が壊れていないか
   - 導通チェック

**デバッグ:**
```python
from gpiozero import Button

button = Button(2)

while True:
    print(f"Pressed: {button.is_pressed}, Value: {button.pin.state}")
    sleep(0.1)
```

### センサーが動作しない

**PIRセンサー:**
- 電源は5Vか
- 調整ダイヤルを確認（感度、遅延時間）
- ウォームアップ時間（30～60秒）が必要

**超音波センサー:**
- 電源は5Vか
- Echo信号の電圧レベルは適切か
- 測定距離は範囲内か（2cm～4m）

## 安全な配線のチェックリスト

### 接続前

- [ ] 電源をOFFにする
- [ ] 静電気を放電する
- [ ] 配線図を確認する
- [ ] 部品の向きを確認する

### 接続中

- [ ] 5VをGPIOに接続していないか
- [ ] ショートしていないか
- [ ] 抵抗は適切か
- [ ] LEDの向きは正しいか

### 接続後

- [ ] 配線を再確認する
- [ ] ショートがないか確認
- [ ] 電源投入前に最終確認
- [ ] 電源投入後、異常な発熱がないか

## 参考資料

- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [gpiozero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html)
- [GPIO Zero Pin Recipes](https://gpiozero.readthedocs.io/en/stable/recipes_basic.html)

## 次のステップ

- **[gpiozero詳細ガイド](./gpio_gpiozero_guide.md)** でプログラミング方法を学ぶ
- **[実装例集](./gpio_examples.md)** で実践的なサンプルを試す
