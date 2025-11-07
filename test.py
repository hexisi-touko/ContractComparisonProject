# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog, QMessageBox,
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
import mammoth
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from ui.optimized_compare import Ui_Form
from PyQt6.QtCore import Qt  # 注意：PyQt6 中是小写的 qt（区分大小写）


class CompareApp(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("文件对比工具")

        # 绑定按钮事件
        self.importOriginalFileButton.clicked.connect(self.load_original_file)
        self.importCompareFileButton.clicked.connect(self.load_compare_file)
        self.compareButton.clicked.connect(self.compare_files)

        # 存储路径与HTML内容
        self.original_file_path = None
        self.compare_file_path = None
        self.original_html = None
        self.compare_html = None
        self.original_nodes = []  # 存储原文件的<p>和<li>节点（含完整文本和标签）
        self.compare_nodes = []   # 存储对比文件的<p>和<li>节点（含完整文本和标签）

        # 模拟 Word 样式
        self.word_css = """
        <style>
            body {
                font-family: 'SimSun', '宋体', serif;
                font-size: 12pt;
                line-height: 1.8;
                color: #000000;
                background-color: #ffffff;
                max-width: 21cm;
                margin: 0 auto;
                padding: 2.5cm 2cm;
            }
            .contract-main-title {
                text-align: center;
                font-size: 16pt;
                font-weight: bold;
                margin: 0 0 40pt 0;
                text-indent: 0;
            }
            .party-info {
                text-align: left;
                margin: 15pt 0;
                text-indent: 0;
            }
            .contract-preface {
                text-align: justify;
                text-indent: 2em;
                margin: 20pt 0;
            }
            .clause-level1 {
                font-weight: bold;
                font-size: 13pt;
                margin: 25pt 0 10pt 0;
                text-indent: 0;
            }
            .clause-level2 {
                font-weight: bold;
                text-indent: 2em;
                margin: 15pt 0 5pt 0;
            }
            p {
                text-align: justify;
                text-indent: 2em;
                margin: 8pt 0;
            }
            ul, ol {
                margin: 5pt 0 5pt 4em;
                padding-left: 0;
            }
            li {
                text-align: justify;
                margin: 6pt 0;
                text-indent: 0;
            }
            .signature-area {
                margin-top: 60pt;
                text-indent: 0;
            }
            .signature-item {
                margin: 20pt 0;
                text-indent: 0;
            }
            .sign-date {
                margin-top: 30pt;
                text-indent: 0;
            }
            .diff-highlight {
                background-color: #ffcccc;
                color: #ff0000;
                font-weight: bold;
                padding: 0 2px;
            }
            .diff-delete {
                color: #ff0000;
                text-decoration: line-through;
                font-weight: bold;
                padding: 0 2px;
            }
        </style>
        """

    def load_file(self, is_original):
        """加载文件并提取所有段落/列表项节点"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择" + ("原文件" if is_original else "对比文件"), "", "Word 文件 (*.docx)"
        )
        if not file_path:
            return

        try:
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
                   ## convert_image=mammoth.images.img_element
                )
                html_content = result.value
                soup = BeautifulSoup(html_content, 'html.parser')

            full_html = f"""
            <!DOCTYPE html><html><head>
            <meta charset="UTF-8">{self.word_css}</head><body>
            {html_content}</body></html>
            """

            # 提取所有<p>和<li>节点（含完整标签和文本）
            nodes = soup.find_all(['p', 'li'])
            if is_original:
                self.original_file_path = file_path
                self.original_html = html_content
                self.original_nodes = nodes
                self.webEngineOriginView.setHtml(full_html)
            else:
                self.compare_file_path = file_path
                self.compare_html = html_content
                self.compare_nodes = nodes
                self.webEngineCompareView.setHtml(full_html)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法显示{('原' if is_original else '对比')}文件内容：\n{e}")

    def load_original_file(self):
        self.load_file(is_original=True)

    def load_compare_file(self):
        self.load_file(is_original=False)

    def highlight_differences(self, original_text, compare_text):
        """精准标红差异：仅当文本不同时才标记，支持新增、删除、替换"""
        if original_text == compare_text:
            return compare_text  # 文本完全一致时，不做任何标记

        matcher = SequenceMatcher(None, original_text, compare_text)
        result = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                result.append(compare_text[j1:j2])
            elif tag == 'insert':
                result.append(f'<span class="diff-highlight">{compare_text[j1:j2]}</span>')
            elif tag == 'delete':
                result.append(f'<span class="diff-delete">{original_text[i1:i2]}</span>')
            elif tag == 'replace':
                result.append(
                    f'<span class="diff-delete">{original_text[i1:i2]}</span><span class="diff-highlight">{compare_text[j1:j2]}</span>'
                )
        return ''.join(result)

    def compare_files(self):
        """严格对比同位置、同类型节点，仅标记真实差异"""
        if not self.original_nodes or not self.compare_nodes:
            QMessageBox.warning(self, "警告", "请先导入原文件和对比文件！")
            return

        try:
            soup = BeautifulSoup(self.compare_html, 'html.parser')
            compare_nodes = soup.find_all(['p', 'li'])
            min_len = min(len(self.original_nodes), len(compare_nodes))
            diff_count = 0

            for i in range(min_len):
                orig_node = self.original_nodes[i]
                comp_node = compare_nodes[i]
                # 仅对比同类型节点（p对p，li对li）
                if orig_node.name != comp_node.name:
                    continue

                orig_text = orig_node.get_text().strip()
                comp_text = comp_node.get_text().strip()
                highlighted_html = self.highlight_differences(orig_text, comp_text)

                if highlighted_html != comp_text:
                    diff_count += 1
                    # 替换节点内容，保留原始标签结构
                    comp_node.clear()
                    comp_node.append(BeautifulSoup(highlighted_html, 'html.parser'))

            # 处理对比文件中多余的节点（新增内容）
            for extra_node in compare_nodes[min_len:]:
                extra_text = extra_node.get_text().strip()
                if extra_text:
                    diff_count += 1
                    extra_node.clear()
                    extra_node.append(BeautifulSoup(
                        f'<span class="diff-highlight">{extra_text}</span>',
                        'html.parser'
                    ))

            highlighted_full_html = f"""
            <!DOCTYPE html><html><head>
            <meta charset="UTF-8">{self.word_css}</head><body>
            {str(soup)}</body></html>
            """

            self.webEngineCompareView.setHtml(highlighted_full_html)
            QMessageBox.information(self, "完成", f"文件对比完成！共发现 {diff_count} 处差异。")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"文件对比失败：\n{e}")


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