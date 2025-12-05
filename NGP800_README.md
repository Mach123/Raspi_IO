# NGP800 Power Supply Control for Raspberry Pi

Rohde & Schwarz NGP800電源をRaspberry PiからEthernet経由でSCPI制御するためのPythonプログラムです。

## 概要

このプログラムは、GitHubの `Rohde-Schwarz/Examples` リポジトリにある `RsNgx_GettingStarted_Example.py` と同等の機能を、PyVISAを使用してRaspberry Pi上で実現します。

## 機能

- NGP800への接続（TCP/IP経由）
- 機器のリセット
- 複数チャンネルの電圧・電流設定
- マスタースイッチによる全出力の一括ON/OFF
- 各チャンネルの電圧・電流測定

## 必要な環境

### ハードウェア
- Raspberry Pi (任意のモデル)
- Rohde & Schwarz NGP800シリーズ電源
- Ethernetケーブル（またはネットワーク接続）

### ソフトウェア
- Python 3.6以上
- PyVISA
- PyVISA-py (バックエンド)

## インストール

### 1. 依存パッケージのインストール

```bash
# システムパッケージの更新
sudo apt update
sudo apt upgrade -y

# Pythonとpipのインストール（既にインストール済みの場合はスキップ）
sudo apt install python3 python3-pip -y

# PyVISAとバックエンドのインストール
pip3 install pyvisa pyvisa-py
```

### 2. プログラムの準備

`ngp800_control.py` をダウンロードまたはコピーして、実行権限を付与します：

```bash
chmod +x ngp800_control.py
```

## 設定

プログラム内の以下の行を編集して、NGP800のIPアドレスを設定します：

```python
POWER_SUPPLY_IP = '10.102.52.45'  # あなたのNGP800のIPアドレスに変更
```

### NGP800のIPアドレス確認方法

1. NGP800のフロントパネルで `Setup` → `Interface` → `LAN` を選択
2. 表示されるIPアドレスをメモ
3. または、NGP800のウェブインターフェースから確認

### ネットワーク接続の確認

```bash
# NGP800にpingが通るか確認
ping 10.102.52.45  # IPアドレスは適宜変更
```

## 使用方法

### 基本的な実行

```bash
python3 ngp800_control.py
```

### 実行例

```
============================================================
NGP800 Power Supply Control Script
============================================================

Connecting to TCPIP0::10.102.52.45::inst0::INSTR...

Hello, I am: Rohde&Schwarz,NGP824,1234567890,1.00.000

Resetting instrument...
Turning OFF all outputs (master switch)...

Configuring Output 1:
  - Selecting channel 1
  - Setting voltage: 3.3 V
  - Setting current limit: 0.1 A
  - Preparing output for master switch ON

Configuring Output 2:
  - Selecting channel 2
  - Setting voltage: 5.1 V
  - Setting current limit: 0.05 A
  - Preparing output for master switch ON

Turning ON all outputs (master switch)...
Waiting for outputs to settle...

Reading measurements:
  Output 1: 3.3000 V, 0.000050 A
  Output 2: 5.1000 V, 0.000020 A

============================================================
Script completed successfully!
============================================================
```

## プログラムの構造

### NGP800Controllerクラス

主要なメソッド：

- `__init__(resource_string, timeout)` - 電源への接続
- `get_idn()` - 機器識別情報の取得
- `reset()` - 機器のリセット
- `set_general_output_state(state)` - 全出力のON/OFF
- `select_channel(channel)` - チャンネル選択
- `set_voltage(voltage)` - 電圧設定
- `set_current(current)` - 電流リミット設定
- `set_output_select(state)` - 個別チャンネルの出力準備
- `read_measurement()` - 電圧・電流測定
- `close()` - 接続のクローズ

## カスタマイズ

### 電圧・電流値の変更

`main()` 関数内の以下の部分を編集：

```python
# Output 1の設定
ngx.set_voltage(3.3)    # 電圧 (V)
ngx.set_current(0.1)    # 電流リミット (A)

# Output 2の設定
ngx.set_voltage(5.1)    # 電圧 (V)
ngx.set_current(0.05)   # 電流リミット (A)
```

### チャンネル数の変更

NGP800シリーズには2チャンネル/4チャンネルモデルがあります。
チャンネルを追加する場合：

```python
# Output 3の設定例
ngx.select_channel(3)
ngx.set_voltage(12.0)
ngx.set_current(0.5)
ngx.set_output_select(True)
```

## トラブルシューティング

### 接続エラー

**症状**: `VISA Error: VI_ERROR_RSRC_NFOUND`

**対処法**:
1. IPアドレスが正しいか確認
2. NGP800がネットワークに接続されているか確認
3. Raspberry PiからNGP800にpingが通るか確認
4. NGP800のSCPIインターフェースが有効になっているか確認

### タイムアウトエラー

**症状**: `VISA Error: VI_ERROR_TMO`

**対処法**:
1. タイムアウト値を増やす（デフォルト5000ms）
2. NGP800が応答しているか確認
3. ネットワーク遅延を確認

```python
ngx = NGP800Controller(resource_string, timeout=10000)  # 10秒に延長
```

### PyVISAが見つからない

**症状**: `ModuleNotFoundError: No module named 'pyvisa'`

**対処法**:
```bash
pip3 install --user pyvisa pyvisa-py
```

## 主要なSCPIコマンド対応表

| 機能 | RsNgxメソッド | SCPIコマンド | このプログラム |
|------|--------------|-------------|---------------|
| 機器ID取得 | `utilities.idn_string` | `*IDN?` | `get_idn()` |
| リセット | `utilities.reset()` | `*RST` | `reset()` |
| 全出力ON/OFF | `output.general.set_state()` | `OUTPut:GENeral:STATe` | `set_general_output_state()` |
| チャンネル選択 | `instrument.select.set()` | `INSTrument:SELect` | `select_channel()` |
| 電圧設定 | `source.voltage.level.immediate.set_amplitude()` | `SOURce:VOLTage:LEVel:IMMediate:AMPlitude` | `set_voltage()` |
| 電流設定 | `source.current.level.immediate.set_amplitude()` | `SOURce:CURRent:LEVel:IMMediate:AMPlitude` | `set_current()` |
| 出力選択 | `output.set_select()` | `OUTPut:SELect` | `set_output_select()` |
| 測定 | `read()` | `READ?` | `read_measurement()` |

## 参考リンク

- [Rohde-Schwarz/Examples GitHub Repository](https://github.com/Rohde-Schwarz/Examples)
- [RsNgx PyPI Package](https://pypi.org/project/RsNgx/)
- [RsNgx Documentation](https://rsngx.readthedocs.io/en/latest/getting_started.html)
- [PyVISA Documentation](https://pyvisa.readthedocs.io/)

## ライセンス

このプログラムは教育・研究目的で自由に使用できます。

## 作成情報

- 元のサンプル: `RsNgx_GettingStarted_Example.py` (Rohde & Schwarz)
- PyVISA版作成日: 2025-12-05
- 対象機器: Rohde & Schwarz NGP800シリーズ電源
