
# Dual Bot Communication Protocol

## Commands Available:

### Python Bot Commands:
- `!ping` - Python bot responds and writes to shared.txt
- `!check_rust` - Python bot reads messages from Rust bot
- `!dual_status` - Shows current shared communication status
- `!hello` - Simple greeting

### Rust Bot Commands:
- `!rust_ping` - Rust bot responds and writes to shared.txt
- `!check_python` - Rust bot reads messages from Python bot

## Communication Flow:
1. Both bots use `shared.txt` as a communication medium
2. When one bot receives a command, it writes to the shared file
3. The other bot can read from this file when requested
4. This allows for asynchronous communication between the two bots

## File Structure:
```
dual-bot/
├── main.py           # Python Discord bot
├── run_dual_bots.py  # Script to run both bots
├── Cargo.toml        # Rust project configuration
├── src/
│   └── main.rs       # Rust Discord bot
├── shared.txt        # Communication file (created at runtime)
└── .env              # Environment variables (use Secrets instead)
```

## Usage:
1. Set up both BOT_TOKEN_PY and BOT_TOKEN_RS in Secrets
2. Run `python3 run_dual_bots.py` to start both bots
3. Use commands in Discord to test communication
