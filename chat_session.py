# chat_session.py

from openai import OpenAI
from prompt_toolkit import PromptSession
import json
import time

class ChatSession:
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
        self.history = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]
        self.prompt_session = PromptSession()
        self.running = True
        self.max_history = 10  # 最大历史记录数
    
    def get_prompt_message(self):
        """生成提示信息，显示当前上下文状态"""
        history_length = len(self.history)
        percentage = min(100, int(history_length / self.max_history * 100))
        
        prompt = f"ctx: {history_length}/{self.max_history} ({percentage}%)> "
        return prompt
    
    
    def handle_input(self, user_input: str):
        """处理用户输入，返回是否继续对话"""
        if not user_input.strip():
            return True
            
        if user_input.startswith(":"):
            return self.handle_command(user_input)
            
        # 添加用户消息到历史
        self.history.append({"role": "user", "content": user_input})
        
        # 检查并限制历史长度
        self.limit_history_length()
        
        # 获取AI回复
        ai_response = self.get_ai_response()
        if ai_response is None:
            return True
            
        # 添加AI回复到历史
        self.history.append({"role": "assistant", "content": ai_response})
        
        # 检查并限制历史长度
        self.limit_history_length()
        
        # 打印回复
        print(f"\n🤖: {ai_response}\n")
        return True
    
    def limit_history_length(self):
        """限制历史长度，保留最近的对话"""
        if len(self.history) > self.max_history:
            # 保留系统消息和最近的对话
            self.history = [self.history[0]] + self.history[-self.max_history+1:]
    
    def get_ai_response(self):
        """获取AI回复"""
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=self.history,
                stream=False
            )
            response_time = time.time() - start_time
            
            ai_response = response.choices[0].message.content
            print(f"⏱️ 响应时间: {response_time:.2f}秒")
            return ai_response
            
        except Exception as e:
            print(f"\n⚠️ API错误: {str(e)}")
            print("🔄 5秒后重试...")
            time.sleep(5)
            return None
    
    def handle_command(self, command_input: str) -> bool:
        """处理命令，返回是否继续对话"""
        command = command_input[1:].strip().lower()
        
        if command == "quit" or command == "exit":
            print("👋 再见！")
            self.running = False
            return False
            
        if command == "reset":
            # 重置对话历史，保留系统消息
            self.history = [self.history[0]]
            print("\n🔄 对话历史已重置\n")
            return True
            
        if command == "history":
            self.print_history()
            return True
            
        if command == "help":
            self.print_help()
            return True
            
        if command == "save":
            self.save_history()
            return True
            
        if command == "load":
            self.load_history()
            return True
            
        if command == "max":
            print(f"\n当前最大历史记录数: {self.max_history}")
            return True
            
        if command.startswith("max "):
            try:
                new_max = int(command.split()[1])
                if new_max < 2:
                    print("\n⚠️ 最大历史记录数不能小于2\n")
                else:
                    self.max_history = new_max
                    print(f"\n🔄 最大历史记录数已设置为: {self.max_history}\n")
                    self.limit_history_length()  # 立即应用新限制
            except (ValueError, IndexError):
                print("\n⚠️ 无效格式。使用:max <数字>\n")
            return True
            
        print(f"\n⚠️ 未知命令: :{command}。输入 :help 查看帮助\n")
        return True
    
    def print_history(self):
        """打印对话历史"""
        print("\n📜 对话历史:")
        for i, msg in enumerate(self.history):
            prefix = "🧠" if msg["role"] == "system" else "👤" if msg["role"] == "user" else "🤖"
            print(f"{i+1}. {prefix} {msg['content'][:80]}{'...' if len(msg['content']) > 80 else ''}")
        print()
    
    def print_help(self):
        """打印帮助信息"""
        print("\n🆘 可用命令:")
        print("  :help        - 显示帮助信息")
        print("  :history     - 显示对话历史")
        print("  :reset       - 重置对话")
        print("  :quit        - 退出程序")
        print("  :save        - 保存对话历史")
        print("  :load        - 加载对话历史")
        print("  :max         - 显示当前最大历史记录数")
        print("  :max <数字>   - 设置最大历史记录数")
        print()
    
    def save_history(self):
        """保存对话历史到文件"""
        try:
            with open("conversation.json", "w", encoding="utf-8") as f:
                json.dump({
                    "history": self.history,
                    "max_history": self.max_history
                }, f, ensure_ascii=False, indent=2)
            print("\n💾 对话历史已保存到 conversation.json\n")
        except Exception as e:
            print(f"\n⚠️ 保存失败: {str(e)}\n")
    
    def load_history(self):
        """从文件加载对话历史"""
        try:
            with open("conversation.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.history = data.get("history", [self.history[0]])
                self.max_history = data.get("max_history", 10)
            print("\n📂 对话历史已加载\n")
        except Exception as e:
            print(f"\n⚠️ 加载失败: {str(e)}\n")
    
    def run(self):
        """运行聊天会话"""
        print(f"🚀 使用模型: {self.config['model']}")
        print("💡 输入 :help 查看可用命令")
        
        while self.running:
            try:
                # 获取提示信息
                prompt_message = self.get_prompt_message()
                
                # 获取用户输入
                user_input = self.prompt_session.prompt(message=prompt_message)
                
                # 处理输入
                self.handle_input(user_input)
                
            except KeyboardInterrupt:
                print("\n提示: 输入 :quit 退出程序\n")
            except Exception as e:
                print(f"\n⚠️ 错误: {str(e)}")
                print("🔄 继续对话...")