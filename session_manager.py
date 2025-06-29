import datetime

class SessionManagerPlugin:
    name = "SessionManager"
    typ = "session"

    def on_init(self, session_id):
        self.history = []
        print(f"SessionManager initialized for {session_id}")

    def on_send(self, session_id, timestamp, input, target, vector, result):
        self.history.append({
            "session": session_id,
            "time": timestamp,
            "direction": "send",
            "input": input,
            "target": target,
            "vector": vector,
            "result": result
        })

    def on_listen(self, session_id, timestamp, input, emotions):
        self.history.append({
            "session": session_id,
            "time": timestamp,
            "direction": "listen",
            "input": input,
            "emotions": emotions
        })

    def on_evaluate(self, session_id, metrics):
        self.history.append({
            "session": session_id,
            "time": datetime.datetime.utcnow().isoformat(),
            "direction": "evaluate",
            "metrics": metrics
        })

    def on_reset(self, old_session_id, new_session_id):
        print(f"Reset session {old_session_id} -> {new_session_id}")
        self.history.clear()

def setup():
    return SessionManagerPlugin()