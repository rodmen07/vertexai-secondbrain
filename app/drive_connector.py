"""Simple Google Drive connector utilities.

This module provides a minimal, testable wrapper for listing Drive files
and downloading file contents. It imports the real Google API client lazily,
and allows tests to inject a fake `build` implementation via the
`_TEST_BUILD` global.

Note: In production, provide a `google.oauth2` credentials object (service
account or OAuth2 credentials) when initializing `DriveConnector`.
"""
from typing import Optional, List, Dict, Any

# Testing hook: tests can set this to a fake `build` callable to avoid
# importing the actual googleapiclient package.
_TEST_BUILD = None


def _build_service(credentials: Optional[Any] = None):
    """Return a Drive API service instance.

    Tries to import `googleapiclient.discovery.build`, falling back to the
    `_TEST_BUILD` hook for unit tests.
    """
    try:
        from googleapiclient.discovery import build  # type: ignore
    except Exception:
        build = _TEST_BUILD
        if not build:
            raise ImportError(
                "googleapiclient is required: pip install google-api-python-client google-auth"
            )
    return build("drive", "v3", credentials=credentials)


class DriveConnector:
    """Minimal Drive connector.

    Methods are synchronous and return plain Python objects for easy testing.
    """

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    def __init__(self, credentials: Optional[Any] = None):
        self.credentials = credentials

    def list_files(self, q: Optional[str] = None, page_size: int = 100) -> List[Dict[str, Any]]:
        """List files in Drive.

        Returns a list of file dicts with `id` and `name` keys when available.
        """
        service = _build_service(self.credentials)
        resp = service.files().list(q=q, pageSize=page_size, fields="files(id,name)", spaces="drive").execute()
        return resp.get("files", [])

    def download_file(self, file_id: str) -> bytes:
        """Download the raw bytes of a file by id.

        This implementation uses `files().get_media(...).execute()` which is
        simple to test; for production large-file downloads prefer
        `MediaIoBaseDownload`.
        """
        service = _build_service(self.credentials)
        request = service.files().get_media(fileId=file_id)
        return request.execute()
