from pathlib import Path
from typing import Optional

from pytube import YouTube


class AudioExtractor:
    """This class helps in downloading the audio from a youtube video.

    Attributes
    ----------
    parent_folder : str | Path
        Path to the parent folder that contains the extracted audio files.
    """

    def __init__(self, parent_folder: str | Path):
        if parent_folder is None:
            raise ValueError("Please provide a path to parent folder.")

        self.parent_folder = Path(parent_folder)

    def download_audio_from_yt(self, url: str, filename: Optional[str] = None) -> Path:
        """Downloads the audio from youtube videos to the directory specified.
        Optionally, the filename can be changed.

        Parameters
        ----------
        url : str
            The url to the youtube video of which the audio is to be downloaded.

        filename : str, optional
            The filename for the audio file to be downloaded.
        """
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True)
        _filename = filename if filename is not None else f"{yt._title} audio"
        stream[0].download(output_path=self.parent_folder, filename=_filename + ".mp3")
        return self.parent_folder + '/' + _filename + ".mp3"
