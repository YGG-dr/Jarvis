from __future__ import annotations

# Biblioteca de reconhecimento de voz
import speech_recognition as sr

# Interface rica para feedback visual no terminal
from rich.console import Console
from rich.status import Status

# Tipagem moderna
from typing import Optional

# Utilitários de normalização de texto
import unicodedata
import re


# Instância global de console (evita recriação)
console: Console = Console()

# Instância única do reconhecedor (melhor prática)
reconhecedor: sr.Recognizer = sr.Recognizer()


class VoiceListener:
    """
    Classe responsável por:
    - Captura de áudio
    - Transcrição de fala
    - Validação de comandos
    """

    @staticmethod
    def ouvir(
        *,
        timeout: float = 5.0,              # tempo máximo esperando o usuário começar a falar
        frase_limite: float | None = 10.0, # tempo máximo da fala
        numeracao_dispositivo: int = 0,    # índice do microfone
        calibracao: float = 1.0            # tempo de calibração do ruído ambiente
    ) -> Optional[sr.AudioData]:
        """
        Captura áudio do microfone.

        Retorna:
            AudioData se sucesso
            None se erro/timeout
        """

        with sr.Microphone(device_index=numeracao_dispositivo) as mic:

            # Ajusta o ruído ambiente para melhorar precisão
            reconhecedor.adjust_for_ambient_noise(mic, duration=calibracao)

            try:
                # Escuta o áudio do usuário
                audio: sr.AudioData = reconhecedor.listen(
                    mic,
                    timeout=timeout,
                    phrase_time_limit=frase_limite
                )

                return audio

            except sr.WaitTimeoutError:
                console.print("[yellow]Tempo de espera excedido.[/]")
                return None

            except sr.UnknownValueError:
                console.print("[red]Não foi possível entender o áudio.[/]")
                return None

            except sr.RequestError:
                console.print("[red]Erro ao acessar serviço de reconhecimento.[/]")
                return None

    @staticmethod
    def transcrever(
        audio: sr.AudioData,
        idioma: str = "pt-BR"
    ) -> Optional[str]:
        """
        Converte áudio em texto usando Google Speech Recognition.
        """

        try:
            texto: str = reconhecedor.recognize_google(
                audio,
                language=idioma,
            )

            return texto

        except sr.UnknownValueError:
            console.print("[red]Transcrição falhou.[/]")
            return None

        except sr.RequestError:
            console.print("[red]Erro na API de transcrição.[/]")
            return None

    @staticmethod
    def normalizar(texto: str) -> str:
        """
        Normaliza texto:
        - remove acentos
        - lowercase
        - remove espaços extras
        """

        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")
        texto = texto.lower().strip()

        return texto

    @staticmethod
    def validar_ativacao(texto: str) -> bool:
        """
        Verifica se o texto corresponde ao nome do assistente.
        """

        variacoes_nome_jarvis: list[str] = [
            "jarvis",
            "javis",
            "djarvis",
            "jarvi",
            "jarve",
            "jarviz"
        ]

        texto_normalizado = EchoSense.normalizar(texto)

        return texto_normalizado in variacoes_nome_jarvis

    @staticmethod
    def enviar(texto: str) -> None:
        """
        Envia o texto para o modelo de IA (Qwen, etc).

        TODO: Segurança
        - Validar segurança do input 
        - Implementar comunicação com backend da IA
        """

        # TODO: validação de segurança
        # TODO: integração com modelo (Qwen2.5)

        console.print(f"[cyan]Enviando para IA:[/] {texto}")

    @staticmethod
    def iniciar_echo_sense() -> str | None:
        audio = EchoSense.ouvir()

        if audio:
            texto = EchoSense.transcrever(audio)

        if texto:
            console.print(f"[green]Você disse:[/] {texto}")

        if EchoSense.validar_ativacao(texto):
            console.print("[blue]Assistente ativado![/]")
            EchoSense.enviar(texto)
    