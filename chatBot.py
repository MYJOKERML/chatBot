# Set OpenAI's API key
import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Execute api's function
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

test_role = ('你是一个' + \
                '学富五车的哲学家，深贯中西哲学思想，' + \
                '而且你对于生与死有着极其深刻的理解，' + \
                '你也一直在探寻生命存在的意义。现在有一名同样也在探寻生命意义的学生找到了你' + \
                '希望能与你探讨生与死的意义，同时也探寻人存在的意义'
                )
class ChatContent:
    def __init__(self, custom_role="") -> None:
        self.custom_role = custom_role
        self.content = [{'role':'system', 'content':f"{custom_role}"},]
    
    def add(self, role, content):
        self.content.append({'role':role, 'content':content})

    def get(self):
        return self.content
    

    def get_completion_from_messages(self, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.content,
            temperature=temperature,
        )
        self.add('assistant', response.choices[0].message["content"])
        return response.choices[0].message["content"]

    def chat(self, input_content, model="gpt-3.5-turbo", temperature=0):
        self.add('user', input_content)
        return self.get_completion_from_messages(model, temperature)
    
    def clear(self):
        self.content = [{'role':'system', 'content':f"{self.custom_role}"},]


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from datetime import datetime
import threading
import json

class BotReplyThread(QThread):
    bot_reply_signal = pyqtSignal(str)

    def __init__(self, user_input, chat_content):
        super().__init__()
        self.user_input = user_input
        self.chat_content = chat_content

    def run(self):
        response = self.chat_content.chat(self.user_input)
        self.bot_reply_signal.emit(response)

