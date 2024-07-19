import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import minimalmodbus
import serial

# Dictionary mapping register values to baud rates
BAUDRATE_MAP = {
    0x0000: 1200,
    0x0001: 2400,
    0x0002: 4800,
    0x0003: 9600,
    0x0004: 19200,
    0x0005: 38400,
    0x0006: 57600,
    0x0007: 115200
}

# Dictionary mapping register values to units for measured values
UNIT_MAP = {
    0x0000: "MPa",
    0x0001: "kPa",
    0x0002: "Pa",
    0x0003: "bar",
    0x0004: "mbar",
    0x0005: "kg/cm²",
    0x0006: "psi",
    0x0007: "mH2O",
    0x0008: "mmH2O"
}

# Dictionary mapping register values to decimal points
DECIMAL_POINT_MAP = {
    0x0000: 1,
    0x0001: 0.1,
    0x0002: 0.01,
    0x0003: 0.001,
    # Add more entries as needed
}

def get_baudrate_value(register_value):
    return BAUDRATE_MAP.get(register_value, "Unknown")

def get_unit_value(register_value):
    return UNIT_MAP.get(register_value, "Unknown")

def get_decimal_value(register_value):
    return DECIMAL_POINT_MAP.get(register_value, "Unknown")

def search_and_connect():
    try:
        port = port_entry.get()

        for device_address in range(1, 256):
            try:
                # Define serial port settings
                BAUDRATE = 9600
                BYTESIZE = 8
                PARITY = serial.PARITY_NONE
                STOPBITS = 1
                TIMEOUT = 1

                # Set up instrument
                instrument = minimalmodbus.Instrument(port, device_address, mode=minimalmodbus.MODE_RTU)
                instrument.serial.baudrate = BAUDRATE
                instrument.serial.bytesize = BYTESIZE
                instrument.serial.parity = PARITY
                instrument.serial.stopbits = STOPBITS
                instrument.serial.timeout = TIMEOUT

                # Read register values
                device_address_value = instrument.read_register(0x0000)
                baudrate_value = instrument.read_register(0x0001)
                measured_unit_value = instrument.read_register(0x0002)
                measured_decimal_value = instrument.read_register(0x0003)
                measured_values_value = instrument.read_register(0x0004)
                measured_zero_value = instrument.read_register(0x000A)
                measured_full_value = instrument.read_register(0x000B)
                data_storage_value = instrument.read_register(0x001F)

                # Display register values
                device_address_var.set(f"Device Address: {device_address_value}")
                baudrate_var.set(f"Baud Rate: {get_baudrate_value(baudrate_value)}")
                measured_unit_var.set(f"Measured Unit: {get_unit_value(measured_unit_value * get_decimal_value(measured_decimal_value))}")
                measured_unit_var.set(f"Measured Unit: {get_unit_value(measured_unit_value)}")
                #measured_decimal_var.set(f"Decimal value: {get_decimal_value(measured_decimal_value)}")
                measured_values_var.set(f"Measured Values: {measured_values_value}")
                zero_value_var.set(f"Zero Value: {measured_zero_value}")
                full_value_var.set(f"Full Value:  {measured_full_value * get_decimal_value(measured_decimal_value)}")
                # data_storage_var.set(f"Data Storage: {data_storage_value}")

                messagebox.showinfo("Success", f"Device found at address {device_address}")
                
                # Update current device address entry
                device_address_entry.delete(0, tk.END)
                device_address_entry.insert(0, str(device_address_value))
                
                break  # Exit loop if device is found

            except Exception as e:
                continue  # Try next address if connection fails

        else:
            messagebox.showinfo("Info", "No devices found")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def change_address():
    try:
        port = port_entry.get()
        current_device_address = int(device_address_entry.get())
        new_device_address = int(new_device_address_entry.get())

        # Define serial port settings
        BAUDRATE = 9600
        BYTESIZE = 8
        PARITY = serial.PARITY_NONE
        STOPBITS = 1
        TIMEOUT = 1

        # Set up instrument
        instrument = minimalmodbus.Instrument(port, current_device_address, mode=minimalmodbus.MODE_RTU)
        instrument.serial.baudrate = BAUDRATE
        instrument.serial.bytesize = BYTESIZE
        instrument.serial.parity = PARITY
        instrument.serial.stopbits = STOPBITS
        instrument.serial.timeout = TIMEOUT

        # Change device address
        instrument.write_register(0x0000, new_device_address, functioncode=6)

        # Create new instrument object with updated device address
        instrument = minimalmodbus.Instrument(port, new_device_address, mode=minimalmodbus.MODE_RTU)

        messagebox.showinfo("Success", "Address changed and save successfully")
        
        # Save new address
        instrument.write_register(0x001F, 0x001F, functioncode=6)  # Write data 0x001F to address 0x001F

        #messagebox.showinfo("Success", "Address saved successfully")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def save_configuration():
    try:
        port = port_entry.get()
        current_device_address = int(device_address_entry.get())

        # Define serial port settings
        BAUDRATE = 9600
        BYTESIZE = 8
        PARITY = serial.PARITY_NONE
        STOPBITS = 1
        TIMEOUT = 1

        # Set up instrument
        instrument = minimalmodbus.Instrument(port, current_device_address, mode=minimalmodbus.MODE_RTU)
        instrument.serial.baudrate = BAUDRATE
        instrument.serial.bytesize = BYTESIZE
        instrument.serial.parity = PARITY
        instrument.serial.stopbits = STOPBITS
        instrument.serial.timeout = TIMEOUT

        # Save setting by writing to address 0x001F
        instrument.write_register(0x001F, 0x001F, functioncode=6)  # Write data 0x001F to address 0x001F

        messagebox.showinfo("Success", "Configuration saved successfully")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Create main window
