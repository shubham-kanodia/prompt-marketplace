from helpers.text_embeddings import TextEmbeddingsHelper
from helpers.latents import LatentsHelper
from helpers.cache import CacheHelper
from helpers.auto_encoder import AutoEncoderHelper

import torch

# device = "cpu"
#
# text_embeddings_helper = TextEmbeddingsHelper(device)
# latents_helper = LatentsHelper(device)
# cache_helper = CacheHelper()
# auto_encoder_helper = AutoEncoderHelper(device)
#
#
# prompts = ['Super cool anime character']
#
#
# # text_embeds = text_embeddings_helper.embed(prompts)
# text_embeddings = cache_helper.get_object("embeds")
#
# latents = cache_helper.get_object("latents")
# # latents = latents_helper.produce_latents(text_embeds)
#
# latents = 1 / 0.18215 * latents
#
# with torch.no_grad():
#     imgs, semi_inp = auto_encoder_helper.decode(latents)

# print(imgs)

# decoder_model_layers = list(self.state_dict().keys())
# conv2d_weights_layer_name = 'conv_out.weight'
# conv2d_bias_layer_name = 'conv_out.bias'
#
# conv_layer_weights_data = self.conv_out.weight.data
# conv_layer_bias_data = self.conv_out.bias.data

import json
from zk.zk_utils import ZKInferenceUtils

zk_inference_utils = ZKInferenceUtils()

inputs = json.load(open("zk/data/input.json", "r"))
zk_inference_utils.generate_proof(inputs)
# auto_encoder_helper.export_minified_model(semi_inp, imgs, "data/model.onnx")


# from helpers.export_helper import generate_proof
#
#
# generate_proof("data/model.onnx", "data/pk.key", "data/20.srs", "data/settings.json")