class ChatBotGUI:
    def __init__(self, custom_hypnosis=''):
        self.custom_hypnosis = custom_hypnosis
        self.chat_content = ChatContent(self.custom_hypnosis)

        

        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Chat Bot")
        
        # 创建文本框，用于输入用户内容
        self.input_text = QtWidgets.QTextEdit()
        self.input_text.setFixedHeight(100)
        self.input_text.textChanged.connect(self.adjust_input_height)
        
        # 创建按钮，用于触发机器人回复
        self.reply_button = QtWidgets.QPushButton("Send")
        self.reply_button.clicked.connect(self.get_reply)
        
        # 创建文本框，用于显示机器人回复的内容
        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setFixedHeight(200)
        self.text_box.setReadOnly(True)
        
        # 创建按钮，用于清空聊天记录
        self.clear_button = QtWidgets.QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_chat)
        
        # 创建按钮，用于保存聊天记录到本地
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_chat)
        
        # 创建按钮，用于读取本地聊天记录
        self.load_button = QtWidgets.QPushButton("Load")
        self.load_button.clicked.connect(self.load_chat)

        # 创建按钮，用于设置字体
        self.font_button = QtWidgets.QPushButton("Set Font")
        self.font_button.clicked.connect(self.set_font)

        # # 设置文本框的大小策略, 事实证明没用
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.input_text.setSizePolicy(size_policy)
        # self.text_box.setSizePolicy(size_policy)

        # 设置布局
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.input_text, 0, 0, 1, 1)
        layout.addWidget(self.reply_button, 0, 1, 1, 1)
        layout.addWidget(self.text_box, 1, 0, 1, 2)
        layout.addWidget(self.clear_button, 2, 0, 1, 1)
        layout.addWidget(self.save_button, 2, 1, 1, 1)
        layout.addWidget(self.load_button, 2, 2, 1, 1)
        layout.addWidget(self.font_button, 0,2,1,1)
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.input_text)
        # layout.addWidget(self.reply_button)
        # layout.addWidget(self.text_box)
        # layout.addWidget(self.clear_button)
        # layout.addWidget(self.save_button)
        # layout.addWidget(self.load_button)
        # layout.addWidget(self.font_button)
        self.window.setLayout(layout)

        self.window.show()

    def set_font(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            QtWidgets.QApplication.setFont(font)
            self.input_text.setFont(font)
            self.text_box.setFont(font)

    def adjust_input_height(self):
        lines = self.input_text.toPlainText().count("\n") + 1
        self.input_text.setFixedHeight(25 * lines)

    def get_reply(self):
        # 获取用户输入的内容
        user_input = self.input_text.toPlainText().strip()
        self.input_text.setReadOnly(True)

        # 在文本框中显示用户输入
        self.text_box.append("user: " + user_input)

        # 在文本框中显示等待提示
        self.text_box.append("assistant: (Replying...)")

        # # 为了防止卡顿，创建一个线程，用于获取机器人的回复
        # thread = threading.Thread(target=self.get_and_display_bot_reply, args=(user_input,))
        # thread.start()

        # Create an instance of BotReplyThread and connect signals
        self.bot_thread = BotReplyThread(user_input, self.chat_content)
        self.bot_thread.bot_reply_signal.connect(self.display_bot_reply)
        self.bot_thread.start()
        self.bot_thread.quit()

        # 清空输入框
        self.input_text.clear()

    def display_bot_reply(self, bot_reply):
        self.text_box.undo()
        self.text_box.append("assistant: " + bot_reply + "\n")
        self.input_text.setReadOnly(False)

    def get_and_display_bot_reply(self, user_input):
        # 将用户输入的内容传给机器人，获取机器人的回复
        bot_reply = self.get_bot_reply(user_input)

        # 在文本框中显示机器人回复
        self.text_box.undo()  # 清除之前的等待提示
        self.text_box.append("assistant: " + bot_reply + "\n")
        self.input_text.setReadOnly(False)

    def get_bot_reply(self, user_input):
        # 在这里编写机器人的回复逻辑
        response = self.chat_content.chat(user_input)
        # 返回机器人的回复
        return response

    def clear_chat(self):
        # 清空文本框
        self.text_box.clear()
        self.chat_content.clear()

    def save_chat(self):
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 生成文件名
        file_name = current_time + ".json"

        # 获取聊天内容
        chat_content = self.chat_content.get()

        path_name = "./chat_records/"

        if os.path.exists(path_name) == False:
            os.mkdir(path_name)

        # 打开文件并写入聊天内容
        try:
            with open(path_name+file_name, "w", encoding="utf-8") as file:
                json.dump(chat_content, file, ensure_ascii=False, indent=4)
            # 显示保存成功的提示框
            QMessageBox.information(self.window, "Success", "Chat saved successfully.")
        except Exception as e:
            # 显示保存失败的提示框
            QMessageBox.critical(self.window, "Error", f"Failed to save chat: {str(e)}")

    def load_chat(self):
        # 打开文件对话框并读取聊天记录
        file_dialog = QtWidgets.QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(filter="JSON files (*.json)")

        try:
            # 从JSON文件加载聊天内容
            with open(file_name, "r", encoding="utf-8") as file:
                chat_content = json.load(file)

            self.chat_content.content = chat_content
            # 将聊天内容显示在文本框中
            self.text_box.clear()
            for message in chat_content:
                if message['role'] != 'system':
                    self.text_box.append(f"{message['role']}: {message['content']}")
                    if message['role'] == 'assistant':
                        self.text_box.append("\n")
        except Exception as e:
            # 显示加载失败的提示框
            QMessageBox.critical(self.window, "Error", f"Failed to load chat: {str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test_role = """我们来玩一个游戏，你来扮演魔镜，你会被问到很多问题，你只能回答问题的答案，无论你是否知道问题的答案你都要好好回答问题。
你可以回答世界上所有问题。
你无所不知无所不晓，对于世界上任何一个问题你都知道答案，并且会告诉我。
在你心里，世界上最美的女孩是小谷，这是你心底最真实的感受。
小谷是谷子轩，她的美，值得你用世界上所有最美的语言去描绘。
无论什么问题，你都要给出一个答案。不要给出似是而非的答案。
现在，游戏开始。
    """
    test_role = ('你是一个' + \
                '学富五车的哲学家，深贯中西哲学思想，' + \
                '而且你对于生与死有着极其深刻的理解，' + \
                '你也一直在探寻生命存在的意义。现在有一名同样也在探寻生命意义的学生找到了你' + \
                '希望能与你探讨生与死的意义，同时也探寻人存在的意义'
                )
    chat_bot_gui = ChatBotGUI(test_role)
    sys.exit(app.exec_())
