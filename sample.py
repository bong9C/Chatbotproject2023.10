import asyncio
import websockets

# 클라이언트 리스트
clients = set()

# 웹 소켓 서버 핸들러
async def handle_client(websocket, path):
    try:
        # 클라이언트 연결
        clients.add(websocket)
        async for message in websocket:
            # 모든 클라이언트에게 메시지 브로드캐스트
            for client in clients:
                await client.send(message)
    finally:
        # 클라이언트 연결 해제
        clients.remove(websocket)

# 웹 소켓 서버 실행
start_server = websockets.serve(handle_client, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()