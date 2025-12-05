# Raspi_IO

Raspberry PiでNGP800電源とGPIOデバイスを制御するための包括的なプログラム集とドキュメント

## 概要

このプロジェクトは、Raspberry Pi上で以下の制御を実現します：

1. **NGP800電源制御** - Rohde & Schwarz NGP800シリーズ電源のリモート制御（PyVISA + SCPI）
2. **GPIO制御** - LED、ボタン、センサー等の電子部品制御（gpiozero）

## 主な特徴

- ✅ **包括的なドキュメント** - 初心者から上級者まで対応
- ✅ **実用的なサンプルコード** - すぐに使える実装例
- ✅ **自動セットアップ** - 簡単インストール
- ✅ **ベストプラクティス** - 安全で効率的なコード

## プロジェクト構成

```
Raspi_IO/
├── 📄 README.md                    # このファイル
│
├── 🔌 NGP800電源制御
│   ├── ngp800_control.py           # 基本制御プログラム
│   ├── ngp800_simple_control.py    # CLIツール
│   ├── setup_ngp800.sh             # セットアップスクリプト
│   └── NGP800_README.md            # 詳細ガイド
│
├── 💡 GPIO制御
│   ├── gpio_led_blink.py           # LED点滅（gpiozero）
│   ├── gpio_pwm_led.py             # PWM制御
│   ├── gpio_button_led.py          # ボタン制御
│   ├── gpio_led_blink_rpigpio.py   # RPi.GPIO版（参考）
│   └── GPIO_README.md              # 詳細ガイド
│
└── 📚 docs/                        # 詳細ドキュメント
    ├── README.md                   # ドキュメントインデックス
    ├── NGP800関連 (3ファイル)
    └── GPIO関連 (4ファイル)
```

## クイックスタート

### NGP800電源制御

```bash
# セットアップ
./setup_ngp800.sh

# IPアドレスを設定して実行
python3 ngp800_control.py
```

**詳細**: [NGP800_README.md](./NGP800_README.md)

### GPIO制御

```bash
# gpiozeroインストール（通常プリインストール済み）
sudo apt install python3-gpiozero

# LED点滅
python3 gpio_led_blink.py
```

**詳細**: [GPIO_README.md](./GPIO_README.md)

## ドキュメント

### 📘 NGP800電源制御

| ドキュメント | 説明 |
|-------------|------|
| [NGP800_README.md](./NGP800_README.md) | 詳細な使用ガイド |
| [docs/ngp800_specifications.md](./docs/ngp800_specifications.md) | 仕様・接続情報 |
| [docs/scpi_command_reference.md](./docs/scpi_command_reference.md) | SCPIコマンドリファレンス |
| [docs/pyvisa_examples.md](./docs/pyvisa_examples.md) | PyVISA実装例集 |

**対応機種**: NGP802/804/814/824
**制御方法**: PyVISA + SCPI over TCP/IP
**必要環境**: Python 3.6+, PyVISA, PyVISA-py

### 💡 GPIO制御

| ドキュメント | 説明 |
|-------------|------|
| [GPIO_README.md](./GPIO_README.md) | 詳細な使用ガイド |
| [docs/gpio_overview.md](./docs/gpio_overview.md) | GPIO概要・ライブラリ比較 |
| [docs/gpio_gpiozero_guide.md](./docs/gpio_gpiozero_guide.md) | gpiozero完全ガイド |
| [docs/gpio_hardware_connection.md](./docs/gpio_hardware_connection.md) | ハードウェア接続ガイド |
| [docs/gpio_examples.md](./docs/gpio_examples.md) | 実装例集（20+サンプル） |

**推奨ライブラリ**: gpiozero
**対応デバイス**: LED、ボタン、センサー、モーター等
**必要環境**: Python 3.6+, gpiozero

### 📚 すべてのドキュメント

[docs/README.md](./docs/README.md) - ドキュメント全体のインデックス

