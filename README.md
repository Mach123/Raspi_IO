# Raspi_IO

Raspberry PiからRohde & Schwarz NGP800シリーズ電源をEthernet経由でSCPI制御するためのPythonプログラム集

## 概要

このプロジェクトは、Rohde & Schwarz NGP800シリーズ電源をRaspberry Pi上でPyVISAを使用してリモート制御するための完全なソリューションを提供します。

**主な特徴:**
- ✅ PyVISAベースのシンプルな実装（依存関係最小限）
- ✅ Ethernet/TCP/IP経由のSCPI制御
- ✅ 複数チャンネルの電圧・電流制御
- ✅ リアルタイム測定機能
- ✅ コマンドライン制御ツール
- ✅ 包括的なドキュメント
- ✅ 自動セットアップスクリプト

## 対応機種

- NGP802 (2チャンネル)
- NGP804 (4チャンネル)
- NGP814 (4チャンネル、高出力)
- NGP824 (4チャンネル、高出力)

## クイックスタート

### 1. セットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd Raspi_IO

# 自動セットアップを実行
./setup_ngp800.sh
```

### 2. 基本的な使用

#### メインプログラム

```bash
# ngp800_control.py のIPアドレスを編集
nano ngp800_control.py
# POWER_SUPPLY_IP を自分のNGP800のIPアドレスに変更

# 実行
python3 ngp800_control.py
```

#### コマンドライン制御ツール

```bash
# チャンネル1を3.3V/1Aで出力ON
python3 ngp800_simple_control.py --ip 192.168.1.100 --channel 1 --voltage 3.3 --current 1.0 --on

# 全チャンネルの状態を表示
python3 ngp800_simple_control.py --ip 192.168.1.100 --status

# 全出力をOFF
python3 ngp800_simple_control.py --ip 192.168.1.100 --all-off
```

## プロジェクト構成

```
Raspi_IO/
├── README.md                      # このファイル（プロジェクト概要）
├── NGP800_README.md               # NGP800制御の詳細ガイド
│
├── ngp800_control.py              # メインの制御プログラム
├── ngp800_simple_control.py       # コマンドライン制御ツール
├── setup_ngp800.sh                # 自動セットアップスクリプト
│
└── docs/                          # 詳細ドキュメント
    ├── README.md                  # ドキュメントインデックス
    ├── ngp800_specifications.md   # 仕様・接続情報
    ├── scpi_command_reference.md  # SCPIコマンドリファレンス
    └── pyvisa_examples.md         # PyVISA実装例集
```

## ファイル説明

### プログラムファイル

#### **ngp800_control.py**
GitHubの `RsNgx_GettingStarted_Example.py` と同等の機能を実装した基本プログラム。
2チャンネルの電圧・電流設定、出力制御、測定のデモンストレーション。

**機能:**
- NGP800への接続・切断
- 複数チャンネルの設定
- マスタースイッチによる一括出力制御
- 電圧・電流測定

#### **ngp800_simple_control.py**
コマンドライン引数で簡単に操作できるユーティリティツール。

**機能:**
- 個別チャンネルのON/OFF制御
- 電圧・電流の設定
- 全チャンネルの状態表示
- マスタースイッチ制御
- 機器のリセット

#### **setup_ngp800.sh**
Raspberry Pi環境のセットアップを自動化するスクリプト。

**実行内容:**
- Python3とpip3のインストール確認
- PyVISAとPyVISA-pyのインストール
- スクリプトの実行権限付与
- インストール確認

### ドキュメントファイル

#### **NGP800_README.md**
NGP800制御の詳細な使用ガイド。インストール手順、設定方法、トラブルシューティングを含む。

#### **docs/README.md**
ドキュメント全体のインデックス。クイックスタートガイドとコマンド早見表を含む。

#### **docs/ngp800_specifications.md**
ハードウェア仕様、ネットワーク設定、接続方法、トラブルシューティング。

#### **docs/scpi_command_reference.md**
NGP800で使用可能なSCPIコマンドの完全なリファレンス。

#### **docs/pyvisa_examples.md**
PyVISAを使用した実装例集。基本から高度な使用例、ベストプラクティスまで。

## 必要な環境

### ハードウェア
- Raspberry Pi (任意のモデル)
- Rohde & Schwarz NGP800シリーズ電源
- Ethernetケーブル（またはネットワーク接続）

### ソフトウェア
- Python 3.6以上
- PyVISA (`pip3 install pyvisa`)
- PyVISA-py (`pip3 install pyvisa-py`)

## インストール

### 自動インストール（推奨）

```bash
./setup_ngp800.sh
```

### 手動インストール

```bash
# システムパッケージ更新
sudo apt update
sudo apt upgrade -y

# Python環境確認
python3 --version
pip3 --version

# PyVISA関連パッケージのインストール
pip3 install --user pyvisa pyvisa-py
```

## 使用例

### Python APIとして使用

```python
from ngp800_control import NGP800Controller

# 接続
ngx = NGP800Controller('TCPIP0::192.168.1.100::inst0::INSTR')

# チャンネル1を設定
ngx.select_channel(1)
ngx.set_voltage(3.3)
ngx.set_current(1.0)
ngx.set_output_select(True)

# 全出力ON
ngx.set_general_output_state(True)

# 測定
voltage, current = ngx.read_measurement()
print(f"測定値: {voltage}V, {current}A")

# 全出力OFF
ngx.set_general_output_state(False)

