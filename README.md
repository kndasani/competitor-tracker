\# Automated Competitor \& Feature Tracker 🚀



An event driven competitive intelligence tool that monitors competitor changelogs and pricing pages, detects delta changes using Parallel Web Systems, synthesizes insights with Google Gemini 2.5 Flash, and posts structured PM alerts directly to Slack.



\## Features

\* \*\*Web Content Extraction\*\*: Converts target websites into clean Markdown snapshots via Parallel Web Systems Extract API.

\* \*\*Snapshot Diff Engine\*\*: Compares historical snapshots to isolate text additions and line level updates.

\* \*\*LLM PM Analysis\*\*: Uses Gemini 2.5 Flash with structured Pydantic schemas to output update category, impact level, summary, and key takeaways.

\* \*\*Automated Alerting\*\*: Delivers rich card formatted alerts directly to Slack via webhooks.



\## Architecture \& Flow

1\. \*\*Extraction\*\*: Fetch target web pages as Markdown.

2\. \*\*Snapshot Storage\*\*: Store timestamped Markdown snapshots locally.

3\. \*\*Diff Analysis\*\*: Run unified line diffing on consecutive snapshots.

4\. \*\*AI Synthesis\*\*: Send raw deltas to Gemini 2.5 Flash for product management evaluation.

5\. \*\*Notification\*\*: Send real time structured update alerts to Slack.



\## Getting Started



\### Prerequisites

\* Python 3.10+

\* Parallel Web Systems API Key

\* Google Gemini API Key

\* Slack Incoming Webhook URL



\### Installation

1\. Clone the repository:

&#x20;  ```bash

&#x20;  git clone \[https://github.com/your-username/competitor-tracker.git](https://github.com/your-username/competitor-tracker.git)

&#x20;  cd competitor-tracker

