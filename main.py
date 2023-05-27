import scapy.all as scapy
import PySimpleGUI as sg
import socket

window = sg.Window("LNS", [
    [sg.Output(size=(100, 20))],
    [
        [sg.ProgressBar(10, size=(30, 20), key="sgBar",
                        bar_color="white", expand_x=True)],
        [sg.Button("Start", button_color="green", expand_x=True)]
    ]
], background_color="green")

# Your device configuration
state = True
network_ip = ""
device_ip = "192.168.0.255"
device_mac = "5c:61:99:44:af:35"

while True:
    button, _ = window.read(timeout=100)

    if button in (None, "Exit"):
        window.close()
        break

    if state:
        print(f'{"":30}{"   Your device IP    ":45}{"      MAC     ":45}\n')
        state = False

    if button == "Start":
        window["sgBar"].UpdateBar(0, 10)

        clients = [{"iad": scapsr[1].psrc, "mad": scapsr[1].hwsrc} for scapsr in
                   scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=(f"{network_ip}/24")), timeout=1, verbose=False)[0]]

        window["sgBar"].UpdateBar(0, len(clients))

        print(f"Device:\n{'':30}{device_ip:45}{device_mac:45}\nLocal network:")

        for i in range(len(clients)):
            if clients[i]["iad"] != device_ip:
                try:
                    name = socket.gethostbyaddr(clients[i]["iad"])[0]
                except Exception:
                    name = "unknown"

                ip = str(clients[i]["iad"])
                mac = str(clients[i]["mad"])

                print(f"{'':30}{ip:45}{mac:45}{str(name):45}")

                window["sgBar"].UpdateBar(i + 1)
            else:
                window["sgBar"].UpdateBar(i + 1)
        print()
