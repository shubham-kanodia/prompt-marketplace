from torch import nn
import ezkl
import os
import json
import torch
from decoder.MinifiedModel import MinifiedModel
from zk.export_helper import export

import subprocess
import re


class ZKSetupUtils:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), "data")
        self.onnx_path = os.path.join(self.base_path, "network.onnx")
        self.data_path = os.path.join(self.base_path, "input.json")
        self.settings_path = os.path.join(self.base_path, "settings.json")
        self.witness_path = os.path.join(self.base_path, "witness.json")
        self.srs_path = os.path.join(self.base_path, "17.srs")

        self.vk_path = os.path.join(self.base_path, "vk.key")
        self.pk_path = os.path.join(self.base_path, "pk.key")

    @staticmethod
    def _prepare_model(decoder):
        conv_layer_weights_data = decoder.conv_out.weight.data
        conv_layer_bias_data = decoder.conv_out.bias.data

        minified_model = MinifiedModel()

        minified_model.conv_out.weight.data = conv_layer_weights_data
        minified_model.conv_out.bias.data = conv_layer_bias_data

        minified_model.eval()

        return minified_model

    def _patch_model_settings(self):
        with open(self.settings_path, "r") as f:
            settings = json.load(f)

        settings["model_output_scales"] = [
            14
        ]

        with open(self.settings_path, "w") as f:
            json.dump(settings, f)

    def _generate_settings(self):
        run_args = ezkl.PyRunArgs()
        run_args.input_visibility = "private"
        run_args.param_visibility = "public"
        run_args.output_visibility = "hashed"

        ezkl.gen_settings(self.onnx_path, self.settings_path, py_run_args=run_args)

    def export_model(self, decoder, input_shape):
        # Input shape: [128, 3, 3]
        minified_model = self._prepare_model(decoder)

        export(minified_model, input_shape=input_shape, onnx_filename=self.onnx_path, input_filename=self.data_path,
               settings_filename=self.settings_path)

        self._generate_settings()
        # self._patch_model_settings()

    def generate_srs(self):
        ezkl.gen_srs(self.srs_path, 17)

    def generate_witness(self):
        ezkl.gen_witness(
            self.data_path, self.onnx_path, self.witness_path, settings_path=self.settings_path)

        assert os.path.isfile(self.witness_path)

    def setup_circuit(self):
        res = ezkl.setup(
            self.onnx_path,
            self.vk_path,
            self.pk_path,
            self.srs_path,
            self.settings_path,
        )

        assert res
        assert os.path.isfile(self.vk_path)
        assert os.path.isfile(self.pk_path)
        assert os.path.isfile(self.settings_path)

    def execute(self, decoder):
        print("Exporting model...")
        self.export_model(decoder, [128, 3, 3])

        print("Generating Witness...")
        self.generate_witness()

        print("Generating SRS...")
        self.generate_srs()

        print("Doing circuit setup...")
        self.setup_circuit()


class ZKInferenceUtils:
    def __init__(self):
        self.temp_base_path = "/tmp"
        self.base_path = os.path.join(os.path.dirname(__file__), "data")

        self.onnx_path = os.path.join(self.base_path, "network.onnx")
        self.pk_path = os.path.join(self.base_path, "pk.key")
        self.vk_path = os.path.join(self.base_path, "vk.key")
        self.params_path = os.path.join(self.base_path, "kzg.params")
        self.settings_path = os.path.join(self.base_path, "settings.json")

        self.witness_path = os.path.join(self.base_path, "witness.json")
        self.srs_path = os.path.join(self.base_path, "17.srs")
        self.contract_path = os.path.join(self.base_path, "Verifier.sol")
        self.abi_path = os.path.join(self.base_path, "Verifier.abi")

    def generate_proof(self, inputs):
        input_path = os.path.join(self.temp_base_path, "input.json")
        json.dump(inputs, open(input_path, "w"))

        proof_path = os.path.join(
            self.base_path,
            'test.pf'
        )

        print("Proving..")

        res = ezkl.prove(
            self.witness_path,
            self.onnx_path,
            self.pk_path,
            proof_path,
            self.srs_path,
            "evm",
            "single",
            self.settings_path,
        )

        assert res
        assert os.path.isfile(proof_path)

        print("Generated proof..")

    def get_proof_and_inputs(self):
        proof_path = os.path.join(
            self.base_path,
            'test.pf'
        )

        proof = ezkl.print_proof_hex(proof_path=proof_path)

        cmd = f"/tmp/ezkl/target/release/ezkl print-proof-hex --proof-path={proof_path}"
        op = subprocess.run(cmd, shell=True, capture_output=True)
        refined_output = op.stdout.strip()

        pb_inputs = None
        for line in refined_output.split():
            pattern = r'\[0x[0-9a-fA-F]+\]'
            addresses = re.findall(pattern, line.decode('utf-8'))
            if len(addresses):
                pb_inputs = addresses[0].strip("[]")
                break

        return pb_inputs, proof

    # def export_contract(self):
    #     # ezkl create-evm-verifier --srs-path=17.srs --settings-path=settings.json --vk-path=vk.key
    #     try:
    #         ezkl.create_evm_verifier(
    #             self.vk_path,
    #             self.srs_path,
    #             self.settings_path,
    #             self.contract_path,
    #             self.abi_path
    #         )
    #     except:
    #         pass
