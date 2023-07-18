ezkl gen-settings -M network.onnx

ezkl setup -M network.onnx --srs-path=20.srs --vk-path=vk.key --pk-path=pk.key --settings-path=settings.json

ezkl gen-witness -D input.json -M network.onnx --settings-path=settings.json

ezkl prove --transcript=poseidon --strategy=accum -M network.onnx --proof-path test.pf --srs-path=20.srs --pk-path=pk.key --settings-path=settings.json --witness=witness.json

ezkl aggregate --logrows=20 --aggregation-snarks=test.pf --srs-path=20.srs

ezkl create-evm-verifier-aggr --srs-path=20.srs --vk-path vk_aggr.key
