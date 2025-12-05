# NGP800 電源制御ドキュメント

Rohde & Schwarz NGP800シリーズ電源をPyVISAで制御するための包括的なドキュメント集です。

## ドキュメント一覧

### 📘 [仕様・接続情報](./ngp800_specifications.md)
NGP800の基本仕様、ネットワーク接続設定、トラブルシューティングガイド

**主な内容:**
- 製品ラインナップ（NGP802/804/814/824）
- ネットワーク接続仕様（TCP/IP、ポート5025）
- IPアドレスの設定と確認方法
- チャンネル構成の概念
- SCPI通信の基本仕様
- 接続確認方法（Ping、Telnet、PyVISA）
- トラブルシューティング

### 📗 [SCPIコマンドリファレンス](./scpi_command_reference.md)
NGP800で使用可能なSCPIコマンドの詳細リファレンス

**主な内容:**
- 共通コマンド（*IDN?, *RST, *OPCなど）
- INSTrumentサブシステム（チャンネル選択）
- OUTPutサブシステム（出力制御）
- SOURceサブシステム（電圧・電流設定）
- MEASureサブシステム（測定）
- SYSTemサブシステム（システム設定）
- コマンド短縮形一覧
- エラー処理

### 📙 [PyVISA実装例集](./pyvisa_examples.md)
PyVISAを使用したPython実装例の詳細ガイド

**主な内容:**
- 基本的な接続方法
- チャンネル制御（コンテキストマネージャ）
- 電圧・電流設定（範囲チェック付き）
- 測定（単発、連続、ロギング）
- 高度な使用例（シーケンス制御、過電流検出）
- エラーハンドリング（リトライ、デコレータ）
- ベストプラクティス
- 完全なアプリケーション例

## クイックスタート

### 1. 必要な環境

```bash
# PyVISAとバックエンドのインストール
pip3 install pyvisa pyvisa-py
```

### 2. 最小限の接続例

```python
import pyvisa

# 接続
rm = pyvisa.ResourceManager('@py')
ngx = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR')

# 機器確認
print(ngx.query('*IDN?'))

# 出力制御
ngx.write('INSTrument:NSELect 1')  # チャンネル1選択
ngx.write('VOLTage 3.3')            # 電圧設定
ngx.write('CURRent 1.0')            # 電流設定
ngx.write('OUTPut ON')              # 出力ON

# 測定
response = ngx.query('READ?')
voltage, current = map(float, response.split(','))
print(f"測定値: {voltage}V, {current}A")

# クローズ
ngx.close()
```

### 3. 実用的なプログラム

本リポジトリには、すぐに使えるプログラムが用意されています：

- **[ngp800_control.py](../ngp800_control.py)** - 基本的な制御プログラム
- **[ngp800_simple_control.py](../ngp800_simple_control.py)** - コマンドライン制御ツール
- **[setup_ngp800.sh](../setup_ngp800.sh)** - 自動セットアップスクリプト

詳細は [NGP800_README.md](../NGP800_README.md) を参照してください。

## 主要なSCPIコマンド早見表

### 接続・確認

| コマンド | 説明 | 例 |
|---------|------|-----|
| `*IDN?` | 機器識別 | `Rohde&Schwarz,NGP824,...` |
| `*RST` | リセット | - |

### チャンネル選択

| コマンド | 説明 | 例 |
|---------|------|-----|
| `INSTrument:NSELect <ch>` | チャンネル選択 | `INSTrument:NSELect 1` |
| `INSTrument:NSELect?` | 現在のチャンネル確認 | `1` |

### 出力制御

| コマンド | 説明 | 例 |
|---------|------|-----|
| `OUTPut:GENeral:STATe <ON\|OFF>` | 全出力マスタースイッチ | `OUTPut:GENeral:STATe ON` |
| `OUTPut:SELect <ON\|OFF>` | チャンネル出力準備 | `OUTPut:SELect ON` |
| `OUTPut <ON\|OFF>` | チャンネル出力ON/OFF | `OUTPut ON` |
| `OUTPut?` | 出力状態確認 | `1` (ON) / `0` (OFF) |

### 電圧・電流設定

| コマンド | 説明 | 例 |
|---------|------|-----|
| `VOLTage <値>` | 電圧設定 | `VOLTage 3.3` |
| `VOLTage?` | 電圧設定値確認 | `3.3` |
| `CURRent <値>` | 電流リミット設定 | `CURRent 1.0` |
| `CURRent?` | 電流設定値確認 | `1.0` |

### 測定

| コマンド | 説明 | 例 |
|---------|------|-----|
| `MEASure:VOLTage?` | 電圧測定 | `3.3001` |
| `MEASure:CURRent?` | 電流測定 | `0.05234` |
| `READ?` | 電圧・電流同時測定 | `3.3001,0.05234` |

## 典型的な制御フロー

