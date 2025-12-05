# Raspberry Pi GPIO制御 - 概要

## GPIOとは

**GPIO (General Purpose Input/Output)** は、Raspberry Piの40ピンヘッダーに配置された汎用入出力ピンです。これらのピンを使用して、LEDの点灯、ボタンの読み取り、センサーからのデータ取得など、様々な電子部品を制御できます。

## このガイドについて

このガイドでは、**gpiozero** ライブラリを使用したGPIO制御を推奨します。

### なぜgpiozeroを推奨するのか

1. **シンプルで直感的**
   - 初心者にも理解しやすいAPI
   - 少ないコードで実現可能

2. **公式推奨**
   - Raspberry Pi財団が推奨
   - Raspberry Pi OSにプリインストール

3. **豊富な機能**
   - LED、ボタン、センサーなど多数の部品をサポート
   - イベント駆動プログラミングが容易

4. **良いドキュメント**
   - 公式ドキュメントが充実
   - 多数のサンプルコード

5. **将来性**
   - 継続的にメンテナンスされている
   - 新しいRaspberry Pi OSに対応

## GPIO制御ライブラリの比較

| ライブラリ | 推奨度 | 特徴 | 適用場面 |
|-----------|--------|------|---------|
| **gpiozero** | ⭐⭐⭐⭐⭐ | シンプル、高レベルAPI | **推奨：すべての用途** |
| RPi.GPIO | ⭐⭐⭐ | 広く使用、互換性高 | 既存コードの保守 |
| lgpio | ⭐⭐⭐⭐ | 新しいAPI、高速 | 高度な制御 |
| pigpio | ⭐⭐⭐ | 高精度PWM、リモート制御 | 精密な制御が必要な場合 |

### 詳細比較

#### gpiozero（本ガイドの推奨）

**メリット:**
- 最もシンプルで直感的
- 豊富な組み込みデバイスクラス
- イベント駆動プログラミングが容易
- 公式ドキュメントが充実
- Raspberry Pi OSに標準搭載

**デメリット:**
- 非常に低レベルな制御には不向き

**コード例:**
```python
from gpiozero import LED
led = LED(17)
led.on()
```

#### RPi.GPIO（参考）

**メリット:**
- 最も広く使われている
- 豊富なチュートリアル
- 既存コードとの互換性

**デメリット:**
- やや複雑なAPI
- 将来的に非推奨の可能性

**コード例:**
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
```

#### lgpio（参考）

**メリット:**
- 新しいLinux GPIOインターフェース使用
- root権限不要
- 高速動作

**デメリット:**
- ドキュメントが少ない
- 学習曲線が急

**コード例:**
```python
import lgpio
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, 17)
lgpio.gpio_write(h, 17, 1)
```

## GPIOピン配置

### Raspberry Pi 40ピンヘッダー

```
     3.3V  (1) (2)  5V
    GPIO2  (3) (4)  5V
    GPIO3  (5) (6)  GND
    GPIO4  (7) (8)  GPIO14 (TXD)
      GND  (9) (10) GPIO15 (RXD)
   GPIO17 (11) (12) GPIO18 (PWM0)
   GPIO27 (13) (14) GND
   GPIO22 (15) (16) GPIO23
     3.3V (17) (18) GPIO24
   GPIO10 (19) (20) GND
    GPIO9 (21) (22) GPIO25
   GPIO11 (23) (24) GPIO8
      GND (25) (26) GPIO7
    GPIO0 (27) (28) GPIO1
    GPIO5 (29) (30) GND
    GPIO6 (31) (32) GPIO12 (PWM0)
   GPIO13 (33) (34) GND
   GPIO19 (35) (36) GPIO16
   GPIO26 (37) (38) GPIO20
      GND (39) (40) GPIO21
```

### ピンの種類

| 種類 | 説明 | ピン数 |
|------|------|--------|
| **GPIO** | プログラム可能な汎用I/O | 26本 |
| **3.3V電源** | 3.3V出力（最大50mA） | 2本 |
| **5V電源** | 5V出力（電源による） | 2本 |
| **GND** | グランド（0V） | 8本 |
| **特殊機能** | I2C, SPI, UART等 | 複数 |

### よく使用するGPIOピン

**推奨されるGPIOピン（一般的な用途）:**

- **GPIO17** (ピン11) - LED、リレー等
- **GPIO27** (ピン13) - LED、リレー等
- **GPIO22** (ピン15) - LED、リレー等
- **GPIO23** (ピン16) - LED、リレー等
- **GPIO24** (ピン18) - LED、リレー等
- **GPIO25** (ピン22) - LED、リレー等

**注意が必要なピン:**

- **GPIO2, GPIO3** (ピン3, 5) - I2Cバスと共用、内蔵プルアップあり
- **GPIO14, GPIO15** (ピン8, 10) - UART (シリアル通信)と共用
- **GPIO18, GPIO12, GPIO13** - ハードウェアPWM対応

## GPIO番号の指定方法

gpiozeroでは、常に**BCM番号（GPIO番号）**を使用します。

```python
from gpiozero import LED

