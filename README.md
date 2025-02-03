# Discord QR Code Login - Reverse Engineering 🕵️‍♂️🔒

## Description

This project offers a detailed technical examination of Discord's QR Code authentication process, focusing on the WebSocket communication and cryptographic methods involved in remote authentication. By analyzing the authentication flow, the goal is to better understand how secure remote login mechanisms are implemented.

## 🎯 Project Objectives

- Reverse engineer Discord's QR Code login authentication process
- Understand WebSocket communication protocols
- Analyze the cryptographic mechanisms used in authentication
- Provide educational insights into authentication security

## 📂 Project Structure

```
discord-qr-login/
│
├── main.py                    # Main application entry point
│
├── lib/
│   ├── discord_websocket.py   # WebSocket connection management
│   ├── discord_crypto.py      # Cryptography handling
│   ├── discord_ticket.py      # Authentication ticket management
│   └── utils.py               # Utility functions
│
└── lib/types/                 # Data structure definitions
```

## 🔍 Technical Deep Dive

### Authentication Workflow

The authentication process involves a sophisticated WebSocket communication protocol:

1. **WebSocket Connection Establishment**

   - Open secure WebSocket connection
   - Generate RSA 2048-bit key pair
2. **Initial Handshake**

   - Receive `HELLO` message with heartbeat interval
   - Send public RSA key
   - Decrypt and validate server-sent nonce
3. **QR Code Generation**

   - Receive fingerprint
   - Generate scannable QR code
   - Wait for mobile device authentication
4. **User Data Exchange**

   - Receive encrypted user data
   - Decrypt and validate user information
   - Obtain authentication ticket
5. **Token Retrieval**

   - Exchange ticket for authentication token
   - Securely decrypt final token

### Key WebSocket Message Types

- `HEARTBEAT`: Maintain connection
- `HELLO`: Initial server greeting
- `INIT`: Client initialization
- `NONCE_PROOF`: Authentication verification
- `PENDING_REMOTE_INIT`: QR code generation
- `PENDING_TICKET`: User data exchange
- `PENDING_LOGIN`: Token retrieval

## 🔐 Sequence Diagrams

### WebSocket Workflow

![WebSocket Workflow](https://images-ext-1.discordapp.net/external/mN0bY6edSCX53mUKdlLTMuSpDek6bdqa-ISjzd8Ayxs/%3Ftype%3Dpng%29%5D%28https%3A%2F%2Fmermaid.live%2Fedit/https/mermaid.ink/img/pako%3AeNqNVNFum0AQ_JXVPVSOlKhW1IeKh0gWxjayA9RQWaqQrPOxtk_Bd_Q4klpR_j0LxC5JXNe8wK1mZodl2GcmdIbMYSX-rlAJHEq-MXyXKqCLV1arardC056ttDnCUJZCmwx-zMElMtzAAlexFg9o4QtMkiSCQWW3qKwU3EqtYJTrp1S1GgU3VJcFVxbcXBLqc30RAy87qjGax4OHLm4Q-TWwvh0gLagVvrm7W8QOhAWqjpjQSqGofbXYRUy4luDAxJvNQuhNkLqskFvwlSVlnl8dpANtETT1ggNnjAoNp-o8HsBt_9t3mOL-hA8_8BPoRdUql6KGHCXfOQjCwPWW0TwMR9DzlDD7wmJGbenjnDExxAbZ4uBJ2i1ERj7Wtk67edfnjU19IqP1-rSzyAuGfjBezr37MPGW7euMpNqgKYxU9pIRHTLTGOxw_0VccGlhrQ38LKkaC67OWkt8d-ol3bk1vCG3_ILZHbH_deMeM1Q_rqXZ8TZQZ7zNwrEfQC-RdQqvTibVzXWJnai6nah-gFPmSTqME_iKf8SW0ySXtpH-1IKgHTu3_T6E0-6IEv2A6oLxfPipGxpwlcFMb6Ri12yHNAeZ0TZ5rrVSRvgdpsyhxwzXvMptylL1QtB6s8R7JZhjTYXXzOhqs2XOmuclnaoio7C8raJjlX75X1r_PWMmrTb37f5q1tjLK_Yvlrk?format=webp&width=385&height=468)

### Ticket Exchange Details

![Ticket Exchange Details](https://images-ext-1.discordapp.net/external/EWohZBhSOU7Q5TbHMSCnXgS4nx7ZUk0Fmp6oXMNvh6Q/%3Ftype%3Dpng%29%5D%28https%3A%2F%2Fmermaid.live%2Fedit/https/mermaid.ink/img/pako%3AeNp9Uk1PwzAM_StWzpvKgQs9IBAbjANsYkVCqJeQeGtEmwQnGUNo_x2v7Rhi03ppY78PO33fQjmNIhcBPxJahSMjlySb0gI_MkVnU_OG1J29pGiU8dJGuKkN8uuwMTJBOdIgA1zP7kvbITr48PKyb-dwNy4gk95kq4sM1x7JNIwIO0KPGzKl4-bwhDGRhVtjl0iejI078KOLCG6FBDvss9eSaxOUGinAy7Agqd7h08TqmMDheLPpnOdLgdnZVYMZYcMmQ76SKqvd0vREWUeYJ6UwhEWqYbxWlWT1rnl6j7FV9OUjaijcO9o95XCbEbbQv0CsA8KN9JENuR9RsdJJ20lRzOD87AzGRI5O2U2O67aW01gx8p_EEbcWwasG72zo7wOtFgPRIDXSaA7d97ZcClZssBQ5f2pcyFTHUpR2w9BtAOdfVok8UsKBIJeWlcgXkicZiNT-4z6xv1UO4atz-zNqEx09dDFv0775ATjh_FI?format=webp&width=399&height=468)

## 🛡️ Security Considerations

- RSA 2048-bit encryption
- Nonce-based authentication
- Encrypted message exchanges
- Dynamic fingerprint generation

## ⚠️ Ethical Warning

**Disclaimer:** This project is strictly for educational and research purposes. Any misuse for unauthorized access or malicious activities is strictly prohibited.

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/discord-qr-login.git

# Navigate to project directory
cd discord-qr-login

# Install dependencies
pip install -r requirements.txt
```

### Running the Project

```bash
python main.py
```

## 🤝 Contributing

💡 We welcome contributions! If you have ideas for improvements, feel free to submit a pull request or open an issue. Let's make this project even better together!

⭐ If you like this project, consider giving it a star on GitHub to show your support! Your feedback and suggestions are always appreciated!

## 📜 License

This project is licensed under the MIT License. You are free to modify and share it.
