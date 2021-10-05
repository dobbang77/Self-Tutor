import cv2, os, datetime
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


class TimeCount(VideoCamera):
	tm = cv2.TickMeter()
	end_time = 0

	def time_count(self):
		success, image = self.video.read()
		con_time = 0
		con_sum = 0
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

		if len(faces_detected):  # 인식이 됐을때
			self.tm.start()
			self.end_time = self.tm.getTimeSec()
		'''
		else:  # 인식이 안 됐을때
			  if self.tm.getTimeSec() - self.end_time < 100:
				 self.tm.reset()
		'''
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=5)
			self.tm.stop()
			con_time = self.tm.getTimeSec()
			cv2.putText(image, str(con_time), (0, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2,
						color=(0, 255, 0), thickness=5)

		frame_flip = cv2.flip(image, 1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()
