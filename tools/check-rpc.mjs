import { createClient } from 'genlayer-js';
import { testnetBradbury } from 'genlayer-js/chains';
const client = createClient({ chain: testnetBradbury });
try {
  const bal = await client.getBalance({ address: '0xc833fA7C02f5de5D5666A55aaBeB3752FBf24C9e' });
  console.log('Bradbury RPC OK, demo account balance:', bal.toString());
} catch (e) {
  console.log('RPC error:', String(e).slice(0, 200));
}
