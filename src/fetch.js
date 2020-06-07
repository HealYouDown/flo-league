import { getToken } from "./auth";

var API_URL;

switch (process.env.NODE_ENV) {
  case "development":
    API_URL = "http://127.0.0.1:5000/api";
    break
  default:
    API_URL = "/api";
};

function getHeaders() {
  const token = getToken();
  let httpHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
  };

  if (token) {
    httpHeaders["Authorization"] = `Bearer ${token}`;
  }

  return new Headers(httpHeaders);
}

// API Functions
function getRanking(server) {
  const url = `${API_URL}/ranking/${server}`;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

function login(username, password) {
  const url = `${API_URL}/login`;
  return fetch(url, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({username, password})
  })
}

function getPlayers(server) {
  const url = `${API_URL}/players/${server}`
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

function getPlayer(server, name) {
  const url = `${API_URL}/players/${server}/${name}`
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

function createMatches(server, playerIds) {
  const url = `${API_URL}/active_matches/${server}`
  return fetch(url, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ids: playerIds})
  })
}

function getActiveMatches(server) {
  const url = `${API_URL}/active_matches/${server}`
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

function setActiveMatchWinner(server, matchId, winner) {
  const url = `${API_URL}/active_matches/${server}/${matchId}`
  return fetch(url, {
    method: "PATCH",
    headers: getHeaders(),
    body: JSON.stringify({winner})
  })
}

function updateMatchWinner(matchId, newWinner) {
  const url = `${API_URL}/matches/${matchId}`
  return fetch(url, {
    method: "PATCH",
    headers: getHeaders(),
    body: JSON.stringify({winner: newWinner})
  })
}

function deleteActiveMatches(server) {
  const url = `${API_URL}/active_matches/${server}`;
  return fetch(url, {
    method: "DELETE",
    headers: getHeaders(),
  })
}

function updatePlayer(server, name, newPlayer) {
  const url = `${API_URL}/players/${server}/${name}`;
  return fetch(url, {
    method: "PATCH",
    headers: getHeaders(),
    body: JSON.stringify(newPlayer),
  })
}

function addPlayer(server, newPlayer) {
  const url = `${API_URL}/players/${server}`;
  return fetch(url, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(newPlayer),
  })
}

export {
  getRanking,
  login,
  getPlayers,
  getPlayer,
  createMatches,
  getActiveMatches,
  setActiveMatchWinner,
  updateMatchWinner,
  deleteActiveMatches,
  updatePlayer,
  addPlayer,
}