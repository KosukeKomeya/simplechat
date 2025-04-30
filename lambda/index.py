import json
import urllib.request

FASTAPI_URL = "https://a8a1-34-125-51-156.ngrok-free.app/docs"  # ← Colab で控えた URL

def call_fastapi(message, conversation_history):
    payload = json.dumps({
        "message": message,
        "conversationHistory": conversation_history
    }).encode('utf-8')
    req = urllib.request.Request(FASTAPI_URL, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())
    except Exception as e:
        print("Error calling FastAPI:", e)
        return None

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        msg = body['message']
        hist = body.get('conversationHistory', [])

        resp = call_fastapi(msg, hist)
        if not resp:
            raise Exception("FastAPI から応答を取得できませんでした")

        assistant = resp.get("response")
        hist.append({"role": "assistant", "content": assistant})

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "response": assistant,
                "conversationHistory": hist
            })
        }
    except Exception as err:
        print("Lambda error:", err)
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(err)})
        }
