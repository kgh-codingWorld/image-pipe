import gradio as gr
from frontend.utils.process_util import process_image

with gr.Blocks() as demo:
    gr.Markdown("### 이미지 처리 서버 (FastAPI + Celery + Gradio)")

    with gr.Row():
        image_input = gr.Image(type="filepath", label="이미지 업로드")
        method_input = gr.Radio(["싱글 스레드", "멀티 스레드", "멀티 프로세스"], label="처리 방식")

    submit_btn = gr.Button("처리 시작")

    status_output = gr.Text(label="처리 상태")
    result_output = gr.Image(label="처리된 이미지")

    submit_btn.click(
        fn=process_image,
        inputs=[image_input, method_input],
        outputs=[status_output, result_output],
        queue=True,  # 요청 큐잉. 처리 중인 요청 끝나기 전까진 다음 요청 안 받음 -> 이거 쓰려면 Blocks()으로 바꿔야 함
        show_progress=True
    )

demo.launch()
