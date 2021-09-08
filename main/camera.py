import cv2, os
import numpy as np
from django.conf import settings
face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR, 'main/haarcascades/haarcascade_frontalface_default.xml'))
# faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
# maskNet = load_model(os.path.join(settings.BASE_DIR,'face_detector/mask_detector.model'))

# Load Yolo
net = cv2.dnn.readNet(os.path.join(settings.BASE_DIR, "main/yolo/yolov3.weights"), os.path.join(
			settings.BASE_DIR, "main/yolo/yolov3.cfg"))
classes = []
with open("main/yolo/coco.names", "r") as f:
	classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def face_frame(self):
		success, image = self.video.read()
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=7)
		frame_flip = cv2.flip(image, 1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()

	def object_frame(self):
		success, img = self.video.read()
		min_confidence = 0.5
		img = cv2.resize(img, None, fx=0.4, fy=0.4)
		height, width, channels = img.shape

		# Detecting objects
		blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
		net.setInput(blob)
		outs = net.forward(output_layers)

		# Showing informations on the screen
		class_ids = []
		confidences = []
		boxes = []

		for out in outs:
			for detection in out:
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]
				if confidence > min_confidence:
					# Object detected
					center_x = int(detection[0] * width)
					center_y = int(detection[1] * height)
					w = int(detection[2] * width)
					h = int(detection[3] * height)

					# Rectangle coordinates
					x = int(center_x - w / 2)
					y = int(center_y - h / 2)

					boxes.append([x, y, w, h])
					confidences.append(float(confidence))
					class_ids.append(class_id)
		indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
		font = cv2.FONT_HERSHEY_PLAIN
		for i in range(len(boxes)):
			if i in indexes:
				x, y, w, h = boxes[i]
				label = "{}: {:.2f}".format(classes[class_ids[i]], confidences[i] * 100)
				print(i, label)
				color = colors[i]
				cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
				cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
		ret, jpeg = cv2.imencode('.jpg', img)
		return jpeg.tobytes()

# class MaskDetect(object):
# 	def __init__(self):
# 		self.vs = VideoStream(src=0).start()

# 	def __del__(self):
# 		cv2.destroyAllWindows()

# 	def detect_and_predict_mask(self,frame, faceNet, maskNet):
# 		# grab the dimensions of the frame and then construct a blob
# 		# from it
# 		(h, w) = frame.shape[:2]
# 		blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
# 									 (104.0, 177.0, 123.0))

# 		# pass the blob through the network and obtain the face detections
# 		faceNet.setInput(blob)
# 		detections = faceNet.forward()

# 		# initialize our list of faces, their corresponding locations,
# 		# and the list of predictions from our face mask network
# 		faces = []
# 		locs = []
# 		preds = []

# 		# loop over the detections
# 		for i in range(0, detections.shape[2]):
# 			# extract the confidence (i.e., probability) associated with
# 			# the detection
# 			confidence = detections[0, 0, i, 2]

# 			# filter out weak detections by ensuring the confidence is
# 			# greater than the minimum confidence
# 			if confidence > 0.5:
# 				# compute the (x, y)-coordinates of the bounding box for
# 				# the object
# 				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
# 				(startX, startY, endX, endY) = box.astype("int")

# 				# ensure the bounding boxes fall within the dimensions of
# 				# the frame
# 				(startX, startY) = (max(0, startX), max(0, startY))
# 				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

# 				# extract the face ROI, convert it from BGR to RGB channel
# 				# ordering, resize it to 224x224, and preprocess it
# 				face = frame[startY:endY, startX:endX]
# 				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
# 				face = cv2.resize(face, (224, 224))
# 				face = img_to_array(face)
# 				face = preprocess_input(face)

# 				# add the face and bounding boxes to their respective
# 				# lists
# 				faces.append(face)
# 				locs.append((startX, startY, endX, endY))

# 		# only make a predictions if at least one face was detected
# 		if len(faces) > 0:
# 			# for faster inference we'll make batch predictions on *all*
# 			# faces at the same time rather than one-by-one predictions
# 			# in the above `for` loop
# 			faces = np.array(faces, dtype="float32")
# 			preds = maskNet.predict(faces, batch_size=32)

# 		# return a 2-tuple of the face locations and their corresponding
# 		# locations
# 		return (locs, preds)

# 	def get_frame(self):
# 		frame = self.vs.read()
# 		frame = imutils.resize(frame, width=650)
# 		frame = cv2.flip(frame, 1)
# 		# detect faces in the frame and determine if they are wearing a
# 		# face mask or not
# 		(locs, preds) = self.detect_and_predict_mask(frame, faceNet, maskNet)

# 		# loop over the detected face locations and their corresponding
# 		# locations
# 		for (box, pred) in zip(locs, preds):
# 			# unpack the bounding box and predictions
# 			(startX, startY, endX, endY) = box
# 			(mask, withoutMask) = pred

# 			# determine the class label and color we'll use to draw
# 			# the bounding box and text
# 			label = "Mask" if mask > withoutMask else "No Mask"
# 			color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

# 			# include the probability in the label
# 			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

# 			# display the label and bounding box rectangle on the output
# 			# frame
# 			cv2.putText(frame, label, (startX, startY - 10),
# 						cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
# 			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
# 		ret, jpeg = cv2.imencode('.jpg', frame)
# 		return jpeg.tobytes()



