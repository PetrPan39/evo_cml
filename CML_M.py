PLUGIN_CATEGORY = 'M'
PLUGIN_NAME     = 'CloudMemoryManager'
PLUGIN_TAGS     = ['encryption', 's3', 'pinecone', 'kem']

PLUGIN_CATEGORY = 'M'
PLUGIN_NAME     = 'CloudMemoryManager'
PLUGIN_TAGS     = ['encryption', 's3', 'pinecone', 'kem']

import os
import boto3
# Fallback pro post-quantové KEM: liboqs Python bindings nebo pyoqs-sdk
try:
    import oqs
except ImportError:
    from pyoqs_sdk import KeyEncapsulation as _KEM
    class oqs:
        class KeyEncapsulation:
            def __init__(self, algorithm):
                self._kem = _KEM(algorithm)
            def import_public_key(self, key):
                pass
            def encapsulate(self):
                return self._kem.encap()
            def import_secret_key(self, key):
                pass
            def decapsulate(self, ct):
                return self._kem.decap(ct)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# … zbytek souboru beze změny …

class CloudMemoryManager:
    def __init__(self, user_id, s3_bucket, pinecone_index, kms_key_alias):
        self.user_id = user_id
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.kms = boto3.client('kms')
        self.kms_alias = kms_key_alias
        pinecone.init()
        self.index = pinecone.Index(pinecone_index)

    def encapsulate_key(self, pk_user: bytes) -> (bytes, bytes):
        with oqs.KeyEncapsulation("Kyber512") as kem:
            kem.import_public_key(pk_user)
            ct, ss = kem.encapsulate()
        return ct, ss

    def decapsulate_key(self, ct: bytes, sk_user: bytes) -> bytes:
        with oqs.KeyEncapsulation("Kyber512") as kem:
            kem.import_secret_key(sk_user)
            ss = kem.decapsulate(ct)
        return ss

    def derive_key(self, ss: bytes) -> bytes:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'cml-data-key'
        )
        return hkdf.derive(ss)

    def derive_matrices(self, ss: bytes):
        return {'seed': ss}

    def encrypt_blob(self, data: bytes, data_key: bytes) -> bytes:
        aes = AESGCM(data_key)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, data, None)
        return nonce + ct

    def decrypt_blob(self, blob: bytes, matrices: dict) -> bytes:
        data_key = self.derive_key(matrices['seed'])
        aes = AESGCM(data_key)
        nonce, ct = blob[:12], blob[12:]
        return aes.decrypt(nonce, ct, None)

    def upload_encrypted(self, key: str, ct_bytes: bytes, encrypted_blob: bytes):
        meta = {'kms_ct': ct_bytes.hex()}
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=encrypted_blob,
            Metadata=meta
        )

    def download_encrypted(self, key: str) -> (bytes, bytes):
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        ct_hex = obj['Metadata'].get('kms_ct')
        return bytes.fromhex(ct_hex), obj['Body'].read()

    def index_embedding(self, vector: list, metadata: dict):
        self.index.upsert([(f"{self.user_id}-{metadata['id']}", vector, metadata)])

    def query_memory(self, vector: list, top_k: int = 5) -> list:
        res = self.index.query(vector, top_k=top_k, include_metadata=True)
        return res.matches
