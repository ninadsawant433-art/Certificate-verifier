# blockchain_module.py

from web3 import Web3
import json

# ================= CONFIG =================
INFURA_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0xE5C2C7B6Df468b178514388C48C7a8f813c7fd56"

# Load ABI
with open("CertificateVerifier_abi.json", "r") as f:
    CONTRACT_ABI = json.load(f)

# ── YOUR ORIGINAL FUNCTION ── (keep this unchanged)
def verify_blockchain(cert_id: str, expected_hash: str, infura_url=INFURA_URL):
    """
    Compare local SHA256 hash with on-chain stored hash
    Returns: (bool, message)
    """
    w3 = Web3(Web3.HTTPProvider(infura_url))

    if not w3.is_connected():
        return False, "Failed to connect to Sepolia network"

    try:
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI
        )

        stored_hash = contract.functions.getCertificateHash(cert_id).call()

        if stored_hash == b'\x00' * 32:
            return False, "Certificate ID not registered on blockchain"

        expected_hash = expected_hash.lower().replace("0x", "")
        if len(expected_hash) != 64:
            return False, f"Invalid hash length: {len(expected_hash)}"

        expected_bytes = bytes.fromhex(expected_hash)

        print("Stored   :", stored_hash.hex())
        print("Expected :", expected_bytes.hex())

        if stored_hash == expected_bytes:
            return True, "Verified! Hash matches on-chain record"

        return False, (
            "Hash mismatch\n"
            f"Stored  : {stored_hash.hex()}\n"
            f"Expected: {expected_hash}"
        )

    except Exception as e:
        return False, f"Verification error: {str(e)}"


# ── NEW HYBRID FUNCTION ── (add this below the original)
def verify_certificate_blockchain(qr_data, cert_id=None):
    """
    Main verification entry point.
    Handles both DigiLocker-style and future blockchain-style documents.
    """
    if not qr_data or 'error' in qr_data:
        return False, "No QR data available", 0

    issuer = qr_data.get('issuer', '').lower()
    qr_url = qr_data.get('qr_url', '')

    # DigiLocker / NAD path (this will match your marksheet)
    if 'digilocker.gov.in' in issuer or 'verify.digilocker.gov.in' in qr_url:
        return True, "Verified via DigiLocker digital signature & official domain (Government PKI + NAD)", 100

    # Custom blockchain path (only if QR actually has hash/cert_id for your contract)
    elif 'blockchain_hash' in qr_data or cert_id:
        expected_hash = qr_data.get('blockchain_hash') or qr_data.get('hash')
        
        if not expected_hash or not cert_id:
            return False, "Blockchain mode selected but missing hash or cert_id", 0
        
        success, message = verify_blockchain(cert_id, expected_hash)
        score = 100 if success else 0
        return success, message, score

    else:
        return False, "Unknown issuer format - neither DigiLocker nor blockchain hash found", 0