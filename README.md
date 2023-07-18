# Prompt Marketplace

# Setup

* Create a python virtual env

* Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

* Running model inference script to get the output and input of last layer from variational auto-encoder (VAE) 

    ```bash
    python scripts/model_inference.py
    ```
  
* Setting up srs, prover and verifier keys, circuit

    ```bash
    python zk_setup.py
    ```

# Basic Code Walkthrough

* The entire ML pipeline runs through the [pipeline file](helpers/pipeline.py). It is further supported by [auto encoder helper](helpers/auto_encoder.py), [latents helper](helpers/latents.py), [text embeddings generator](helpers/text_embeddings.py).

* The ZK utils responsible for generating srs, pk, vk and circuit is [here](zk/zk_utils.py).

* Circuit related commands for ezkl are in [commands](commands/) directory.
