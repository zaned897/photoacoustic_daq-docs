#!/usr/bin/env python3
"""Captura pantalla + datos del osciloscopio por USB-TMC/SCPI (Mac/Linux/Windows).

Conexión: puerto USB-Device del scope (Tipo-B cuadrado) -> PC.
Requisitos:
    pip install pyvisa pyvisa-py pyusb
    (en Mac además:  brew install libusb)
Antes de correr: en el menú del scope, pon el puerto USB-Device en modo
    "USBTMC" / "Computer" (NO "Printer" ni "USB Drive").

Uso:
    python3 scope_capture.py                  # autodetecta
    python3 scope_capture.py "USB0::...::INSTR"   # recurso explícito

Salida (en la carpeta actual):  scope_screen.png/bmp  y  scope_CHn.csv
"""
import sys
import os

try:
    import pyvisa
except ImportError:
    sys.exit("Falta pyvisa. Instala:\n  pip install pyvisa pyvisa-py pyusb\n"
             "  (Mac: brew install libusb)")

OUT = os.getcwd()


def pick_resource(rm):
    if len(sys.argv) > 1:
        return sys.argv[1]
    res = list(rm.list_resources())
    print("Recursos detectados:", res if res else "(ninguno)")
    usb = [r for r in res if "USB" in r and "INSTR" in r]
    cand = usb or [r for r in res if "INSTR" in r]
    if not cand:
        sys.exit("No se encontró el osciloscopio.\n"
                 " - ¿Encendido y conectado por el puerto USB-Device (cuadrado)?\n"
                 " - ¿El puerto está en modo USBTMC/Computer en el menú del scope?\n"
                 " - Mac: revisa 'Información del sistema > USB' que aparezca el equipo.")
    return cand[0]


def save_screenshot(inst, vendor):
    try:
        if "rigol" in vendor:
            img = inst.query_binary_values(":DISP:DATA? ON,0,PNG", datatype="B",
                                           container=bytes)
            ext = "png"
        elif "keysight" in vendor or "agilent" in vendor:
            img = inst.query_binary_values(":DISPlay:DATA? PNG,COLor", datatype="B",
                                           container=bytes)
            ext = "png"
        elif "siglent" in vendor:
            inst.write("SCDP")
            img = inst.read_raw()
            ext = "bmp"
        elif "tektronix" in vendor:
            inst.write("SAVE:IMAGe:FILEFormat PNG")
            inst.write("HARDCopy STARt")
            img = inst.read_raw()
            ext = "png"
        else:  # intento genérico estilo SCPI
            img = inst.query_binary_values(":DISPlay:DATA? PNG,COLor", datatype="B",
                                           container=bytes)
            ext = "png"
        path = os.path.join(OUT, f"scope_screen.{ext}")
        with open(path, "wb") as f:
            f.write(img)
        print(f"[OK] Pantalla -> {path} ({len(img)} bytes)")
    except Exception as e:
        print("[!] No se pudo capturar la pantalla automáticamente:", e)
        print("    (Manda el IDN de abajo y ajusto el comando a tu modelo.)")


def save_waveforms(inst):
    # Estilo :WAV: (Rigol/Keysight/Siglent SCPI). Tektronix usa otro set.
    saved = 0
    for ch in (1, 2, 3, 4):
        try:
            on = inst.query(f":CHAN{ch}:DISP?").strip()
        except Exception:
            on = "1" if ch <= 2 else "0"
        if on not in ("1", "ON", "on"):
            continue
        try:
            inst.write(f":WAV:SOUR CHAN{ch}")
            inst.write(":WAV:MODE NORM")
            inst.write(":WAV:FORM ASCII")
            data = inst.query(":WAV:DATA?")
            if data.startswith("#"):            # quitar header TMC #9xxxxxxxxx
                n = int(data[1])
                data = data[2 + n:]
            path = os.path.join(OUT, f"scope_CH{ch}.csv")
            with open(path, "w") as f:
                f.write(data.strip())
            print(f"[OK] CH{ch} -> {path}")
            saved += 1
        except Exception as e:
            print(f"[!] CH{ch}: ajuste necesario para este modelo:", e)
    if saved == 0:
        print("[!] No se guardó forma de onda (modelo con SCPI distinto; con el IDN lo ajusto).")


def main():
    rm = pyvisa.ResourceManager("@py")
    addr = pick_resource(rm)
    print("Usando:", addr)
    inst = rm.open_resource(addr)
    inst.timeout = 20000
    try:
        idn = inst.query("*IDN?").strip()
    except Exception as e:
        sys.exit(f"Conectó pero *IDN? falló: {e}\n"
                 "Revisa que el puerto esté en modo USBTMC/Computer.")
    print("\n========================================")
    print("*IDN? =>", idn)
    print("========================================\n")
    vendor = idn.split(",")[0].lower()
    save_screenshot(inst, vendor)
    save_waveforms(inst)
    inst.close()
    print("\n>>> Envíame la línea *IDN? de arriba y los archivos generados "
          "(scope_screen.* y scope_CHn.csv).")


if __name__ == "__main__":
    main()