# GPIO17を使用（BCM番号）
led = LED(17)  # 物理ピン11番に対応
```

### BCM vs BOARD

| 方式 | 説明 | gpiozero |
|------|------|----------|
| **BCM** | GPIO番号で指定（GPIO17等） | ✅ 使用 |
| **BOARD** | 物理ピン番号で指定（11番等） | ❌ 不使用 |

**推奨**: BCM番号を使用（gpiozeroのデフォルト）

### ピン番号の確認方法

```bash
# GPIOピン配置を確認
pinout

# 詳細情報
gpio readall
```

## 電気的特性

### 重要な仕様

| 項目 | 仕様 | 注意事項 |
|------|------|---------|
| **動作電圧** | 3.3V | ⚠️ **5Vは厳禁！** |
| **最大電流（1ピン）** | 16mA | **必ず抵抗を使用** |
| **最大電流（全ピン合計）** | 50mA | 複数LED使用時は注意 |
| **入力電圧範囲** | 0 ～ 3.3V | 3.3V以上で破損の恐れ |

### ⚠️ 安全上の注意事項

1. **絶対に5VをGPIOピンに接続しない**
   - GPIOは3.3V動作
   - 5Vを印加すると即座に破損

2. **LEDには必ず抵抗を使用**
   - 推奨: 330Ω ～ 1kΩ
   - 抵抗なしでは過電流で破損

3. **電流制限を守る**
   - 1ピンあたり最大16mA
   - 複数ピン使用時は合計50mA以内

4. **ショートさせない**
   - GPIO同士
   - GPIOとGND
   - 3.3Vと5V

5. **静電気対策**
   - 触る前に金属に触れて放電
   - 特に乾燥した環境で注意

## 基本的な使い方

### LED点滅（最もシンプルな例）

```python
from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

さらにシンプルに:

```python
from gpiozero import LED

led = LED(17)
led.blink()  # 1秒間隔で点滅

input("Enterで終了...")
```

### ボタン入力

```python
from gpiozero import Button

button = Button(2)

while True:
    if button.is_pressed:
        print("ボタンが押されています")
    else:
        print("ボタンは離されています")
```

イベント駆動で:

```python
from gpiozero import Button
from signal import pause

button = Button(2)

button.when_pressed = lambda: print("押された！")
button.when_released = lambda: print("離された！")

pause()
```

## ドキュメント構成

このGPIOガイドは以下のドキュメントで構成されています：

1. **[gpio_overview.md](./gpio_overview.md)** (このファイル)
   - GPIO制御の概要
   - ライブラリ比較
   - GPIOピン配置
   - 電気的特性

2. **[gpio_gpiozero_guide.md](./gpio_gpiozero_guide.md)**
   - gpiozeroの詳細ガイド
   - 主要なデバイスクラス
   - イベント駆動プログラミング
   - ベストプラクティス

3. **[gpio_hardware_connection.md](./gpio_hardware_connection.md)**
   - ハードウェア接続方法
   - LED接続図
   - ボタン接続図
   - 各種センサーの接続

4. **[gpio_examples.md](./gpio_examples.md)**
   - 実装例集
   - LED制御
   - ボタン入力
   - PWM制御
   - 複合的な例

5. **[gpio_troubleshooting.md](./gpio_troubleshooting.md)**
   - トラブルシューティング
   - よくあるエラー
   - デバッグ方法

6. **[gpio_reference.md](./gpio_reference.md)**
   - その他のライブラリ参考情報
   - RPi.GPIO詳細
   - lgpio詳細
   - ライブラリ間の移行ガイド

## クイックスタート

### 1. インストール確認

```bash
# gpiozeroは通常プリインストール済み
python3 -c "import gpiozero; print(gpiozero.__version__)"
```

インストールされていない場合:

```bash
sudo apt update
sudo apt install python3-gpiozero
```

### 2. 権限設定

```bash
# ユーザーをgpioグループに追加（必要に応じて）
sudo usermod -a -G gpio $USER

# 再ログインが必要
```

### 3. 最初のプログラム

LED点滅プログラムを実行:

```bash
python3 gpio_led_blink.py
```

## 参考リンク

### 公式ドキュメント

- [gpiozero Documentation](https://gpiozero.readthedocs.io/)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header)
- [GPIO Pinout (Interactive)](https://pinout.xyz/)

### チュートリアル

- [gpiozero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html)
- [Raspberry Pi GPIO入門](https://projects.raspberrypi.org/en/projects/physical-computing)

### ツール

- [pinout コマンド](https://gpiozero.readthedocs.io/en/stable/cli_tools.html#pinout)
- [GPIO Zero GUI Tool](https://gpiozero.readthedocs.io/en/stable/remote_gpio.html)

## 次のステップ

1. **[gpiozero詳細ガイド](./gpio_gpiozero_guide.md)** でgpiozeroの使い方を学ぶ
2. **[ハードウェア接続ガイド](./gpio_hardware_connection.md)** で安全な接続方法を確認
3. **[実装例集](./gpio_examples.md)** でサンプルコードを試す

---

**Note:** GPIO制御は実際のRaspberry Piハードウェア上でのみ動作します。
