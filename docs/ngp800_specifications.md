# Rohde & Schwarz NGP800 電源 - 仕様・接続情報

## 概要

Rohde & Schwarz NGP800シリーズは、Ethernet経由でSCPI（Standard Commands for Programmable Instruments）プロトコルによるリモート制御が可能な高性能電源です。

## 製品ラインナップ

NGP800シリーズには以下のモデルがあります：

- **NGP802** - 2チャンネル
- **NGP804** - 4チャンネル
- **NGP814** - 4チャンネル（高出力）
- **NGP824** - 4チャンネル（高出力）

## ネットワーク接続仕様

### 接続方式

| 項目 | 仕様 |
|------|------|
| インターフェース | LAN (Ethernet) |
| プロトコル | SCPI over TCP/IP (Socket通信) |
| デフォルトポート | 5025 |
| 通信方式 | Raw Socket / VXI-11 |

### VISA リソース文字列

NGP800への接続には以下の形式を使用します：

```
TCPIP0::<IPアドレス>::inst0::INSTR
```

または

```
TCPIP0::<IPアドレス>::5025::SOCKET
```

**例:**
```
TCPIP0::192.168.1.100::inst0::INSTR
TCPIP0::10.102.52.45::inst0::INSTR
```

## ネットワーク設定

### IPアドレスの設定方法

1. **DHCP（自動取得）**
   - フロントパネル: `Setup` → `Interface` → `LAN` → `DHCP: ON`
   - SCPIコマンド: `SYSTem:COMMunicate:SOCKet:DHCP ON`

2. **静的IP（手動設定）**
   - フロントパネル: `Setup` → `Interface` → `LAN` → `DHCP: OFF`
   - SCPIコマンド: `SYSTem:COMMunicate:SOCKet:DHCP OFF`

### IPアドレスの確認方法

1. フロントパネルで確認:
   - `Setup` → `Interface` → `LAN`
   - 画面にIPアドレスが表示されます

2. ウェブインターフェースで確認:
   - ブラウザでNGP800のIPアドレスにアクセス
   - SCPI Device Control画面で確認可能

3. SCPIコマンドで確認:
   ```
   SYSTem:COMMunicate:SOCKet:IPADdress?
   ```

## チャンネル構成

### チャンネルの概念

NGP800では、各チャンネルがSCPI標準に準拠して独立した「インストルメント」として扱われます。

- チャンネル番号: 1, 2, 3, 4（モデルによる）
- 各チャンネルは独立した電圧・電流設定が可能
- マスタースイッチで全チャンネルを一括制御可能

### チャンネル選択

チャンネルを選択するには `INSTRument` ノードを使用します：

```
INSTrument:NSELect <チャンネル番号>
INSTrument:SELect <チャンネル番号>
```

## SCPI通信の基本仕様

### コマンド構造

SCPIコマンドは、ヘッダーとパラメータで構成されます：

```
<ヘッダー> <パラメータ>
```

- ヘッダーとパラメータは空白で区切られます
- コマンドは改行文字（LF）で終了します

### ブール値の表現

ON/OFFの状態は以下のように表現されます：

| 状態 | 表現方法 |
|------|---------|
| ON（真） | `ON` または `1` |
| OFF（偽） | `OFF` または `0` |

**例:**
```
OUTPut ON
OUTPut 1
OUTPut OFF
OUTPut 0
```

### クエリコマンド

設定値や状態を問い合わせるには、コマンドの末尾に `?` を付けます：

```
OUTPut?          # 出力状態の問い合わせ
VOLTage?         # 電圧設定値の問い合わせ
MEASure:VOLTage? # 電圧測定値の問い合わせ
```

## タイムアウト設定

通信タイムアウトは、ネットワーク環境に応じて調整してください：

- **推奨値**: 5000ms（5秒）
- **最小値**: 1000ms（1秒）
- **長時間動作時**: 10000ms（10秒）以上

## ウェブインターフェース

NGP800はウェブベースのSCPI制御インターフェースを提供しています：

### アクセス方法

1. ブラウザでNGP800のIPアドレスにアクセス
2. 「SCPI Device Control」ページを開く

### 機能

- SCPIコマンドの送信と応答確認
- 画面データの表示とダウンロード
- リモート制御のテスト

## 通信確認方法

### 1. Pingテスト

```bash
ping 192.168.1.100
```

正常に応答があれば、ネットワーク接続は確立されています。

### 2. Telnetテスト

```bash
telnet 192.168.1.100 5025
```

接続後、以下のコマンドを送信：

```
*IDN?
```

機器情報が返信されれば、SCPI通信が可能です。

### 3. PyVISAでのテスト

```python
import pyvisa
rm = pyvisa.ResourceManager('@py')
ngx = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR')
print(ngx.query('*IDN?'))
ngx.close()
```

## セキュリティ設定

### ファイアウォール

NGP800と通信するには、以下のポートが開いている必要があります：

- **ポート 5025**: SCPI Raw Socket通信
- **ポート 80**: ウェブインターフェース（オプション）

### Raspberry Piでの設定例

```bash
# ファイアウォールでポート5025を許可（必要に応じて）
sudo ufw allow 5025/tcp
```

## トラブルシューティング

### 接続できない場合

1. **ネットワーク接続の確認**
   - Ethernetケーブルが接続されているか
   - NGP800のLANポートのLEDが点灯しているか
   - 同一ネットワーク上にあるか

2. **IPアドレスの確認**
   - NGP800のIPアドレスが正しいか
   - DHCPで取得されているか、静的IPが設定されているか

3. **SCPIインターフェースの確認**
   - NGP800でリモート制御が有効になっているか
   - ローカルロックアウトモードになっていないか

4. **ファイアウォールの確認**
   - ポート5025が開いているか
   - セキュリティソフトが通信をブロックしていないか

## 参考資料

### 公式ドキュメント

- [R&S NGP800 User Manual](https://www.rohde-schwarz.com/us/manual/r-s-ngp800-power-supply-series-user-manual-manuals_78701-746240.html)
- [R&S NGP800 Getting Started Guide](https://www.farnell.com/datasheets/3965928.pdf)
- [R&S NGP800 Datasheet](https://www.batronix.com/files/Rohde-&-Schwarz/Power-Supplies/NGP/NGP800_datasheet.pdf)

### オンラインリソース

- [Rohde-Schwarz GitHub Examples](https://github.com/Rohde-Schwarz/Examples)
- [RsInstrument Python Module](https://github.com/Rohde-Schwarz/RsInstrument)
- [PyVISA Documentation](https://pyvisa.readthedocs.io/)

## 付録: 仕様一覧表

### NGP802/804 仕様

| 項目 | 仕様 |
|------|------|
| チャンネル数 | 2ch / 4ch |
| 最大電圧 | 32V |
| 最大電流 | 3A |
| 最大電力 | 100W |

### NGP814/824 仕様

| 項目 | 仕様 |
|------|------|
| チャンネル数 | 4ch |
| 最大電圧 | Ch1-2: 32V, Ch3-4: 6V |
| 最大電流 | Ch1-2: 10A, Ch3-4: 10A |
| 最大電力 | 400W |

*詳細な仕様は製品データシートを参照してください。*
