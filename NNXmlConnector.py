
import xml.etree.ElementTree as ET
import NNGlobals



class NNXmlConnector(object):
    """
    THIS OBJECT IMPORT THE XML FILE AND CONVERT TO THE PROPER VALUE
    """


    def __init__(self, doc_path, main_surface):


        self.doc_path = doc_path
        self.xml_tree = ET.parse(self.doc_path)
        self.xml_root = self.xml_tree.getroot()

        # MAIN SURFACE
        self.surface = main_surface


    def get_first_layer(self, tag_name):
        first_layer = self.xml_root.findall(tag_name)
        #print(first_layer)
        return first_layer


    def get_scene_elem(self, scene_number):
        first_layer = self.get_first_layer('scene')
        result = None

        for scene in first_layer:
            # IF THE ATTRIBUTES 'number' IS SAME AS THE PARAMETER
            if int(scene.attrib["number"]) is scene_number:
                result = scene

        return result


    def get_all_scene_layer(self):
        scenes_layer = self.get_first_layer('scene')
        return scenes_layer


    def get_scene_count(self):
        scenes_layer = self.get_first_layer('scene')
        return len(scenes_layer)




    # ROUTER FOR STRING VALUES
    # THIS IS FOR PREVENTING TO USE eval() FUNCTION !
    def check_string(self, input_text):

        if input_text == 'self.surface':
            return self.surface
        elif input_text == 'NNGlobals.USER_RESULT':
            return NNGlobals.NNGlobals.USER_RESULT
        else:
            return input_text

