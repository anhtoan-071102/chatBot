from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification
import torch

def initialize_models():
    global collection_name, qdrant_client, embedding_model, reranking_model, reranking_tokenizer, generate_model, generate_tokenizer
    qdrant_client = QdrantClient(
        "https://9dbbe406-0914-4443-9775-e5bd6f13e026.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="AJzXRQb9y__l32ROSB_ZEG1bQJ9gM54r6mJ_xq7Y5maw5URvP74xKQ",

    )

    collection_name = "tailieuchung_jina_vectors"
    embedding_model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True).to('cuda')
    reranking_model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-v2-m3").to('cuda')
    reranking_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
    generate_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")
    generate_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")

def retrieve_data(query, top_k=15, threshold=0.4):
    query_vector = embedding_model.encode(query, task="retrieval.query", prompt_name="retrieval.query",)
    response = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    return [result.payload['text'] for result in response if result.score >= threshold]


def rerank_documents(query, docs):
    if not docs:
        return None
    pairs = [(query, doc) for doc in docs]
    inputs = reranking_tokenizer(pairs, padding=True, truncation=True, return_tensors='pt').to('cuda')

    with torch.no_grad():
        scores = reranking_model(**inputs).logits.view(-1)
        indices = torch.argsort(scores, descending=True)
    return [docs[idx] for idx in indices.tolist()]


def generate_answer(query, reranked_docs, top_k=2):
    if not rerank_documents:
        return "xin lỗi, hiện tôi không thể trợ giúp bạn ở câu hỏi này"
    context = "\n".join(reranked_docs[:top_k])
    prompt = f"Dựa vào văn bản sau đây:\n{context}\nHãy trả lời câu hỏi: {query}"
    messages = [
        {"role": "system", "content": "Bạn là Qwen. Bạn là một trợ lý tuyệt vời giúp tư vấn về các vấn đề trong trường học cho sinh viên bằng tiếng Việt"},
        {"role": "user", "content": prompt}
    ]

    text = generate_tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = generate_tokenizer([text], return_tensors="pt").to(generate_model.device)
    try:
        generated_ids = generate_model.generate(**inputs, max_new_tokens=200, top_k=9, top_p=0.9, temperature=0.4)
    except Exception as e:
        return "đã xảy ra lỗi khi sinh câu trả lời."
    output = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
    ]

    answer = generate_tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    return answer

def answer(query):
    retrieved_docs = retrieve_data(query, top_k=15)
    reranked_docs = rerank_documents(query, retrieved_docs)
    answer = generate_answer(query, reranked_docs, top_k=2)
    return answer
    

initialize_models()
