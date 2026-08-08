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
    Client for communicating with the LeetCode GraphQL API.
    """

    GRAPHQL_URL = "https://leetcode.com/graphql"

    USER_AGENT = "CodeInsight/1.0"

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

    def __init__(self, timeout=10):
        self.timeout = timeout

    def _execute_query(self, query, variables):
        """
        Execute a GraphQL query against LeetCode.
        """

        payload = {
            "query": query,
            "variables": variables,
        }

        try:
            response = requests.post(
                self.GRAPHQL_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self.USER_AGENT,
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

        return result.get("data", {})

    def get_user_profile(self, username):
        """
        Fetch a user's public profile and solved-problem statistics.
        """

        data = self._execute_query(
            query=self.PROFILE_QUERY,
            variables={
                "username": username,
            },
        )

        matched_user = data.get("matchedUser")

        if matched_user is None:
            raise LeetCodeUserNotFoundError(
                "LeetCode user not found."
            )

        return matched_user

    def get_recent_submissions(
        self,
        username,
        limit=20,
    ):
        """
        Fetch recent accepted submissions for a LeetCode user.
        """

        data = self._execute_query(
            query=self.RECENT_SUBMISSIONS_QUERY,
            variables={
                "username": username,
                "limit": limit,
            },
        )

        submissions = data.get(
            "recentAcSubmissionList"
        )

        return submissions or []