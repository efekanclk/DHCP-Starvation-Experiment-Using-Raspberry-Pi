📡 Raspberry Pi ile DHCP Starvation Saldırısı Simülasyonu
Ders: Ankara Üniversitesi - YMH347 Mikroişlemciler ve Programlama

Dönem: 2025-2026 Güz

Platform: Raspberry Pi (DietPi OS) & Python

Bu proje, yerel ağlarda (LAN/WLAN) DHCP (Dynamic Host Configuration Protocol) güvenliğini test etmek amacıyla geliştirilmiştir. Proje kapsamında, kontrollü bir laboratuvar ortamında DHCP Starvation (Tüketme) saldırısı simüle edilmiş, ağ protokollerinin davranışları ve donanımsal kısıtlamalar analiz edilmiştir.

🎯 Projenin Amacı
DHCP protokolü, ağa katılan cihazlara otomatik IP dağıtımı yapar. Bu proje, "DORA" (Discover, Offer, Request, Acknowledge) sürecini manipüle ederek:

Sahte MAC adresleri ile sunucudan sürekli IP talep etmeyi,

Sunucunun IP havuzunu (IP Pool) tüketmeyi,

Ağ güvenliği ve DoS (Hizmet Engelleme) saldırılarına karşı farkındalık oluşturmayı hedefler.

⚙️ Metodoloji ve Yaklaşımlar
Proje geliştirme sürecinde, kablosuz ağların (Wi-Fi) güvenlik yapısını aşmak için iki farklı yöntem denenmiştir. Bu kodlar repoda ayrı ayrı sunulmuştur.

1. Aşama: Scapy ile Paket Manipülasyonu (scapy_dhcp_starvation.py)
(IP/UDP/BOOTP) en alt seviyede (Raw Packet) oluşturulmuştur.

Yöntem: Her döngüde rastgele bir MAC adresi ve Transaction ID (XID) üretilerek DHCP Discover paketleri "Broadcast" olarak yayılmıştır.

Gözlem: Kablosuz ağlarda (802.11), Erişim Noktası (Access Point) ile "Association" (İlişkilendirme) kurmayan MAC adreslerinden gelen paketler reddedildiği için başarı oranı düşük kalmıştır.

2. Aşama: Sistem Tabanlı Multithread Saldırı (dhclient_flood_optimized.py) (Nihai Kod)
İlk aşamadaki sorunları aşmak için Linux işletim sisteminin yerel aracı olan dhclient manipüle edilmiştir.

Yöntem: Python subprocess ve ThreadPoolExecutor kullanılarak aynı anda 10 farklı iş parçacığı (thread) çalıştırılmıştır.

Özellik: Her işlem için izole edilmiş PID ve Lease dosyaları oluşturularak, işletim sistemi aynı anda birden fazla DHCP istemcisi çalıştırmaya zorlanmıştır.

Sonuç: Saniyede yüzlerce istek üretilmiş, ancak donanımsal MAC adresi kısıtlaması nedeniyle (Wi-Fi kartının fiziksel adresi değişmediği için) sunucu IP havuzunu tüketmek yerine mevcut IP süresini yenilemiştir (Renew).

🛠️ Kurulum ve Gereksinimler
Donanım
Raspberry Pi 3/4/5 (Tercihen DietPi veya Raspberry Pi OS Lite yüklü)

Wi-Fi bağlantısı (wlan0) veya Ethernet (eth0)

Test için hedef bir Modem veya Hotspot

Yazılım Kütüphaneleri
Gerekli Python kütüphanelerini ve sistem araçlarını yükleyin:

Bash

# Sistem güncellemeleri ve araçlar
sudo apt-get update && sudo apt-get install tcpdump dhcp-client -y

# Python bağımlılıkları (Scapy sürümü için)
sudo pip3 install scapy
🚀 Kullanım
1. Scapy Sürümünü Çalıştırma
Bash

sudo python3 scapy_dhcp_starvation.py
2. Optimized (Multithread) Sürümü Çalıştırma
Bash

# wlan0 arayüzü üzerinden saldırı başlatır
sudo python3 dhclient_flood_optimized.py wlan0

# Belirli bir sayıda (örn: 500) istek göndermek için
sudo python3 dhclient_flood_optimized.py wlan0 500
Not: Script çalıştırılmadan önce ağ trafiğini izlemek için farklı bir terminalde sudo tcpdump -i wlan0 komutunu kullanabilirsiniz.

📊 Test Sonuçları ve Teknik Analiz
Yapılan testlerde saldırı trafiğinin başarıyla oluştuğu ancak IP havuzunun tükenmediği gözlemlenmiştir. Bunun teknik nedenleri şunlardır:

802.11 Association Kuralı: Wi-Fi protokolü gereği, modemler kendisiyle şifreli bağlantı (Handshake) kurmamış rastgele MAC adreslerinden gelen veri paketlerini (Data Frames) kabul etmez.

Donanımsal MAC Bağlılığı: dhclient aracı kullanıldığında, yazılım ne kadar sahte MAC üretirse üretsin, Linux kernel seviyesinde paket ağ kartından çıkarken kartın fiziksel MAC adresini kullanır.



⚠️ Yasal Uyarı (Disclaimer)
Bu proje ve içerdiği kodlar tamamen eğitim ve akademik araştırma amaçlı hazırlanmıştır. Sadece izin alınan, kontrollü laboratuvar ağlarında kullanılmalıdır. Halka açık ağlarda veya izinsiz sistemlerde kullanılması yasa dışıdır ve suç teşkil eder. Geliştiriciler, aracın kötüye kullanımından sorumlu tutulamaz.# DHCP-Starvation-Experiment-Using-Raspberry-Pi-
