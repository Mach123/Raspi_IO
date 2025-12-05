#!/usr/bin/env python3
"""
NGP800 Power Supply Control Script for Raspberry Pi
Based on RsNgx_GettingStarted_Example.py

Requirements:
    pip install pyvisa pyvisa-py

Usage:
    python3 ngp800_control.py

Configuration:
    Edit the POWER_SUPPLY_IP variable below to match your NGP800's IP address.
"""

import time
import pyvisa


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


def main():
    """Main function demonstrating NGP800 control"""

    # Configuration - Edit this to match your NGP800's IP address
    POWER_SUPPLY_IP = '192.168.0.10'  # Change to your NGP800's IP address

    # Create resource string for TCP/IP connection
    resource_string = f'TCPIP0::{POWER_SUPPLY_IP}::inst0::INSTR'

    print("=" * 60)
    print("NGP800 Power Supply Control Script")
    print("=" * 60)

    try:
        # Connect to the power supply
        print(f"\nConnecting to {resource_string}...")
        ngx = NGP800Controller(resource_string)

        # Greetings, stranger...
        idn = ngx.get_idn()
        print(f'\nHello, I am: {idn}')

        # Reset instrument
        print("\nResetting instrument...")
        ngx.reset()

        # Master switch for all the outputs - switch OFF
        print("Turning OFF all outputs (master switch)...")
        ngx.set_general_output_state(False)

        # Select and set Output 1
        print("\nConfiguring Output 1:")
        print("  - Selecting channel 1")
        ngx.select_channel(1)
        print("  - Setting voltage: 3.3 V")
        ngx.set_voltage(3.3)
        print("  - Setting current limit: 0.1 A")
        ngx.set_current(0.1)
        print("  - Preparing output for master switch ON")
        ngx.set_output_select(True)

        # Select and set Output 2
        print("\nConfiguring Output 2:")
        print("  - Selecting channel 2")
        ngx.select_channel(2)
        print("  - Setting voltage: 5.1 V")
        ngx.set_voltage(5.1)
        print("  - Setting current limit: 0.05 A")
        ngx.set_current(0.05)
        print("  - Preparing output for master switch ON")
        ngx.set_output_select(True)

        # The outputs are still OFF, they wait for this master switch:
        print("\nTurning ON all outputs (master switch)...")
        ngx.set_general_output_state(True)

        # Insert a small pause to allow the instrument to settle the output
        print("Waiting for outputs to settle...")
        time.sleep(0.5)

        # Read measurements from Output 1
        print("\nReading measurements:")
        ngx.select_channel(1)
        voltage1, current1 = ngx.read_measurement()
        print(f'  Output 1: {voltage1:.4f} V, {current1:.6f} A')

        # Read measurements from Output 2
        ngx.select_channel(2)
        voltage2, current2 = ngx.read_measurement()
        print(f'  Output 2: {voltage2:.4f} V, {current2:.6f} A')

        print("\n" + "=" * 60)
        print("Script completed successfully!")
        print("=" * 60)

        # Close connection
        ngx.close()

    except pyvisa.errors.VisaIOError as e:
        print(f"\nVISA Error: {e}")
        print("Please check:")
        print("  1. The IP address is correct")
        print("  2. The NGP800 is powered on and connected to the network")
        print("  3. The SCPI interface is enabled on the instrument")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
