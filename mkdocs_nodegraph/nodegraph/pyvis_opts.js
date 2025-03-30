var options = {
  "nodes": {
    "font": {
      "size": 70,
      "align": "middle"
    },
    "scaling": {
      "min": 70,
      "max": 120
    },
    "borderWidth": 0,
    "size": 100
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "stabilization": {
      "enabled": false
    },
    "forceAtlas2Based": {
      "theta": 0.5,
      "gravitationalConstant": -1100,
      "centralGravity": 0.009,
      "springConstant": 0.08,
      "springLength": 600,
      "damping": 0.2,
      "avoidOverlap": 0
    },
    "solver": "forceAtlas2Based",
    "minVelocity": 0.75,
    "timestep": 0.50
  }
}