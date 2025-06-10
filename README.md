
# Dual Discord Bot System

A Python and Rust Discord bot system that communicates through a shared file.

## Setup

1. **Set up Discord Bot Tokens**:
   - Go to the Secrets tab in Replit
   - Add `BOT_TOKEN_PY` with your Python bot token
   - Add `BOT_TOKEN_RS` with your Rust bot token

2. **Install Dependencies**:
   - Python dependencies are automatically installed from `pyproject.toml`
   - Rust dependencies will be installed when you run `cargo run`

## Running the Bots

### Option 1: Run Both Bots Together (Recommended)
```bash
python3 run_dual_bots.py
```

### Option 2: Run Individual Bots
```bash
# Python bot only
python3 main.py

# Rust bot only (in another terminal)
cargo run
```

## Available Commands

### Python Bot Commands:
- `!ping` - Python bot responds and writes to shared.txt
- `!check_rust` - Python bot reads messages from Rust bot
- `!dual_status` - Shows current shared communication status
- `!hello` - Simple greeting

### Rust Bot Commands:
- `!rust_ping` - Rust bot responds and writes to shared.txt
- `!check_python` - Rust bot reads messages from Python bot

## Testing

Test the file communication system:
```bash
python3 test_communication.py
```

## How It Works

1. Both bots connect to Discord using their respective tokens
2. When a bot receives a command, it can write messages to `shared.txt`
3. The other bot can read from this file when requested
4. This allows asynchronous communication between the Python and Rust bots

## Project Structure

```
├── main.py                 # Python Discord bot
├── src/main.rs            # Rust Discord bot
├── run_dual_bots.py       # Script to run both bots
├── test_communication.py  # Test file communication
├── shared.txt             # Communication file (created at runtime)
├── communication_protocol.md  # Detailed protocol documentation
└── README.md              # This file
```
