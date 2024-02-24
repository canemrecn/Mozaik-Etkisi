import cv2  # OpenCV kütüphanesini içe aktarır
import imutils  # imutils kütüphanesini içe aktarır
import numpy as np  # numpy kütüphanesini içe aktarır

# Görüntünün genişlik ve yüksekliği için sabit değerler tanımlanır
W = 640
H = 480

# Karelerin çizileceği renk (siyah) tanımlanır
RENK = (0, 0, 0)

# Karelerin boyutu için d değeri tanımlanır
d = 9

# Karelerle çevrili görüntüyü oluşturan fonksiyon
def karelaj2(kare):
    # Kareler arasındaki boşluk miktarını hesaplar
    kal = int(d * 8 / 100) + 1
    x = 0
    while x < W-1:
        y = 0
        while y < H-1:
            # Her bir karenin etrafında siyah bir çerçeve çizer
            cv2.rectangle(kare, (x, y), (x+d, y+d), RENK, kal)
            y += d
        x += d
    x = 0
    while x < W-d:
        y = 0
        while y < H-d:
            # Her bir karenin içini, karenin merkez noktasındaki renk ile doldurur
            (b, g, r) = kare[y+d//2, x+d//2]
            b = int(b)
            g = int(g)
            r = int(r)
            cv2.rectangle(kare, (x+kal, y+kal), (x+d-kal, y+d-kal), (b, g, r), -1)
            y += d
        x += d
    return kare

# Karelerle dolu bir görüntü oluşturan fonksiyon
def karelaj(kare):
    karel = np.zeros(kare.shape, np.uint8)
    kal = int(d * 12 / 100) + 1
    x = 0
    while x < W-d:
        y = 0
        while y < H-d:
            # Her bir karenin içini, karenin merkez noktasındaki renk ile doldurur
            (b, g, r) = kare[y+d//2, x+d//2]
            b = int(b)
            g = int(g)
            r = int(g)  # Burada r değeri hatalı, g olarak değiştirilmeli
            cv2.rectangle(karel, (x+kal, y+kal), (x+d-kal, y+d-kal), (b, g, r), -1)
            y += d
        x += d
    return karel

# Eğer resim kullanılacaksa
resim = False

if resim:
    # Resim yüklenir
    kare = cv2.imread('resimler/aile.png')
else:
    # Kamera kullanılacaksa
    kamera = cv2.VideoCapture(0)
    kamera.set(cv2.CAP_PROP_BRIGHTNESS, 0.8)
kes = False  # Keskinleştirme efektinin durumunu tutan değişken
blur = False  # Bulanıklık efektinin durumunu tutan değişken
mozayik = False  # Mozayik efektinin durumunu tutan değişken

while True:
    if resim:
        # Eğer resim kullanılıyorsa, resim okunur
        kare = cv2.imread('resimler/aile.png')
    else:
        # Kamera kullanılıyorsa, kameradan görüntü alınır
        _, kare = kamera.read()

    kare = imutils.resize(kare, W)  # Görüntüyü yeniden boyutlandırır

    if H != kare.shape[1]:
        H = kare.shape[0]  # Yükseklik değeri güncellenir

    if kes:
        # Keskinleştirme efekti uygulanır
        keskinlestir = np.ones((d, d), np.float) * -1
        keskinlestir[(d-1)//2, (d-1)//2] = d * d
        kare = cv2.filter2D(kare, -1, keskinlestir)

    if blur:
        # Bulanıklık efekti uygulanır
        kare = cv2.medianBlur(kare, d-2)

    if mozayik:
        # Mozayik efekti uygulanır
        kare = karelaj2(kare)

    cv2.imshow('kare', kare)  # İşlenmiş görüntüyü ekranda gösterir

    k = cv2.waitKey(10)
    if k == -1:
        continue

    if k == 27 or k == ord('a'):
        # 'Esc' veya 'a' tuşuna basıldığında, karenin boyutu artırılır
        if d < 25:
            d += 2
        print(d)

    elif k == ord('-') or k == ord('s'):
        # '-' veya 's' tuşuna basıldığında, karenin boyutu azaltılır
        if d > 3:
            d -= 2
        print(d)

    elif k == ord('k'):
        # 'k' tuşuna basıldığında, keskinleştirme efekti açılır/kapatılır
        kes = not kes

    elif k == ord('b'):
        # 'b' tuşuna basıldığında, bulanıklık efekti açılır/kapatılır
        blur = not blur

    elif k == ord('m'):
        # 'm' tuşuna basıldığında, mozayik efekti açılır/kapatılır
        mozayik = not mozayik

if not resim:
    # Eğer resim kullanılmıyorsa, kamerayı kapatır
    _, kare = kamera.read()
    kare = imutils.resize(kare, width=W, height=H)

cv2.destroyAllWindows()  # Tüm pencereleri kapatır




