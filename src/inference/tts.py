
import os
from pathlib import Path
from gtts import gTTS
import pygame


class TTSEngine:
    
    def __init__(self, language='es', slow=False):
        self.language = language
        self.slow = slow
        pygame.mixer.init()
        print(f" Motor TTS inicializado")
    
    def speak(self, text, save_path=None, play=True):
        try:
            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            
            if save_path is None:
                save_path = "temp_audio.mp3"
            
            tts.save(save_path)
            
            if play:
                pygame.mixer.music.load(save_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                if save_path == "temp_audio.mp3":
                    os.remove(save_path)
            
            return True
        except Exception as e:
            print(f" Error TTS: {e}")
            return False
    
    def speak_bill_result(self, denomination, confidence=None):
        if confidence is not None and confidence < 90:
            text = f"Posible billete de {denomination}, con {int(confidence)} por ciento de confianza"
        else:
            text = f"Billete de {denomination}"
        
        print(f" {text}")
        self.speak(text)


if __name__ == "__main__":
    engine = TTSEngine()
    engine.speak("Prueba de voz")