```
1. 接続
   ↓
2. 機器識別 (*IDN?)
   ↓
3. リセット (*RST)
   ↓
4. 全出力OFF (OUTPut:GENeral:STATe OFF)
   ↓
5. チャンネル選択 (INSTrument:NSELect <ch>)
   ↓
6. 電圧設定 (VOLTage <値>)
   ↓
7. 電流設定 (CURRent <値>)
   ↓
8. 出力準備 (OUTPut:SELect ON)
   ↓
9. (複数チャンネルの場合、5～8を繰り返し)
   ↓
10. 全出力ON (OUTPut:GENeral:STATe ON)
   ↓
11. 安定化待機 (time.sleep)
   ↓
12. 測定 (READ?)
   ↓
13. 全出力OFF (OUTPut:GENeral:STATe OFF)
   ↓
14. 接続クローズ
```

## PyVISAリソース文字列

NGP800への接続には以下の形式を使用：

```python
# VXI-11プロトコル（推奨）
'TCPIP0::<IPアドレス>::inst0::INSTR'

# Raw Socketプロトコル
'TCPIP0::<IPアドレス>::5025::SOCKET'
```

**例:**
```python
'TCPIP0::192.168.1.100::inst0::INSTR'
'TCPIP0::10.102.52.45::inst0::INSTR'
```

## RsNgxパッケージとの対応

Rohde & Schwarz公式の `RsNgx` パッケージを使用する場合：

```bash
pip3 install RsNgx
```

| RsNgxメソッド | SCPI/PyVISA相当 |
|--------------|----------------|
| `RsNgx('TCPIP::...')` | `rm.open_resource('TCPIP0::...::inst0::INSTR')` |
| `ngx.utilities.idn_string` | `ngx.query('*IDN?')` |
| `ngx.utilities.reset()` | `ngx.write('*RST')` |
| `ngx.output.general.set_state(True)` | `ngx.write('OUTPut:GENeral:STATe ON')` |
| `ngx.instrument.select.set(1)` | `ngx.write('INSTrument:NSELect 1')` |
| `ngx.source.voltage.level.immediate.set_amplitude(3.3)` | `ngx.write('VOLTage 3.3')` |
| `ngx.source.current.level.immediate.set_amplitude(1.0)` | `ngx.write('CURRent 1.0')` |
| `ngx.output.set_select(True)` | `ngx.write('OUTPut:SELect ON')` |
| `ngx.read()` | `ngx.query('READ?')` |

## トラブルシューティング

### 接続できない

1. **ネットワーク接続確認**
   ```bash
   ping 192.168.1.100
   ```

2. **ポート確認**
   ```bash
   telnet 192.168.1.100 5025
   ```
   接続後、`*IDN?` を送信して応答を確認

3. **PyVISAバックエンド確認**
   ```python
   import pyvisa
   print(pyvisa.ResourceManager('@py').list_resources())
   ```

### タイムアウトエラー

```python
# タイムアウト値を増やす
ngx.timeout = 10000  # 10秒
```

### 詳細なエラー情報

```python
# SCPIエラーを確認
error = ngx.query('SYSTem:ERRor?')
print(error)
```

詳細は [仕様・接続情報ドキュメント](./ngp800_specifications.md#トラブルシューティング) を参照してください。

## 参考リンク

### 公式ドキュメント

- [R&S NGP800 User Manual](https://www.rohde-schwarz.com/us/manual/r-s-ngp800-power-supply-series-user-manual-manuals_78701-746240.html)
- [R&S NGP800 Getting Started Guide](https://www.farnell.com/datasheets/3965928.pdf)
- [NGP800 Datasheet](https://www.batronix.com/files/Rohde-&-Schwarz/Power-Supplies/NGP/NGP800_datasheet.pdf)

### GitHubリポジトリ

- [Rohde-Schwarz/Examples](https://github.com/Rohde-Schwarz/Examples) - 公式サンプルコード集
- [Rohde-Schwarz/RsInstrument](https://github.com/Rohde-Schwarz/RsInstrument) - Python通信モジュール
- [Rohde-Schwarz/RsNgx (PyPI)](https://pypi.org/project/RsNgx/) - NGP800専用ドライバ

### ドキュメント

- [PyVISA Documentation](https://pyvisa.readthedocs.io/)
- [RsNgx Documentation](https://rsngx.readthedocs.io/en/latest/getting_started.html)
- [RsInstrument Documentation](https://rsinstrument.readthedocs.io/en/latest/StepByStepGuide.html)

### マニュアルページ（ManualsLib）

- [SCPI Command Structure (Page 157)](https://www.manualslib.com/manual/1834650/Rohde-And-Schwarz-RAnds-Ngp800-Series.html?page=157)
- [Configuration Commands (Page 117)](https://www.manualslib.com/manual/2605820/Rohde-And-Schwarz-Ngp800-Series.html?page=117)

## 貢献

このドキュメントは、最初のチャットで得られた情報を元に作成されました。
改善提案やバグ報告は、Issueまたはプルリクエストでお願いします。

## ライセンス

このドキュメントは教育・研究目的で自由に使用できます。

---

**作成日:** 2025-12-05
**対象機器:** Rohde & Schwarz NGP800シリーズ電源
**制御方法:** PyVISA + SCPI over TCP/IP
