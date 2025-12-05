#!/usr/bin/env python3
"""
NGP800 Power Supply Control Script for Raspberry Pi
Periodic ON/OFF control: 55 seconds ON, 5 seconds OFF

Requirements:
    pip install pyvisa pyvisa-py

Usage:
    python3 ngp800_control.py

Configuration:
    Edit the POWER_SUPPLY_IP variable below to match your NGP800's IP address.
"""

import time
import pyvisa
import signal
import sys


class NGP800Controller:
    """
    Rohde & Schwarz NGP800 Power Supply Controller using PyVISA
    """

    def __init__(self, resource_string, timeout=5000):
        """
        Initialize connection to NGP800

        Args:
            resource_string: VISA resource string (e.g., 'TCPIP0::192.168.1.100::inst0::INSTR')
            timeout: Communication timeout in milliseconds (default: 5000)
        """
        self.rm = pyvisa.ResourceManager('@py')
        try:
            self.instrument = self.rm.open_resource(resource_string)
            self.instrument.timeout = timeout
            self.instrument.read_termination = '\n'
            self.instrument.write_termination = '\n'
        except Exception as e:
            print(f"Error connecting to instrument: {e}")
            raise

    def query(self, command):
        """Send a query command and return the response"""
        return self.instrument.query(command).strip()

    def write(self, command):
        """Send a write command"""
        self.instrument.write(command)

    def get_idn(self):
        """Get instrument identification"""
        return self.query('*IDN?')

    def reset(self):
        """Reset the instrument to default state"""
        self.write('*RST')
        time.sleep(1)  # Wait for reset to complete

    def set_general_output_state(self, state):
        """
        Master switch for all outputs

        Args:
            state: True for ON, False for OFF
        """
        state_str = 'ON' if state else 'OFF'
        self.write(f'OUTPut:GENeral:STATe {state_str}')

    def select_channel(self, channel):
        """
        Select instrument channel

        Args:
            channel: Channel number (1-4 depending on model)
        """
        self.write(f'INSTrument:SELect {channel}')

    def set_voltage(self, voltage):
        """
        Set voltage for currently selected channel

        Args:
            voltage: Voltage in Volts
        """
        self.write(f'SOURce:VOLTage:LEVel:IMMediate:AMPlitude {voltage}')

    def set_current(self, current):
        """
        Set current limit for currently selected channel

        Args:
            current: Current in Amperes
        """
        self.write(f'SOURce:CURRent:LEVel:IMMediate:AMPlitude {current}')

    def set_output_select(self, state):
        """
        Prepare channel output for master switch

        Args:
            state: True for ON, False for OFF
        """
        state_str = 'ON' if state else 'OFF'
        self.write(f'OUTPut:SELect {state_str}')

    def read_measurement(self):
        """
        Read voltage and current measurement from currently selected channel

        Returns:
            tuple: (voltage, current) in V and A
        """
        response = self.query('READ?')
        # Response format: "voltage,current"
        values = response.split(',')
        voltage = float(values[0])
        current = float(values[1])
        return voltage, current

    def close(self):
        """Close the connection"""
        if hasattr(self, 'instrument'):
            self.instrument.close()
        if hasattr(self, 'rm'):
            self.rm.close()


def initialize_power_supply(ngx):
    """
    Initialize power supply with default channel configurations

    Args:
        ngx: NGP800Controller instance
    """
    print("\n" + "=" * 60)
    print("Initializing Power Supply")
    print("=" * 60)

    # Reset instrument
    print("\nResetting instrument...")
    ngx.reset()

    # Master switch for all the outputs - switch OFF
    print("Turning OFF all outputs (master switch)...")
    ngx.set_general_output_state(False)

    # Configure Output 1
    print("\nConfiguring Output 1:")
    print("  - Selecting channel 1")
    ngx.select_channel(1)
    print("  - Setting voltage: 3.3 V")
    ngx.set_voltage(3.3)
    print("  - Setting current limit: 0.1 A")
    ngx.set_current(0.1)
    print("  - Preparing output for master switch ON")
    ngx.set_output_select(True)

    # Configure Output 2
    print("\nConfiguring Output 2:")
    print("  - Selecting channel 2")
    ngx.select_channel(2)
    print("  - Setting voltage: 5.1 V")
    ngx.set_voltage(5.1)
    print("  - Setting current limit: 0.05 A")
    ngx.set_current(0.05)
    print("  - Preparing output for master switch ON")
    ngx.set_output_select(True)

    print("\n" + "=" * 60)
    print("Initialization completed!")
    print("=" * 60)


