import qrcode
img = qrcode.make('https://www.informaticsoma.com')
img.show()



# USE BELOW
# qr --factory=svg-path "https://www.facebook.com/ChoiSiYoung.sy" > qrcode_1.svg
# qr --factory=svg-path "https://www.informaticsoma.com" > qrcode_2.svg

