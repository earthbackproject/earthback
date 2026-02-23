// Earthback AI Visualizer — Netlify Function
// Calls Replicate Flux Schnell API, returns image URL

const https = require('https');

const REPLICATE_MODEL = "black-forest-labs/flux-schnell";
const REPLICATE_API_PATH = `/v1/models/${REPLICATE_MODEL}/predictions`;

// Prompt engineering
const STYLE_MODIFIERS = {
  photorealistic: "DSLR architectural photography, golden hour warm lighting, 85mm lens, shallow depth of field, professional real estate photo",
  sketch: "Architectural concept sketch, pencil and watercolor on warm textured paper, hand-drawn feel, loose confident lines",
  blueprint: "Technical architectural blueprint, white lines on dark blue background, annotated dimensions, cross-section view"
};

const CLIMATE_CONTEXT = {
  "high-desert": "Red rock desert landscape, sage and juniper, wide open sky, arid terrain, warm earth tones",
  "prairie": "Open grassland, big sky, windbreak trees, gentle rolling terrain, golden light",
  "forest": "Dense conifer forest, dappled sunlight, moss and fern undergrowth, rich greens",
  "coastal": "Ocean coastal setting, salt-tolerant native plants, sandy soil, weathered natural wood",
  "mountain": "Alpine meadow, mountain backdrop, stone foundation, steep pitched roof for snow",
  "tropical": "Lush tropical vegetation, palm shade, open-air design, cross-ventilation, bright light"
};

const STRUCTURE_CONTEXT = {
  "single-home": "Single family residence, one story",
  "duplex": "Duplex two-unit dwelling, shared wall",
  "community-hub": "Community gathering building, large open interior, welcoming entrance",
  "workshop": "Workshop and maker space, high ceilings, large doors, functional layout",
  "full-village": "Small village or co-housing community, multiple structures, shared courtyard, pathways"
};

function buildPrompt(userPrompt, structure, climate, style) {
  const prefix = "Photorealistic architectural visualization of sustainable construction. Natural building materials: hempcrete walls, rammed earth, cob, adobe, living green roofs, timber frame structure. Permaculture landscaping. The building should look real, lived-in, and beautiful — not futuristic or sci-fi.";
  const parts = [prefix];
  if (structure && STRUCTURE_CONTEXT[structure]) parts.push(STRUCTURE_CONTEXT[structure]);
  if (climate && CLIMATE_CONTEXT[climate]) parts.push(CLIMATE_CONTEXT[climate]);
  if (userPrompt && userPrompt.trim()) parts.push(userPrompt.trim());
  if (style && STYLE_MODIFIERS[style]) parts.push(STYLE_MODIFIERS[style]);
  return parts.join(". ");
}

// Use Node.js https module for maximum compatibility
function replicateRequest(apiKey, body) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(body);
    const options = {
      hostname: 'api.replicate.com',
      path: REPLICATE_API_PATH,
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Prefer': 'wait'
      },
      timeout: 55000
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({ statusCode: res.statusCode, body: data });
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timed out'));
    });

    req.write(postData);
    req.end();
  });
}

function replicatePoll(apiKey, url) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname,
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + apiKey
      },
      timeout: 10000
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Poll timed out')); });
    req.end();
  });
}

exports.handler = async (event) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json"
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers, body: JSON.stringify({ error: "Method not allowed" }) };
  }

  // Check for API key — trim whitespace
  const apiKey = (process.env.REPLICATE_API_TOKEN || '').trim();
  if (!apiKey) {
    return {
      statusCode: 500, headers,
      body: JSON.stringify({ error: "Server config error: missing REPLICATE_API_TOKEN" })
    };
  }

  try {
    const reqBody = JSON.parse(event.body || "{}");
    const { prompt, structure, climate, style } = reqBody;

    if (!prompt || prompt.trim().length < 10) {
      return {
        statusCode: 400, headers,
        body: JSON.stringify({ error: "Please describe your vision in at least a few words." })
      };
    }

    const fullPrompt = buildPrompt(prompt, structure, climate, style || "photorealistic");

    // Call Replicate
    const response = await replicateRequest(apiKey, {
      input: {
        prompt: fullPrompt,
        num_outputs: 1,
        aspect_ratio: "4:3",
        output_format: "webp",
        output_quality: 90
      }
    });

    // Surface the actual error from Replicate
    if (response.statusCode !== 200 && response.statusCode !== 201) {
      console.error("Replicate error:", response.statusCode, response.body);
      let detail = response.body;
      try { detail = JSON.parse(response.body).detail || response.body; } catch(e) {}
      return {
        statusCode: 502, headers,
        body: JSON.stringify({ error: "Replicate " + response.statusCode + ": " + String(detail).substring(0, 300) })
      };
    }

    let prediction;
    try {
      prediction = JSON.parse(response.body);
    } catch(e) {
      return {
        statusCode: 502, headers,
        body: JSON.stringify({ error: "Invalid response from Replicate: " + response.body.substring(0, 200) })
      };
    }

    // With "Prefer: wait", result should be ready
    if (prediction.status === "succeeded" && prediction.output) {
      const imageUrl = Array.isArray(prediction.output) ? prediction.output[0] : prediction.output;
      return {
        statusCode: 200, headers,
        body: JSON.stringify({ image_url: imageUrl })
      };
    }

    // Poll if not yet done
    if (prediction.urls && prediction.urls.get) {
      let result = prediction;
      let attempts = 0;
      while (result.status !== "succeeded" && result.status !== "failed" && attempts < 20) {
        await new Promise(r => setTimeout(r, 1500));
        const pollRes = await replicatePoll(apiKey, result.urls.get);
        try { result = JSON.parse(pollRes.body); } catch(e) { break; }
        attempts++;
      }

      if (result.status === "succeeded" && result.output) {
        const imageUrl = Array.isArray(result.output) ? result.output[0] : result.output;
        return {
          statusCode: 200, headers,
          body: JSON.stringify({ image_url: imageUrl })
        };
      }

      if (result.status === "failed") {
        return {
          statusCode: 502, headers,
          body: JSON.stringify({ error: "Replicate generation failed: " + (result.error || "unknown error") })
        };
      }
    }

    // Catch-all: return whatever we got for debugging
    return {
      statusCode: 504, headers,
      body: JSON.stringify({ error: "Generation timed out. Status: " + prediction.status })
    };

  } catch (err) {
    console.error("Function error:", err);
    return {
      statusCode: 500, headers,
      body: JSON.stringify({ error: "Function error: " + err.message })
    };
  }
};
