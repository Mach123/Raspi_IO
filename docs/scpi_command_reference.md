# NGP800 SCPI コマンドリファレンス

## 目次

1. [共通コマンド](#共通コマンド)
2. [INSTrumentサブシステム](#instrumentサブシステム)
3. [OUTPutサブシステム](#outputサブシステム)
4. [SOURceサブシステム](#sourceサブシステム)
5. [MEASureサブシステム](#measureサブシステム)
6. [SYSTemサブシステム](#systemサブシステム)

## 共通コマンド

SCPIで定義されている標準的な共通コマンドです。

### *IDN? - 機器識別

機器の識別情報を取得します。

**構文:**
```
*IDN?
```

**戻り値:**
```
Rohde&Schwarz,NGP824,<シリアル番号>,<ファームウェアバージョン>
```

**例:**
```python
response = ngx.query('*IDN?')
# 例: "Rohde&Schwarz,NGP824,1234567890,1.00.000"
```

---

### *RST - リセット

機器を初期状態にリセットします。

**構文:**
```
*RST
```

**パラメータ:** なし

**注意:** リセット後、設定が完了するまで約1秒待機してください。

**例:**
```python
ngx.write('*RST')
time.sleep(1)  # リセット完了待ち
```

---

### *CLS - ステータスクリア

すべてのイベントステータスレジスタをクリアします。

**構文:**
```
*CLS
```

**パラメータ:** なし

---

### *OPC? - 動作完了クエリ

すべての保留中のコマンドが完了したら "1" を返します。

**構文:**
```
*OPC?
```

**戻り値:** `1`

---

## INSTrumentサブシステム

チャンネル（インストルメント）の選択を行います。

### INSTrument:NSELect - チャンネル選択（数値）

チャンネル番号で選択します。

**構文:**
```
INSTrument:NSELect <チャンネル番号>
INSTrument:NSELect?
```

**パラメータ:**
- `<チャンネル番号>`: 1 ～ 4（モデルによる）

**例:**
```python
# チャンネル1を選択
ngx.write('INSTrument:NSELect 1')

# 現在選択されているチャンネルを確認
channel = ngx.query('INSTrument:NSELect?')
```

---

### INSTrument:SELect - チャンネル選択（名前）

チャンネル名で選択します。

**構文:**
```
INSTrument:SELect <チャンネル名>
INSTrument:SELect?
```

**パラメータ:**
- `<チャンネル名>`: "OUT1", "OUT2", "OUT3", "OUT4"

**例:**
```python
ngx.write('INSTrument:SELect OUT1')
```

---

## OUTPutサブシステム

出力のON/OFF制御を行います。

### OUTPut:GENeral:STATe - 全出力マスタースイッチ

すべてのチャンネルの出力を一括でON/OFFします。

**構文:**
```
OUTPut:GENeral:STATe <状態>
OUTPut:GENeral:STATe?
```

**パラメータ:**
- `<状態>`: `ON` | `OFF` | `1` | `0`

**例:**
```python
# 全出力をON
ngx.write('OUTPut:GENeral:STATe ON')

# 全出力をOFF
ngx.write('OUTPut:GENeral:STATe OFF')

# 状態確認
state = ngx.query('OUTPut:GENeral:STATe?')
```

---

### OUTPut:SELect - 個別チャンネル出力選択

選択中のチャンネルの出力をマスタースイッチの対象にするか設定します。

**構文:**
```
OUTPut:SELect <状態>
OUTPut:SELect?
```

**パラメータ:**
- `<状態>`: `ON` | `OFF` | `1` | `0`

**動作:**
- `ON`: マスタースイッチがONになったときに出力開始
- `OFF`: マスタースイッチに関係なく出力しない

**例:**
```python
# チャンネル1を選択
ngx.write('INSTrument:NSELect 1')
# マスタースイッチの対象にする
ngx.write('OUTPut:SELect ON')
```

---

### OUTPut[:STATe] - 個別チャンネル出力ON/OFF

選択中のチャンネルの出力を直接ON/OFFします。

**構文:**
```
OUTPut[:STATe] <状態>
OUTPut[:STATe]?
```

**パラメータ:**
- `<状態>`: `ON` | `OFF` | `1` | `0`

**例:**
```python
# チャンネル1を選択して出力ON
ngx.write('INSTrument:NSELect 1')
ngx.write('OUTPut ON')

# 出力状態確認
state = ngx.query('OUTPut?')
```

---

## SOURceサブシステム

電圧・電流の設定を行います。

### SOURce:VOLTage:LEVel:IMMediate:AMPlitude - 電圧設定

選択中のチャンネルの出力電圧を設定します。

**構文:**
```
SOURce:VOLTage:LEVel:IMMediate:AMPlitude <電圧>
SOURce:VOLTage:LEVel:IMMediate:AMPlitude?
```

**短縮形:**
```
VOLT <電圧>
VOLT?
```

**パラメータ:**
- `<電圧>`: 電圧値（V）

**範囲:** 0V ～ 最大電圧（モデルにより32Vまたは6V）

**例:**
```python
# チャンネル1に3.3Vを設定
ngx.write('INSTrument:NSELect 1')
ngx.write('SOURce:VOLTage:LEVel:IMMediate:AMPlitude 3.3')

# 短縮形
ngx.write('VOLT 3.3')

# 設定値の確認
voltage = ngx.query('VOLT?')
```

---

### SOURce:CURRent:LEVel:IMMediate:AMPlitude - 電流リミット設定

選択中のチャンネルの電流リミットを設定します。

**構文:**
```
SOURce:CURRent:LEVel:IMMediate:AMPlitude <電流>
SOURce:CURRent:LEVel:IMMediate:AMPlitude?
```

**短縮形:**
```
CURR <電流>
CURR?
```

**パラメータ:**
- `<電流>`: 電流値（A）

**範囲:** 0A ～ 最大電流（モデルにより3Aまたは10A）

**例:**
```python
# チャンネル1に1Aの電流リミットを設定
ngx.write('INSTrument:NSELect 1')
ngx.write('SOURce:CURRent:LEVel:IMMediate:AMPlitude 1.0')

# 短縮形
ngx.write('CURR 1.0')

# 設定値の確認
current = ngx.query('CURR?')
```

---

## MEASureサブシステム

実際の出力値を測定します。

### MEASure:VOLTage? - 電圧測定

選択中のチャンネルの出力電圧を測定します。

**構文:**
```
MEASure:VOLTage?
```

**短縮形:**
```
MEAS:VOLT?
```

**戻り値:** 電圧値（V）

**例:**
```python
# チャンネル1の電圧を測定
ngx.write('INSTrument:NSELect 1')
voltage = float(ngx.query('MEASure:VOLTage?'))
```

---

### MEASure:CURRent? - 電流測定

選択中のチャンネルの出力電流を測定します。

**構文:**
```
MEASure:CURRent?
```

**短縮形:**
```
MEAS:CURR?
```

**戻り値:** 電流値（A）

**例:**
```python
# チャンネル1の電流を測定
ngx.write('INSTrument:NSELect 1')
current = float(ngx.query('MEASure:CURRent?'))
```

---

### READ? - 電圧・電流同時測定

選択中のチャンネルの電圧と電流を同時に測定します。

**構文:**
```
READ?
```

**戻り値:** `<電圧>,<電流>` （カンマ区切り）

**例:**
```python
# チャンネル1の電圧・電流を同時測定
ngx.write('INSTrument:NSELect 1')
response = ngx.query('READ?')
values = response.split(',')
voltage = float(values[0])
current = float(values[1])

print(f"電圧: {voltage} V, 電流: {current} A")
```

---

## SYSTemサブシステム

システム設定やネットワーク設定を行います。

### SYSTem:COMMunicate:SOCKet:DHCP - DHCP設定

DHCPの有効/無効を設定します。

**構文:**
```
SYSTem:COMMunicate:SOCKet:DHCP <状態>
SYSTem:COMMunicate:SOCKet:DHCP?
```

**パラメータ:**
- `<状態>`: `ON` | `OFF` | `1` | `0`

**例:**
```python
# DHCPを有効化
ngx.write('SYSTem:COMMunicate:SOCKet:DHCP ON')

# 設定確認
dhcp = ngx.query('SYSTem:COMMunicate:SOCKet:DHCP?')
```

---

### SYSTem:COMMunicate:SOCKet:IPADdress? - IPアドレス取得

現在のIPアドレスを取得します。

**構文:**
```
SYSTem:COMMunicate:SOCKet:IPADdress?
```

**戻り値:** IPアドレス（文字列）

**例:**
```python
ip_address = ngx.query('SYSTem:COMMunicate:SOCKet:IPADdress?')
print(f"IPアドレス: {ip_address}")
```

---

### SYSTem:ERRor? - エラー情報取得

エラーキューから最も古いエラーを取得します。

**構文:**
```
SYSTem:ERRor?
```

**短縮形:**
```
SYST:ERR?
```

**戻り値:** `<エラー番号>,"<エラーメッセージ>"`

**例:**
```python
error = ngx.query('SYSTem:ERRor?')
print(f"エラー: {error}")
# 例: "0,No error"
```

---

## コマンド使用例

### 基本的な出力制御シーケンス

```python
import pyvisa
import time

# 接続
rm = pyvisa.ResourceManager('@py')
ngx = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR')

# 1. 機器識別
print(ngx.query('*IDN?'))

# 2. リセット
ngx.write('*RST')
time.sleep(1)

# 3. 全出力をOFF
ngx.write('OUTPut:GENeral:STATe OFF')

# 4. チャンネル1を設定
ngx.write('INSTrument:NSELect 1')
ngx.write('SOURce:VOLTage:LEVel:IMMediate:AMPlitude 3.3')
ngx.write('SOURce:CURRent:LEVel:IMMediate:AMPlitude 1.0')
ngx.write('OUTPut:SELect ON')

# 5. チャンネル2を設定
ngx.write('INSTrument:NSELect 2')
ngx.write('SOURce:VOLTage:LEVel:IMMediate:AMPlitude 5.0')
ngx.write('SOURce:CURRent:LEVel:IMMediate:AMPlitude 0.5')
ngx.write('OUTPut:SELect ON')

# 6. 全出力をON
ngx.write('OUTPut:GENeral:STATe ON')
time.sleep(0.5)

# 7. 測定
ngx.write('INSTrument:NSELect 1')
response = ngx.query('READ?')
values = response.split(',')
print(f"Ch1: {values[0]} V, {values[1]} A")

# 8. 出力をOFF
ngx.write('OUTPut:GENeral:STATe OFF')

# 接続終了
ngx.close()
```

---

## コマンド短縮形一覧

SCPIコマンドは、大文字部分のみを使用して短縮できます。

| 完全形 | 短縮形 |
|--------|--------|
| `INSTrument:NSELect` | `INST:NSEL` |
| `OUTPut:GENeral:STATe` | `OUTP:GEN:STAT` |
| `OUTPut:SELect` | `OUTP:SEL` |
| `SOURce:VOLTage:LEVel:IMMediate:AMPlitude` | `SOUR:VOLT:LEV:IMM:AMPL` または `VOLT` |
| `SOURce:CURRent:LEVel:IMMediate:AMPlitude` | `SOUR:CURR:LEV:IMM:AMPL` または `CURR` |
| `MEASure:VOLTage` | `MEAS:VOLT` |
| `MEASure:CURRent` | `MEAS:CURR` |

**推奨:** 可読性のため、完全形または一般的な短縮形（`VOLT`, `CURR`など）の使用を推奨します。

---

## エラー処理

### エラーの確認

コマンド実行後、エラーが発生していないか確認することを推奨します：

```python
def check_error(ngx):
    """エラーをチェックして表示"""
    error = ngx.query('SYSTem:ERRor?')
    if not error.startswith('0,'):
        print(f"警告: {error}")
        return True
    return False

# 使用例
ngx.write('VOLTage 3.3')
check_error(ngx)
```

### よくあるエラー

| エラーコード | 説明 | 対処法 |
|-------------|------|--------|
| -100 | コマンドエラー | コマンド構文を確認 |
| -200 | 実行エラー | パラメータ範囲を確認 |
| -300 | デバイス依存エラー | 機器の状態を確認 |
| -400 | クエリエラー | クエリコマンドの使用方法を確認 |

---

## 参考資料

- [NGP800 User Manual - SCPI Command Structure (Page 157)](https://www.manualslib.com/manual/1834650/Rohde-And-Schwarz-RAnds-Ngp800-Series.html?page=157)
- [NGP800 User Manual - Configuration Commands (Page 117)](https://www.manualslib.com/manual/2605820/Rohde-And-Schwarz-Ngp800-Series.html?page=117)
- [SCPI Standard Documentation](https://www.ivifoundation.org/downloads/SCPI/)