## インストール

### 前提条件

- Raspberry Pi (任意のモデル)
- Raspberry Pi OS Bullseye/Bookworm
- Python 3.6以上

### NGP800電源制御

```bash
# 自動セットアップ（推奨）
./setup_ngp800.sh

# または手動インストール
pip3 install pyvisa pyvisa-py
```

### GPIO制御

```bash
# gpiozero（通常プリインストール済み）
sudo apt install python3-gpiozero

# 権限設定（必要に応じて）
sudo usermod -a -G gpio $USER
```

## 使用例

### NGP800電源制御

```python
from ngp800_control import NGP800Controller

# 接続
ngx = NGP800Controller('TCPIP0::192.168.1.100::inst0::INSTR')

# チャンネル1を3.3V/1Aに設定
ngx.select_channel(1)
ngx.set_voltage(3.3)
ngx.set_current(1.0)
ngx.set_general_output_state(True)

# 測定
voltage, current = ngx.read_measurement()
print(f"{voltage}V, {current}A")

ngx.close()
```

### GPIO制御

```python
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2)

# ボタンを押すとLED点灯
button.when_pressed = led.on
button.when_released = led.off

pause()
```

## プログラム一覧

### NGP800電源制御

| プログラム | 説明 | 使用方法 |
|-----------|------|---------|
| `ngp800_control.py` | 基本的な制御プログラム | `python3 ngp800_control.py` |
| `ngp800_simple_control.py` | コマンドラインツール | `python3 ngp800_simple_control.py --help` |
| `setup_ngp800.sh` | 自動セットアップ | `./setup_ngp800.sh` |

### GPIO制御

| プログラム | 説明 | 使用方法 |
|-----------|------|---------|
| `gpio_led_blink.py` | LED点滅（gpiozero） | `python3 gpio_led_blink.py` |
| `gpio_pwm_led.py` | PWM明るさ制御 | `python3 gpio_pwm_led.py` |
| `gpio_button_led.py` | ボタン制御 | `python3 gpio_button_led.py` |
| `gpio_led_blink_rpigpio.py` | LED点滅（RPi.GPIO参考） | `python3 gpio_led_blink_rpigpio.py` |

## トラブルシューティング

### NGP800電源制御

**問題**: 接続できない

```bash
# ネットワーク確認
ping 192.168.1.100

# ポート確認
telnet 192.168.1.100 5025
```

**詳細**: [NGP800_README.md - トラブルシューティング](./NGP800_README.md#トラブルシューティング)

### GPIO制御

**問題**: LEDが点灯しない

- LED の向きを確認（長い足がGPIO側）
- 330Ω抵抗が接続されているか確認
- GPIO番号が正しいか確認

**詳細**: [GPIO_README.md - トラブルシューティング](./GPIO_README.md#トラブルシューティング)

## 参考リンク

### NGP800電源制御

- [Rohde & Schwarz NGP800 公式サイト](https://www.rohde-schwarz.com/us/product/ngp800/)
- [PyVISA Documentation](https://pyvisa.readthedocs.io/)
- [Rohde-Schwarz GitHub Examples](https://github.com/Rohde-Schwarz/Examples)

### GPIO制御

- [gpiozero Documentation](https://gpiozero.readthedocs.io/)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)

## 貢献

改善提案やバグ報告は、IssueまたはPull Requestでお願いします。

## ライセンス

このプロジェクトは教育・研究目的で自由に使用できます。

## 作成情報

- **作成日**: 2025-12-05
- **対象環境**: Raspberry Pi OS Bullseye/Bookworm
- **対象機器**:
  - Rohde & Schwarz NGP800シリーズ電源
  - Raspberry Pi GPIO対応デバイス

---

**Note**:
- NGP800制御は実際のNGP800ハードウェアが必要です
- GPIO制御は実際のRaspberry Piハードウェアが必要です
