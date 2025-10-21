// server/userRepo.js
const db = require('./db');

async function upsertUserByEmail(email, pricingPlan = 'free') {
  const q = `
    INSERT INTO users (email, pricing_plan)
    VALUES ($1, $2)
    ON CONFLICT (email)
    DO UPDATE SET pricing_plan = COALESCE(users.pricing_plan, EXCLUDED.pricing_plan)
    RETURNING id;
  `;
  const { rows } = await db.query(q, [email, pricingPlan]);
  return rows[0].id;
}

async function upsertUserToken(userId, encryptedTokenData) {
  const q = `
    INSERT INTO user_tokens (user_id, encrypted_token_data)
    VALUES ($1, $2)
    ON CONFLICT (user_id)
    DO UPDATE SET encrypted_token_data = EXCLUDED.encrypted_token_data,
                  updated_at = NOW();
  `;
  await db.query(q, [userId, encryptedTokenData]);
}

module.exports = { upsertUserByEmail, upsertUserToken };