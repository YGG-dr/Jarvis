from Jarvis.src.jarvis.core.app import InitJarvis
from Jarvis.src.jarvis.core.echo_sense import VoiceListener

routes_jarvis: list[str] = [
    "InitJarvis",
    "EchoSense"
]

__all__ = routes_jarvis