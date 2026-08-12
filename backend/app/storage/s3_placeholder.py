class S3StorageProvider:
    """Future extension point only. LocalStorageProvider is the default and requires no cloud account."""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("S3 storage is intentionally not implemented for this local-first assignment.")
