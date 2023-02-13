import os
import pyttsx3
from gtts import gTTS
from PyPDF2 import PdfReader

pdfreader = PdfReader('archivos/mypdfexample.pdf')
speaker = pyttsx3.init()
concat_text = ''

for page_num in pdfreader.pages:
    text = page_num.extract_text()
    clean_text = text.strip().replace('\n', ' ')
    clean_text = clean_text.strip()
    clean_text = clean_text.rstrip()
    concat_text = concat_text + ' ' + clean_text
    

print(concat_text)
    
speaker.setProperty('rate', 150)
speaker.save_to_file(concat_text, 'prueba.wav')

# myobj = gTTS(text=concat_text, lang='es', slow=False)

speaker.runAndWait()
# myobj.save("archivos/playme.mp3")
speaker.stop()
# os.system("mpg321 welcome.mp3")
# os.rename("prueba.aiff", "archivos/playme.mp3")
