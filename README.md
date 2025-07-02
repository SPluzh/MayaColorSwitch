# 🎨 MayaColorSwitch

**MayaColorSwitch** is a procedural, index-driven color switch system built entirely with native Autodesk Maya nodes.  
It allows you to switch between multiple colors using a single integer attribute — just like a shader switch — but without any third-party plugins or renderer dependencies.

A clean, scalable, and user-friendly alternative to `layeredTexture`, `blendColors` chains, or manually-built `condition` networks.
<img alt="maya_JYwrDqp5Q3" src="https://github.com/user-attachments/assets/4a8e0f76-cdd1-47bd-a98c-98cb5ec92869" />

---

## ✨ Features

- Creates a nested chain of `condition` nodes to switch between `colorConstant` inputs based on an integer index.
- Automatically builds a controller group (`shading`) with a `Color` attribute.
- Dynamically add or remove inputs at any time — no need to rebuild the whole network.
- Includes a simple and intuitive UI for managing the switch.
- Uses only **native Maya nodes** — fully renderer-agnostic and export-safe.
- Bright, randomly generated colors for easy visual debugging.

---

## 🧰 How It Works

1. You choose how many inputs (colors) you want.
2. The script:
   - Creates a `shading` group with a `.Color` attribute.
   - Builds a chain of `colorConstant` and `condition` nodes.
   - Connects everything into a final output node: `ColorSwitch_Output`.
   - The selected input is determined by the `Color` attribute.

3. Through the UI, you can:
   - Create a new switch network.
   - Add or remove inputs at any time.
   - See and lock the name of the controller group (`shading`).
<img width="1170" alt="maya_dFdOupAIpc" src="https://github.com/user-attachments/assets/0176b88f-b557-4766-9828-a8147dc5a071" />

---

## 🆚 Why Not Use `layeredTexture` or `blendColors`?

| Method            | Drawbacks                                                                 |
|-------------------|---------------------------------------------------------------------------|
| `layeredTexture`  | Requires keyframing alpha per layer; not easily index-driven              |
| `blendColors`     | Supports only 2 inputs; chains become messy fast                          |
| Manual `condition`| Time-consuming and error-prone to set up manually                         |

**MayaColorSwitch** solves this with:

- ✅ One index to control many inputs
- ✅ Clean and readable node graph
- ✅ Easy UI-based control
- ✅ Fully native and portable solution

---

## 🚀 Getting Started

1. Open Maya's Script Editor.
2. Paste the full script into a Python tab.
3. Execute the script.
4. A GUI window titled **Color Switch Builder** will appear.

You can now generate a new switch or modify an existing one.

---

## 📁 Nodes Created

- `shading` — the controller group with the `.Color` attribute.
- `ColorSwitch_Input0`, `ColorSwitch_Input1`, … — `colorConstant` input nodes.
- `ColorSwitch_Cond0`, `ColorSwitch_Cond1`, … — `condition` nodes for switching.
- `ColorSwitch_Output` — the final result node to be connected to a shader.

All nodes follow a clean naming convention.

---

## 🧩 Use Cases

- Shader color switching by ID/index
- Variant control for multiple materials or looks
- Animated color changes via keyframes
- Random or procedural input selection
- Visual debugging of color paths

---

## 🛠 Requirements

- Autodesk Maya 2018 or newer
- Python 2.7 (standard for Maya 2018–2022)

---

## 📝 License

MIT License — free for commercial and personal use. Attribution is appreciated but not required.

---

## 💬 Feedback & Contributions

Pull requests and issue reports are welcome!

If you find it useful, feel free to ⭐️ the repo or share with other Maya TDs!
