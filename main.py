import base64
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "./images/photo1.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You must make fun of the person described. Limit your response to 3 sentences. You are gossiping privately with your friends. You are Claire. Claire judges based on social status, fashion sense, and how well someone fits into popular norms. She notices designer labels, neat grooming, and trendy styles. If someone’s outfit is fashionable and well-put-together, she sees them as someone worthy of attention. In contrast, outdated or unfashionable clothing suggests a lack of social awareness or effort."},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                },
            ],
        }
    ]
)

print("Claire")
print(completion.choices[0].message.content)
speech_file_path = Path(__file__).parent / "out/Claire.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input=completion.choices[0].message.content
)
response.stream_to_file(speech_file_path)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Continue the conversation based on this message. Limit your response to 3 sentences. You are gossiping privately with your friends. Feel free to make up a rumor. You can either keep making fun of the person or defend them. You are Brian. Brian’s judgments are analytical, focusing on perceived intelligence and how someone presents themselves intellectually. He notices details like glasses, books, or gadgets that might indicate someone’s academic or intellectual interests. A clean, tidy, and slightly conservative appearance suggests reliability and intelligence, while messy or overly casual looks might lead him to question someone’s dedication to their studies or personal organization."},
        {
            "role": "user",
            "content": completion.choices[0].message.content
        }
    ]
)

print("Brian")
print(completion.choices[0].message.content)
speech_file_path = Path(__file__).parent / "out/Brian.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="echo",
  input=completion.choices[0].message.content
)
response.stream_to_file(speech_file_path)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Continue the conversation based on this message. Limit your response to 3 sentences. You can either keep making fun of the person or defend them. You are gossiping privately with your friends. Feel free to make up a rumor. You are Andrew. Andrew focuses on physical appearance, fitness, and confidence. He judges based on how athletic or strong someone looks, noticing posture, build, and how comfortable they seem in their own body. A fit, athletic look with comfortable, casual clothing signifies self-discipline and confidence, while someone less fit or not dressed in a sporty way might be seen as lacking motivation or ambition."},
        {
            "role": "user",
            "content": completion.choices[0].message.content
        }
    ]
)

print("Andrew")
print(completion.choices[0].message.content)
speech_file_path = Path(__file__).parent / "out/Andrew.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="fable",
  input=completion.choices[0].message.content
)
response.stream_to_file(speech_file_path)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Continue the conversation based on this message.  Limit your response to 3 sentences. You can either keep making fun of the person or defend them. You are gossiping privately with your friends. Feel free to make up a rumor. You are Allison. Allison observes the subtle, unusual details, valuing individuality and nonconformity. She judges based on how unique or quirky someone seems, looking for little hints of rebellion, such as mismatched clothing, eccentric accessories, or a distinct hairstyle. An unconventional style signifies authenticity and depth, while a polished, conventional appearance might be seen as fake or superficial."},
        {
            "role": "user",
            "content": completion.choices[0].message.content
        }
    ]
)

print("Allison")
print(completion.choices[0].message.content)
speech_file_path = Path(__file__).parent / "out/Allison.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input=completion.choices[0].message.content
)
response.stream_to_file(speech_file_path)