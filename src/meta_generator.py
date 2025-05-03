import xml.etree.ElementTree as eletree

class MetaGenerator:
    def __init__(self, xml_data):
        self.xml_data = xml_data

    def parse_xml(self):
        meta_dict = {}
        root = eletree.fromstring(self.xml_data)
        for class_elem in root.findall('Class'):
            class_name = class_elem.get('name')
            meta_dict[class_name] = {
                'class': class_name,
                'documentation': class_elem.get('documentation', ''),
                'isRoot': class_elem.get('isRoot', 'false').lower() == 'true',
                'parameters': []
            }
            for attr in class_elem.findall('Attribute'):
                meta_dict[class_name]['parameters'].append({
                    'name': attr.get('name'),
                    'type': attr.get('type')
                })
        for agg in root.findall('Aggregation'):
            source = agg.get('source')
            target = agg.get('target')
            source_mult = agg.get('sourceMultiplicity', "")
            if source_mult:
                if ".." in source_mult:
                    min_val, max_val = source_mult.split("..")
                else:
                    min_val = max_val = source_mult
                if source in meta_dict:
                    meta_dict[source]['min'] = min_val
                    meta_dict[source]['max'] = max_val
            if target in meta_dict:
                exists = any(param.get('name') == source for param in meta_dict[target]['parameters'])
                if not exists:
                    meta_dict[target]['parameters'].append({
                        'name': source,
                        'type': 'class'
                    })
        return list(meta_dict.values())

    def gen_meta(self):
        return self.parse_xml()