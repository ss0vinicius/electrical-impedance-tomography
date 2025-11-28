import serial
import pandas as pd
import csv
import sys
import glob
import time

def list_serial_ports():
    patterns = ('/dev/ttyUSB*', '/dev/ttyACM*', '/dev/ttyAMA*', '/dev/rfcomm*')
    ports = []
    for pattern in patterns:
        ports += glob.glob(pattern)
    return ports

def choose_port():
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found! Pair HC-06 and ensure /dev/rfcomm0 exists.")
        sys.exit(1)
    print("Available serial ports:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p}")
    return ports[0]

def is_control_line(s: str) -> bool:
    s_up = s.upper()
    if s == "F":
        return True
    control_keywords = [
        "CALL TAKEITERATION", "INICIANDO ENVIO", "ENVIO CONCLUÍDO", "ERRO AO ABRIR",
        "RECEBIDO VIA", "ENVIADO '1' DE VOLTA", "CALL TAKEITERATION WITH BLUETOOTH",
        "START", "READY", "HC-06", "BLUETOOTH"
    ]
    return any(k in s_up for k in control_keywords)

def parse_data_line(raw: str):
    """Expect: Protocol;Module;Phase;Real;Imaginary"""
    parts = [p.strip() for p in raw.split(';')]
    if len(parts) != 5:
        return None
    # Basic sanity: columns 3..5 should be numeric
    try:
        float(parts[2]); float(parts[3]); float(parts[4])
    except ValueError:
        return None
    return parts  # [Protocol, Module, Phase, Real, Imaginary]

def main():
    port = choose_port()
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=2)
    except Exception as e:
        print(f"Could not open {port}: {e}")
        sys.exit(1)

    N = 208  # expected measurements
    cols = ['Protocol', 'Module', 'Phase', 'Real', 'Imaginary']
    print(f"Connected to {ser.name}")

    try:
        # Optional handshake
        ser.write(b'H')
        time.sleep(0.1)
        _ = ser.readline()

        # Trigger acquisition
        ser.write(b'T')
        print("Sent 'T' to Arduino. Waiting for data…")

        rows = []
        deadline = time.time() + 60  # global safety timeout

        while True:
            raw = ser.readline().decode('utf-8', errors='replace').strip()
            if not raw:
                if time.time() > deadline:
                    print("[error] Timeout waiting for data.")
                    break
                continue

            deadline = time.time() + 60

            if raw == "F":
                print("Received finish flag 'F'.")
                break

            if is_control_line(raw):
                print(f"[ctrl] {raw}")
                continue

            data = parse_data_line(raw)
            if data is None:
                print(f"[warn] Skipping non-data line: {raw!r}")
                continue

            rows.append(data)
            if len(rows) % 20 == 0:
                print(f"…received {len(rows)} rows")

            if len(rows) >= N:
                print(f"Reached target count: {N}")
                break

        if not rows:
            print("[error] No data rows captured.")
            return

        df = pd.DataFrame(rows, columns=cols)

        # Coerce numeric columns (Module kept as string)
        for c in ['Phase', 'Real', 'Imaginary']:
            df[c] = pd.to_numeric(df[c], errors='coerce')

        # Save full table
        df.to_csv("HC06DataOutput.csv", index=False)
        print(f"Saved HC06DataOutput.csv with {len(df)} rows.")

        # Save single-row, semicolon-separated Module list
        modules = df['Module'].astype(str).tolist()
        with open("ModuleOutput.csv", "w", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(modules)
        print("Saved ModuleOutput.csv (single row, ';' separated).")

        # (Optional) Protocol-only file
        df['Protocol'].to_csv("ProtocolOutput.csv", index=False, header=False)
        print("Saved ProtocolOutput.csv")

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        try:
            ser.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
