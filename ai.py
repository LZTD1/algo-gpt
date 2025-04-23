from g4f.client import Client
import loguru

logger = loguru.logger

class AI:
    def __init__(self, cfg):
        self.client = Client()
        self.image_model = cfg['image_model']
        self.text_model = cfg['text_model']
        self.chat_history = {}
    def clear_dialog(self, uid):
        self.chat_history[uid] = []
    def generate_text(self, query, uid):
        # Инициализируем историю чата, если пользователь новый
        if uid not in self.chat_history:
            self.chat_history[uid] = []

        # Добавляем пользовательский запрос
        self.chat_history[uid].append({
            "role": "user",
            "content": query
        })

        try: # Обворачиваем в try, потенциально опасный на ошибки код,
            # Для того что бы приложение не упало с ошибкой в ненужный момент
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=self.chat_history[uid],
                web_search=False
            )

            # Добавляем ответ ассистента в историю
            text = response.choices[0].message.content
            self.chat_history[uid].append({
                "role": "assistant",
                "content": text
            })
            
            return text
        except Exception as e:
            logger.warning("Произошла ошибка! {}", str(e))
            return f"Произошла ошибка ({str(e)})"
    def generate_image(self, promt):
        try:
            response = self.client.images.generate(
                model=self.image_model,
                prompt=promt,
                response_format="url"
            )
            url = response.data[0].url
            return url
        except Exception as e:
            logger.warning("Произошла ошибка! {}", str(e))
            raise e # Передаем ошибку выше 