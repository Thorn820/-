# 导入 Tkinter 库，创建图形界面
import tkinter as tk
# 导入 Tkinter 中的对话框和文件选择器
from tkinter import colorchooser, simpledialog, filedialog, PhotoImage
# 导入 PIL 库，用于处理图像和在 Tkinter 中显示图像
from PIL import Image, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root  # 设置主窗口
        self.root.title("涂鸦画板")  # 设置窗口标题为 "涂鸦画板"

        # 画布尺寸设置
        self.canvas_width = 800  # 画布的初始宽度
        self.canvas_height = 600  # 画布的初始高度
        self.canvas = tk.Canvas(root, bg='white', width=self.canvas_width, height=self.canvas_height)  # 创建画布，背景为白色
        self.canvas.pack()  # 将画布添加到窗口中

        # 工具栏容器
        self.toolbar = tk.Frame(root)  # 创建一个工具栏
        self.toolbar.pack(side=tk.TOP, fill=tk.X)  # 将工具栏添加到窗口顶部并横向填充

        # 工具按钮：画笔
        self.pen_button = tk.Button(self.toolbar, text="画笔", command=self.toggle_pen)  # 创建“画笔”按钮
        self.pen_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐
        self.pen_active = True  # 默认画笔启用

        # 工具按钮：橡皮擦
        self.eraser_button = tk.Button(self.toolbar, text="橡皮擦", command=self.toggle_eraser)  # 创建“橡皮擦”按钮
        self.eraser_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐
        self.eraser_active = False  # 默认橡皮擦禁用

        # 工具按钮：选择颜色
        self.color_button = tk.Button(self.toolbar, text="选择颜色", command=self.choose_color)  # 创建“选择颜色”按钮
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐
        self.paint_color = "black"  # 默认画笔颜色为黑色

        # 工具按钮：设置背景色
        self.bg_color_button = tk.Button(self.toolbar, text="设置背景色", command=self.choose_bg_color)  # 创建“设置背景色”按钮
        self.bg_color_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐
        self.bg_color = "white"  # 默认背景色为白色
        self.eraser_color = self.bg_color  # 默认橡皮擦颜色与背景色相同

        # 工具按钮：画笔粗细
        self.brush_size_label = tk.Label(self.toolbar, text="画笔粗细:")  # 标签，显示画笔粗细
        self.brush_size_label.pack(side=tk.LEFT, padx=5, pady=5)  # 将标签添加到工具栏中
        self.brush_size_var = tk.IntVar(value=2)  # 创建画笔粗细的变量，默认值为2
        self.brush_size_slider = tk.Scale(self.toolbar, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.brush_size_var)  # 创建滑块，用于选择画笔粗细
        self.brush_size_slider.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中

        # 工具按钮：橡皮擦粗细
        self.eraser_size_label = tk.Label(self.toolbar, text="橡皮擦粗细:")  # 标签，显示橡皮擦粗细
        self.eraser_size_label.pack(side=tk.LEFT, padx=5, pady=5)  # 将标签添加到工具栏中
        self.eraser_size_var = tk.IntVar(value=10)  # 创建橡皮擦粗细的变量，默认值为10
        self.eraser_size_slider = tk.Scale(self.toolbar, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.eraser_size_var)  # 创建滑块，用于选择橡皮擦粗细
        self.eraser_size_slider.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中

        # 工具按钮：清空画板
        self.clear_button = tk.Button(self.toolbar, text="清空画板", command=self.clear_canvas)  # 创建“清空画板”按钮
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)  # 添加到工具栏中，右对齐

        # 工具按钮：设置画布大小
        self.resize_button = tk.Button(self.toolbar, text="设置画布大小", command=self.set_canvas_size)  # 创建“设置画布大小”按钮
        self.resize_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐

        # 工具按钮：添加图片
        self.add_image_button = tk.Button(self.toolbar, text="添加图片", command=self.add_image)  # 创建“添加图片”按钮
        self.add_image_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐

        # 缩放按钮：放大
        self.zoom_in_button = tk.Button(self.toolbar, text="放大", command=self.zoom_in)  # 创建“放大”按钮
        self.zoom_in_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐

        # 缩放按钮：缩小
        self.zoom_out_button = tk.Button(self.toolbar, text="缩小", command=self.zoom_out)  # 创建“缩小”按钮
        self.zoom_out_button.pack(side=tk.LEFT, padx=5, pady=5)  # 添加到工具栏中，左对齐

        # 绑定画布绘图事件
        self.canvas.bind("<B1-Motion>", self.draw)  # 鼠标左键拖动时绘制图形
        self.canvas.bind("<ButtonRelease-1>", self.reset)  # 鼠标左键释放时重置位置

        # 初始化坐标变量
        self.old_x, self.old_y = None, None  # 用于记录上一个鼠标位置
        self.image_on_canvas = None  # 用于存储添加到画布的图像
        self.magnifier_rect = None  # 用于显示放大镜区域

        # 初始化缩放比例变量
        self.scale_factor = 1.0  # 初始缩放比例为 1.0

    def toggle_pen(self):
        self.pen_active = True  # 启用画笔
        self.eraser_active = False  # 禁用橡皮擦
        self.update_widget_states()  # 更新工具按钮状态

    def toggle_eraser(self):
        self.pen_active = False  # 禁用画笔
        self.eraser_active = True  # 启用橡皮擦
        self.update_widget_states()  # 更新工具按钮状态

    def update_widget_states(self):
        # 根据画笔或橡皮擦状态启用或禁用滑块
        self.brush_size_slider.config(state=tk.NORMAL if self.pen_active else tk.DISABLED)
        self.eraser_size_slider.config(state=tk.NORMAL if self.eraser_active else tk.DISABLED)

    def choose_color(self):
        color = colorchooser.askcolor()[1]  # 弹出颜色选择器
        if color:
            self.paint_color = color  # 设置选中的颜色为画笔颜色

    def choose_bg_color(self):
        bg_color = colorchooser.askcolor()[1]  # 弹出背景颜色选择器
        if bg_color:
            self.bg_color = bg_color  # 设置选中的颜色为背景色
            self.eraser_color = self.bg_color  # 设置橡皮擦颜色为背景色
            self.canvas.config(bg=self.bg_color)  # 更新画布的背景色

    def clear_canvas(self):
        self.canvas.delete("all")  # 删除画布上的所有内容
        self.old_x, self.old_y = None, None  # 重置鼠标位置

    def set_canvas_size(self):
        # 弹出对话框设置画布大小
        width = simpledialog.askinteger("画布宽度", "请输入画布宽度:", minvalue=100, maxvalue=2000, initialvalue=self.canvas_width)
        height = simpledialog.askinteger("画布高度", "请输入画布高度:", minvalue=100, maxvalue=2000, initialvalue=self.canvas_height)
        if width and height:
            self.canvas.config(width=width, height=height)  # 更新画布的大小
            self.canvas_width = width  # 更新画布宽度
            self.canvas_height = height  # 更新画布高度

    def add_image(self):
        # 弹出文件选择框，用户选择一个图片文件
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

        # 如果用户选择了图片文件
        if file_path:
            # 打开选中的图片文件
            img = Image.open(file_path)

            # 调整图片大小以适应画布大小
            img.thumbnail((self.canvas_width, self.canvas_height))  # Resize to fit canvas

            # 将Pillow图像转换为Tkinter兼容的图像格式
            self.photo = ImageTk.PhotoImage(img)

            # 在画布中心创建图像对象
            self.image_on_canvas = self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2,
                                                            image=self.photo)

    def draw(self, event):
        # 如果没有记录上次的鼠标位置，更新初始位置并返回
        if self.old_x is None or self.old_y is None:
            self.old_x, self.old_y = event.x, event.y
            return

        # 如果当前选择的是画笔工具
        if self.pen_active:
            # 在画布上绘制线条，从上次鼠标位置到当前位置
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.brush_size_var.get(),  # 获取画笔的大小
                                    fill=self.paint_color,  # 获取画笔颜色
                                    capstyle=tk.ROUND,  # 设置线条末端为圆形
                                    smooth=tk.TRUE,  # 平滑线条
                                    splinesteps=36)  # 平滑度，越大线条越光滑

        # 如果当前选择的是橡皮擦工具
        elif self.eraser_active:
            # 获取橡皮擦的大小
            eraser_size = self.eraser_size_var.get()
            # 在当前位置绘制一个圆形橡皮擦
            self.canvas.create_oval(event.x - eraser_size // 2, event.y - eraser_size // 2,
                                    event.x + eraser_size // 2, event.y + eraser_size // 2,
                                    outline="", fill=self.eraser_color)  # 无边框，填充为橡皮擦颜色

        # 更新上次鼠标位置
        self.old_x, self.old_y = event.x, event.y

    def reset(self, event):
        # 重置鼠标位置
        self.old_x, self.old_y = None, None

    def zoom_in(self):
        # 放大画布内容
        self.scale_factor *= 1.1  # 增加缩放比例
        # 使用canvas的scale方法来实现放大，参数“all”表示对所有元素进行缩放
        self.canvas.scale("all", self.canvas_width / 2, self.canvas_height / 2, 1.1, 1.1)

    def zoom_out(self):
        # 缩小画布内容
        self.scale_factor /= 1.1  # 减小缩放比例
        # 使用canvas的scale方法来实现缩小，参数“all”表示对所有元素进行缩放
        self.canvas.scale("all", self.canvas_width / 2, self.canvas_height / 2, 0.9, 0.9)

# 如果当前脚本是作为主程序运行
if __name__ == "__main__":

    # 创建主窗口
    root = tk.Tk()

    # 创建绘图应用实例，并传入主窗口作为参数
    app = DrawingApp(root)

    # 进入Tkinter事件循环
    root.mainloop()
