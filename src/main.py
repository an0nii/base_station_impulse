import json
import os
from conf_generator import ConfGenerator
from meta_generator import MetaGenerator

if __name__ == '__main__':
    input_dir = '../input'
    output_dir = '../out'
    with open(os.path.join(input_dir, 'impulse_test_input.xml'), 'r') as xml_file:
        xml_data = xml_file.read()
    with open(os.path.join(input_dir, 'config.json'), 'r') as config_file:
        config_data = json.load(config_file)
    with open(os.path.join(input_dir, 'patched_config.json'), 'r') as patched_config_file:
        patched_config_data = json.load(patched_config_file)
    config_generator = ConfGenerator(xml_data, config_data, patched_config_data)
    config_xml = config_generator.gen_xml_conf()
    with open(os.path.join(output_dir, 'config.xml'), 'w') as xml_output_file:
        xml_output_file.write(config_xml)
    delta = config_generator.gen_delta()
    with open(os.path.join(output_dir, 'delta.json'), 'w') as delta_output_file:
        json.dump(delta, delta_output_file, indent=4)
    res_patched = config_generator.delta_apply(delta)
    with open(os.path.join(output_dir, 'res_patched_config.json'), 'w') as res_output_file:
        json.dump(res_patched, res_output_file, indent=4)
    meta_generator = MetaGenerator(xml_data)
    meta_output = meta_generator.gen_meta()
    with open(os.path.join(output_dir, 'meta.json'), 'w') as meta_output_file:
        json.dump(meta_output, meta_output_file, indent=4)