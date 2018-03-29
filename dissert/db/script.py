import bpy
import os
import os.path
import urllib
import wget

def import_anim(LINK, TARGET_NAME):
    FILENAME = LINK.split('/')[-1]
    if not os.path.isfile('tmp/' + FILENAME):
        wget.download(LINK, 'tmp/' + FILENAME)


    for object in bpy.data.objects:
        object.select = True
    bpy.ops.object.delete()
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)

    fpath = os.getcwd() + '/tmp/' + FILENAME
    bpy.ops.import_anim.bvh(filepath=fpath, use_fps_scale=True, rotate_mode='QUATERNION')


    #rename action
    bpy.context.area.type = 'DOPESHEET_EDITOR'
    bpy.context.space_data.mode = 'ACTION'
    #rename
    bpy.data.actions[0].name = TARGET_NAME
    frame_range = bpy.data.actions[0].frame_range
    action = bpy.data.actions[0]
    bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(-1, 0, 0, 0), axis=(0, 0, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(1, 0, 0, 0), axis=(0, 0, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


    anims_to_delete = ["Hips", "RightHip", "RightKnee", "RightAnkle", "RightToe",
                               "LeftHip", "LeftKnee", "LeftAnkle", "LeftToe",
                               "Chest4", "Chest3"]
    channels_to_delete = []

    for f in action.fcurves:
        print(f.data_path)
        for a in anims_to_delete:
            if a in f.data_path:
                channels_to_delete.append(f)
                print("appending: " + f.data_path)
                
    for f in channels_to_delete:
        action.fcurves.remove(f)



    bpy.context.area.type = 'VIEW_3D'
    bpy.context.scene.frame_set(1)
    bpy.ops.import_scene.fbx(filepath='armature.fbx', filter_glob="*.fbx;", ignore_leaf_bones=False)
    for obj in bpy.data.objects:
        obj.select = False
    bpy.data.objects[FILENAME.split(".")[0]].select = True
    bpy.ops.object.delete()
    obj = bpy.data.objects[0]
    obj.animation_data.action = action

    bpy.ops.object.posemode_toggle()
    bpy.ops.pose.transforms_clear()
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.context.scene.frame_end = int(frame_range[1])


    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.object.posemode_toggle()
    bpy.data.objects[0].select = True
    bpy.ops.export_scene.fbx(filepath="imported/"+TARGET_NAME+'_f-'+ str(frame_range[1]) +'.fbx', check_existing = False, \
    use_selection=True, object_types={'ARMATURE'}, \
    bake_anim = True, bake_anim_use_all_bones = True, \
    bake_anim_use_nla_strips = False, bake_anim_use_all_actions = False, \
    bake_anim_force_startend_keying = True, \
    add_leaf_bones=False)
    bpy.context.area.type = 'TEXT_EDITOR'



#anger
angers = [
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_91_560809_563542_2733_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_91_560809_563542_2733_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0708_ftf_bluebeard_t3-002_35_168275_171108_2833_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0708_ftf_bluebeard_t3-002_61_292100_296475_4375_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_ft_nr_anger_11350-12160.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_nv_al_t2_anger_10680-11274.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_nv_so_anger_11170-11931.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ft_ch_t1_anger_07830-08215.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ft_na_t1_anger_09487-09801.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-002_47_329008_333383_4375_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_140_866275_870883_4608_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_95_637292_642767_5475_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_119_681075_685242_4167_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_23_134275_139242_4967_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_53_307159_311300_4141_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_flower_t3-002_12_114233_120041_5808_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_flower_t3-002_18_162391_167775_5384_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_flower_t3-002_83_761666_768450_6784_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_goose_t3-001_27_283292_287775_4483_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_goose_t3-001_28_292150_295883_3733_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_goose_t3-001_31_317325_322125_4800_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_goose_t3-001_73_651092_655242_4150_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_90_702233_706583_4350_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_98_754833_759883_5050_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-003_16_180558_186375_5817_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-003_18_191842_195567_3725_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-003_30_279267_284850_5583_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-003_31_295125_299917_4792_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_ft_ch_t2_anger_12061-12659.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_ft_nr_t2_anger_22960-23791.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_nv_al_t2_anger_08558-09811.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_nv_so_t2_anger_10662-12043.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_nv_so_t2_anger_10662-12043.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_0409_ftf_hoodie_t2-002_77_550542_556450_5908_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_0409_ftf_wd_t3-003_96_779833_783883_4050_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_0409_ftf_wd_t3-004_0_53000_57142_4142_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_2308_ftf_goose_t2-005_10_95658_99275_3617_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_2308_nv_al_t2_anger_04654-05152.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_2308_nv_al_t2_anger_04654-05152.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/MaMa_ft_ch_anger_0_138_1114_976_anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/MaMa_ft_nr_anger_0_128_1272_1144_anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/MaMa_nv_al_anger_0_230_711_481_anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/MaMa_nv_so_anger_00900-01440.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_93_896700_901733_5033_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-002_10_53984_56834_2850_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-002_28_136992_141917_4925_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-002_47_220284_225984_5700_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-002_66_352842_359200_6358_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ft_na_t2_anger_08744-09541.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_13_138125_143150_5025_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_27_234933_238325_3392_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_27_234933_238325_3392_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_28_240400_243891_3491_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_29_243891_247941_4050_Anger.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_nv_al_t2_anger_11097-11422.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_nv_so_t1_anger_02060-02512.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/SiGl_ft_sp_anger_17429-17946.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/SiGl_nv_so_anger_10984-11701.bvh",
    
    ]
    
fears = [
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_ft_sp_fear_12575-13504.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ft_na_t1_fear_15453-16392.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-001_81_553517_558633_5116_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-001_94_650408_655442_5034_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-002_46_319166_322858_3692_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_36_201267_205750_4483_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_70_411675_414417_2742_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_78_458717_461242_2525_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_ft_ch_t2_fear_15955-16782.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-001_65_800784_804300_3516_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_1_35592_38317_2725_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_8_83584_86450_2866_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_14_247125_250517_3392_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_48_487883_491942_4059_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_66_642683_648500_5817_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_69_679125_683492_4367_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_71_708442_710850_2408_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_73_728225_732508_4283_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_84_831083_837525_6442_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_91_870250_874833_4583_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_41_325708_331608_5900_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_nv_al_t2_fear_14955-15777.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_nv_so_t1_fear_14760-15025.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/Session2_AnBh-011_11_53325_57258_3933_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/SiGl_2007_ftf_hh_t1.5-003_61_313825_317617_3792_Fear.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/SiGl_ft_sp_fear_16149-17162.bvh",
    
    ]

joys = [
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_nv_al_t1_joy_08424-09448.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_flower_t3-001_0_115683_121166_5483_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_flower_t3-002_62_562208_566791_4583_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0308_ftf_flower_t3-002_91_841516_846750_5234_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_0_53258_56966_3708_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_103_800558_806008_5450_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_106_850866_854816_3950_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_15_153858_158233_4375_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_3_73166_77633_4467_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_nv_al_t2_joy_10456-11405.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_2308_ftf_goose_t2-005_91_656408_660466_4058_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-001_2_182309_186450_4141_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_106_850866_854816_3950_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_15_153858_158233_4375_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_0708_ftf_swineherd_t2-001_3_73166_77633_4467_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/HeGa_2907_nv_al_t2_joy_10456-11405.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_2308_ftf_goose_t2-005_91_656408_660466_4058_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-001_2_182309_186450_4141_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_45_376734_383167_6433_Joy.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_48_400641_406525_5884_Joy.bvh"
    
    ]
    

sadnesses = [
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_64_407150_411592_4442_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_68_430984_434925_3941_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_ft_nr_sadness_18464-19721.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_ft_sp_sadness_15770-16402.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_nv_so_sadness_15509-16137.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ft_ch_t1_sadness_13329-14058.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-001_102_703675_710433_6758_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-001_64_433950_438433_4483_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-002_54_367741_370358_2617_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-002_61_428375_432991_4616_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_117_761375_766958_5583_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_142_876025_881167_5142_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_159_965808_971742_5934_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_161_974467_980175_5708_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-002_6_58083_62225_4142_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_102_592934_598284_5350_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_35_197559_201267_3708_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_wd_t1-003_79_464825_470517_5692_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/LeSt_0409_ftf_wd_t3-003_24_193808_197733_3925_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/MaMaftoe-003_11_75683_82467_6784_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_18_155134_158300_3166_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_22_197992_200417_2425_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_30_252567_255100_2533_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_32_280034_283534_3500_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_0608_ftf_whiteduck_t3-002_34_297100_302667_5567_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-001_4_186967_191133_4166_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_1208_ftf_bluebeard_t2-002_75_425142_429642_4500_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ft_na_t2_sadness_03905-04579.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_30_255158_258525_3367_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_ftf_hedgehog-003_54_458375_461991_3616_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/NoVo_s1_nv_al_t2_sadness_09302-09722.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/PaPi_2109_ftf_hedgehog_t2-001_31_201858_206550_4692_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/Session2_AnBh-012_85_377875_382042_4167_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/SiGl_2007_ftf_6s_t-002_57_393042_397317_4275_Sadness.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/SiGl_2007_ftf_hh_t1.5-003_55_295959_298525_2566_Sadness.bvh"
    
    ]
    
# 20 clips
neutrals = [
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_13_108975_113234_4259_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_16_125484_129659_4175_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_18_146942_151300_4358_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_31_211017_216484_5467_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_34_235409_239784_4375_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_44_300400_305734_5334_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_4_44017_48042_4025_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_51_337692_342259_4567_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_55_355825_359875_4050_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_60_389392_393675_4283_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_74_460509_466200_5691_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_93_572400_576559_4159_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0208_ftf_wd_t3-002_98_594709_598650_3941_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/AnBh_0708_ftf_bluebeard_t3-001_1_89341_93500_4159_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_flower_t1-002_26_190208_194150_3942_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_116_756675_761375_4700_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_131_824183_828517_4334_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_19_216142_220192_4050_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_35_304942_308908_3966_Neutral.bvh",
    "http://ebmdb.tuebingen.mpg.de/data/bvh/DiMi_0709_ftf_goose_t1-001_64_483767_487717_3950_Neutral.bvh",
    ]
    
i = 0
name = "neutral"
imported = []
for anim in neutrals:
    if anim not in imported:
        try:
            import_anim(anim, str(i) + name)
        except:
            print(anim + " not imported")
        i += 1
        imported.append(anim)






