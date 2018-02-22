import bpy
import os
import sys
import traceback
from pprint import pprint
from mathutils import *

dialogue = [
    {
        "text": " I hate this place.  This zoo. I can't stand it any longer.", 
        "character": "AGENT SMITH", 
        "clip": [
            {"name": "fear3", "joy": 0.0, "sadness": 0.0, "score": 0.472359, "file": "fear3.fbx", "anger": 0.85, "surprise": 0.0, "fear": 0.0, "disgust": 0.0, "id": 5}, 
            {"name": "anger", "joy": 0.7, "sadness": 0.0, "score": 0.347359, "file": "anger1.fbx", "anger": 0.6, "surprise": 0.0, "fear": 0.0, "disgust": 0.0, "id": 4}
        ], 
        "tones": {"joy": 0.0, "sadness": 0.836783, "disgust": 0.91887, "anger": 0.986412, "surprise": 0.0, "fear": 0.0}
    }, 
    {
        "text": " Repulsive, isn't it?", 
        "character": "AGENT SMITH2", 
        "clip": [
            {"name": "anger1", "joy": 0.0, "sadness": 0.0, "file": "anger1.fbx", "anger": 0.0, "surprise": 0.0, "fear": 0.0, "disgust": 0.0, "id": 6}
        ], 
        "tones": {"joy": 0.0, "sadness": 0.0, "disgust": 0.0, "anger": 0.0, "surprise": 0.0, "fear": 0.0}
    },
    {
        "text": " Damn.", 
        "character": "AGENT SMITH", 
        "clip": [
            {"name": "anger2", "joy": 0.0, "sadness": 0.0, "score": 0.472359, "file": "anger2.fbx", "anger": 0.85, "surprise": 0.0, "fear": 0.0, "disgust": 0.0, "id": 5}, 
        ], 
        "tones": {"joy": 0.0, "sadness": 0.836783, "disgust": 0.91887, "anger": 0.986412, "surprise": 0.0, "fear": 0.0}
    }, 
]

ANIM_FOLDER = "mocap"
MODEL_FOLDER = "models"

def unselect_all_objects():
    for obj in bpy.data.objects:
        obj.select = False
        

def select_obj(obj):
    unselect_all_objects()
    unselect_all_nla()
    obj.select = True
    bpy.context.scene.objects.active = obj

