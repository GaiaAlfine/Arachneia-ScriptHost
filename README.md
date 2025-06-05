# Arachneia Script Host

This project hosts an interface for running helper scripts via PyQt5.

## Running on Linux

Install dependencies and run the main script with Python:

```bash
pip install PyQt5
python3 Arachneia-ScriptHost.pyw
```

The application was originally targeted at Windows. The main script now checks the
current platform before applying Windows-specific arguments so it can start on
Linux as well.

