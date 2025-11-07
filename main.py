# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from ui.optimized_compare import Ui_Form  # 路径保持不变
from PyQt6.QtWebEngineWidgets import QWebEngineView
import mammoth  # mammoth 是独立库，无需修改
import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog, QMessageBox,
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt6.QtWebEngineWidgets import QWebEngineView
import mammoth
from ui.optimized_compare import Ui_Form
from PyQt6.QtCore import Qt  # 注意：PyQt6 中是小写的 qt（区分大小写）

class CompareApp(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("文件对比工具")

        # 初始化历史文件存储目录
        self.history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history_files")
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

        # 绑定按钮事件（补充历史查询按钮）
        self.historyButton.clicked.connect(self.show_history_page)

        # 绑定按钮事件
        self.importOriginalFileButton.clicked.connect(self.load_original_file)
        self.importCompareFileButton.clicked.connect(self.load_compare_file)  # 绑定对比文件按钮

        # 存储文件路径（用于后续对比）
        self.original_file_path = None  # 原文件路径
        self.compare_file_path = None  # 对比文件路径

        # 历史页面实例（作为子窗口）
        self.history_page = None

        # 定义模拟Word的CSS样式
        self.word_css = """
        <style>
            body {
                font-family: 'SimSun', '宋体', serif;
                font-size: 12pt;
                line-height: 1.8;  /* 合同行间距，匹配模板可读性 */
                color: #000000;
                background-color: #ffffff;
                max-width: 21cm;  /* A4纸宽度 */
                margin: 0 auto;  /* 页面居中 */
                padding: 2.5cm 2cm;  /* 上下左右留白，贴近合同排版 */
            }
            /* 合同主标题：居中、加粗、大字号 */
            .contract-main-title {
                text-align: center;
                font-size: 16pt;
                font-weight: bold;
                margin: 0 0 40pt 0;  /* 标题下方留白 */
                text-indent: 0;  /* 取消首行缩进 */
            }
            /* 甲乙双方信息行：左对齐、上下留白 */
            .party-info {
                text-align: left;
                margin: 15pt 0;
                text-indent: 0;  /* 取消首行缩进 */
            }
            /* 合同前言段落：首行缩进2字符 */
            .contract-preface {
                text-align: justify;
                text-indent: 2em;
                margin: 20pt 0;
            }
            /* 大条款标题（一、二、三...）：加粗、左对齐、取消缩进 */
            .clause-level1 {
                font-weight: bold;
                font-size: 13pt;
                margin: 25pt 0 10pt 0;
                text-indent: 0;
            }
            /* 小条款标题（第一条、第二条...）：加粗、首行缩进2字符 */
            .clause-level2 {
                font-weight: bold;
                text-indent: 2em;
                margin: 15pt 0 5pt 0;
            }
            /* 普通正文段落：首行缩进2字符、两端对齐 */
            p {
                text-align: justify;
                text-indent: 2em;
                margin: 8pt 0;
            }
            /* 列表项（1、2、3...）：缩进适配、对齐正文 */
            ul, ol {
                margin: 5pt 0 5pt 4em;  /* 列表整体右移，匹配条款缩进 */
                padding-left: 0;
            }
            li {
                text-align: justify;
                margin: 6pt 0;
                text-indent: 0;  /* 列表项取消首行缩进 */
            }
            /* 签名区：上下留白、左对齐 */
            .signature-area {
                margin-top: 60pt;
                text-indent: 0;
            }
            .signature-item {
                margin: 20pt 0;
                text-indent: 0;
            }
            /* 签订日期行：左对齐、留白 */
            .sign-date {
                margin-top: 30pt;
                text-indent: 0;
            }
        </style>
        """

    def load_original_file(self, file_path=None):
        """导入原文件 (.docx)，并在左侧展示区显示，支持从历史记录加载"""
        # 如果没有传入路径，则打开文件选择对话框
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择原文件",
                "",
                "Word 文件 (*.docx)"
            )

        if not file_path:
            return  # 用户取消选择

        try:
            # 备份文件到历史文件夹（仅当不是从历史记录加载时）
            if not file_path.startswith(self.history_dir):
                # 生成带时间戳的文件名，避免重复
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.basename(file_path)
                name, ext = os.path.splitext(filename)
                history_filename = f"{name}_{timestamp}{ext}"
                history_path = os.path.join(self.history_dir, history_filename)

                # 复制文件到历史文件夹
                shutil.copy2(file_path, history_path)
                self.original_file_path = history_path
            else:
                self.original_file_path = file_path

            # 读取 docx 并转为 HTML（后续代码保持不变）
            with open(self.original_file_path, "rb") as docx_file:
                # 样式映射代码保持不变
                style_map = """
                p[style-name='标题 1'] => p.contract-main-title
                p[style-name='正文'] => p.contract-preface
                p[style-name='标题 2'] => p.clause-level1
                p[style-name='标题 3'] => p.clause-level2
                p[style-name='普通段落'] => p.party-info
                p[style-name='签名区'] => p.signature-area
                p[style-name='签名项'] => p.signature-item
                p[style-name='日期'] => p.sign-date
                """
                result = mammoth.convert_to_html(
                    docx_file,
                    style_map=style_map,
                    # convert_image=mammoth.images.img_element

                )
                html_content = result.value

            # 组合CSS和HTML内容，使样式生效
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                {self.word_css}
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            # 加载到左侧展示区（webEngineOriginView）
            self.webEngineOriginView.setHtml(full_html)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法显示 Word 文件内容：\n{e}")

    def load_compare_file(self):
        """导入对比文件 (.docx)，并在右侧展示区显示"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择对比文件",
            "",
            "Word 文件 (*.docx)"
        )

        if not file_path:
            return  # 用户取消选择

        try:
            # 读取对比文件并转换为HTML（复用原文件的样式映射）
            with open(file_path, "rb") as docx_file:
                style_map = """
                p[style-name='标题 1'] => p.contract-main-title
                p[style-name='正文'] => p.contract-preface
                p[style-name='标题 2'] => p.clause-level1
                p[style-name='标题 3'] => p.clause-level2
                p[style-name='普通段落'] => p.party-info
                p[style-name='签名区'] => p.signature-area
                p[style-name='签名项'] => p.signature-item
                p[style-name='日期'] => p.sign-date
                """
                result = mammoth.convert_to_html(
                    docx_file,
                    style_map=style_map,
                    # convert_image=mammoth.images.img_element

                )
                html_content = result.value

            # 组合CSS和HTML内容（保持与原文件格式一致）
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                {self.word_css}
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            # 加载到右侧展示区（假设控件名为 webEngineCompareView，需与UI文件一致）
            self.webEngineCompareView.setHtml(full_html)
            # 保存对比文件路径（供后续对比功能使用）
            self.compare_file_path = file_path

        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法显示对比文件内容：\n{e}")

    def handle_image(self,image):
        """处理图片转换，出错时返回空标签避免崩溃"""
        try:
            # 尝试转换图片为HTML标签
            return mammoth.images.img_element(image)
        except Exception:
            # 出错时返回空标签（或提示文字）
            return ("<p>[无法显示的图片]</p>",)  # 必须返回可迭代对象（如元组）

    # 在CompareApp类中添加显示历史页面的方法
    def show_history_page(self):
        """显示历史页面，大小与主界面一致并覆盖主界面"""
        # 创建历史页面（主窗口为父窗口）
        self.history_page = HistoryPage(
            parent=self,  # 关键：设置主窗口为父窗口
            history_dir=self.history_dir,
            callback=self.load_original_file
        )
        # 设置历史页面大小与主界面完全一致
        self.history_page.setGeometry(self.rect())  # 关键：同步大小和位置
        # 显示历史页面（会覆盖主界面）
        self.history_page.show()

    # 重写窗口大小改变事件：同步历史页面大小
    def resizeEvent(self, event):
        if self.history_page and self.history_page.isVisible():
            self.history_page.setGeometry(self.rect())  # 主窗口 resize 时，历史页面同步
        super().resizeEvent(event)


# 添加历史记录页面类
class HistoryPage(QWidget):
    def __init__(self, parent=None, history_dir=None, callback=None):
        super().__init__(parent)
        self.history_dir = history_dir
        self.callback = callback  # 用于回调显示选中的历史文件

        # 1. 先设置窗口属性（在初始化UI前设置）
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")  # 确保背景不透明

        # 2. 只调用一次 init_ui()（关键修复：避免重复初始化覆盖布局）
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("历史文件查询")
        layout = QVBoxLayout(self)

        # 步骤1：清空布局（确保无残留元素）
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 步骤2：设置拉伸因子（顺序：标题0、列表1、按钮0）
        layout.setStretch(0, 0)  # 标题不拉伸
        layout.setStretch(1, 1)  # 列表占满剩余空间
        layout.setStretch(2, 0)  # 按钮不拉伸

        # 1. 标题（索引0）- 修改这里
        title_label = QLabel("历史文件列表")
        # 关键修改：通过样式表减少上下边距，限制最小高度
        title_label.setStyleSheet("""
            font: 700 14pt 'Microsoft YaHei UI';
            margin-top: 5px;    /* 顶部边距 */
            margin-bottom: 0px; /* 底部边距 */
            padding-top: 2px;   /* 内边距顶部 */
            padding-bottom: 2px; /* 内边距底部 */
            min-height: 20px;   /* 最小高度（仅够显示文字） */
            max-height: 25px;   /* 最大高度限制 */
        """)
        # 设置固定高度策略
        title_label.setFixedHeight(25)  # 强制固定高度

        layout.addWidget(title_label)

        # 2. 历史文件列表（索引1）
        self.file_list_widget = QWidget()
        self.file_list_layout = QVBoxLayout(self.file_list_widget)
        # 列表容器添加少量内边距，避免内容贴边
        self.file_list_layout.setContentsMargins(5, 5, 5, 5)  # 左、上、右、下内边距
        self.file_list_layout.setStretch(0, 1)  # 确保列表内容拉伸
        layout.addWidget(self.file_list_widget)
        self.load_history_files()

        # 3. 返回按钮（索引2）
        back_btn = QPushButton("返回主界面")
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)

        # 强制应用布局
        self.setLayout(layout)
        layout.update()

    def load_history_files(self):
        """加载历史文件并显示（保持不变）"""
        # 清空现有列表
        while self.file_list_layout.count():
            item = self.file_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 获取并排序历史文件（按修改时间倒序）
        if os.path.exists(self.history_dir):
            files = [f for f in os.listdir(self.history_dir) if f.endswith(".docx")]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.history_dir, x)), reverse=True)

            for file in files:
                file_path = os.path.join(self.history_dir, file)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")

                # 创建文件信息和查看按钮
                file_widget = QWidget()
                file_layout = QHBoxLayout(file_widget)

                file_info = QLabel(f"{file}  ({mod_time})")
                view_btn = QPushButton("点击查看")
                view_btn.clicked.connect(lambda checked, path=file_path: self.view_file(path))

                file_layout.addWidget(file_info)
                file_layout.addWidget(view_btn)
                self.file_list_layout.addWidget(file_widget)

    def view_file(self, file_path):
        """回调主页面显示选中的历史文件（保持不变）"""
        if self.callback:
            self.callback(file_path)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompareApp()
    window.show()
    sys.exit(app.exec())