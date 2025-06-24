import whisper

import whisper

model = whisper.load_model("base")
file = "data/test_meteo.m4a"

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio(file)
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

# --------------

result = model.transcribe(file, language="ca")
print(result["text"])
