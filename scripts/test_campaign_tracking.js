const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require.resolve('../script.js'), 'utf8');
const functions = source.slice(source.indexOf('function getTrackingFields()'), source.indexOf('\ngetTrackingFields();'));
const storage = new Map();
let consent = 'accepted';
const context = {
  URLSearchParams,
  CAMPAIGN_SESSION_KEY: 'campaign',
  getAnalyticsConsent: () => consent,
  window: {location: {search: '?utm_source=test&utm_campaign=launch'}, sessionStorage: {
    getItem: key => storage.get(key) || null,
    setItem: (key,value) => storage.set(key,value),
    removeItem: key => storage.delete(key),
  }},
};
vm.createContext(context);
vm.runInContext(functions, context);
assert.equal(context.getTrackingFields().utm_source, 'test');
context.window.location.search = '';
assert.equal(context.getTrackingFields().utm_campaign, 'launch');
context.window.location.search = '?utm_source=other';
assert.equal(context.getTrackingFields().utm_source, 'other');
assert.equal(context.getTrackingFields().utm_campaign, '');
consent = 'rejected';
context.window.location.search = '';
assert.equal(context.getTrackingFields().utm_source, '');
assert.equal(storage.size, 0);
context.window.sessionStorage.getItem = () => { throw Error('blocked'); };
consent = 'accepted';
assert.equal(context.getTrackingFields().utm_source, '');
console.log('Campaign tracking tests passed: persistence, replacement, consent withdrawal, blocked storage.');
