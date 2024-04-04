from .audio_extraction import AudioExtractor
from pathlib import Path

from faster_whisper import WhisperModel


class Transcriber:
    def __init__(
        self,
        audio_folder: str | Path,
        model_path: str | Path,
        device: str,
    ):
        self.audio_folder = audio_folder
        self.audio_extractor = AudioExtractor(self.audio_folder)
        self.model_path = model_path
        self.device = device

    @property
    def audio_folder(self):
        return self._audio_folder

    @audio_folder.setter
    def audio_folder(self, folder_loc: str | Path):
        self._audio_folder = Path(folder_loc).absolute()

    @property
    def model_path(self):
        return self._model_path

    @model_path.setter
    def model_path(self, path: str | Path):
        self._model_path = Path(path).absolute()

    def transcribe(self, urls: str | list[str]) -> list[str]:
        """
        Transcribes the videos in the url list

        Parameters
        ----------
        urls : str | list[str]
            Contains the urls for the videos to be transcribed

        Returns
        -------
        result_list : list[str]
            A list where each of the elements are transcription of different audio files
        """
        # This helps handling both a single url and list of urls case with 1 LOC
        _urls = urls if urls is list else [urls]
        model = self._get_model()
        result_list = []

        for url in _urls:
            transcript = ""
            print(f"Fetching audio for {url}..")
            audio_file = self.audio_extractor.download_audio_from_yt(url)
            print(f"Transcribing {audio_file}")
            segments, _ = model.transcribe(audio_file)
            print("Transcription complete.")
            print(f"Appending to result list")
            for segment in segments:
                transcript += segment.text
                transcript += " "
            result_list.append(transcript)
        return result_list

    def _get_model(self) -> WhisperModel:
        """
        Returns the whisper model class
        """
        return WhisperModel(self.model_path, device=self.device)
