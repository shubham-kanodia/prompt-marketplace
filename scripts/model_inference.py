from helpers.text_embeddings import TextEmbeddingsHelper
from helpers.latents import LatentsHelper
from helpers.auto_encoder import AutoEncoderHelper

from helpers.pipeline import Pipe

import pickle

device = "cpu"

text_embeddings_helper = TextEmbeddingsHelper(device)
latents_helper = LatentsHelper(device)
auto_encoder_helper = AutoEncoderHelper(device)

pipeline = Pipe(text_embeddings_helper, latents_helper, auto_encoder_helper)

img, semi_inp = pipeline.forward("a cat smoking a pipe")


# img - The generated image
# semi_inp - The input to second last layer


pickle.dump(img, open("img.pkl", "wb"))
pickle.dump(semi_inp, open("semi_inp.pkl", "wb"))
