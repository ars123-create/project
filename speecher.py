from __future__ import annotations

from speechkit import Session, SpeechSynthesis, DataStreamingRecognition
from decouple import config
from io import BytesIO
from pyaudio import PyAudio, paInt16


class Speecher(object):

    CHANNELS_NUMBER = 1
    SAMPLE_RATE = 8_000
    CHUNK_SIZE = 4_000

    VOICE = "ermil"
    EMOTION = "good"
    AUDIO_FORMAT = "lpcm"
    LANGUAGE_CODE = "ru-RU"
    AUDIO_ENCODING = "LINEAR16_PCM"

    __oauth_token: str
    __catalog_id: str
    __session: Session


    def __init__(self: Speecher) -> None:
        self.__oauth_token = config('oauth_token', default='')
        self.__catalog_id = config('catalog_id', default='')
        self.__session = Session.from_yandex_passport_oauth_token(
            self.__oauth_token, 
            self.__catalog_id
        )


    def __pyaudio_play_audio_function(
        self: Speecher, 
        audio_data: BytesIO
    ) -> None:
    
        pyaudio_object = PyAudio()
        stream = pyaudio_object.open(
            format              = paInt16,
            channels            = self.CHANNELS_NUMBER,
            rate                = self.SAMPLE_RATE,
            output              = True,
            frames_per_buffer   = self.CHUNK_SIZE
        )
        for i in range(0, len(audio_data), self.CHUNK_SIZE):
            stream.write(audio_data[i:i + self.CHUNK_SIZE])

        stream.stop_stream()
        stream.close()
        pyaudio_object.terminate()


    def synthesize(self: Speecher, input_text: str) -> None:
        synthesizeAudio = SpeechSynthesis(self.__session)
        audio_data = synthesizeAudio.synthesize_stream(
            text            = input_text,
            voice           = self.VOICE,
            emotion         = self.EMOTION,
            format          = self.AUDIO_FORMAT, 
            sampleRateHertz = self.SAMPLE_RATE
        )
        self.__pyaudio_play_audio_function(audio_data)


    def __gen_audio_capture_function(self: Speecher):
        pyaudio_object = PyAudio()
        stream = pyaudio_object.open(
            format              = paInt16,
            channels            = self.CHANNELS_NUMBER,
            rate                = self.SAMPLE_RATE,
            input               = True,
            frames_per_buffer   = self.CHUNK_SIZE
        )
        try:
            while True:
                yield stream.read(self.CHUNK_SIZE)
        finally:
            stream.stop_stream()
            stream.close()
            pyaudio_object.terminate()


    def recognize(self: Speecher) -> str:
        data_streaming_recognition = DataStreamingRecognition(
            self.__session,
            language_code       = self.LANGUAGE_CODE,
            audio_encoding      = self.AUDIO_ENCODING,
            sample_rate_hertz   = self.SAMPLE_RATE,
            partial_results     = False,
            single_utterance    = True,
        )

        result_data = ""
        for text, final, end_of_utt in data_streaming_recognition.recognize(
            self.__gen_audio_capture_function
        ):
            result_data += text[0]
            if final:
                break

        return result_data
