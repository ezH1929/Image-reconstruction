/**
 * @file
 * @brief Implementation of a convex hull algorithm using the Kirkpatrick-Seidel algorithm.
 */

// Define canvas and context
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Initialize UI elements
const startButton = document.getElementById("startButton");
const statusDiv = document.getElementById("valid");
const checking = document.getElementById("checking");
const upper = document.getElementById("upper");
const lower = document.getElementById("lower");

// Define point radius
const pointRadius = 10;

// Initialize variables
let count = 0;
let points = [];

/**
 * @brief Represents a point in 2D space.
 * @class
 */
class Point {
  constructor(x, y, count) {
    this.x = x;
    this.y = y;
    this.count = count;
  }
}

// Add event listener to canvas for adding points
canvas.addEventListener("click", function (event) {
  count++;
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  points.push(new Point(x, y, count));
  clear();
  drawPoints(points, "white");
});

/**
 * @brief Draw points on the canvas.
 * @param {Array} p - Array of points to draw.
 * @param {string} color - Color of the points.
 */
function drawPoints(p, color) {
  p.forEach((point) => {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(point.x, point.y, pointRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "black";
    ctx.fillText(point.count, point.x - 2, point.y + 2);
  });
}

// Event listener for start button
startButton.addEventListener("click", async function () {
  convexHull = await kirkpatrickSeidelConvexHull(points);
  clear();
  drawConvexHull(convexHull, "red");
  drawPoints(points, "white");
  drawPoints(convexHull, "red");
  statusDiv.innerHTML = getDIV(convexHull);
  checking.innerHTML +=
    'DONE : <span id="done"> Algorithm Complete !!</span><br>';
});

/**
 * @brief Draw the convex hull on the canvas.
 * @param {Array} hull - Array of points representing the convex hull.
 * @param {string} color - Color of the convex hull lines.
 */
function drawConvexHull(hull, color) {
  if (hull.length > 0) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(hull[0].x, hull[0].y);
    for (let i = 1; i < hull.length; i++) {
      ctx.lineTo(hull[i].x, hull[i].y);
    }
    ctx.closePath();
    ctx.stroke();
  }
}

/**
 * @brief Draw points, upper hull, and lower hull on the canvas.
 * @param {Array} up - Array of points representing the upper hull.
 * @param {Array} low - Array of points representing the lower hull.
 */
function draw(up, low) {
  clear();
  drawPoints(points, "white");
  drawPoints(up, "yellow");
  drawPoints(low, "blue");
  drawConvexHull(low, "blue");
  drawConvexHull(up, "yellow");
}

/**
 * @brief Compute the orientation of three points.
 * @param {Object} p - First point.
 * @param {Object} q - Second point.
 * @param {Object} r - Third point.
 * @returns {number} 0 if collinear, 1 if clockwise, and 2 if counterclockwise.
 */
async function Orientation(p, q, r) {
  await delay(1000);
  const val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
  if (val == 0) {
    checking.innerHTML += `FOUND : <span> point (${r.count}) is Collinear w.r.t point (${p.count}) and (${q.count})</span><br>`;
    return 0;
  } else if (val > 0) {
    checking.innerHTML += `FOUND : <span> point (${r.count}) is CW w.r.t point (${p.count}) and (${q.count})</span><br>`;
    return 1;
  } else {
    checking.innerHTML += `FOUND : <span> point (${r.count}) is CCW w.r.t point (${p.count}) and (${q.count})</span><br>`;
    return 2;
  }
}

/**
 * @brief Find the convex hull using the Kirkpatrick-Seidel algorithm.
 * @param {Array} points - Array of points.
 * @returns {Array} Array of points representing the convex hull.
 */
async function kirkpatrickSeidelConvexHull(points) {
  upper.innerHTML = "";
  lower.innerHTML = "";
  statusDiv.innerHTML = "";
  // Sort points lexicographically
  points.sort((a, b) => a.x - b.x || a.y - b.y);

  const n = points.length;
  if (n <= 1) return points;

  // Initialize upper and lower hulls
  const upperHull = [];
  const lowerHull = [];

  // Build upper hull
  checking.innerHTML = "";
  for (let i = 0; i < n; i++) {
    await delay(1000);
    checking.innerHTML += `CHECKING : <span> point ${points[i].count} in upper Hull</span><br>`;
    while (
      lowerHull.length >= 2 &&
      (await Orientation(
        lowerHull[lowerHull.length - 2],
        lowerHull[lowerHull.length - 1],
        points[i]
      )) !== 2
    ) {
      await delay(1000);
      let p = lowerHull.pop();
      checking.innerHTML += `REMOVING : <span> point ${p.count} from upper Hull</span><br><br>`;
      lower.innerHTML = getDIV(lowerHull);
      draw(upperHull, lowerHull);
    }
    await delay(1000);
    lowerHull.push(points[i]);
    checking.innerHTML += `ADDING : <span> point ${points[i].count} in upper Hull</span><br><br>`;
    lower.innerHTML = getDIV(lowerHull);
    draw(upperHull, lowerHull);
  }

  // Build lower hull
  checking.innerHTML = "";
  for (let i = n - 1; i >= 0; i--) {
    await delay(1000);
    checking.innerHTML += `CHECKING : <span> point ${points[i].count} in lower Hull</span><br>`;
    while (
      upperHull.length >= 2 &&
      (await Orientation(
        upperHull[upperHull.length - 2],
        upperHull[upperHull.length - 1],
        points[i]
      )) !== 2
    ) {
      await delay(1000);
      let p = upperHull.pop();
      checking.innerHTML += `REMOVING : <span> point ${p.count} from lower Hull</span><br><br>`;
      upper.innerHTML = getDIV(upperHull);
      draw(upperHull, lowerHull);
    }
    await delay(1000);
    upperHull.push(points[i]);
    draw(upperHull, lowerHull);
    upper.innerHTML = getDIV(upperHull);
    checking.innerHTML += `ADDING : <span> point ${points[i].count} in lower Hull</span><br><br>`;
  }

  // Remove the last point of each hull (as it's repeated)
  lowerHull.pop();
  upperHull.pop();

  // Concatenate the upper and lower hulls
  return lowerHull.concat(upperHull);
}
