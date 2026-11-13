# Venom

A lightweight command-line scanner for **reflected XSS** and **SQL injection** (error-based, boolean-based, and time-based).

```
 ██▒   █▓▓█████  ███▄    █  ▒█████   ███▄ ▄███▓
▓██░   █▒▓█   ▀  ██ ▀█   █ ▒██▒  ██▒▓██▒▀█▀ ██▒
 ▓██  █▒░▒███   ▓██  ▀█ ██▒▒██░  ██▒▓██    ▓██░
  ▒██ █░░▒▓█  ▄ ▓██▒  ▐▌██▒▒██   ██░▒██    ▒██ 
   ▒▀█░  ░▒████▒▒██░   ▓██░░ ████▓▒░▒██▒   ░██▒
   ░ ▐░  ░░ ▒░ ░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░   ░  ░
   ░ ░░   ░ ░  ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░  ░      ░
     ░░     ░      ░   ░ ░ ░ ░ ░ ▒  ░      ░   
      ░     ░  ░         ░     ░ ░         ░   
```

## Features

- **XSS scan** — injects a set of context-aware payloads (HTML, attribute breakout, `img`/`svg` event handlers) and flags any reflected unencoded in the response.
- **SQLi scan** — runs three detection techniques:
  - **Error-based** — sends syntax-breaking characters and matches known database error signatures.
  - **Boolean-based** — compares a always-true vs always-false condition and detects response differences.
  - **Time-based** — injects a delay payload and measures response time.

## Install

```bash
git clone https://github.com/pr0lificz/venom.git
cd venom
pip install -r requirements.txt
```

## Usage

```bash
python3 venom.py <command> [options]
```

| Command   | Description                                              |
|-----------|---------------------------------------------------------|
| `xss`     | Scan a parameter for reflected XSS                      |
| `sqli`    | Scan a parameter for SQL injection (error/boolean/time) |
| `credits` | Show credits                                            |
| `help`    | Show help / usage                                       |

**Options** (for `xss` / `sqli`):

| Flag          | Description              |
|---------------|--------------------------|
| `-u`, `--url` | Target URL (with param)  |
| `-p`, `--param` | Parameter to inject    |

### Examples

```bash
python3 venom.py xss  -u "http://target/?search=test" -p search
python3 venom.py sqli -u "http://target/?id=1"        -p id
```

## Disclaimer

Venom is for **authorized security testing and education only**. Only use it against systems you own or have explicit, written permission to test. Unauthorized scanning is illegal. The author accepts no liability for misuse.

## Credits

Dev: **pr0lificz**
