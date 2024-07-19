---

# Recipet Worbby

Recipet is a GUI-based application built using Tkinter and Python. It facilitates the management and configuration of devices over RS-485 using Modbus RTU protocol. The application supports functionalities like searching and connecting to devices, changing device addresses, and saving configuration settings. This project was developed for Trumen Technologies, an IoT devices company based in Indore.

## Features

- **Search and Connect:** Automatically search and connect to devices on the RS-485 network.
- **Change and Save Address:** Change the address of connected devices and save the new address.
- **Display Register Values:** Display various register values including device address, baud rate, measured values, and more.
- **User-Friendly Interface:** Intuitive and easy-to-use interface built with Tkinter.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayushkhale/recieptworbby.git
   cd Recordsvita
   ```

2. **Install the required dependencies:**
   Ensure you have Python installed. Then, install the necessary packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application:**
   Start the application by running the main Python file:
   ```bash
   python main.py
   ```

2. **Interact with the Interface:**
   - Enter the USB port (COMXX) where the device is connected.
   - Use the "Search and Connect" button to find and connect to devices.
   - View and modify device addresses, and save configurations as needed.

## Contributing

We welcome contributions to improve Recipet! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch`
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Technologies Used

- **Python**
- **Tkinter**
- **minimalmodbus**
- **PIL (Pillow)**

## Contact

For any questions or feedback, please reach out:

- **Author:** Ayush Khale
- **Company:** Trumen Technologies
- **Location:** Indore, India
- **GitHub:** [ayushkhale](https://github.com/ayushkhale)

---
