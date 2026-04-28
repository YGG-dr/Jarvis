from whisper import Whisper
import ollama

class Jarvis():
    @staticmethod
    def get_input() -> str | None:
        pass
        
    @staticmethod
    def format_input() -> str | None:
        pass
    
    @staticmethod
    def execute() -> str | None:
        response = ollama.chat(model='llama2', messages=[
            {
                'role' = 'user',
                'content' = 'Whats a femboy'
            },
        ])
        
        return response['message']['content']

Jarvis.execute()