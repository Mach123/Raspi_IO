#!/usr/bin/env python3
"""
NGP800 Simple Control Utility
個別チャンネルのON/OFFとパラメータ設定を簡単に行うためのユーティリティ

Usage examples:
    # チャンネル1を3.3V/1Aで出力ON
    python3 ngp800_simple_control.py --ip 192.168.1.100 --channel 1 --voltage 3.3 --current 1.0 --on

    # チャンネル2を出力OFF
    python3 ngp800_simple_control.py --ip 192.168.1.100 --channel 2 --off

    # 全チャンネルの状態を表示
    python3 ngp800_simple_control.py --ip 192.168.1.100 --status
"""

import argparse
import sys
import pyvisa
from ngp800_control import NGP800Controller


def print_channel_status(ngx, channel):
    """指定チャンネルの状態を表示"""
    ngx.select_channel(channel)
    voltage, current = ngx.read_measurement()
    print(f"  Channel {channel}: {voltage:.4f} V, {current:.6f} A")


def main():
    parser = argparse.ArgumentParser(
        description='NGP800 Power Supply Simple Control Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # チャンネル1を3.3V/1Aで出力ON
  %(prog)s --ip 192.168.1.100 --channel 1 --voltage 3.3 --current 1.0 --on

  # チャンネル2を出力OFF
  %(prog)s --ip 192.168.1.100 --channel 2 --off

  # 全チャンネルの状態を表示
  %(prog)s --ip 192.168.1.100 --status

  # 全出力をOFF (マスタースイッチ)
  %(prog)s --ip 192.168.1.100 --all-off
        """
    )

    parser.add_argument('--ip', required=True, help='NGP800のIPアドレス')
    parser.add_argument('--channel', type=int, choices=[1, 2, 3, 4],
                        help='チャンネル番号 (1-4)')
    parser.add_argument('--voltage', type=float, help='設定電圧 (V)')
    parser.add_argument('--current', type=float, help='設定電流リミット (A)')
    parser.add_argument('--on', action='store_true', help='出力をON')
    parser.add_argument('--off', action='store_true', help='出力をOFF')
    parser.add_argument('--all-on', action='store_true',
                        help='全出力をON (マスタースイッチ)')
    parser.add_argument('--all-off', action='store_true',
                        help='全出力をOFF (マスタースイッチ)')
    parser.add_argument('--status', action='store_true',
                        help='全チャンネルの状態を表示')
    parser.add_argument('--reset', action='store_true', help='機器をリセット')

    args = parser.parse_args()

    # 引数の妥当性チェック
    if args.on and args.off:
        print("Error: --on と --off は同時に指定できません")
        sys.exit(1)

    if (args.voltage or args.current or args.on or args.off) and not args.channel:
        print("Error: --channel を指定してください")
        sys.exit(1)

    # NGP800に接続
    resource_string = f'TCPIP0::{args.ip}::inst0::INSTR'
    print(f"Connecting to {resource_string}...")

    try:
        ngx = NGP800Controller(resource_string)
        idn = ngx.get_idn()
        print(f"Connected: {idn}\n")

        # リセット
        if args.reset:
            print("Resetting instrument...")
            ngx.reset()
            print("Reset completed\n")

        # 全出力ON/OFF (マスタースイッチ)
        if args.all_on:
            print("Turning ON all outputs (master switch)...")
            ngx.set_general_output_state(True)
            print("All outputs ON\n")

        if args.all_off:
            print("Turning OFF all outputs (master switch)...")
            ngx.set_general_output_state(False)
            print("All outputs OFF\n")

        # チャンネル個別制御
        if args.channel:
            print(f"Selecting Channel {args.channel}...")
            ngx.select_channel(args.channel)

            # 電圧設定
            if args.voltage is not None:
                print(f"Setting voltage: {args.voltage} V")
                ngx.set_voltage(args.voltage)

            # 電流設定
            if args.current is not None:
                print(f"Setting current limit: {args.current} A")
                ngx.set_current(args.current)

            # 出力ON
            if args.on:
                print(f"Turning ON Channel {args.channel}")
                ngx.set_output_select(True)
                # マスタースイッチもONにする場合
                ngx.set_general_output_state(True)

            # 出力OFF
            if args.off:
                print(f"Turning OFF Channel {args.channel}")
                ngx.set_output_select(False)

            print()

        # 状態表示
        if args.status:
            print("Reading channel status...")
            # NGP800のモデルに応じてチャンネル数を調整（ここでは4チャンネルと仮定）
            max_channels = 4
            for ch in range(1, max_channels + 1):
                try:
                    print_channel_status(ngx, ch)
                except:
                    # チャンネルが存在しない場合はスキップ
                    pass
            print()

        print("Operation completed successfully!")
        ngx.close()

    except pyvisa.errors.VisaIOError as e:
        print(f"\nVISA Error: {e}")
        print("接続を確認してください:")
        print(f"  - IPアドレス: {args.ip}")
        print("  - NGP800がネットワークに接続されているか")
        print("  - SCPIインターフェースが有効か")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
