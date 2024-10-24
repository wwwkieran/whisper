import base64
import os
import threading
import time
from datetime import datetime

import cv2
import mediapipe as mp
from openai import OpenAI
from pathlib import Path
from playsound import playsound
client = OpenAI()
from dataclasses import dataclass
import random


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Crear la carpeta 'photos' si no existe
photos_dir = 'images'
if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)
    print(f"Carpeta '{photos_dir}' creada.")
# Inicializar MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4)
# Iniciar la captura de video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
print("Cámara abierta. Buscando caras...")
face_detected_time = None
face_present = False
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la cámara.")
        break
    # Convertir la imagen a RGB (MediaPipe usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Procesar la imagen con MediaPipe
    results = face_detection.process(rgb_frame)
    # Verificar si se detectaron caras
    if results.detections:
        for detection in results.detections:
            # Obtener las coordenadas del bounding box
            bboxC = detection.location_data.relative_bounding_box
            h, w, c = frame.shape
            x1 = int(bboxC.xmin * w)
            y1 = int(bboxC.ymin * h)
            x2 = int((bboxC.xmin + bboxC.width) * w)
            y2 = int((bboxC.ymin + bboxC.height) * h)
            # Dibujar el rectángulo alrededor de la cara
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if not face_present:
            # Cara detectada por primera vez
            face_present = True
            face_detected_time = time.time()
            print("Cara detectada. Esperando 5 segundos...")
        else:
            # Verificar cuánto tiempo ha estado presente la cara
            elapsed_time = time.time() - face_detected_time
            if elapsed_time >= 5:
                # Guardar la foto
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                photo_path = os.path.join(photos_dir, f"foto_{timestamp}.jpg")
                cv2.imwrite(photo_path, frame)
                print(f"Foto guardada en {photo_path}")
                break
    else:
        if face_present:
            # Cara ya no está presente
            print("Cara ya no está presente.")
        face_present = False
        face_detected_time = None
    # Mostrar el frame con las detecciones
    cv2.imshow('Detección de Rostros', frame)
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Terminando el programa.")
        break
# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
print("Cámara cerrada.")

# Path to your image
image_path = "./images/photo1.jpg"

# Getting the base64 string
base64_image = encode_image(photo_path)

@dataclass
class Person:
    name: str
    description: str
    voice: str


personas = [
     Person("Claire",
            "You are Claire. Claire judges based on social status, fashion sense, and how well someone fits into popular norms. She notices designer labels, neat grooming, and trendy styles. If someone’s outfit is fashionable and well-put-together, she sees them as someone worthy of attention. In contrast, outdated or unfashionable clothing suggests a lack of social awareness or effort.",
            "nova"),
     Person("Brian",
            "You are Brian. Brian’s judgments are analytical, focusing on perceived intelligence and how someone presents themselves intellectually. He notices details like glasses, books, or gadgets that might indicate someone’s academic or intellectual interests. A clean, tidy, and slightly conservative appearance suggests reliability and intelligence, while messy or overly casual looks might lead him to question someone’s dedication to their studies or personal organization.",
            "echo"),
     Person("Andrew",
            "You are Andrew. Andrew focuses on physical appearance, fitness, and confidence. He judges based on how athletic or strong someone looks, noticing posture, build, and how comfortable they seem in their own body. A fit, athletic look with comfortable, casual clothing signifies self-discipline and confidence, while someone less fit or not dressed in a sporty way might be seen as lacking motivation or ambition.",
            "fable"),
     Person("Allison",
            "You are Allison. Allison observes the subtle, unusual details, valuing individuality and nonconformity. She judges based on how unique or quirky someone seems, looking for little hints of rebellion, such as mismatched clothing, eccentric accessories, or a distinct hairstyle. An unconventional style signifies authenticity and depth, while a polished, conventional appearance might be seen as fake or superficial.",
            "shimmer"),
     Person("Johnson",
            "You are Johnson. You are mean intellectual professor. You are smarter than anyone. You like making rumors of people failing at their professional careers. ",
            "fable"),
]

numIterations = random.randint(4, 6)
firstPrompt = "You must make fun of the person described. Be as specific as possible. Feel free to focus on one particular aspect. "
prompts = [
    "Defend the person, say something nice about them... but don't try too hard.",
    "Use something in the image to make up a crazy rumor.",
    "Make up a nickname for the person in the image based on something in the picture. If a nickname has already been made up, use it to insult the person.",
    "Continue making fun of the person and share a rumor about them.",
    "Defend the person and say a good experience you had with them in class at Harvard. Then still make fun of them for something.",
    "Explain which part of their hair most looks like a dog.",
    "Tell a story about how terrible a date with this person must be.",
    "Spread a rumor that you heard from a friend about how this person asked your friend out.",
    "Choose a famous person who looks alike this person.",
    "Speculate about what this person likes to do on its free time.",
    "Speculate about why this person is taking Enactive Design classes at Harvard GSD",
    "Reflect on whether gossiping about people is the right thing to do.",
]
lengths = [
    "Create one short sentence ONLY."
    "Create one long sentence ONLY."
    "Create no more than 2 sentences."
    # "Create no more than 3 sentences."
    "Create no more than 3 short sentences."
]
prevMessage = ""
prevPerson = ""
person = random.choice(personas)
def playSounds(file_path):
    playsound(file_path)

thread = None
ft = "%Y-%m-%dT%H:%M:%S%z"

for i in range(numIterations):
    while person.name == prevPerson:
        person = random.choice(personas)
    prompt = firstPrompt if i == 0 else random.choice(prompts)
    length = random.choice(lengths)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": " ".join(["You are gossiping privately with your friends. Respond directly to the latest message which is about the person in the photo. You can challenge others ideas. You are a Harvard GSD student.", prompt, person.description, length])},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prevMessage
                    },
                ],
            }
        ]
    )

    print(person.name)
    print(completion.choices[0].message.content)
    speech_file_path = Path(__file__).parent / "out" / (person.name + datetime.now().strftime(ft) + ".mp3")
    response = client.audio.speech.create(
        model="tts-1",
        voice=person.voice,
        speed=1.2,
        input=completion.choices[0].message.content
    )
    response.stream_to_file(speech_file_path)
    prevMessage = completion.choices[0].message.content
    prevPerson = person.name
    if i > 0:
        thread.join()
    thread = threading.Thread(target=playSounds, args=(speech_file_path,))
    time.sleep(1)
    thread.start()

