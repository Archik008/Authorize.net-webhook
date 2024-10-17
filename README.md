# Authorize.net Webhook

This project is a web server for receiving payments from the Authorize.net payment system. It demonstrates the payment process for a CARFAX report using a vehicle's VIN code.

## Features

- **Authorize.net Payment Integration**: The server is configured to receive webhook notifications from Authorize.net .
- **CARFAX Report Payment**: Example use case for paying and retrieving a CARFAX report with the provided VIN code.

## Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)
- Authorize.net sandbox or production account
- CARFAX API access (optional, if integrating live VIN report retrieval)

### Installation

1. Clone the repository:

   <code>
   git clone https://github.com/Archik008/Authorize.net-webhook.git
   cd Authorize.net-webhook
   </code>

2. Set up a virtual environment:

   <code>
   python3 -m venv venv
   </code>

3. Activate the virtual environment:

   - On Windows:

     <code>
     venv\Scripts\activate.ps1
     </code>

   - On macOS/Linux:

     <code>
     source venv/bin/activate
     </code>

4. Install the required dependencies:

   <code>
   pip install -r requirements.txt
   </code>

### Configuration

1. In the root of your project, in file "config.py" add your **Authorize.net** API credentials.
2. Optionally, configure any CARFAX-related parameters for VIN report requests.

### Running the Server

To run the server, use the following command:

<code>
python app.py
</code>

The server will start listening for payment notifications and demonstrate the CARFAX report payment process.

## License

This project is licensed under the MIT License.