def turn_on_outputs(ngx):
    """
    Turn ON all configured outputs

    Args:
        ngx: NGP800Controller instance
    """
    print("\n🟢 Turning ON all outputs...")
    ngx.set_general_output_state(True)

    # Wait for outputs to settle
    time.sleep(0.5)

    # Read and display measurements
    ngx.select_channel(1)
    voltage1, current1 = ngx.read_measurement()
    print(f"   Output 1: {voltage1:.4f} V, {current1:.6f} A")

    ngx.select_channel(2)
    voltage2, current2 = ngx.read_measurement()
    print(f"   Output 2: {voltage2:.4f} V, {current2:.6f} A")


def turn_off_outputs(ngx):
    """
    Turn OFF all outputs

    Args:
        ngx: NGP800Controller instance
    """
    print("\n🔴 Turning OFF all outputs...")
    ngx.set_general_output_state(False)


def main():
    """
    Main function: Initialize and run periodic ON/OFF cycle
    55 seconds ON, 5 seconds OFF
    """

    # Configuration - Edit this to match your NGP800's IP address
    POWER_SUPPLY_IP = '192.168.0.10'  # Change to your NGP800's IP address

    # Timing configuration
    ON_TIME = 55   # seconds
    OFF_TIME = 5   # seconds

    # Create resource string for TCP/IP connection
    resource_string = f'TCPIP0::{POWER_SUPPLY_IP}::inst0::INSTR'

    print("=" * 60)
    print("NGP800 Power Supply Periodic Control")
    print("=" * 60)
    print(f"Cycle: {ON_TIME} sec ON, {OFF_TIME} sec OFF")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    ngx = None

    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n" + "=" * 60)
        print("Ctrl+C detected. Shutting down...")
        print("=" * 60)
        if ngx:
            try:
                turn_off_outputs(ngx)
                ngx.close()
                print("Power supply outputs turned OFF and connection closed.")
            except Exception as e:
                print(f"Error during shutdown: {e}")
        sys.exit(0)

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Connect to the power supply
        print(f"\nConnecting to {resource_string}...")
        ngx = NGP800Controller(resource_string)

        # Get instrument identification
        idn = ngx.get_idn()
        print(f'\nConnected to: {idn}')

        # Initialize power supply
        initialize_power_supply(ngx)

        # Periodic ON/OFF cycle
        print("\n" + "=" * 60)
        print("Starting periodic cycle...")
        print("=" * 60)

        cycle_count = 0

        while True:
            cycle_count += 1
            print(f"\n--- Cycle {cycle_count} ---")

            # Turn ON
            turn_on_outputs(ngx)
            print(f"Outputs will remain ON for {ON_TIME} seconds...")
            time.sleep(ON_TIME)

            # Turn OFF
            turn_off_outputs(ngx)
            print(f"Outputs will remain OFF for {OFF_TIME} seconds...")
            time.sleep(OFF_TIME)

    except pyvisa.errors.VisaIOError as e:
        print(f"\n❌ VISA Error: {e}")
        print("\nPlease check:")
        print("  1. The IP address is correct")
        print("  2. The NGP800 is powered on and connected to the network")
        print("  3. The SCPI interface is enabled on the instrument")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # Ensure outputs are turned off on exit
        if ngx:
            try:
                turn_off_outputs(ngx)
                ngx.close()
            except:
                pass


if __name__ == '__main__':
    main()
