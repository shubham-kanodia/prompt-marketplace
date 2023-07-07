import torch
from transformers import CLIPTextModel, CLIPTokenizer


class TextEmbeddingsHelper:
    def __init__(self, device):
        self.tokenizer = CLIPTokenizer.from_pretrained('openai/clip-vit-large-patch14')
        text_encoder = CLIPTextModel.from_pretrained('openai/clip-vit-large-patch14')
        self.text_encoder = text_encoder.to(device)
        self.device = device

    def embed(self, prompt):
        # Tokenize text and get embeddings
        text_input = self.tokenizer(
            prompt, padding='max_length', max_length=self.tokenizer.model_max_length,
            truncation=True, return_tensors='pt')
        with torch.no_grad():
            text_embeddings = self.text_encoder(text_input.input_ids.to(self.device))[0]

        # Do the same for unconditional embeddings
        uncond_input = self.tokenizer(
            [''] * len(prompt), padding='max_length',
            max_length=self.tokenizer.model_max_length, return_tensors='pt')
        with torch.no_grad():
            uncond_embeddings = self.text_encoder(uncond_input.input_ids.to(self.device))[0]

        # Cat for final embeddings
        text_embeddings = torch.cat([uncond_embeddings, text_embeddings])
        return text_embeddings
