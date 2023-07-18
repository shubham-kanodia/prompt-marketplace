from helpers.text_embeddings import TextEmbeddingsHelper
from helpers.latents import LatentsHelper
from helpers.cache import CacheHelper
from helpers.auto_encoder import AutoEncoderHelper


class Pipe:
    def __init__(self, text_embeddings_helper: TextEmbeddingsHelper, latents_helper: LatentsHelper, auto_encoder_helper: AutoEncoderHelper, cache_helper = None):
        if not cache_helper:
            self.cache_helper = CacheHelper()
        else:
            self.cache_helper = cache_helper

        self.text_embeddings_helper = text_embeddings_helper
        self.latents_helper = latents_helper

        self.auto_encoder_helper = auto_encoder_helper

    def forward(self):
        pass
