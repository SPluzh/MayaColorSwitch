import maya.cmds as cmds
import random

prefix = "ColorSwitch"

def random_bright_color():
    while True:
        r = round(random.uniform(0.1, 1.0), 2)
        g = round(random.uniform(0.1, 1.0), 2)
        b = round(random.uniform(0.1, 1.0), 2)
        
        # Ensure channels differ enough (avoid grayish)
        if abs(r - g) > 0.1 or abs(g - b) > 0.1 or abs(r - b) > 0.1:
            # Ensure overall brightness (sum of RGB) is high enough
            if (r + g + b) / 3 > 0.3:
                return (r, g, b)

def get_input_nodes():
    return sorted(cmds.ls("{}_Input*".format(prefix), type="colorConstant"), key=lambda n: int(n.split("Input")[-1]))

def get_condition_nodes():
    return sorted(cmds.ls("{}_Cond*".format(prefix), type="condition"), key=lambda n: int(n.split("Cond")[-1]))

def get_output_node():
    out = "{}_Output".format(prefix)
    return out if cmds.objExists(out) else None

def update_color_attr_range(group, count):
    if cmds.attributeQuery("Color", node=group, exists=True):
        cmds.addAttr("{}.Color".format(group), e=True, min=0, max=max(0, count - 1))

def create_initial_switch(group_input, count):
    group = group_input.strip()
    if not group:
        group = "shading"

    if not cmds.objExists(group):
        group = cmds.group(empty=True, name=group)
        # Update GUI field if group was created
        if cmds.textField("shadingGroupField", exists=True):
            cmds.textField("shadingGroupField", e=True, text=group)

    for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v']:
        try:
            cmds.setAttr("{}.{}".format(group, attr), keyable=False, channelBox=False)
        except:
            pass

    if not cmds.attributeQuery("Color", node=group, exists=True):
        cmds.addAttr(group, ln="Color", at="long", min=0, max=count - 1, dv=0, k=True)
    else:
        update_color_attr_range(group, count)

    for i in range(count):
        add_single_input(group)

def add_single_input(group):
    inputs = get_input_nodes()
    conds = get_condition_nodes()
    idx = len(inputs)

    # Create a new colorConstant node
    color = random_bright_color()
    const_name = "{}_Input{}".format(prefix, idx)
    const = cmds.shadingNode("colorConstant", asUtility=True, name=const_name)
    cmds.setAttr("{}.inColor".format(const), color[0], color[1], color[2], type="double3")

    out_node = get_output_node()
    if not out_node:
        out_node = cmds.shadingNode("colorConstant", asUtility=True, name="{}_Output".format(prefix))

    if idx == 0:
        # Only one input, connect directly to output
        try:
            cmds.disconnectAttr("{}.inColor".format(out_node))
        except:
            pass
        cmds.connectAttr("{}.outColor".format(const), "{}.inColor".format(out_node), f=True)

    elif idx == 1:
        # First condition: compare to 0, Input0 is True, Input1 is False
        cond = cmds.shadingNode("condition", asUtility=True, name="{}_Cond0".format(prefix))
        cmds.setAttr("{}.secondTerm".format(cond), 0)
        cmds.setAttr("{}.operation".format(cond), 0)
        cmds.connectAttr("{}.Color".format(group), "{}.firstTerm".format(cond), f=True)
        cmds.connectAttr("{}.outColor".format(inputs[0]), "{}.colorIfTrue".format(cond), f=True)
        cmds.connectAttr("{}.outColor".format(const), "{}.colorIfFalse".format(cond), f=True)

        try:
            cmds.disconnectAttr("{}.inColor".format(out_node))
        except:
            pass
        cmds.connectAttr("{}.outColor".format(cond), "{}.inColor".format(out_node), f=True)

    else:
        # Add new condition at the top
        cond_name = "{}_Cond{}".format(prefix, idx - 1)
        cond = cmds.shadingNode("condition", asUtility=True, name=cond_name)
        cmds.setAttr("{}.secondTerm".format(cond), idx - 1)
        cmds.setAttr("{}.operation".format(cond), 0)
        cmds.connectAttr("{}.Color".format(group), "{}.firstTerm".format(cond), f=True)

        # True case → InputN-1
        cmds.connectAttr("{}.outColor".format(inputs[-1]), "{}.colorIfTrue".format(cond), f=True)

        # False case → new InputN
        cmds.connectAttr("{}.outColor".format(const), "{}.colorIfFalse".format(cond), f=True)

        # Rewire previous condition
        prev_cond = conds[-1]
        try:
            cmds.disconnectAttr("{}.colorIfFalse".format(prev_cond))
        except:
            pass
        cmds.connectAttr("{}.outColor".format(cond), "{}.colorIfFalse".format(prev_cond), f=True)

        # Top condition connects to output
        try:
            cmds.disconnectAttr("{}.inColor".format(out_node))
        except:
            pass
        cmds.connectAttr("{}.outColor".format(conds[0]), "{}.inColor".format(out_node), f=True)

    update_color_attr_range(group, idx + 1)



