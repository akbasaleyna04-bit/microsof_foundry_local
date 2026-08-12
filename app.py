import gradio as gr
from rag.pipeline import RagAssistant

assistant = RagAssistant()

def predict(message, history):
    if not message.strip():
        return "Lütfen geçerli bir soru yazın."
    answer, results = assistant.answer(message)
    return answer

demo = gr.ChatInterface(
    fn=predict,
    title="Yerel RAG Asistanı - Microsoft Foundry Local",
    description="İnternet veya Azure gerektirmeden, tamamen cihazınızda çalışan çevrimdışı belge soru-cevap asistanı.",
    textbox=gr.Textbox(placeholder="Belgeleriniz hakkında bir şeyler sorun...", container=False, scale=7),
)

if __name__ == "__main__":
    demo.launch()