class Character:
    current_pushdown_strip = 1
    
    def __init__(self, obj, name):
        self.current_strip = 0
        self.name = name
        self.object = obj
        self.camoffset = Vector((-0.5, -1.8, 1.65))
        self.select()
        bpy.context.area.type = 'NLA_EDITOR'
        bpy.ops.nla.action_pushdown(channel_index=Character.current_pushdown_strip)
        Character.current_pushdown_strip += 3
        bpy.ops.nla.delete()
        
    def select(self):
        unselect_all_objects()
        unselect_all_nla()
        self.object.select = True
        bpy.context.scene.objects.active = self.object
    
    def move(self, vec):
        self.select()
        self.object.location += Vector((vec))
        
    def rotate(self, vec):
        self.select()
        self.object.rotation_euler = vec
    
    def get_camera_position(self):
        pos = Vector(self.object.location)
        offset = Vector((self.camoffset))
        mat = Matrix.Rotation(self.object.rotation_euler.z, 4, 'Z')
        offset.rotate(mat)

        return pos + offset
    
    def get_camera_rotation(self, cam):
        headloc = Vector(self.object.location)
        headloc += Vector((0.0, 0.0, 1.3))
        camloc = cam.location
        direction = headloc - camloc
        rot_quat = direction.to_track_quat('-Z', 'Y')
        rot = rot_quat.to_euler()
        return rot
        
    def select_nla_by_index(self, index):
        unselect_all_nla()
        ob = self.object
        ad = ob.animation_data
        if ad:
            print("SELECC: ", len(ad.nla_tracks))
            if ad.nla_tracks == None: return
            for i, track in enumerate(ad.nla_tracks):
                res = i == index
                track.select = res
                if res: ad.nla_tracks.active = track
                for key in track.strips.keys():
                    track.strips[key].select = False
        
    def add_action(self, action_name, frame):
        self.select()
        bpy.context.area.type = 'NLA_EDITOR'
        action = bpy.data.actions[action_name]
        action_len = action.frame_range[1] - action.frame_range[0]
        
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
        
        
        bpy.ops.transform.transform(mode='TRANSLATION', value=(frame, -1.00505, 0, 0), axis=(0, 0, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return action, action_len+1
            
        

def switch_to_layer(index):
    length = len(bpy.data.scenes["Scene"].layers)
    bpy.data.scenes["Scene"].layers[index] = True
    for i in range(0, length):
        bpy.data.scenes["Scene"].layers[i] = i == index
        
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

def clear_sequences():
    for sequence in bpy.context.sequences:
        sequence.select = True
    bpy.ops.sequencer.delete()


def cleanup():
    #remove objects and actions
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
    
        
def add_subtitle(text, start_frame, end_frame):
    bpy.context.area.type = 'SEQUENCE_EDITOR'
    bpy.ops.sequencer.effect_strip_add(frame_start=start_frame+1, frame_end=end_frame-1, channel=1, type='TEXT')
    seq = bpy.context.selected_sequences[0]
    seq.text = text
    seq.wrap_width = 1
    seq.font_size = 60
    seq.color = (0.75, 0.75, 0.75, 1)


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

def prepare_lines(dialogue):
    lines = []
    for line in dialogue:
        new_line = {}
        new_line['character'] = line['character']
        new_line['anim'] = line['clip'][0]['name']
        new_line['text'] = line['text']
        lines.append(new_line)
    return lines

def main():
    cleanup()
    #add them alphabetically?
    
    required_characters, anims = prepare_dialogue(dialogue)
    
    for anim in anims:
        import_anim(anim[0], anim[1])
        
    characters = {}
    for char in required_characters:
        name = char
        file = 'untitled.fbx'
        characters[name] = Character(import_character(name, file), name)
        
    if len(required_characters) > 1:
        char = characters[required_characters[1]]
        char.move((0.0, -1.8, 0.0))
        char.rotate((0.0, 0.0, 3.14))
        
    lines = prepare_lines(dialogue)
    
    current_frame = 0
    texts = []
    for line in lines:
        old_frame = current_frame
        character = characters[line['character']]
        current_frame += character.add_action(line['anim'], current_frame)[1]
        texts.append({'character': character.name, 'text': line['text'], 'from': old_frame, 'to': current_frame})
    bpy.context.scene.frame_end = current_frame+1
    
    
    bpy.context.area.type = 'SEQUENCE_EDITOR'
    bpy.ops.sequencer.scene_strip_add(frame_start=1, channel=1, scene='Scene')
    for text in texts:
        add_subtitle(text['text'], text['from'], text['to'])
        

    
    
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.object.add(type="CAMERA")
    cam = bpy.data.objects["Camera"]
    cam.location += Vector((0.0, 0.0, 5.0))
    lamps = []
    bpy.ops.object.add(type="LAMP")
    lamps.append(bpy.context.scene.objects.active)
    bpy.ops.object.add(type="LAMP")
    lamps.append(bpy.context.scene.objects.active)
    lamps[0].data.type = "SUN"; lamps[1].data.type = "SUN"
    lamps[0].location += Vector((-3.0, 0.0, 6.0))
    lamps[0].rotation_euler = Vector((0.0, -0.8, 0.0))
    lamps[1].location += Vector((3.0, 0.0, 6.0))
    lamps[1].rotation_euler = Vector((0.0, 0.8, 0.0))
    
    
    select_obj(cam)
    for text in texts:
        char = characters[text['character']]
        cam.location = char.get_camera_position()
        cam.rotation_euler = char.get_camera_rotation(cam)
        bpy.context.scene.frame_current = text['from']+1
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        
    bpy.context.area.type = 'GRAPH_EDITOR'
    bpy.ops.graph.interpolation_type(type='CONSTANT')

    
    bpy.ops.mesh.primitive_plane_add()
    plane = bpy.context.scene.objects.active
    plane.location += Vector((0.0, 0.0, -0.2))
    plane.scale = Vector((50.0, 50.0, 0.0))

    

#select_nla_by_index(0)
main()


bpy.context.scene.frame_current = 1
bpy.context.area.type = 'TEXT_EDITOR'
