ezkl gen-settings -M network.onnx

ezkl gen-srs --srs-path=17.srs --logrows=17

ezkl calibrate-settings -M network.onnx -D input.json -O settings.json

ezkl setup -M network.onnx --srs-path=17.srs --vk-path=vk.key --pk-path=pk.key --settings-path=settings.json

ezkl gen-witness -D input.json -M network.onnx --settings-path=settings.json

ezkl prove -M network.onnx --witness witness.json --pk-path=pk.key --proof-path=model.proof --srs-path=17.srs --settings-path=settings.json

ezkl verify --proof-path=model.proof --settings-path=settings.json --vk-path=vk.key --srs-path=17.srs


