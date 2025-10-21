// server/crypto.js
const crypto = require('crypto');

const keyB64 = process.env.ENCRYPTION_KEY;
if (!keyB64) {
  throw new Error('ENCRYPTION_KEY is required (32-byte base64) for token encryption');
}
const key = Buffer.from(keyB64, 'base64');
if (key.length !== 32) {
  throw new Error('ENCRYPTION_KEY must decode to 32 bytes for AES-256-GCM');
}

function encryptJson(obj) {
  const iv = crypto.randomBytes(12); // GCM nonce
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const plaintext = Buffer.from(JSON.stringify(obj), 'utf8');
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  // Store iv + tag + ciphertext in base64
  const payload = Buffer.concat([iv, tag, ciphertext]).toString('base64');
  return payload;
}

function decryptJson(payloadB64) {
  const buf = Buffer.from(payloadB64, 'base64');
  const iv = buf.subarray(0, 12);
  const tag = buf.subarray(12, 28);
  const ciphertext = buf.subarray(28);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(plaintext.toString('utf8'));
}

module.exports = { encryptJson, decryptJson };