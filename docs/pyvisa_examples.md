# NGP800 PyVISA 実装例集

## 目次

1. [基本的な接続](#基本的な接続)
2. [チャンネル制御](#チャンネル制御)
3. [電圧・電流設定](#電圧電流設定)
4. [測定](#測定)
5. [高度な使用例](#高度な使用例)
6. [エラーハンドリング](#エラーハンドリング)
7. [ベストプラクティス](#ベストプラクティス)

---

## 基本的な接続

### 最小限の接続例

```python
import pyvisa

# PyVISAリソースマネージャを作成（Python純正バックエンド使用）
rm = pyvisa.ResourceManager('@py')

# NGP800に接続
ngx = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR')

# 機器識別
print(ngx.query('*IDN?'))

# 接続を閉じる
ngx.close()
```

### 完全な接続設定例

```python
import pyvisa

# リソースマネージャ作成
rm = pyvisa.ResourceManager('@py')

# 接続設定付きでオープン
ngx = rm.open_resource(
    'TCPIP0::192.168.1.100::inst0::INSTR',
    timeout=5000,              # タイムアウト: 5秒
    read_termination='\n',     # 読み取り終端文字
    write_termination='\n'     # 書き込み終端文字
)

# エンコーディング設定（必要に応じて）
ngx.encoding = 'utf-8'

print(f"Connected to: {ngx.query('*IDN?')}")

ngx.close()
rm.close()
```

### 接続確認の完全な例

```python
import pyvisa
import sys

def connect_ngp800(ip_address, timeout=5000):
    """
    NGP800に接続し、接続を確認する

    Args:
        ip_address: NGP800のIPアドレス
        timeout: タイムアウト（ミリ秒）

    Returns:
        pyvisa.Resource: 接続されたリソース

    Raises:
        Exception: 接続に失敗した場合
    """
    try:
        rm = pyvisa.ResourceManager('@py')
        resource_string = f'TCPIP0::{ip_address}::inst0::INSTR'

        print(f"Connecting to {resource_string}...")
        ngx = rm.open_resource(resource_string)
        ngx.timeout = timeout
        ngx.read_termination = '\n'
        ngx.write_termination = '\n'

        # 接続確認
        idn = ngx.query('*IDN?')
        print(f"Successfully connected: {idn}")

        return ngx

    except pyvisa.errors.VisaIOError as e:
        print(f"VISA Error: {e}", file=sys.stderr)
        print("Please check:", file=sys.stderr)
        print(f"  - IP address: {ip_address}", file=sys.stderr)
        print("  - Network connectivity", file=sys.stderr)
        print("  - NGP800 is powered on", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        raise

# 使用例
try:
    ngx = connect_ngp800('192.168.1.100')
    # ここで操作を行う
    ngx.close()
except Exception:
    sys.exit(1)
```

---

## チャンネル制御

### チャンネル選択

```python
# チャンネル1を選択
ngx.write('INSTrument:NSELect 1')

# 現在のチャンネルを確認
current_channel = int(ngx.query('INSTrument:NSELect?'))
print(f"Current channel: {current_channel}")
```

### チャンネル切り替え（コンテキストマネージャ）

```python
class ChannelSelector:
    """チャンネル選択のコンテキストマネージャ"""

    def __init__(self, instrument, channel):
        self.instrument = instrument
        self.channel = channel
        self.previous_channel = None

    def __enter__(self):
        # 現在のチャンネルを保存
        self.previous_channel = int(
            self.instrument.query('INSTrument:NSELect?')
        )
        # 新しいチャンネルを選択
        self.instrument.write(f'INSTrument:NSELect {self.channel}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 元のチャンネルに戻す
        if self.previous_channel is not None:
            self.instrument.write(
                f'INSTrument:NSELect {self.previous_channel}'
            )

# 使用例
with ChannelSelector(ngx, 1):
    # チャンネル1で操作
    ngx.write('VOLTage 3.3')
    voltage = ngx.query('VOLTage?')
    print(f"Ch1 voltage: {voltage}")
# 自動的に元のチャンネルに戻る
```

---

## 電圧・電流設定

### 基本的な設定

```python
# チャンネル1を選択
ngx.write('INSTrument:NSELect 1')

# 電圧を3.3Vに設定
ngx.write('VOLTage 3.3')

# 電流リミットを1Aに設定
ngx.write('CURRent 1.0')

# 設定値の確認
voltage = float(ngx.query('VOLTage?'))
current = float(ngx.query('CURRent?'))
print(f"Set: {voltage}V, {current}A")
```

### 複数チャンネルの一括設定

```python
def setup_channels(ngx, channel_configs):
    """
    複数チャンネルを一括設定

    Args:
        ngx: PyVISAリソース
        channel_configs: dict {channel: (voltage, current)}
    """
    for channel, (voltage, current) in channel_configs.items():
        ngx.write(f'INSTrument:NSELect {channel}')
        ngx.write(f'VOLTage {voltage}')
        ngx.write(f'CURRent {current}')
        print(f"Ch{channel}: {voltage}V, {current}A")

# 使用例
configs = {
    1: (3.3, 1.0),   # Ch1: 3.3V, 1.0A
    2: (5.0, 0.5),   # Ch2: 5.0V, 0.5A
    3: (12.0, 0.3),  # Ch3: 12.0V, 0.3A
}

setup_channels(ngx, configs)
```

### 範囲チェック付き設定

```python
class NGP800ChannelConfig:
    """NGP800チャンネル設定（範囲チェック付き）"""

    # モデルごとの最大値（例）
    VOLTAGE_MAX = {1: 32, 2: 32, 3: 6, 4: 6}  # NGP824の例
    CURRENT_MAX = {1: 10, 2: 10, 3: 10, 4: 10}

    def __init__(self, instrument):
        self.instrument = instrument

    def set_voltage(self, channel, voltage):
        """電圧設定（範囲チェック付き）"""
        max_voltage = self.VOLTAGE_MAX.get(channel, 32)

        if not 0 <= voltage <= max_voltage:
            raise ValueError(
                f"Voltage {voltage}V out of range (0-{max_voltage}V)"
            )

        self.instrument.write(f'INSTrument:NSELect {channel}')
        self.instrument.write(f'VOLTage {voltage}')
        print(f"Ch{channel} voltage set to {voltage}V")

    def set_current(self, channel, current):
        """電流設定（範囲チェック付き）"""
        max_current = self.CURRENT_MAX.get(channel, 10)

        if not 0 <= current <= max_current:
            raise ValueError(
                f"Current {current}A out of range (0-{max_current}A)"
            )

        self.instrument.write(f'INSTrument:NSELect {channel}')
        self.instrument.write(f'CURRent {current}')
        print(f"Ch{channel} current limit set to {current}A")

# 使用例
config = NGP800ChannelConfig(ngx)
try:
    config.set_voltage(1, 3.3)
    config.set_current(1, 1.0)
except ValueError as e:
    print(f"設定エラー: {e}")
```

---

## 測定

### 基本的な測定

```python
# チャンネル1を選択
ngx.write('INSTrument:NSELect 1')

# 電圧測定
voltage = float(ngx.query('MEASure:VOLTage?'))
print(f"Voltage: {voltage}V")

# 電流測定
current = float(ngx.query('MEASure:CURRent?'))
print(f"Current: {current}A")

# 電圧と電流を同時測定
response = ngx.query('READ?')
values = response.split(',')
voltage = float(values[0])
current = float(values[1])
print(f"Measured: {voltage}V, {current}A")
```

### 複数チャンネルの測定

```python
def measure_all_channels(ngx, num_channels=4):
    """
    全チャンネルの測定

    Args:
        ngx: PyVISAリソース
        num_channels: チャンネル数

    Returns:
        dict: {channel: (voltage, current)}
    """
    measurements = {}

    for channel in range(1, num_channels + 1):
        try:
            ngx.write(f'INSTrument:NSELect {channel}')
            response = ngx.query('READ?')
            values = response.split(',')
            voltage = float(values[0])
            current = float(values[1])
            measurements[channel] = (voltage, current)
        except Exception as e:
            print(f"Ch{channel} measurement failed: {e}")
            measurements[channel] = (None, None)

    return measurements

# 使用例
results = measure_all_channels(ngx, num_channels=4)
for channel, (voltage, current) in results.items():
    if voltage is not None:
        power = voltage * current
        print(f"Ch{channel}: {voltage:.4f}V, {current:.6f}A, {power:.6f}W")
```

### 連続測定（ロギング）

```python
import time
from datetime import datetime

def continuous_measurement(ngx, channel, duration_sec=10, interval_sec=1):
    """
    連続測定とロギング

    Args:
        ngx: PyVISAリソース
        channel: チャンネル番号
        duration_sec: 測定時間（秒）
        interval_sec: 測定間隔（秒）
    """
    ngx.write(f'INSTrument:NSELect {channel}')

    start_time = time.time()
    end_time = start_time + duration_sec

    print(f"{'Time':<20} {'Voltage (V)':<15} {'Current (A)':<15} {'Power (W)':<15}")
    print("-" * 65)

    while time.time() < end_time:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = ngx.query('READ?')
        values = response.split(',')
        voltage = float(values[0])
        current = float(values[1])
        power = voltage * current

        print(f"{timestamp:<20} {voltage:<15.4f} {current:<15.6f} {power:<15.6f}")

        time.sleep(interval_sec)

# 使用例
continuous_measurement(ngx, channel=1, duration_sec=30, interval_sec=2)
```

---

## 高度な使用例

### シーケンス制御

```python
import time

def power_sequence(ngx, sequence_steps):
    """
    電源投入シーケンス

    Args:
        ngx: PyVISAリソース
        sequence_steps: list of (channel, voltage, current, delay)
    """
    print("Power-on sequence started...")

    # 全出力をOFF
    ngx.write('OUTPut:GENeral:STATe OFF')

    for step, (channel, voltage, current, delay) in enumerate(sequence_steps, 1):
        print(f"\nStep {step}: Ch{channel} - {voltage}V, {current}A")

        # チャンネル設定
        ngx.write(f'INSTrument:NSELect {channel}')
        ngx.write(f'VOLTage {voltage}')
        ngx.write(f'CURRent {current}')
        ngx.write('OUTPut:SELect ON')

        # 出力ON
        ngx.write('OUTPut:GENeral:STATe ON')

        # 待機
        if delay > 0:
            print(f"Waiting {delay}s...")
            time.sleep(delay)

        # 測定
        response = ngx.query('READ?')
        values = response.split(',')
        print(f"Measured: {values[0]}V, {values[1]}A")

    print("\nPower-on sequence completed!")

# 使用例: 段階的な電源投入
sequence = [
    (1, 3.3, 1.0, 1.0),   # Ch1: 3.3V, 1A, 1秒待機
    (2, 5.0, 0.5, 0.5),   # Ch2: 5.0V, 0.5A, 0.5秒待機
    (3, 12.0, 0.3, 0.5),  # Ch3: 12V, 0.3A, 0.5秒待機
]

power_sequence(ngx, sequence)
```

### 過電流検出

```python
def monitor_overcurrent(ngx, channel, current_limit, check_interval=0.1):
    """
    過電流監視

    Args:
        ngx: PyVISAリソース
        channel: チャンネル番号
        current_limit: 電流制限値（A）
        check_interval: チェック間隔（秒）
    """
    ngx.write(f'INSTrument:NSELect {channel}')

    print(f"Monitoring Ch{channel} for overcurrent (limit: {current_limit}A)")
    print("Press Ctrl+C to stop")

    try:
        while True:
            response = ngx.query('READ?')
            values = response.split(',')
            voltage = float(values[0])
            current = float(values[1])

            if current > current_limit:
                print(f"\n⚠ OVERCURRENT DETECTED!")
                print(f"Ch{channel}: {voltage}V, {current}A")

                # 出力をOFF
                ngx.write('OUTPut OFF')
                print("Output turned OFF for safety")
                break

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

# 使用例
monitor_overcurrent(ngx, channel=1, current_limit=1.5)
```

---

## エラーハンドリング

### エラーチェック関数

```python
def check_scpi_error(ngx):
    """
    SCPIエラーをチェック

    Returns:
        tuple: (error_code, error_message)
    """
    response = ngx.query('SYSTem:ERRor?')
    parts = response.split(',', 1)
    error_code = int(parts[0])
    error_message = parts[1].strip('"') if len(parts) > 1 else ""

    return error_code, error_message

# 使用例
ngx.write('VOLTage 3.3')
error_code, error_message = check_scpi_error(ngx)

if error_code != 0:
    print(f"Error {error_code}: {error_message}")
else:
    print("No error")
```

### デコレータによるエラーチェック

```python
from functools import wraps

def with_error_check(func):
    """SCPIコマンド実行後にエラーをチェックするデコレータ"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        # エラーチェック
        response = self.instrument.query('SYSTem:ERRor?')
        if not response.startswith('0,'):
            print(f"⚠ SCPI Error after {func.__name__}: {response}")

        return result

    return wrapper

class NGP800WithErrorCheck:
    def __init__(self, instrument):
        self.instrument = instrument

    @with_error_check
    def set_voltage(self, channel, voltage):
        """電圧設定（エラーチェック付き）"""
        self.instrument.write(f'INSTrument:NSELect {channel}')
        self.instrument.write(f'VOLTage {voltage}')

    @with_error_check
    def set_current(self, channel, current):
        """電流設定（エラーチェック付き）"""
        self.instrument.write(f'INSTrument:NSELect {channel}')
        self.instrument.write(f'CURRent {current}')

# 使用例
ngp = NGP800WithErrorCheck(ngx)
ngp.set_voltage(1, 3.3)  # エラーがあれば自動的に表示
```

### リトライ機能

```python
import time
from functools import wraps

def retry_on_timeout(max_retries=3, delay=1.0):
    """タイムアウト時にリトライするデコレータ"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except pyvisa.errors.VisaIOError as e:
                    if 'VI_ERROR_TMO' in str(e):
                        if attempt < max_retries - 1:
                            print(f"Timeout, retrying... ({attempt + 1}/{max_retries})")
                            time.sleep(delay)
                        else:
                            print(f"Failed after {max_retries} retries")
                            raise
                    else:
                        raise
        return wrapper
    return decorator

@retry_on_timeout(max_retries=3, delay=1.0)
def query_with_retry(ngx, command):
    """リトライ付きクエリ"""
    return ngx.query(command)

# 使用例
try:
    idn = query_with_retry(ngx, '*IDN?')
    print(idn)
except pyvisa.errors.VisaIOError as e:
    print(f"Communication failed: {e}")
```

---

## ベストプラクティス

### リソース管理（コンテキストマネージャ）

```python
class NGP800Connection:
    """NGP800接続のコンテキストマネージャ"""

    def __init__(self, ip_address, timeout=5000):
        self.ip_address = ip_address
        self.timeout = timeout
        self.rm = None
        self.instrument = None

    def __enter__(self):
        self.rm = pyvisa.ResourceManager('@py')
        resource_string = f'TCPIP0::{self.ip_address}::inst0::INSTR'
        self.instrument = self.rm.open_resource(resource_string)
        self.instrument.timeout = self.timeout
        self.instrument.read_termination = '\n'
        self.instrument.write_termination = '\n'

        # 接続確認
        idn = self.instrument.query('*IDN?')
        print(f"Connected: {idn}")

        return self.instrument

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.instrument:
            self.instrument.close()
        if self.rm:
            self.rm.close()
        print("Connection closed")

# 使用例
with NGP800Connection('192.168.1.100') as ngx:
    ngx.write('INSTrument:NSELect 1')
    ngx.write('VOLTage 3.3')
    voltage = ngx.query('VOLTage?')
    print(f"Voltage: {voltage}")
# 自動的に接続がクローズされる
```

### 設定の保存と復元

```python
def save_channel_config(ngx, channel):
    """チャンネル設定を保存"""
    ngx.write(f'INSTrument:NSELect {channel}')

    config = {
        'voltage': float(ngx.query('VOLTage?')),
        'current': float(ngx.query('CURRent?')),
        'output': bool(int(ngx.query('OUTPut?'))),
    }

    return config

def restore_channel_config(ngx, channel, config):
    """チャンネル設定を復元"""
    ngx.write(f'INSTrument:NSELect {channel}')
    ngx.write(f'VOLTage {config["voltage"]}')
    ngx.write(f'CURRent {config["current"]}')

    if config['output']:
        ngx.write('OUTPut ON')
    else:
        ngx.write('OUTPut OFF')

# 使用例
# 設定を保存
original_config = save_channel_config(ngx, 1)

# 一時的に変更
ngx.write('INSTrument:NSELect 1')
ngx.write('VOLTage 5.0')

# 元に戻す
restore_channel_config(ngx, 1, original_config)
```

---

## 完全なアプリケーション例

```python
#!/usr/bin/env python3
"""NGP800 完全制御アプリケーション例"""

import pyvisa
import time
import sys
from contextlib import contextmanager

class NGP800Controller:
    """NGP800電源制御クラス"""

    def __init__(self, ip_address, timeout=5000):
        self.rm = pyvisa.ResourceManager('@py')
        resource_string = f'TCPIP0::{ip_address}::inst0::INSTR'

        try:
            self.instrument = self.rm.open_resource(resource_string)
            self.instrument.timeout = timeout
            self.instrument.read_termination = '\n'
            self.instrument.write_termination = '\n'

            idn = self.instrument.query('*IDN?')
            print(f"Connected: {idn}")
        except Exception as e:
            print(f"Connection failed: {e}")
            raise

    @contextmanager
    def channel(self, channel_number):
        """チャンネル選択コンテキストマネージャ"""
        self.instrument.write(f'INSTrument:NSELect {channel_number}')
        yield

    def set_voltage(self, voltage):
        """電圧設定（現在のチャンネル）"""
        self.instrument.write(f'VOLTage {voltage}')

    def set_current(self, current):
        """電流設定（現在のチャンネル）"""
        self.instrument.write(f'CURRent {current}')

    def enable_output(self, state=True):
        """出力ON/OFF（現在のチャンネル）"""
        self.instrument.write(f'OUTPut {"ON" if state else "OFF"}')

    def measure(self):
        """測定（現在のチャンネル）"""
        response = self.instrument.query('READ?')
        values = response.split(',')
        return float(values[0]), float(values[1])

    def master_output(self, state=True):
        """全出力マスタースイッチ"""
        self.instrument.write(f'OUTPut:GENeral:STATe {"ON" if state else "OFF"}')

    def close(self):
        """接続をクローズ"""
        if hasattr(self, 'instrument'):
            self.instrument.close()
        if hasattr(self, 'rm'):
            self.rm.close()

def main():
    # NGP800に接続
    ngp = NGP800Controller('192.168.1.100')

    try:
        # チャンネル1を設定
        with ngp.channel(1):
            ngp.set_voltage(3.3)
            ngp.set_current(1.0)
            ngp.enable_output(True)

        # チャンネル2を設定
        with ngp.channel(2):
            ngp.set_voltage(5.0)
            ngp.set_current(0.5)
            ngp.enable_output(True)

        # 全出力をON
        ngp.master_output(True)
        time.sleep(0.5)

        # 測定
        with ngp.channel(1):
            v, i = ngp.measure()
            print(f"Ch1: {v:.4f}V, {i:.6f}A")

        with ngp.channel(2):
            v, i = ngp.measure()
            print(f"Ch2: {v:.4f}V, {i:.6f}A")

        # 全出力をOFF
        ngp.master_output(False)

    finally:
        ngp.close()

if __name__ == '__main__':
    main()
```

---

## 参考資料

- [PyVISA Documentation](https://pyvisa.readthedocs.io/)
- [Rohde-Schwarz GitHub Examples](https://github.com/Rohde-Schwarz/Examples)
- [RsInstrument Python Module](https://github.com/Rohde-Schwarz/RsInstrument)
- [NGP800 SCPI Command Reference](./scpi_command_reference.md)
