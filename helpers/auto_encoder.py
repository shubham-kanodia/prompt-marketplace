from decoder.vae import AutoencoderKL


class AutoEncoderHelper:
    def __init__(self, device):
        self.vae = AutoencoderKL.from_pretrained(
            'CompVis/stable-diffusion-v1-4', subfolder='vae')
        self.vae = self.vae.to(device)
        self.device = device

    def decode(self, latents):
        dec, semi_inp = self.vae.decode(latents)
        return dec, semi_inp
