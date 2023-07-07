import torch
from torch import autocast
from diffusers import UNet2DConditionModel
from diffusers import LMSDiscreteScheduler

from tqdm import tqdm


class LatentsHelper:
    def __init__(self, device):
        self.unet = UNet2DConditionModel.from_pretrained(
            'CompVis/stable-diffusion-v1-4', subfolder='unet')
        self.unet = self.unet.to(device)
        self.device = device

        self.scheduler = LMSDiscreteScheduler(
            beta_start=0.00085, beta_end=0.012,
            beta_schedule='scaled_linear', num_train_timesteps=1000)

    def produce_latents(self, text_embeddings, height=512, width=512,
                        num_inference_steps=50, guidance_scale=7.5, latents=None):
        if latents is None:
            latents = torch.randn((text_embeddings.shape[0] // 2, self.unet.in_channels, height // 8, width // 8))
        latents = latents.to(self.device)

        self.scheduler.set_timesteps(num_inference_steps)
        latents = latents * self.scheduler.sigmas[0]

        with autocast(self.device):
            for i, t in tqdm(enumerate(self.scheduler.timesteps)):
                # expand the latents if we are doing classifier-free guidance to avoid doing two forward passes.
                latent_model_input = torch.cat([latents] * 2)
                sigma = self.scheduler.sigmas[i]
                latent_model_input = latent_model_input / ((sigma ** 2 + 1) ** 0.5)

                # predict the noise residual
                with torch.no_grad():
                    noise_pred = self.unet(latent_model_input, t, encoder_hidden_states=text_embeddings)['sample']

                # perform guidance
                noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
                noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

                # compute the previous noisy sample x_t -> x_t-1
                latents = self.scheduler.step(noise_pred, i, latents)['prev_sample']

        return latents

