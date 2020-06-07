import decode from 'jwt-decode';

const KEY = "access_token"

const getToken = () => {
  return localStorage.getItem(KEY) || null;
}

const isLoggedIn = () => {
  if (getToken()) {
    return true;
  }
  return false;
}

const loginUser = (token) => {
  localStorage.setItem(KEY, token);
  window.dispatchEvent(new Event("storage"));
}

const logoutUser = () => {
  localStorage.removeItem(KEY);
  window.dispatchEvent(new Event("storage"));
}

const getDecodedToken = () => {
  // Using jwt-decode npm package to decode the token
  return decode(getToken());
}

const getIdentity = () => {
  return getDecodedToken().identity;
}

export {
  getToken,
  isLoggedIn,
  loginUser,
  logoutUser,
  getIdentity,
}