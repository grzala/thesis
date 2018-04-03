import bpy 
from bpy.types import Menu, Panel, UIList 
import os
import sys
import traceback
from pprint import pprint
from mathutils import *
import json
import sqlite3


bl_info= {
    "name": "NLPanim",
    "author": "grzala",
    "version": (1, 0, 0),
    "blender": (2, 70, 0),
    "location": "View3D > Tool Shelf",
    "description": "Generate animation from natural language",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}



# This file is a Blender extension which assembles the final animation given JSON instructions

# Unselect all objects
def unselect_all_objects():
    for obj in bpy.data.objects:
        obj.select = False
        
# Select a given object
def select_obj(obj):
    unselect_all_objects()
    unselect_all_nla()
    obj.select = True
    bpy.context.scene.objects.active = obj

# Imported character
class Character:
    current_pushdown_strip = 1 # static class variable - each new Character instance gets a new pushdown strip
    
    def __init__(self, obj, name):
        self.current_strip = 0 # NLA strip
        self.name = name # Name
        self.object = obj # Blender object (armature and model)
        self.camoffset = Vector((-0.5, -1.8, 1.65)) # Camera offset
        self.camrot = Vector((0.0, 0.0, 1.3)) # Camera rotation
        self.select()
        bpy.context.area.type = 'NLA_EDITOR'
        # Pushdown action on NLA immediately after creating the character
        bpy.ops.nla.action_pushdown(channel_index=Character.current_pushdown_strip)
        Character.current_pushdown_strip += 3 # Increment pushdown strip to prepare for next character
        # Delete the newly added NLA strip to prepare for further animation clips
        bpy.ops.nla.delete()
        
    # Select character object
    def select(self):
        unselect_all_objects()
        unselect_all_nla()
        self.object.select = True
        bpy.context.scene.objects.active = self.object
    
    # Move the character on the scene by an offset
    def move(self, vec):
        self.select()
        self.object.location += Vector((vec))
        
    # Rotate the character on the scene by euler 
    def rotate(self, vec):
        self.select()
        self.object.rotation_euler = vec
        
    def set_cam_offset(self, x, y, z):
        self.camoffset = Vector((x, y, z))
        
    def set_cam_rot(self, x, y, z):
        self.camrot = Vector((x, y, z))
    
    # Get camera position - character position + camera offset
    def get_camera_position(self):
        pos = Vector(self.object.location)
        offset = Vector((self.camoffset))
        mat = Matrix.Rotation(self.object.rotation_euler.z, 4, 'Z')
        offset.rotate(mat)
        
        print("GETTING CAM OFFSET", self.camoffset)

        return pos + offset
    
    # Get camera rotation to point at Character's face
    def get_camera_rotation(self, cam):
        headloc = Vector(self.object.location)
        headloc += self.camrot
        camloc = cam.location
        direction = headloc - camloc
        rot_quat = direction.to_track_quat('-Z', 'Y')
        rot = rot_quat.to_euler()
        return rot
        
    # Select an nla strip that belongs to the character
    def select_nla_by_index(self, index):
        unselect_all_nla()
        ob = self.object
        ad = ob.animation_data
        if ad:
            if ad.nla_tracks == None: return
            # Iterate through all nla_tracks; select the correct one
            for i, track in enumerate(ad.nla_tracks):
                res = i == index
                track.select = res
                if res: ad.nla_tracks.active = track
                for key in track.strips.keys():
                    track.strips[key].select = False
        
    # Make character perform an animation from a given frame
    def add_action(self, action_name, frame):
        self.select()
        bpy.context.area.type = 'NLA_EDITOR'
        action = bpy.data.actions[action_name]
        action_len = action.frame_range[1] - action.frame_range[0]
        
        # Add a new NLA track. Add the action on the newly created NLA track
        if (self.current_strip == 0):
            self.select_nla_by_index(self.current_strip)
            bpy.ops.nla.actionclip_add(action=action_name)
            self.current_strip += 1
        
        else:
            self.select_nla_by_index(self.current_strip-1)
            bpy.ops.nla.tracks_add()
            self.select_nla_by_index(self.current_strip)
            track = get_nla_by_index(self.current_strip)
            self.current_strip += 1
            bpy.ops.nla.actionclip_add(action=action_name)
            strip = track.strips[track.strips.keys()[0]]
            strip.select = True
        
        # Move the animation to begin at a correct frame
        bpy.ops.transform.transform(mode='TRANSLATION', value=(frame, -1.00505, 0, 0), axis=(0, 0, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return action, action_len+1
            
        
# Switch between layers
def switch_to_layer(index):
    length = len(bpy.data.scenes["Scene"].layers)
    bpy.data.scenes["Scene"].layers[index] = True
    for i in range(0, length):
        bpy.data.scenes["Scene"].layers[i] = i == index
        
# Unselect NLA tracks
def unselect_all_nla():
    for ob in bpy.data.objects:
        ad = ob.animation_data
        if ad:
            for track in ad.nla_tracks:
                track.select = False
                for strip in track.strips: 
                    strip.select = False
            ad.nla_tracks.active = None

def get_nla_by_index(index):
    ob = bpy.context.object
    ad = ob.animation_data
    if ad:
        if (index >= len(ad.nla_tracks)): return None
        for i, track in enumerate(ad.nla_tracks):
            if i == index: return track


def import_fbx(name):
    fpath = os.getcwd() + '\\' + name
    bpy.ops.import_scene.fbx(filepath=fpath, filter_glob="*.fbx;")

# Movie sequences and subtitles
def clear_sequences():
    if not bpy.context.sequences: return
    for sequence in bpy.context.sequences:
        sequence.select = True
    bpy.ops.sequencer.delete()


def cleanup():
    # Remove objects from all layers, actions and Movie sequences
    switch_to_layer(0)
    bpy.context.scene.frame_set(1)
    for object in bpy.data.objects:
        object.select = True
    bpy.ops.object.delete()
    switch_to_layer(1)
    bpy.ops.object.delete()
    switch_to_layer(0)
    
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)
        
    clear_sequences()
        
        
# Import an action from FBX and rename it; Leave the imported armature an a different layer
def import_anim(anim_name, anim_file):
    switch_to_layer(1)
    old_actions = []
    for action in bpy.data.actions:
        old_actions.append(action.name)
    import_fbx(ANIM_FOLDER + '\\' + anim_file)
    switch_to_layer(0)
    for action in bpy.data.actions:
        if action.name not in old_actions:
            action.name = anim_name
            return action
    
# Import a character model
def import_character(character_name, character_file):
    switch_to_layer(0)
    old_objects = []
    for object in bpy.data.objects:
        old_objects.append(object.name)
    import_fbx(MODEL_FOLDER + '\\' + character_file)
    for object in bpy.data.objects:
        if object.name not in old_objects:
            object.name = character_name
            return object
    
# Add subtitle strip between given frames
def add_subtitle(text, start_frame, end_frame):
    bpy.context.area.type = 'SEQUENCE_EDITOR'
    bpy.ops.sequencer.effect_strip_add(frame_start=start_frame+1, frame_end=end_frame-1, channel=1, type='TEXT')
    seq = bpy.context.selected_sequences[0]
    seq.text = text
    seq.wrap_width = 1
    seq.font_size = 60
    seq.color = (0.75, 0.75, 0.75, 1)

# Analyze dialogue, decide which characters and actions need importing
def prepare_dialogue(dialogue):
    required_characters = []
    anims = []
    for line in dialogue:
        for anim in line["clip"]:
            to_add = [anim["name"], anim["file"]]
            if to_add not in anims:
                anims.append(to_add)
        name = line["character"]
        if name not in required_characters: required_characters.append(name)
    return required_characters, anims

# Prepare dialogue lines in a more suitable data structure
def prepare_lines(dialogue):
    lines = []
    for line in dialogue:
        new_line = {}
        new_line['character'] = line['character']
        new_line['anim'] = line['clip'][0]['name']
        new_line['text'] = line['text']
        lines.append(new_line)
    return lines




####################### BLENDER ADDON #########################


prepared = False
prepared_data = None
char_choice_to_draw = []
cached_models = {}
error_message = None


# Assemble animation
def prepare(anim_folder, model_folder, db_path, dialogue_path):
    global ANIM_FOLDER, MODEL_FOLDER, error_message
    Character.current_pushdown_strip = 1
    dialogue = None
    try:
        dialogue = json.load(open(os.getcwd() + '\\' + dialogue_path[2:]))
    except:
        return None
    
    ANIM_FOLDER = anim_folder
    MODEL_FOLDER = model_folder
    pprint(dialogue)
    cleanup() # Clean and prepare scene
    
    # Get required characters and animation
    required_characters, anims = prepare_dialogue(dialogue)
    
    # Import all necessary animation clips
    for anim in anims:
        import_anim(anim[0], anim[1])
        
    lines = prepare_lines(dialogue)
    
    if len(required_characters) > 2:
        error_message = "Too many characters in the scene."
        return None
    elif len(required_characters) < 1:
        error_message = "Not enough characters. The scene file may be corrupted."
        return None
    
    result = {}
    result['lines'] = lines
    result['characters'] = required_characters
    result['anim_folder'] = anim_folder
    result['model_folder'] = model_folder
    result['db'] = db_path.replace("/", "")
    
    print("PREPARED")
    error_message = None
    return result
    
    
    
def finalize(character_choice, models, lines):
    # Import all needed character models
    print("MODELS:", models)
    characters = {}
    sorted_char_names = sorted(character_choice.keys())
    print("CHARCHOICE2:", character_choice)
    for charname in sorted_char_names:
        print("NOWADDING:", charname)
        modelname = character_choice[charname]
        name = charname
        model = models[modelname]
        file = model['file']
        
        newchar = Character(import_character(name, file), name)
        newchar.set_cam_offset(model['cam_offset_x'], model['cam_offset_y'], model['cam_offset_z'])
        newchar.set_cam_rot(model['cam_rot_x'], model['cam_rot_y'], model['cam_rot_z'])

        characters[name] = newchar
    
    # Support only two characters. Place the second character in front of the first character
    if len(sorted_char_names) > 1:
        char = characters[sorted_char_names[1]]
        char.move((0.0, -1.8, 0.0))
        char.rotate((0.0, 0.0, 3.14))
    
    # Start assembling the animation
    current_frame = 0
    texts = []
    # For each dialogue line, append animation to character
    for line in lines:
        old_frame = current_frame
        character = characters[line['character']]
        current_frame += character.add_action(line['anim'], current_frame)[1]
        texts.append({'character': character.name, 'text': line['text'], 'from': old_frame, 'to': current_frame})
    bpy.context.scene.frame_end = current_frame+1
    
    # Add Subtitles
    bpy.context.area.type = 'SEQUENCE_EDITOR'
    bpy.ops.sequencer.scene_strip_add(frame_start=1, channel=1, scene='Scene')
    for text in texts:
        add_subtitle(text['text'], text['from'], text['to'])
        

    
    # Add camera
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.object.add(type="CAMERA")
    cam = bpy.data.objects["Camera"]
    cam.location += Vector((0.0, 0.0, 5.0))
    lamps = []
    # Add lamps
    bpy.ops.object.add(type="LAMP")
    lamps.append(bpy.context.scene.objects.active)
    bpy.ops.object.add(type="LAMP")
    lamps.append(bpy.context.scene.objects.active)
    lamps[0].data.type = "SUN"; lamps[1].data.type = "SUN"
    lamps[0].location += Vector((-3.0, 0.0, 6.0))
    lamps[0].rotation_euler = Vector((0.0, -0.8, 0.0))
    lamps[1].location += Vector((3.0, 0.0, 6.0))
    lamps[1].rotation_euler = Vector((0.0, 0.8, 0.0))
    
    # Focus camera on a character when they start talking
    select_obj(cam)
    for text in texts:
        char = characters[text['character']]
        # Position camera, insert keyframe
        cam.location = char.get_camera_position()
        cam.rotation_euler = char.get_camera_rotation(cam)
        bpy.context.scene.frame_current = text['from']+1
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        
    bpy.context.area.type = 'GRAPH_EDITOR'
    bpy.ops.graph.interpolation_type(type='CONSTANT')

    # Add floor
    bpy.ops.mesh.primitive_plane_add()
    plane = bpy.context.scene.objects.active
    plane.location += Vector((0.0, 0.0, -0.2))
    plane.scale = Vector((50.0, 50.0, 0.0))
    
    bpy.context.scene.frame_current = 1
    bpy.context.area.type = 'VIEW_3D'
    
    global prepared 
    prepared = False


############ BLENDER UI #####################

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_available_models(db):
    print("OPENING:", db)
    con = sqlite3.connect(os.getcwd() + '\\' + db)
    query = "SELECT * FROM models"
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result

# Update character choice list
def update_char_choice_list(db, characters):
    global char_choice_to_draw, cached_models
    char_choice_to_draw = []
    cached_models = {}
    
    av_chars = get_available_models(db)
    lst = []
    
    i = 0
    for char in av_chars:
        cached_models[char['name']] = char
        lst.append((str(i), char['name'], char['name']))
        i += 1
            
    i = 0
    for character in characters:
        setattr(bpy.types.Scene, 'character_choice_' + str(i), bpy.props.EnumProperty \
          (
          name = character,
          items = lst
          )
        )
        char_choice_to_draw.append('character_choice_' + str(i))
        i += 1
    setattr(bpy.types.Scene, 'character_choice_' + str(i), None) 
    
# Clean button
class CleanOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.clean_operator"
    bl_label = "CleanOperator"

    # On click
    def execute(self, context):
        cleanup()
        return {'FINISHED'}

# Execute button
class ExecuteOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.execute_operator"
    bl_label = "Assembly Execute Operator"

    # On click
    def execute(self, context):
        global prepared, character_choice_items, prepared_data
        try:
            prepared_data = prepare(context.scene.anim_folder, context.scene.model_folder, context.scene.database, context.scene.dialogue)
            
            if prepared_data:
                prepared = True
                
                update_char_choice_list(prepared_data['db'], prepared_data['characters'])
            
        except Exception as e:
            print(str(e))
            return {'FINISHED'}
        return {'FINISHED'}
    
# Finalize button
class FinalizeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.finalize_operator"
    bl_label = "Assembly Finalize Operator"

    # On click
    def execute(self, context):
        print("FINALIZE")
        
        character_choice = {}
        i = 0
        for name in char_choice_to_draw:
            data = getattr(bpy.types.Scene, name)[1]
            choice_idx = int(getattr(context.scene, name))
            [1]
            character = data['name']
            choice = data['items'][choice_idx][1]
            print("DATA:", data)
            character_choice[character] = choice
            i += 1
            
        print("CHARACTER_CHOICE:", character_choice)
        
        finalize(character_choice, cached_models, prepared_data['lines'])
        
        print("FINALIZED")
        return {'FINISHED'}
    
class View3DPanel(): 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 

# Extension GUI
class GenerateAnimationPanel(View3DPanel, Panel): 
    bl_label = "Sources"
    bl_context = "objectmode" 
    bl_category = "Generate NLP anim" 
    
    def test():
        print("test")
    
    def draw(self, context): 
        layout = self.layout
        col = layout.column()
        
        col.operator("object.clean_operator", text="Clean", icon="ERROR")
        
        col.prop(context.scene, 'anim_folder')
        col.prop(context.scene, 'model_folder')
        col.prop(context.scene, 'database')
        col.prop(context.scene, 'dialogue')
        
        col.operator("object.execute_operator", text="Prepare", icon="ANIM") 
        
class FinalizeAnimationPanel(View3DPanel, Panel): 
    bl_label = "Finalize"
    bl_context = "objectmode" 
    bl_category = "Generate NLP anim" 
        
    @classmethod
    def poll(cls, context):
        return prepared
    
    def draw(self, context): 
        global char_choice_to_draw
        layout = self.layout
        col = layout.column()
        col.label("------- Choose models -------")
        
        for name in char_choice_to_draw:
            col.prop(context.scene, name)
        
        col = layout.column()
        col.label("------------- Assemlbe -------------")
        
        layout.operator("object.finalize_operator", text="Assemble", icon="AUTO") 

class ErrorPanel(View3DPanel, Panel): 
    bl_label = "Error"
    bl_context = "objectmode" 
    bl_category = "Generate NLP anim" 
        
    @classmethod
    def poll(cls, context):
        return error_message != None
    
    def draw(self, context): 
        layout = self.layout
        col = layout.column()
        col.label("ERROR: " + error_message)
        
        

        
# GUI buttons
def register():
    #bpy.utils.register_module(__name__)
    bpy.utils.register_class(GenerateAnimationPanel)
    bpy.utils.register_class(ExecuteOperator)
    bpy.utils.register_class(CleanOperator)
    bpy.utils.register_class(FinalizeOperator)
    bpy.utils.register_class(FinalizeAnimationPanel)
    bpy.utils.register_class(ErrorPanel)
    
    
    bpy.types.Scene.anim_folder = bpy.props.StringProperty \
      (
      name = "Animations Directory",
      default = "",
      description = "Define the animation directory",
      subtype = 'DIR_PATH'
      )
      
    bpy.types.Scene.model_folder = bpy.props.StringProperty \
      (
      name = "Models Directory",
      default = "",
      description = "Define the models directory",
      subtype = 'DIR_PATH'
      )
      
    bpy.types.Scene.database = bpy.props.StringProperty \
      (
      name = "Database",
      default = "",
      description = "SQLite database path",
      subtype = 'FILE_PATH'
      )      
    bpy.types.Scene.dialogue = bpy.props.StringProperty \
      (
      name = "Dialogue",
      default = "",
      description = "Dialogue Path",
      subtype = 'FILE_PATH'
      )

    

def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__": 
    register()
    # Get current path
    dir = os.path.dirname(bpy.data.filepath)
    if not dir in sys.path:
        sys.path.append(dir)