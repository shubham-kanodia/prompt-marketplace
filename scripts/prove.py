from zk.zk_utils import ZKSetupUtils
from helpers.auto_encoder import AutoEncoderHelper

device = "cpu"
auto_encoder_helper = AutoEncoderHelper(device)

decoder = auto_encoder_helper.vae.decoder

zk_utils = ZKSetupUtils()
zk_utils.execute(decoder)

