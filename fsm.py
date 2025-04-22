
# Обьявление всех возможных State`ов
DEFAULT_STATE = 0
TEXT_STATE = 1
IMAGE_STATE = 2

# Реализация FSM
class FSM:
    def __init__(self):
        self.states = {}
    def get_state(self, uid): # Получение state по ID
        if uid not in self.states: # Если такого ID еще нету в словаре
            self.states[uid] = DEFAULT_STATE # Создадим с DEFAULT_STATE
        return self.states[uid] # Вернем
    
    def set_state(self, uid, state): # Установление State по ID
        self.states[uid] = state # Просто переписываем значение