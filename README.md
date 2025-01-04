Have Created a chatbot which would perfrom the following task.
The LLM should be able to:

1. Answer general questions (common for most LLMs).
2. Respond to questions specifically related to your own CV/Resume.

##How to run the code
Step1: Pretrain the model by running cells in llm_train.ipynb file
Step2:Run the ngrok server in train.ipynb file and put the ngrk server url in send_to_llm function present in app.py file
Step3: Run app.py file by writing app.py command
