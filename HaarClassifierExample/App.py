import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img = cv2.imread('faces.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# load glasses with alpha
glasses = cv2.imread('glasses.png', cv2.IMREAD_UNCHANGED)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x, y, w, h) in faces:
    # scale glasses and draw rectangle where is face
    scaled_glasses = cv2.resize(glasses, (w, h))
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

    # alpha variables
    alpha_glasses = scaled_glasses[:, :, 3] / 255.0
    alpha_img = 1.0 - alpha_glasses

    # add alpha channel for original image
    for c in range(0, 3):
        img[y:y+h, x:x+w, c] = (alpha_glasses * scaled_glasses[:, :, c] +
                                alpha_img * img[y:y+h, x:x+w, c])

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    # eyes = eye_cascade.detectMultiScale(roi_gray)
    # for (ex, ey, ew, eh) in eyes:
    #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)


cv2.imshow('GlassesMakerBaker', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
