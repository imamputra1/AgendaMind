class ExecutiveSecretary:
    """Reacts to schedule and message events; handles prioritization logic."""

    def handle_schedule_alert(self, payload: dict) -> None:
        print(f"[ExecutiveSecretary] Processing schedule: {payload}")

    def handle_message_received(self, payload: dict) -> None:
        print(f"[ExecutiveSecretary] Processing message: {payload}")
