from helpers.text_embeddings import TextEmbeddingsHelper
from helpers.latents import LatentsHelper
from helpers.cache import CacheHelper
from helpers.auto_encoder import AutoEncoderHelper

import torch


class Pipe:
    def __init__(self, text_embeddings_helper: TextEmbeddingsHelper, latents_helper: LatentsHelper, auto_encoder_helper: AutoEncoderHelper, cache_helper = None):
        if not cache_helper:
            self.cache_helper = CacheHelper()
        else:
            self.cache_helper = cache_helper

        self.text_embeddings_helper = text_embeddings_helper
        self.latents_helper = latents_helper

        self.auto_encoder_helper = auto_encoder_helper

    def forward(self, prompt):
        text_embeds = self.text_embeddings_helper.embed([prompt])
        latents = self.latents_helper.produce_latents(text_embeds)

        latents = 1 / 0.18215 * latents

        with torch.no_grad():
            imgs, semi_inp = self.auto_encoder_helper.decode(latents)

        return imgs, semi_inp