root = tk.Tk()
root.title("TTPL TFP-TLH")
root.configure(bg='#FFFFFF')

# Load and display image
img = Image.open('Trumen-Logo.jpeg')
resize_img = img.resize((100, 75))
img = ImageTk.PhotoImage(resize_img)
img_label = tk.Label(root, image=img, bg='#FFFFFF')
img_label.pack(pady=(10, 10))

# Create frame for RS-485 configuration
config_frame = tk.Frame(root, bg='#FFFFFF')
config_frame.pack(pady=10)

port_label = tk.Label(config_frame, text="USB Port (COMXX):", bg='#FFFFFF')
port_label.pack(anchor="center")
port_entry = tk.Entry(config_frame)
port_entry.pack(anchor="center")

device_address_label = tk.Label(config_frame, text="Current Device Address (Decimal):", bg='#FFFFFF')
device_address_label.pack(anchor="center")
device_address_entry = tk.Entry(config_frame)
device_address_entry.pack(anchor="center")

new_device_address_label = tk.Label(config_frame, text="New Device Address (Decimal):", bg='#FFFFFF')
new_device_address_label.pack(anchor="center")
new_device_address_entry = tk.Entry(config_frame)
new_device_address_entry.pack(anchor="center")

# Create buttons for search, change address, and save configuration
button_frame = tk.Frame(root, bg='#FFFFFF')
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search and Connect", command=search_and_connect, bg='#FFF5EE')
search_button.pack(fill="x")

change_address_button = tk.Button(button_frame, text="Change and Save Address", command=change_address, bg='#FFF5EE')
change_address_button.pack(fill="x")

# Create frame for displaying register values
values_frame = tk.Frame(root, bg='#FFFFFF')
values_frame.pack(pady=10)

device_address_var = tk.StringVar()
device_address_var.set("Device Address: ")
device_address_value_label = tk.Label(values_frame, textvariable=device_address_var, bg='#FFFFFF')
device_address_value_label.pack(anchor="center")

baudrate_var = tk.StringVar()
baudrate_var.set("Baud Rate: ")
baudrate_value_label = tk.Label(values_frame, textvariable=baudrate_var, bg='#FFFFFF')
baudrate_value_label.pack(anchor="center")

measured_values_var = tk.StringVar()
measured_values_var.set("Measured Values: ")
measured_values_value_label = tk.Label(values_frame, textvariable=measured_values_var, bg='#FFFFFF')
measured_values_value_label.pack(anchor="center")

measured_decimal_var = tk.StringVar()
measured_decimal_var.set("Decimal value: ")
measured_decimal_value_label = tk.Label(values_frame, textvariable=measured_decimal_var, bg='#FFFFFF')
measured_decimal_value_label.pack(anchor="center")

measured_unit_var = tk.StringVar()
measured_unit_var.set("Measured Unit: ")
measured_unit_value_label = tk.Label(values_frame, textvariable=measured_unit_var, bg='#FFFFFF')
measured_unit_value_label.pack(anchor="center")

zero_value_var = tk.StringVar()
zero_value_var.set("Zero Value: ")
zero_value_label = tk.Label(values_frame, textvariable=zero_value_var, bg='#FFFFFF')
zero_value_label.pack(anchor="center")

full_value_var = tk.StringVar()
full_value_var.set("Full Value: ")
full_value_label = tk.Label(values_frame, textvariable=full_value_var, bg='#FFFFFF')
full_value_label.pack(anchor="center")

#data_storage_var = tk.StringVar()
#data_storage_var.set("Data Storage: ")
#data_storage_value_label = tk.Label(values_frame, textvariable=data_storage_var, bg='#FFFFFF')
#data_storage_value_label.pack(anchor="center")

# Text at the bottom
bottom_text_style = {"bg": "#d3f4ff", "font": ("Arial", 10, "italic"), "fg": "#004d40"}
bottom_frame = tk.Frame(root, bg='#FFF5EE')
bottom_frame.pack(pady=15)

bottom_text = tk.Label(bottom_frame, text="Trumen Technologies Pvt. Ltd.", bg='#FFF5EE')
bottom_text.pack(anchor="center",pady=5)

bottom_text = tk.Label(bottom_frame, text="Pressure Department", bg='#FFF5EE')
bottom_text.pack(anchor="center",pady=5)

bottom_text = tk.Label(bottom_frame, text="Rahul Dagur", bg='#FFF5EE')
bottom_text.pack(anchor="center",pady=5)

bottom_text = tk.Label(bottom_frame, text="rahul@trumen.in", bg='#FFF5EE')
bottom_text.pack(anchor="center",pady=5)

root.mainloop()
