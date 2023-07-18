# Commands

forge create --rpc-url $RPC_URL --private-key $PRIVATE_KEY verifier.sol:Verifier


ezkl setup  -M network.onnx --srs-path=20.srs --vk-path=vk.key --pk-path=pk.key --settings-path=settings.json

ezkl gen-circuit-params --calibration-target resources --model examples/onnx/1l_relu/network.onnx --settings-path circuit.json

ezkl aggregate --logrows=20 --aggregation-snarks=test.json --vk-path aggr_c2d.vk --proof-path test.json --srs-path=20.srs --settings-paths=circuit.json
