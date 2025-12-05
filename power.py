#!/usr/bin/env python3
"""
Integrated Power Supply and GPIO Control Script for Raspberry Pi
NGP800 SCPI control + GPIO LED control with synchronized ON/OFF timing

Periodic ON/OFF control: 55 seconds ON, 5 seconds OFF

Requirements:
    pip install pyvisa pyvisa-py
    sudo apt install python3-gpiozero

Hardware:
    - Rohde & Schwarz NGP800 Power Supply (via Ethernet)
    - LED connected to GPIO17 with 330Ω resistor

Usage:
    python3 power.py

Configuration:
    Edit POWER_SUPPLY_IP and LED_PIN variables below
"""

import time
import pyvisa
import signal
import sys
from gpiozero import LED


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


def initialize_system(ngx, led):
    """
    Initialize both power supply and GPIO

    Args:
        ngx: NGP800Controller instance
        led: LED instance
    """
    print("\n" + "=" * 60)
    print("Initializing System")
    print("=" * 60)

    # Initialize GPIO LED
    print("\nInitializing GPIO LED...")
    print(f"  - Using GPIO{led.pin.number}")
    print("  - Turning LED OFF")
    led.off()

    # Initialize Power Supply
    print("\nInitializing Power Supply...")
    print("  - Resetting instrument...")
    ngx.reset()

    print("  - Turning OFF all outputs (master switch)...")
    ngx.set_general_output_state(False)

    # Configure all 4 outputs with 25V 0.1A
    for channel in range(1, 5):
        print(f"\n  Configuring Output {channel}:")
        print(f"    - Selecting channel {channel}")
        ngx.select_channel(channel)
        print("    - Setting voltage: 25.0 V")
        ngx.set_voltage(25.0)
        print("    - Setting current limit: 0.1 A")
        ngx.set_current(0.1)
        print("    - Preparing output for master switch ON")
        ngx.set_output_select(True)

    print("\n" + "=" * 60)
    print("Initialization completed!")
    print("=" * 60)


def turn_on_outputs(ngx, led):
    """
    Turn ON both power supply outputs and GPIO LED

    Args:
        ngx: NGP800Controller instance
        led: LED instance
    """
    print("\n🟢 Turning ON all outputs...")

    # Turn ON power supply
    ngx.set_general_output_state(True)

    # Turn ON LED
    led.on()
    print("   GPIO LED: ON")

    # Wait for outputs to settle
    time.sleep(0.5)

    # Read and display measurements from all 4 channels
    for channel in range(1, 5):
        ngx.select_channel(channel)
        voltage, current = ngx.read_measurement()
        print(f"   NGP800 Ch{channel}: {voltage:.4f} V, {current:.6f} A")


def turn_off_outputs(ngx, led):
    """
    Turn OFF both power supply outputs and GPIO LED

    Args:
        ngx: NGP800Controller instance
        led: LED instance
    """
    print("\n🔴 Turning OFF all outputs...")

    # Turn OFF power supply
    ngx.set_general_output_state(False)

    # Turn OFF LED
    led.off()
    print("   GPIO LED: OFF")


def main():
    """
    Main function: Initialize and run periodic ON/OFF cycle
    55 seconds ON, 5 seconds OFF
    """

    # Configuration
    POWER_SUPPLY_IP = '192.168.0.10'  # Change to your NGP800's IP address
    LED_PIN = 17                       # GPIO pin number for LED

    # Timing configuration
    ON_TIME = 55   # seconds
    OFF_TIME = 5   # seconds

    # Create resource string for TCP/IP connection
    resource_string = f'TCPIP0::{POWER_SUPPLY_IP}::inst0::INSTR'

    print("=" * 60)
    print("Integrated Power Supply and GPIO Control")
    print("=" * 60)
    print(f"NGP800: {POWER_SUPPLY_IP}")
    print(f"GPIO LED: Pin {LED_PIN}")
    print(f"Cycle: {ON_TIME} sec ON, {OFF_TIME} sec OFF")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    ngx = None
    led = None

    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n" + "=" * 60)
        print("Ctrl+C detected. Shutting down...")
        print("=" * 60)
        if ngx and led:
            try:
                turn_off_outputs(ngx, led)
                ngx.close()
                print("All outputs turned OFF and connections closed.")
            except Exception as e:
                print(f"Error during shutdown: {e}")
        elif led:
            try:
                led.off()
                print("GPIO LED turned OFF.")
            except Exception as e:
                print(f"Error turning off LED: {e}")
        sys.exit(0)

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Initialize GPIO LED
        print(f"\nInitializing GPIO LED on pin {LED_PIN}...")
        led = LED(LED_PIN)
        print("GPIO LED initialized successfully.")

        # Connect to the power supply
        print(f"\nConnecting to NGP800 at {resource_string}...")
        ngx = NGP800Controller(resource_string)

        # Get instrument identification
        idn = ngx.get_idn()
        print(f'Connected to: {idn}')

        # Initialize both systems
        initialize_system(ngx, led)

        # Periodic ON/OFF cycle
        print("\n" + "=" * 60)
        print("Starting periodic cycle...")
        print("=" * 60)

        cycle_count = 0

        while True:
            cycle_count += 1
            print(f"\n--- Cycle {cycle_count} ---")

            # Turn ON both power supply and LED
            turn_on_outputs(ngx, led)
            print(f"Outputs will remain ON for {ON_TIME} seconds...")
            time.sleep(ON_TIME)

            # Turn OFF both power supply and LED
            turn_off_outputs(ngx, led)
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
        print("\nTroubleshooting:")
        print("  1. For GPIO errors, ensure gpiozero is installed:")
        print("     sudo apt install python3-gpiozero")
        print("  2. Verify LED is connected to GPIO17 with 330Ω resistor")
        print("  3. Ensure running on Raspberry Pi")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # Ensure outputs are turned off on exit
        if ngx and led:
            try:
                turn_off_outputs(ngx, led)
                ngx.close()
            except:
                pass
        elif led:
            try:
                led.off()
            except:
                pass


if __name__ == '__main__':
    main()
