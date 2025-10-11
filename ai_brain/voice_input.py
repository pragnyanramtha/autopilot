"""
Voice input module for AI Brain.
Provides speech-to-text functionality for voice commands.
"""
import speech_recognition as sr
from typing import Optional
from rich.console import Console


class VoiceInput:
    """Handles voice input using speech recognition."""

    def __init__(self):
        """Initialize the voice input handler."""
        self.recognizer = sr.Recognizer()
        self.console = Console()

        # Adjust for ambient noise on initialization
        try:
            with sr.Microphone() as source:
                self.console.print("[dim]Calibrating microphone for ambient noise...[/dim]")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not calibrate microphone: {e}[/yellow]")

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text.

        Args:
            timeout: Maximum time to wait for speech to start (seconds)
            phrase_time_limit: Maximum time for a single phrase (seconds)

        Returns:
            Transcribed text or None if recognition failed
        """
        try:
            with sr.Microphone() as source:
                self.console.print("[bold yellow]🎤 Listening... (speak now)[/bold yellow]")

                # Listen for audio input
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                self.console.print("[dim]Processing speech...[/dim]")

                # Convert speech to text using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                self.console.print(f"[green]✓ Recognized:[/green] {text}")

                return text

        except sr.WaitTimeoutError:
            self.console.print("[yellow]No speech detected (timeout)[/yellow]")
            return None

        except sr.UnknownValueError:
            self.console.print("[yellow]Could not understand audio[/yellow]")
            return None

        except sr.RequestError as e:
            self.console.print(f"[red]Speech recognition service error: {e}[/red]")
            return None

        except OSError as e:
            self.console.print(f"[red]Microphone error: {e}[/red]")
            self.console.print("[yellow]Please check if your microphone is connected and accessible[/yellow]")
            return None

        except Exception as e:
            self.console.print(f"[red]Unexpected error during voice input: {e}[/red]")
            return None

    def test_microphone(self) -> bool:
        """
        Test if microphone is available and working.

        Returns:
            True if microphone is available, False otherwise
        """
        try:
            with sr.Microphone() as source:
                self.console.print("[green]✓ Microphone is available[/green]")
                return True
        except OSError:
            self.console.print("[red]✗ No microphone detected[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]✗ Microphone test failed: {e}[/red]")
            return False

    def listen_continuous(self, on_command_callback, stop_phrase: str = "stop listening"):
        """
        Listen continuously for voice commands until stop phrase is heard.

        Args:
            on_command_callback: Function to call with each recognized command
            stop_phrase: Phrase to stop continuous listening
        """
        self.console.print(f"[bold cyan]Starting continuous listening mode...[/bold cyan]")
        self.console.print(f"[dim]Say '{stop_phrase}' to exit[/dim]\n")

        try:
            with sr.Microphone() as source:
                while True:
                    try:
                        self.console.print("[yellow]🎤 Listening...[/yellow]")
                        audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

                        text = self.recognizer.recognize_google(audio)
                        self.console.print(f"[green]✓ Recognized:[/green] {text}\n")

                        # Check for stop phrase
                        if stop_phrase.lower() in text.lower():
                            self.console.print("[cyan]Stop phrase detected. Exiting continuous mode.[/cyan]")
                            break

                        # Call the callback with the recognized command
                        on_command_callback(text)

                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.console.print("[dim]Could not understand[/dim]\n")
                        continue
                    except Exception as e:
                        self.console.print(f"[red]Error: {e}[/red]\n")
                        continue

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Continuous listening interrupted[/yellow]")
