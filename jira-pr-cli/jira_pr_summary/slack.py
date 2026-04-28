"""Slack integration for posting PR summaries"""

import json
import urllib.request
import urllib.error
from typing import Optional, Tuple, Dict, List


class SlackPoster:
    """Post PR summaries to Slack using incoming webhooks"""

    def __init__(self, webhook_url: str, channel: Optional[str] = None,
                 username: str = "Jira PR Summary", icon_emoji: str = ":jira:",
                 verbose: bool = False):
        """
        Initialize Slack poster

        Args:
            webhook_url: Slack incoming webhook URL
            channel: Optional channel override (e.g., #engineering)
            username: Bot display name (default: "Jira PR Summary")
            icon_emoji: Bot emoji icon (default: ":jira:")
            verbose: Enable verbose logging
        """
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.verbose = verbose

    def post_message(self, issue_key: str, summary: str, pr_info: List[Dict],
                    jira_url: str, thread_ts: Optional[str] = None,
                    dry_run: bool = False) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Post message to Slack

        Args:
            issue_key: Jira issue key (e.g., ACM-12345)
            summary: PR summary text
            pr_info: List of PR info dicts with 'number', 'title', 'url', etc.
            jira_url: URL to Jira issue
            thread_ts: Optional Slack thread timestamp for threading
            dry_run: If True, don't actually post

        Returns:
            Tuple of (success: bool, error_msg: Optional[str], thread_ts: Optional[str])
        """
        blocks = self._format_blocks(issue_key, summary, pr_info, jira_url)

        payload = {
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": blocks
        }

        if self.channel:
            payload["channel"] = self.channel

        if thread_ts:
            payload["thread_ts"] = thread_ts

        if dry_run:
            if self.verbose:
                print(f"🔍 [DEBUG] Would post to Slack (thread_ts: {thread_ts})")
                print(f"   Payload: {json.dumps(payload, indent=2)}")
            return True, None, thread_ts

        return self._make_request(payload)

    def _format_blocks(self, issue_key: str, summary: str, pr_info: List[Dict],
                      jira_url: str) -> List[Dict]:
        """
        Format message as Slack Block Kit blocks

        Args:
            issue_key: Jira issue key
            summary: PR summary text
            pr_info: List of PR info dicts
            jira_url: URL to Jira issue

        Returns:
            List of Slack Block Kit blocks
        """
        blocks = []

        # Header section with issue key
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📝 {issue_key}",
                "emoji": True
            }
        })

        # PR info section
        if pr_info:
            pr_lines = []
            for pr in pr_info:
                pr_number = pr.get('number', '?')
                pr_title = pr.get('title', 'No title')
                pr_url = pr.get('url', '')
                if pr_url:
                    pr_lines.append(f"• <{pr_url}|PR #{pr_number}>: {pr_title}")
                else:
                    pr_lines.append(f"• PR #{pr_number}: {pr_title}")

            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(pr_lines)
                }
            })

        # Summary section
        # Split summary into chunks if needed (Slack has a 3000 char limit per block)
        summary_chunks = self._split_text(summary, 2900)
        for chunk in summary_chunks:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": chunk
                }
            })

        # View in Jira button
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View in Jira",
                        "emoji": True
                    },
                    "url": jira_url,
                    "style": "primary"
                }
            ]
        })

        # Context footer
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Posted by Jira PR Summary"
                }
            ]
        })

        return blocks

    def _split_text(self, text: str, max_length: int = 2900) -> List[str]:
        """
        Split text into chunks that fit Slack's block text limits

        Args:
            text: Text to split
            max_length: Maximum length per chunk (default: 2900)

        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        while text:
            if len(text) <= max_length:
                chunks.append(text)
                break

            # Try to split at a newline
            split_idx = text.rfind('\n', 0, max_length)
            if split_idx == -1:
                # No newline found, split at max_length
                split_idx = max_length

            chunks.append(text[:split_idx])
            text = text[split_idx:].lstrip()

        return chunks

    def _make_request(self, payload: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Make HTTP POST request to Slack webhook

        Args:
            payload: JSON payload to send

        Returns:
            Tuple of (success: bool, error_msg: Optional[str], thread_ts: Optional[str])
        """
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )

            if self.verbose:
                print(f"🔍 [DEBUG] Posting to Slack webhook...")

            with urllib.request.urlopen(req, timeout=10) as response:
                response_data = response.read().decode('utf-8')
                if self.verbose:
                    print(f"🔍 [DEBUG] Slack response: {response_data}")

                # Slack webhooks return "ok" on success
                if response_data == "ok" or response.status == 200:
                    # For threaded messages, we need the thread_ts
                    # Since webhook doesn't return it, use the one we sent or generate new one
                    thread_ts = payload.get('thread_ts')
                    if not thread_ts and 'ts' in response_data:
                        # This would be for chat.postMessage API, not webhooks
                        # Webhooks don't return ts, so we'll need to track it ourselves
                        pass
                    return True, None, thread_ts
                else:
                    return False, f"Unexpected response: {response_data}", None

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            error_msg = f"HTTP {e.code}: {error_body}"
            if self.verbose:
                print(f"🔍 [DEBUG] Slack HTTP error: {error_msg}")
            return False, error_msg, None

        except urllib.error.URLError as e:
            error_msg = f"URL error: {e.reason}"
            if self.verbose:
                print(f"🔍 [DEBUG] Slack URL error: {error_msg}")
            return False, error_msg, None

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            if self.verbose:
                print(f"🔍 [DEBUG] Slack unexpected error: {error_msg}")
            return False, error_msg, None
