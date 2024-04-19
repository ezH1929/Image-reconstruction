@section subsection1 Details:

Sure, let's summarize the Kirkpatrick-Seidel algorithm with its explanation, complexity analysis, and pseudocode in points:

### Explanation:
1. **Algorithm Overview**: Kirkpatrick-Seidel is an incremental convex hull algorithm that divides the set of points into upper and lower hulls and then merges them to obtain the final convex hull.
2. **Upper and Lower Hulls**: It builds the upper and lower hulls separately by iterating through the sorted points.
3. **Merging Hulls**: After constructing the upper and lower hulls, it merges them to obtain the final convex hull.
4. **Orientation Test**: The algorithm relies on the orientation test to determine the convexity of the hull and the relative positions of points.

### Complexity:
- **Time Complexity**:
  - Sorting: O(n log n)
  - Building Upper and Lower Hulls: O(n log n)
  - Merging Hulls: O(n)
  - Overall Time Complexity: O(n log n)
- **Space Complexity**:
  - Sorting: O(n)
  - Building Upper and Lower Hulls: O(n)
  - Merging Hulls: O(n)
  - Overall Space Complexity: O(n)

### Pseudocode:
```plaintext
Kirkpatrick-Seidel(ConvexHullInput):
    // Sort points lexicographically
    points.sort((a, b) => a.x - b.x || a.y - b.y)
    
    // Initialize upper and lower hulls
    upperHull = []
    lowerHull = []
    
    // Build upper hull
    for each point in points:
        while size(upperHull) >= 2 and orientation(upperHull[-2], upperHull[-1], point) != 2:
            upperHull.pop()
        upperHull.append(point)
    
    // Build lower hull
    for each point in reverse(points):
        while size(lowerHull) >= 2 and orientation(lowerHull[-2], lowerHull[-1], point) != 2:
            lowerHull.pop()
        lowerHull.append(point)
    
    // Remove the last point of each hull (repeated)
    upperHull.pop()
    lowerHull.pop()
    
    // Concatenate upper and lower hulls
    convexHull = lowerHull + upperHull
    
    return convexHull
```

In summary, the Kirkpatrick-Seidel algorithm efficiently computes the convex hull of a set of points with a time complexity of O(n log n) and a space complexity of O(n). It achieves this by dividing the problem into smaller subproblems, building and merging hulls, and relying on the orientation test for efficiency.

#Plot for Kirk Patrik Algorithm:
![](Gem.png)