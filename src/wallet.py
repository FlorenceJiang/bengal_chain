import binascii
import hashlib
import base64

from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError


CODE_FORMAT = "utf-8"


def verify_sign(pubkey, msg, signature):
    """
    verifying the signature is authentic.
    """
    verifier = VerifyingKey.from_pem(pubkey)
    hash = hashlib.sha256(msg.encode(CODE_FORMAT))
    return verifier.verify(binascii.unhexlify(signature), hash.digest())


class Wallet:
    def __init__(self):
        """
        init wallet based on a pair of private/public keys on elliptic curve, which represents an account on the chain.

        """
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self._public_key = self._private_key.get_verifying_key()

    @property
    def address(self):
        """
        generate an address from public key.
        """
        hash = hashlib.sha256(self._public_key.to_pem())
        return base64.b64encode(hash.digest())

    @property
    def pubkey(self):
        """
        return public key string
        """
        return self._public_key.to_pem()

    def sign(self, msg):
        """
        generate digital signatrue
        """
        hash = hashlib.sha256(msg.encode(CODE_FORMAT))
        return binascii.hexlify(self._private_key.sign(hash.digest()))


if __name__ == "__main__":
    # test the wallet
    w = Wallet()
    print(f"wallet address: {w.address}")
    print(f"wallet pubkey: {w.pubkey}")

    test_data = "this is a test!"
    sig = w.sign(test_data)
    print(f"digital signatrue: {sig}")

    # verifying wallet
    print(f"verify signature: {verify_sign(w.pubkey, test_data, sig)}")
