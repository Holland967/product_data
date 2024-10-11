# from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import os

# load_dotenv()

# api_key = os.getenv("API_KEY")
# base_url = os.getenv("BASE_URL")

file_tree = {
    "Electric Deep Fryer": {
        "HD9002A": {
            "Basic": "warmer/HD9002A.txt"
        }
    }
}

st.set_page_config(page_title="Product Data", layout="wide")

st.subheader("Haoda Appliance Data", False)

if "img" not in st.session_state:
    st.session_state.img = None

if "specification" not in st.session_state:
    st.session_state.specification = []



if "msg" not in st.session_state:
    st.session_state.msg = []

if "prompt" not in st.session_state:
    st.session_state.prompt = ""

col_1, col_2, col_3 = st.columns(3)

with col_1:
    with st.container(height=700, border=True):
        product_list = ["Electric Deep Fryer"]
        product_item = st.selectbox("Choose a product", product_list, None, key="product_item")
        if product_item == "Electric Deep Fryer":
            model_list = ["HD9002A"]
            model_item = st.selectbox("Choose a model", model_list, None, key="model_item")
            if model_item == "HD9002A":
                st.session_state.img = "warmer/HD9002A.png"
                st.session_state.specification = ["Basic", "Package"]
            else:
                st.session_state.img = None
                st.session_state.specification = []
        
            if st.session_state.img:
                st.image(st.session_state.img, width=450)
        else:
            st.session_state.img = None
            st.session_state.specification = []

with col_2:
    with st.container(height=700, border=True):
        specification_item = st.selectbox("Choose a specification", st.session_state.specification, 0, key="specification_item")
        if specification_item == "Basic":
            file_path = file_tree[product_item][model_item][specification_item]
            with open(file_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        elif specification_item == "Package":
            st.markdown("### 还没写呢！别看了！")

with col_3:
    with st.container(height=700, border=True):
        st.markdown("##### Chat with AI")

        with st.container(height=515, border=True):
            for i in st.session_state.msg:
                with st.chat_message(i["role"]):
                    st.markdown(i["content"])
            
            if st.session_state.prompt:
                st.session_state.msg.append({"role": "user", "content": st.session_state.prompt})
                with st.chat_message("user"):
                    st.markdown(st.session_state.prompt)

                with open("warmer/HD9002A_AD.txt", "r", encoding="utf-8") as f:
                    warmer_data = f.read()
                system_prompt = f"""你是一名专业的产品顾问，请你根据下文中的产品信息回答用户提出的问题。

产品资料如下：

{warmer_data}

请你不要理睬除与产品本身无关的任何问题。
"""
                
                messages = [{"role": "system", "content": system_prompt}] + st.session_state.msg

                result = st.write("暂时关闭AI服务")

                st.session_state.msg.append({"role": "assistant", "content": result})
                st.session_state.prompt = ""
                st.rerun()
        
        clear_button = st.button("Clear Chat", "clear_chat")
        
        if query := st.chat_input("Say something...", key="query"):
            st.session_state.prompt = query
            st.rerun()
        
        if clear_button:
            st.session_state.msg = []
            st.session_state.prompt = ""
            st.rerun()