# 接続終了
ngx.close()
```

### コマンドラインから使用

```bash
# ヘルプ表示
python3 ngp800_simple_control.py --help

# チャンネル1を5V/2Aで出力ON
python3 ngp800_simple_control.py --ip 192.168.1.100 \
    --channel 1 --voltage 5.0 --current 2.0 --on

# チャンネル2の出力をOFF
python3 ngp800_simple_control.py --ip 192.168.1.100 \
    --channel 2 --off

# 全チャンネルの状態確認
python3 ngp800_simple_control.py --ip 192.168.1.100 --status

# 機器をリセット
python3 ngp800_simple_control.py --ip 192.168.1.100 --reset
```

## 主要なSCPIコマンド

| コマンド | 説明 |
|---------|------|
| `*IDN?` | 機器識別情報取得 |
| `*RST` | 機器リセット |
| `INSTrument:NSELect <ch>` | チャンネル選択 |
| `VOLTage <値>` | 電圧設定 |
| `CURRent <値>` | 電流リミット設定 |
| `OUTPut:GENeral:STATe <ON\|OFF>` | 全出力ON/OFF |
| `OUTPut:SELect <ON\|OFF>` | チャンネル出力準備 |
| `READ?` | 電圧・電流測定 |

詳細は [docs/scpi_command_reference.md](docs/scpi_command_reference.md) を参照してください。

## ドキュメント

詳細なドキュメントは `docs/` ディレクトリにあります：

- **[docs/README.md](docs/README.md)** - ドキュメントインデックスとクイックリファレンス
- **[docs/ngp800_specifications.md](docs/ngp800_specifications.md)** - ハードウェア仕様とネットワーク設定
- **[docs/scpi_command_reference.md](docs/scpi_command_reference.md)** - SCPIコマンド完全リファレンス
- **[docs/pyvisa_examples.md](docs/pyvisa_examples.md)** - PyVISA実装例とベストプラクティス
- **[NGP800_README.md](NGP800_README.md)** - 詳細な使用ガイド

## トラブルシューティング

### 接続できない

1. **ネットワーク接続確認**
   ```bash
   ping <NGP800のIPアドレス>
   ```

2. **SCPI接続確認**
   ```bash
   telnet <NGP800のIPアドレス> 5025
   ```
   接続後、`*IDN?` を送信

3. **PyVISA確認**
   ```python
   import pyvisa
   rm = pyvisa.ResourceManager('@py')
   print(rm.list_resources())
   ```

### よくある問題

| 症状 | 原因 | 対処法 |
|------|------|--------|
| `VI_ERROR_RSRC_NFOUND` | 接続できない | IPアドレス、ネットワーク接続を確認 |
| `VI_ERROR_TMO` | タイムアウト | タイムアウト値を増やす、ネットワーク遅延を確認 |
| `ModuleNotFoundError: pyvisa` | PyVISA未インストール | `pip3 install pyvisa pyvisa-py` |

詳細は [docs/ngp800_specifications.md](docs/ngp800_specifications.md#トラブルシューティング) を参照してください。

## 参考資料

### 公式ドキュメント

- [R&S NGP800 User Manual](https://www.rohde-schwarz.com/us/manual/r-s-ngp800-power-supply-series-user-manual-manuals_78701-746240.html)
- [R&S NGP800 Getting Started](https://www.farnell.com/datasheets/3965928.pdf)
- [NGP800 Datasheet](https://www.batronix.com/files/Rohde-&-Schwarz/Power-Supplies/NGP/NGP800_datasheet.pdf)

### GitHubリポジトリ

- [Rohde-Schwarz/Examples](https://github.com/Rohde-Schwarz/Examples) - 公式サンプルコード
- [Rohde-Schwarz/RsInstrument](https://github.com/Rohde-Schwarz/RsInstrument) - Python通信モジュール

### Pythonパッケージ

- [PyVISA Documentation](https://pyvisa.readthedocs.io/)
- [RsNgx on PyPI](https://pypi.org/project/RsNgx/) - 公式NGP800ドライバ
- [RsNgx Documentation](https://rsngx.readthedocs.io/en/latest/)

## 開発情報

### 元のサンプルコード

このプロジェクトは、Rohde & Schwarz公式の `RsNgx_GettingStarted_Example.py` をベースに、PyVISAで再実装したものです。

**RsNgxパッケージとの対応:**

| RsNgx | PyVISA (このプロジェクト) |
|-------|--------------------------|
| `RsNgx('TCPIP::...')` | `NGP800Controller('TCPIP0::...::inst0::INSTR')` |
| `ngx.utilities.reset()` | `ngx.reset()` |
| `ngx.instrument.select.set(1)` | `ngx.select_channel(1)` |
| `ngx.source.voltage.level.immediate.set_amplitude(3.3)` | `ngx.set_voltage(3.3)` |
| `ngx.output.general.set_state(True)` | `ngx.set_general_output_state(True)` |
| `ngx.read()` | `ngx.read_measurement()` |

## ライセンス

このプロジェクトは教育・研究目的で自由に使用できます。

## 貢献

改善提案やバグ報告は、IssueまたはPull Requestでお願いします。

## 作成情報

- **作成日:** 2025-12-05
- **対象機器:** Rohde & Schwarz NGP800シリーズ電源
- **制御方法:** PyVISA + SCPI over TCP/IP
- **対象環境:** Raspberry Pi (Linux)

---

**Note:** NGP800のIPアドレスは、各自の環境に合わせて設定してください。
