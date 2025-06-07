"""
画像から3Dモデル生成用ユーティリティライブラリ
Blender MCPでの使用を想定
"""


import bpy


class ImageTo3DModeler:
    """画像解析からの3Dモデル生成用基本クラス"""

    def __init__(self):
        self.scene = bpy.context.scene
        self.collection = bpy.context.collection

    def create_primitive(
        self, prim_type, name, location=(0, 0, 0), scale=(1, 1, 1), rotation=(0, 0, 0)
    ):
        """基本プリミティブを作成"""
        if prim_type == 'cylinder':
            bpy.ops.mesh.primitive_cylinder_add(location=location)
        elif prim_type == 'cube':
            bpy.ops.mesh.primitive_cube_add(location=location)
        elif prim_type == 'sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(location=location)
        elif prim_type == 'cone':
            bpy.ops.mesh.primitive_cone_add(location=location)

        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        obj.rotation_euler = rotation
        return obj

    def create_material(self, name, base_color=(1,1,1,1)):
        """マテリアルを作成"""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        mat.node_tree.nodes.clear()

        # Principled BSDFノードを追加
        bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.inputs[0].default_value = base_color  # Base Color

        # Material Outputノードを追加
        output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])

        return mat

    def apply_material(self, obj, material):
        """オブジェクトにマテリアルを適用"""
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

    def boolean_operation(self, obj1, obj2, operation='UNION'):
        """ブーリアン演算を実行"""
        modifier = obj1.modifiers.new(name="Boolean", type='BOOLEAN')
        modifier.operation = operation
        modifier.object = obj2

        # モディファイアを適用
        bpy.context.view_layer.objects.active = obj1
        bpy.ops.object.modifier_apply(modifier="Boolean")

        # 使用済みオブジェクトを削除
        bpy.data.objects.remove(obj2, do_unlink=True)

        return obj1


class ParametricModeler:
    """データ駆動型モデル生成クラス"""

    def __init__(self):
        self.modeler = ImageTo3DModeler()

    def create_from_json(self, model_data):
        """JSON定義からモデルを生成"""
        created_objects = []

        for part in model_data.get('parts', []):
            obj = self.modeler.create_primitive(
                part['type'],
                part['name'],
                part.get('location', (0,0,0)),
                part.get('scale', (1,1,1)),
                part.get('rotation', (0,0,0))
            )

            # マテリアル適用
            if 'material' in part:
                mat = self.modeler.create_material(
                    part['material']['name'],
                    part['material'].get('color', (1,1,1,1))
                )
                self.modeler.apply_material(obj, mat)

            created_objects.append(obj)

        return created_objects


class ShapeAnalyzer:
    """形状解析ユーティリティ"""

    @staticmethod
    def analyze_proportions(width, height):
        """画像の比率分析"""
        aspect_ratio = width / height
        return {
            'aspect_ratio': aspect_ratio,
            'is_portrait': height > width,
            'is_landscape': width > height,
            'is_square': abs(aspect_ratio - 1.0) < 0.1
        }

    @staticmethod
    def color_to_blender(hex_color):
        """16進数カラーをBlender用RGBAに変換"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        return rgb + (1.0,)  # アルファ値追加


def load_utils():
    """ユーティリティクラスを初期化して返す"""
    return {
        'modeler': ImageTo3DModeler(),
        'parametric': ParametricModeler(),
        'analyzer': ShapeAnalyzer()
    }


if __name__ == "__main__":
    print("画像から3Dモデル生成用ライブラリ")
    print("利用可能なクラス:")
    print("- ImageTo3DModeler: 基本的なモデリング操作")
    print("- ParametricModeler: データ駆動型モデル生成")
    print("- ShapeAnalyzer: 形状・色彩解析ユーティリティ")
