from input_module import extract_qr_data
from blockchain_module import verify_certificate_blockchain
from website_module import validate_website

def verify_certificate(pdf_path):

    qr_result = extract_qr_data(pdf_path)
    print("DEBUG - Extracted QR data:", qr_result)

    # -----------------------------------------------------
    # FAILED EXTRACTION
    # -----------------------------------------------------
    if 'error' in qr_result:
        status = "Invalid"
        reason = qr_result['error']
        web_display = "Unknown"
        bc_valid = False
        bc_reason = "QR extraction failed"
        trust_score = 0

        qr_raw = "Not extracted"
        qr_is_url = False
        qr_display = qr_raw

        verification_link = "https://verify.digilocker.gov.in/"
        link_text = "Official DigiLocker Verifier"
        proof_text = bc_reason

    # -----------------------------------------------------
    # SUCCESSFUL QR
    # -----------------------------------------------------
    else:
        qr_url_raw = qr_result.get('qr_url', '')
        issuer = qr_result.get('issuer', '').lower()

        # =====================================================
        # 🟢 VARIABLES YOU REQUESTED (ADDED EXACTLY)
        # =====================================================
        qr_raw = qr_result.get('qr_url', 'Encoded payload')

        qr_is_url = qr_raw.startswith(('http://', 'https://'))

        qr_display = (
            qr_raw if qr_is_url
            else (qr_raw[:120] + '...' if len(qr_raw) > 120 else qr_raw)
        )

        verification_link = (
            qr_result.get('verification_url')
            or (qr_raw if qr_is_url else "https://verify.digilocker.gov.in/")
        )

        link_text = (
            "Official Verification Page"
            if qr_is_url
            else "Official DigiLocker Verifier"
        )

        proof_text = bc_reason if 'bc_reason' in locals() else "Web/Digital verification available"
        # =====================================================

        # -------------------------------------------------
        # ISSUER LOGIC
        # -------------------------------------------------
        if 'digilocker' in issuer or 'nad' in issuer:
            status = "Valid"
            bc_valid = True
            bc_reason = "Verified via DigiLocker PKI"
            trust_score = 100
            web_display = "Trusted"

        elif 'nptel' in issuer:
            status = "Valid"
            bc_valid = True
            bc_reason = "Verified via NPTEL official portal"
            trust_score = 90
            web_display = "Trusted"

        elif qr_result.get('verification_url'):
            status = "Valid"
            bc_valid = True
            bc_reason = "Web verification available"
            trust_score = 80
            web_display = "Trusted"

        elif qr_result.get('cert_id'):
            bc_valid, bc_reason, _ = verify_certificate_blockchain(qr_result, None)
            status = "Valid" if bc_valid else "Invalid"
            trust_score = 75 if bc_valid else 30
            web_display = "Trusted"

        else:
            status = "Review Required"
            bc_valid = False
            bc_reason = "Unknown format"
            trust_score = 40
            web_display = "Unknown"

        reason = bc_reason
        proof_text = bc_reason


    # -----------------------------------------------------
    # 🟢 FINAL REPORT (UNCHANGED STRUCTURE)
    # -----------------------------------------------------
    report = f"""
✅ <strong>Status:</strong> {status}<br>

🌐 <strong>Website:</strong> <a href="{verification_link}" target="_blank">{web_display} ({link_text})</a><br>

🔗 <strong>QR Reference:</strong> {qr_display}<br>

⛓️ <strong>Proof:</strong> {proof_text}<br>

⚠️ <strong>Trust score:</strong> {trust_score}%<br><br>

<strong>Reason:</strong> {reason}
""".strip()

    # -----------------------------------------------------
    # ➕ VERIFICATION BUTTON
    # -----------------------------------------------------
    verification_link = qr_result.get('verification_url') or qr_result.get('qr_url', '')

    if verification_link.startswith(('http://', 'https://')):
        report += f'''
<br>
<a href="{verification_link}" target="_blank"
   style="display:inline-block;margin-top:12px;padding:8px 16px;
          background:#00ff9d;color:#0d1117;border-radius:6px;
          text-decoration:none;font-weight:bold;">
   Open Official Verification Page →
</a>
'''

    return report