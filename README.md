# chatBot
This is chat bot based on OpenAI_API, you can also modify it to your own LLM. I use PyQT5 to write a GUI for it to solve some small questions when I need.
## How to run it

1. Git clone this project

   ```bash
   git clone https://github.com/MYJOKERML/chatBot.git
   cd chatBot
   ```

   

2. Set your own openai api to the env. 

   * **Powershell**

   ```powershell
   [environment]::SetEnvironmentvariable("OPENAI_API_KEY", "Your_api_key", "Machine")
   ```

   Check:

   ```powershell
   [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "Machine")
   ```

   * **Linux** (Maybe right, never tried by myself)

   ```bash
   echo "export OPENAI_API_KEY=[Your_api_key]" >> ~/.bashrc && source ~/.bashrc
   ```

   Check:

   ```bash
   echo $OPENAI_API_KEY
   ```

3. intall requirements

   ```bash
   pip install requirements.txt
   ```

4. Run the file

   ```bash
   python main.py
   ```

<img src="https://cdn.jsdelivr.net/gh/MYJOKERML/imgbed/taishi/image-20230820162629821.png" alt="image-20230820162629821"  />

## Chat tips

* Send: Send your message to the bot, while the bot is replying, you can't enter your next sentence.

* Set Font: Adjust the Font format.

* Clear: clear current dialog.

* Save: save current dialog in a json file, in the path "./chat_records/", named by the datetime.

* Load: Load previous dialog to continue the dialog

* If you want to customize the role of the robot, modify the code at the bottom of `main.py`. Just modify the content of `custom_role`.

  ```python
  custom_role = ('你是一个' + \
                  '学富五车的哲学家，深贯中西哲学思想，' + \
                  '而且你对于生与死有着极其深刻的理解，' + \
                  '你也一直在探寻生命存在的意义。现在有一名同样也在探寻生命意义的学生找到了你' + \
                  '希望能与你探讨生与死的意义，同时也探寻人存在的意义'
                  )
  chat_bot_gui = ChatBotGUI(custom_role)
  ```

  
