import xml.etree.ElementTree as eletree
import xml.dom.minidom as minidom

class ConfGenerator:
    def __init__(self, xml_data, config_data, patched_config_data):
        self.xml_data = xml_data
        self.config_data = config_data
        self.patched_config_data = patched_config_data
        self.classes = {}

    def gen_delta(self):
        additions = []
        deletions = []
        updates = []
        origin = self.config_data
        patch = self.patched_config_data
        for key in patch:
            if key not in origin:
                additions.append({"key": key, "value": patch[key]})
            elif origin[key] != patch[key]:
                updates.append({"key": key, "from": origin[key], "to": patch[key]})
        for key in origin:
            if key not in patch:
                deletions.append(key)
        return {"additions": additions, "deletions": deletions, "updates": updates}

    def delta_apply(self, delta):
        res_conf = self.config_data.copy()
        for upd in delta.get("updates", []):
            res_conf[upd["key"]] = upd["to"]
        for add in delta.get("additions", []):
            res_conf[add["key"]] = add["value"]
        for key in delta.get("deletions", []):
            if key in res_conf:
                del res_conf[key]
        return res_conf
    
    def gen_xml_conf(self):
        root_xml = eletree.fromstring(self.xml_data)
        classes_names = {}
        for elem in root_xml.findall('Class'):
            classes_names[elem.get('name')] = elem
        agg_map = {}
        for agg in root_xml.findall('Aggregation'):
            target = agg.get('target')
            if target not in agg_map:
                agg_map[target] = []
            source = agg.get('source')
            agg_map[target].append(source)
        root_class = None
        for elem in root_xml.findall('Class'):
            if elem.get('isRoot', 'false').lower() == 'true':
                root_class = elem
                break
        if root_class is None:
            return ''
        
        def xml_builder(class_name):
            elem = eletree.Element(class_name)  
            class_elem = classes_names.get(class_name)
            if class_elem is not None:
                for attr in class_elem.findall('Attribute'):
                    att_elem = eletree.SubElement(elem, attr.get('name'))
                    att_elem.text = attr.get('type')
            children = agg_map.get(class_name, [])
            for child_name in children:
                child_elem = xml_builder(child_name)
                elem.append(child_elem)
            return elem
        xml_root_elem = xml_builder(root_class.get('name'))
        reparsed = minidom.parseString(eletree.tostring(xml_root_elem, encoding='utf-8'))
        pretty_xml = '\n'.join(reparsed.toprettyxml(indent="  ").split('\n')[1:])
        return pretty_xml