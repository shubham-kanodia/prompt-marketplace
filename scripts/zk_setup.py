from zk.zk_utils import ZKUtils
from helpers.auto_encoder import AutoEncoderHelper

device = "cpu"
auto_encoder_helper = AutoEncoderHelper(device)

decoder = auto_encoder_helper.vae.decoder

zk_utils = ZKUtils()
zk_utils.execute(decoder)
