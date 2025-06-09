// frontend/src/utils/storage.js
const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'user_preferences',
  HELD_BILLS: 'held_bills',
  RECENT_SEARCHES: 'recent_searches'
};

export const storage = {
  // Token management
  getToken: () => localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN),
  setToken: (token) => localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token),
  removeToken: () => localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN),
  
  // User preferences
  getPreferences: () => {
    const prefs = localStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
    return prefs ? JSON.parse(prefs) : {};
  },
  setPreferences: (prefs) => {
    localStorage.setItem(STORAGE_KEYS.USER_PREFERENCES, JSON.stringify(prefs));
  },
  
  // Held bills
  getHeldBills: () => {
    const bills = localStorage.getItem(STORAGE_KEYS.HELD_BILLS);
    return bills ? JSON.parse(bills) : [];
  },
  addHeldBill: (bill) => {
    const bills = storage.getHeldBills();
    bills.push({ ...bill, heldAt: new Date().toISOString() });
    localStorage.setItem(STORAGE_KEYS.HELD_BILLS, JSON.stringify(bills));
  },
  removeHeldBill: (billId) => {
    const bills = storage.getHeldBills().filter(b => b.id !== billId);
    localStorage.setItem(STORAGE_KEYS.HELD_BILLS, JSON.stringify(bills));
  },
  
  // Recent searches
  getRecentSearches: () => {
    const searches = localStorage.getItem(STORAGE_KEYS.RECENT_SEARCHES);
    return searches ? JSON.parse(searches) : [];
  },
  addRecentSearch: (search) => {
    let searches = storage.getRecentSearches();
    searches = [search, ...searches.filter(s => s !== search)].slice(0, 10);
    localStorage.setItem(STORAGE_KEYS.RECENT_SEARCHES, JSON.stringify(searches));
  }
};