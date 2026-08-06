import requests


class LeetCodeClientError(Exception):
    """
    Base exception for LeetCode client errors.
    """


class LeetCodeUserNotFoundError(LeetCodeClientError):
    """
    Raised when a LeetCode username does not exist.
    """


class LeetCodeClient:
    """
    Client for communicating with LeetCode GraphQL.
    """

    GRAPHQL_URL = "https://leetcode.com/graphql"

    PROFILE_QUERY = """
    query userProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile {
                ranking
                reputation
            }
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """

    def __init__(self, timeout=10):
        self.timeout = timeout

    def get_user_profile(self, username):
        """
        Fetch public profile and solved-problem statistics.
        """

        payload = {
            "query": self.PROFILE_QUERY,
            "variables": {
                "username": username,
            },
        }

        try:
            response = requests.post(
                self.GRAPHQL_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "CodeInsight/1.0",
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            raise LeetCodeClientError(
                "Unable to communicate with LeetCode."
            ) from exc

        try:
            result = response.json()
        except ValueError as exc:
            raise LeetCodeClientError(
                "LeetCode returned an invalid response."
            ) from exc

        if result.get("errors"):
            raise LeetCodeClientError(
                "LeetCode returned an error."
            )

        matched_user = result.get("data", {}).get("matchedUser")

        if matched_user is None:
            raise LeetCodeUserNotFoundError(
                "LeetCode user not found."
            )

        return matched_user
    RECENT_SUBMISSIONS_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
    recentAcSubmissionList(
        username: $username
        limit: $limit
    ) {
        id
        title
        titleSlug
        timestamp
        lang
    }
}
"""

    def get_recent_submissions(self, username, limit=20):
        """
        Fetch recent accepted submissions for a LeetCode user.
        """

        payload = {
            "query": self.RECENT_SUBMISSIONS_QUERY,
            "variables": {
                "username": username,
                "limit": limit,
            },
        }

        try:
            response = requests.post(
                self.GRAPHQL_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "CodeInsight/1.0",
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            raise LeetCodeClientError(
                "Unable to communicate with LeetCode."
            ) from exc

        try:
            result = response.json()

        except ValueError as exc:
            raise LeetCodeClientError(
                "LeetCode returned an invalid response."
            ) from exc

        if result.get("errors"):
            raise LeetCodeClientError(
                "LeetCode returned an error."
            )

        data = result.get("data") or {}

        submissions = data.get("recentAcSubmissionList")

        if submissions is None:
            return []

        return submissions