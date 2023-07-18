from zk.zk_utils import ZKSetupUtils
from helpers.auto_encoder import AutoEncoderHelper

from zk.zk_utils import ZKInferenceUtils

import json

zk_inference_utils = ZKInferenceUtils()

device = "cpu"
auto_encoder_helper = AutoEncoderHelper(device)

decoder = auto_encoder_helper.vae.decoder

zk_utils = ZKSetupUtils()

# Setup pk, vk keys, srs and circuit
# zk_utils.execute(decoder)

inputs = json.load(open("../zk/data/input.json", "r"))

# Uncomment to generate proof
# zk_inference_utils.generate_proof(inputs)

print(
    zk_inference_utils.get_proof_and_inputs()
)
