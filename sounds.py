import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.volume = 0.5
        
    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(self.volume)
        except Exception as e:
            print(f"Failed to load sound {name} from {path}: {e}")
            # Создаем заглушку, если звук не загрузился
            self.sounds[name] = NullSound()
    
    def play(self, name):
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception as e:
                print(f"Failed to play sound {name}: {e}")
    
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
            
    def set_effects_volume(self, volume):
        """Imposta il volume per tutti gli effetti sonori."""
        for sound in self.sounds.values():
            sound.set_volume(volume)

class NullSound:
    """Заглушка для случаев, когда звук не загрузился"""
    def play(self): pass
    def set_volume(self, volume): pass