def remove_last_input(group):
    inputs = get_input_nodes()
    conds = get_condition_nodes()
    count = len(inputs)

    if count <= 1:
        cmds.warning("Cannot remove the last input.")
        return

    last_input = inputs[-1]
    if len(conds) >= 1:
        last_cond = conds[-1]
        cmds.delete(last_cond)
    cmds.delete(last_input)

    if count == 2:
        out_node = get_output_node()
        if out_node:
            try:
                cmds.disconnectAttr("{}.inColor".format(out_node))
            except:
                pass
            cmds.connectAttr("{}.outColor".format(inputs[0]), "{}.inColor".format(out_node), f=True)
    elif count > 2 and len(conds) >= 2:
        prev_cond = conds[-2]
        try:
            cmds.disconnectAttr("{}.colorIfFalse".format(prev_cond))
        except:
            pass
        cmds.connectAttr("{}.outColor".format(inputs[-2]), "{}.colorIfFalse".format(prev_cond), f=True)

    update_color_attr_range(group, count - 1)

def get_group_from_field():
    if cmds.textField("shadingGroupField", exists=True):
        return cmds.textField("shadingGroupField", q=True, text=True)
    return ""

def open_gui():
    win = "colorSwitchWin"
    if cmds.window(win, exists=True):
        cmds.deleteUI(win)

    existing_group = "shading" if cmds.objExists("shading") else ""

    cmds.window(win, title="MayaColorSwitch", widthHeight=(320, 300), sizeable=False)

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    # Shading Group Field
    cmds.frameLayout(label="Group used for switching colors", collapsable=False, marginHeight=8, marginWidth=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    cmds.textField("shadingGroupField", text=existing_group, editable=False)
    cmds.setParent("..")
    cmds.setParent("..")

    # Create New Switch Section
    cmds.frameLayout(label="Create New Switch", collapsable=False, marginHeight=8, marginWidth=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    cmds.text(label="Number of Inputs", align="left")
    cmds.intSliderGrp("colorSwitchSlider", field=True, min=2, max=20, value=5, step=1)
    cmds.button(label="Create Switch", height=30, backgroundColor=(0.1, 0.5, 0.45),
        command=lambda *a: create_initial_switch(
        get_group_from_field(),
        cmds.intSliderGrp("colorSwitchSlider", q=True, value=True)
    ))
    cmds.setParent("..")
    cmds.setParent("..")

    # Modify Section (Add / Remove)
    cmds.frameLayout(label="Modify Existing", collapsable=False, marginHeight=8, marginWidth=10)
    cmds.rowLayout(numberOfColumns=2,
               columnAttach=(1, 'both', 0),  # обе кнопки прилипают к краям
               adjustableColumn=1)
    
    cmds.button(label="Add Input", height=30, backgroundColor=(0.1, 0.5, 0.45),
                command=lambda *a: add_single_input(get_group_from_field()))
    cmds.button(label="Remove Last Input", height=30, backgroundColor=(0.5, 0.1, 0.1),
                command=lambda *a: remove_last_input(get_group_from_field()))

    cmds.setParent("..")
    cmds.setParent("..")

    cmds.showWindow(win)

# Launch GUI
open_gui()
