'''
Small module for networking purposes.
On its first implementation it only contained
one function to verify if the device is connected
to WiFi.
'''
import socket


def is_connected() -> bool:
    ''' Check if the device is connected to WiFi
    by obtaining the ip address.abs
    Returns:
        True (if the device is connected to WiFi)
        False (if the device is not connected to WiFi)
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.com', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = ''
    if ip:
        return True
    else:
        return False
