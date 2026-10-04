import os
import requests
from dotenv import load_dotenv
from analyzer import PMAnalysis

load_dotenv()

def send_slack_notification(analysis: PMAnalysis, url: str) -> bool:
    """
    Sends a formatted PM update card to a Slack incoming webhook.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("[NOTIFIER] SLACK_WEBHOOK_URL not configured in .env. Skipping Slack alert.")
        return False

    takeaways_text = "\n".join([f"• {t}" for t in analysis.key_takeaways])

    slack_payload = {
        "text": f"🚨 *Competitor Update Detected:* {url}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 Competitor Update: {analysis.category}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Impact Level:*\n{analysis.impact_level}"},
                    {"type": "mrkdwn", "text": f"*Target URL:*\n<{url}|View Source>"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n{analysis.summary}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Key Takeaways:*\n{takeaways_text}"
                }
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=slack_payload, timeout=10)
        if response.status_code == 200:
            print("[NOTIFIER] Slack notification sent successfully!")
            return True
        else:
            print(f"[NOTIFIER] Slack API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[NOTIFIER] Failed to send Slack alert: {e}")
        return False

if __name__ == "__main__":
    # Test notifier module
    test_analysis = PMAnalysis(
        category="Feature Release",
        impact_level="High",
        summary="Competitor released automated AI pull request generation and CI/CD security scanning.",
        key_takeaways=[
            "Integrated automated PR generation using AI",
            "Added real-time CI/CD vulnerability scanning",
            "Updated enterprise pricing tier to $21/user/month"
        ]
    )
    send_slack_notification(test_analysis, "https://github.com/readme")