const K = 50;

function calculateEloGain(p1_points, p2_points) {
  // p1 is the winner
  let expected_score_p1 = 1 / (1 + Math.pow(10, (p2_points - p1_points)/400));

  return Math.floor(K * (1 - expected_score_p1));
}

function getImagePath(name) {
  if (process.env.NODE_ENV === "development") {
    return `/images/${name}`;
  } else {
    return `/static/images/${name}`;
  }
}

export {
  calculateEloGain,
  getImagePath
}