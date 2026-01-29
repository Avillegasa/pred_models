"""
Column detector service to identify which ML model to use based on CSV columns
"""
from typing import Optional, List, Set


class ColumnDetector:
    # Required columns for each model
    PHISHING_COLUMNS = {"sender", "subject", "body"}
    ATO_COLUMNS = {"user_id", "ip_address", "country"}
    BRUTE_FORCE_COLUMNS = {"dst_port", "protocol", "flow_duration"}

    # Alternative column names that map to required columns
    COLUMN_ALIASES = {
        # Phishing
        "from": "sender",
        "email_from": "sender",
        "remitente": "sender",
        "asunto": "subject",
        "cuerpo": "body",
        "content": "body",
        "mensaje": "body",
        # ATO
        "userid": "user_id",
        "user": "user_id",
        "ip": "ip_address",
        "ipaddress": "ip_address",
        "pais": "country",
        "country_code": "country",
        # Brute Force
        "dstport": "dst_port",
        "destination_port": "dst_port",
        "protocolo": "protocol",
        "proto": "protocol",
        "flowduration": "flow_duration",
        "duration": "flow_duration",
    }

    @classmethod
    def normalize_columns(cls, columns: List[str]) -> Set[str]:
        """Normalize column names to lowercase and apply aliases"""
        normalized = set()
        for col in columns:
            col_lower = col.lower().strip().replace(" ", "_")
            # Check if it's an alias
            if col_lower in cls.COLUMN_ALIASES:
                normalized.add(cls.COLUMN_ALIASES[col_lower])
            else:
                normalized.add(col_lower)
        return normalized

    @classmethod
    def detect_model(cls, columns: List[str]) -> Optional[str]:
        """
        Detect which ML model to use based on the columns in the file.
        Returns: 'phishing', 'ato', 'brute_force', or None if no match
        """
        normalized = cls.normalize_columns(columns)

        # Check for Phishing columns
        if cls.PHISHING_COLUMNS.issubset(normalized):
            return "phishing"

        # Check for Account Takeover columns
        if cls.ATO_COLUMNS.issubset(normalized):
            return "ato"

        # Check for Brute Force columns
        if cls.BRUTE_FORCE_COLUMNS.issubset(normalized):
            return "brute_force"

        return None

    @classmethod
    def get_required_columns(cls, model_type: str) -> Set[str]:
        """Get the required columns for a specific model"""
        model_columns = {
            "phishing": cls.PHISHING_COLUMNS,
            "ato": cls.ATO_COLUMNS,
            "brute_force": cls.BRUTE_FORCE_COLUMNS,
        }
        return model_columns.get(model_type, set())

    @classmethod
    def get_missing_columns(cls, columns: List[str], model_type: str) -> Set[str]:
        """Get missing required columns for a specific model"""
        normalized = cls.normalize_columns(columns)
        required = cls.get_required_columns(model_type)
        return required - normalized
