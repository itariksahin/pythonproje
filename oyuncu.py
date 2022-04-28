#Video üzerinde secim yapmak için opencv denemesidir
#28.04.2022
#İki futbol takımı oyuncularının secimi amaclanmıştır bu nedenle 
# kırmızı ve mavi formalı iki takım tercih edilmiştir
from getopt import gnu_getopt
import cv2
import os
import numpy as np

#video alınıyor
vidcap = cv2.VideoCapture('mac.mp4')
success,image = vidcap.read()
count = 0
success = True
idx = 0

#Video fotograflara ayırlıyor
while success:
	
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	#yeşil renk için aralık belirleniyor
	lower_yesil= np.array([40,40, 40])
	upper_yesil= np.array([70, 255, 255])
	#Mavi renk için aralık belirleniyor
	lower_mavi = np.array([110,50,50])
	upper_mavi = np.array([130,255,255])

	#Kırmızı renk için aralık belirleniyor
	lower_kirmizi = np.array([0,31,255])
	upper_kirmizi = np.array([176,255,255])

	#Beyaz renk için aralık belirleniyor
	lower_beyaz= np.array([0,0,0])
	upper_beyaz= np.array([0,0,255])

    #Azdan çok renge bir maske tanımlama
	mask = cv2.inRange(hsv, lower_yesil, upper_yesil)
    #maskeleme
	res = cv2.bitwise_and(image, image, mask=mask)
	#fotoraflar griye dönüştürülüyor
	res_bgr = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
	res_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

   
	kernel = np.ones((13,13),np.uint8)
	thresh = cv2.threshold(res_gray,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	

      
	im2,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	

	prev = 0
	font = cv2.FONT_HERSHEY_SIMPLEX
	
	for c in contours:
		x,y,w,h = cv2.boundingRect(c)
		
		#Futbolcular belirleniyor
		if(h>=(1.5)*w):
			if(w>15 and h>= 15):
				idx = idx+1
				player_img = image[y:y+h,x:x+w]
				player_hsv = cv2.cvtColor(player_img,cv2.COLOR_BGR2HSV)
				#Mavi Ağırlık formalıları secelim
				mask1 = cv2.inRange(player_hsv, lower_mavi, upper_mavi)
				res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
				res1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
				res1 = cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)
				sayacmavi = cv2.countNonZero(res1)
				#kırmızı Ağırlık formalıları secelim
				mask2 = cv2.inRange(player_hsv, lower_kirmizi, upper_kirmizi)
				res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
				res2 = cv2.cvtColor(res2,cv2.COLOR_HSV2BGR)
				res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
				sayackirmizid = cv2.countNonZero(res2)

				if(sayacmavi >= 20):
					cv2.putText(image, 'MAVİ TAKIM', (x-2, y-2), font, 0.8, (255,0,0), 2, cv2.LINE_AA)
					cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
				else:
					pass
				if(sayackirmizid>=20):
					cv2.putText(image, 'KIRMIZIsource TAKIM', (x-2, y-2), font, 0.8, (0,0,255), 2, cv2.LINE_AA)
					cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)
				else:
					pass
		if((h>=1 and w>=1) and (h<=30 and w<=30)):
			player_img = image[y:y+h,x:x+w]
		
			player_hsv = cv2.cvtColor(player_img,cv2.COLOR_BGR2HSV)
			#TOPUN SECİLMESİ
			mask1 = cv2.inRange(player_hsv, lower_beyaz, upper_beyaz)
			res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
			res1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
			res1 = cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)
			sayacbeyaz = cv2.countNonZero(res1)
	

			if(sayacbeyaz >= 3):
				cv2.putText(image, 'TOP', (x-2, y-2), font, 0.8, (0,255,0), 2, cv2.LINE_AA)
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)


	cv2.imwrite("./foto/frame%d.jpg" % count, res)
	print ('Yeni cerceve: '), success   
	count += 1
	cv2.imshow('Match Detection',image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	success,image = vidcap.read()
    
vidcap.release()
cv2.destroyAllWindows()