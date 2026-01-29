"""
Client for calling ML prediction APIs
"""
import httpx
from typing import List, Dict, Any, Optional
from ..config import get_settings

settings = get_settings()


class PredictionClient:
    API_URLS = {
        "phishing": settings.PHISHING_API_URL,
        "ato": settings.ATO_API_URL,
        "brute_force": settings.BRUTE_FORCE_API_URL,
    }

    @classmethod
    async def predict_batch(
        cls,
        model_type: str,
        records: List[Dict[str, Any]],
        timeout: float = 120.0
    ) -> Optional[Dict[str, Any]]:
        """
        Send batch prediction request to the appropriate ML API
        """
        base_url = cls.API_URLS.get(model_type)
        if not base_url:
            raise ValueError(f"Unknown model type: {model_type}")

        endpoint = f"{base_url}/predict/batch"

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                # Format payload according to each API's expected format
                payload = cls._format_payload(model_type, records)
                response = await client.post(endpoint, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"API error: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Connection error to {model_type} API: {str(e)}")

    @classmethod
    def _format_payload(cls, model_type: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format payload according to each API's expected structure"""
        if model_type == "phishing":
            return {
                "emails": [
                    {
                        "sender": r.get("sender", ""),
                        "subject": r.get("subject", ""),
                        "body": r.get("body", ""),
                        "has_attachment": r.get("has_attachment", False),
                        "num_links": r.get("num_links", 0),
                    }
                    for r in records
                ]
            }
        elif model_type == "ato":
            return {
                "logins": [
                    {
                        "user_id": str(r.get("user_id", "")),
                        "ip_address": str(r.get("ip_address", "")),
                        "country": str(r.get("country", "US"))[:2],
                        "region": str(r.get("region", "Unknown")),
                        "city": str(r.get("city", "Unknown")),
                        "browser": str(r.get("browser", "Chrome 120.0")),
                        "os": str(r.get("os", "Windows 10")),
                        "device": str(r.get("device", "Desktop")),
                        "login_successful": int(r.get("login_successful", 1)),
                        "is_attack_ip": int(r.get("is_attack_ip", 0)),
                        "asn": int(r.get("asn", 0)),
                        "rtt": float(r.get("rtt", 50.0)),
                    }
                    for r in records
                ]
            }
        elif model_type == "brute_force":
            # All 60 features required by the model, normalized 0-1
            return {
                "flows": [
                    {
                        "dst_port": float(r.get("dst_port", 0)),
                        "protocol": float(r.get("protocol", 0)),
                        "timestamp": float(r.get("timestamp", 0)),
                        "flow_duration": float(r.get("flow_duration", 0)),
                        "tot_fwd_pkts": float(r.get("tot_fwd_pkts", 0)),
                        "tot_bwd_pkts": float(r.get("tot_bwd_pkts", 0)),
                        "totlen_fwd_pkts": float(r.get("totlen_fwd_pkts", 0)),
                        "fwd_pkt_len_max": float(r.get("fwd_pkt_len_max", 0)),
                        "fwd_pkt_len_min": float(r.get("fwd_pkt_len_min", 0)),
                        "fwd_pkt_len_mean": float(r.get("fwd_pkt_len_mean", 0)),
                        "fwd_pkt_len_std": float(r.get("fwd_pkt_len_std", 0)),
                        "bwd_pkt_len_max": float(r.get("bwd_pkt_len_max", 0)),
                        "bwd_pkt_len_min": float(r.get("bwd_pkt_len_min", 0)),
                        "bwd_pkt_len_mean": float(r.get("bwd_pkt_len_mean", 0)),
                        "bwd_pkt_len_std": float(r.get("bwd_pkt_len_std", 0)),
                        "flow_byts_s": float(r.get("flow_byts_s", 0)),
                        "flow_pkts_s": float(r.get("flow_pkts_s", 0)),
                        "flow_iat_mean": float(r.get("flow_iat_mean", 0)),
                        "flow_iat_std": float(r.get("flow_iat_std", 0)),
                        "flow_iat_max": float(r.get("flow_iat_max", 0)),
                        "fwd_iat_std": float(r.get("fwd_iat_std", 0)),
                        "bwd_iat_tot": float(r.get("bwd_iat_tot", 0)),
                        "bwd_iat_mean": float(r.get("bwd_iat_mean", 0)),
                        "bwd_iat_std": float(r.get("bwd_iat_std", 0)),
                        "bwd_iat_max": float(r.get("bwd_iat_max", 0)),
                        "bwd_iat_min": float(r.get("bwd_iat_min", 0)),
                        "fwd_psh_flags": float(r.get("fwd_psh_flags", 0)),
                        "bwd_psh_flags": float(r.get("bwd_psh_flags", 0)),
                        "fwd_urg_flags": float(r.get("fwd_urg_flags", 0)),
                        "bwd_urg_flags": float(r.get("bwd_urg_flags", 0)),
                        "fwd_pkts_s": float(r.get("fwd_pkts_s", 0)),
                        "bwd_pkts_s": float(r.get("bwd_pkts_s", 0)),
                        "pkt_len_min": float(r.get("pkt_len_min", 0)),
                        "pkt_len_max": float(r.get("pkt_len_max", 0)),
                        "pkt_len_mean": float(r.get("pkt_len_mean", 0)),
                        "pkt_len_std": float(r.get("pkt_len_std", 0)),
                        "pkt_len_var": float(r.get("pkt_len_var", 0)),
                        "fin_flag_cnt": float(r.get("fin_flag_cnt", 0)),
                        "rst_flag_cnt": float(r.get("rst_flag_cnt", 0)),
                        "psh_flag_cnt": float(r.get("psh_flag_cnt", 0)),
                        "ack_flag_cnt": float(r.get("ack_flag_cnt", 0)),
                        "urg_flag_cnt": float(r.get("urg_flag_cnt", 0)),
                        "cwe_flag_count": float(r.get("cwe_flag_count", 0)),
                        "down_up_ratio": float(r.get("down_up_ratio", 0)),
                        "fwd_byts_b_avg": float(r.get("fwd_byts_b_avg", 0)),
                        "fwd_pkts_b_avg": float(r.get("fwd_pkts_b_avg", 0)),
                        "fwd_blk_rate_avg": float(r.get("fwd_blk_rate_avg", 0)),
                        "bwd_byts_b_avg": float(r.get("bwd_byts_b_avg", 0)),
                        "bwd_pkts_b_avg": float(r.get("bwd_pkts_b_avg", 0)),
                        "bwd_blk_rate_avg": float(r.get("bwd_blk_rate_avg", 0)),
                        "init_fwd_win_byts": float(r.get("init_fwd_win_byts", 0)),
                        "init_bwd_win_byts": float(r.get("init_bwd_win_byts", 0)),
                        "fwd_act_data_pkts": float(r.get("fwd_act_data_pkts", 0)),
                        "fwd_seg_size_min": float(r.get("fwd_seg_size_min", 0)),
                        "active_mean": float(r.get("active_mean", 0)),
                        "active_std": float(r.get("active_std", 0)),
                        "active_max": float(r.get("active_max", 0)),
                        "active_min": float(r.get("active_min", 0)),
                        "idle_mean": float(r.get("idle_mean", 0)),
                        "idle_std": float(r.get("idle_std", 0)),
                    }
                    for r in records
                ]
            }
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    @classmethod
    async def check_health(cls, model_type: str) -> bool:
        """Check if an ML API is healthy"""
        base_url = cls.API_URLS.get(model_type)
        if not base_url:
            return False

        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{base_url}/health")
                return response.status_code == 200
            except Exception:
                return False
