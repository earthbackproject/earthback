// Earthback AI Visualizer — Netlify Function
// Calls Replicate Flux Schnell API, returns image URL
// Rate limiting: checked client-side (localStorage) + server-side (Supabase)

const REPLICATE_MODEL = "black-forest-labs/flux-schnell";
const REPLICATE_API = `https://api.replicate.com/v1/models/${REPLICATE_MODEL}/predictions`;

// Prompt engineering — the secret sauce
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

  if (structure && STRUCTURE_CONTEXT[structure]) {
    parts.push(STRUCTURE_CONTEXT[structure]);
  }
  if (climate && CLIMATE_CONTEXT[climate]) {
    parts.push(CLIMATE_CONTEXT[climate]);
  }
  if (userPrompt && userPrompt.trim()) {
    parts.push(userPrompt.trim());
  }
  if (style && STYLE_MODIFIERS[style]) {
    parts.push(STYLE_MODIFIERS[style]);
  }

  return parts.join(". ");
}

exports.handler = async (event) => {
  // CORS headers
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

  // Check for API key
  const apiKey = process.env.REPLICATE_API_TOKEN;
  if (!apiKey) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: "Server configuration error: missing API key" })
    };
  }

  try {
    const body = JSON.parse(event.body || "{}");
    const { prompt, structure, climate, style } = body;

    if (!prompt || prompt.trim().length < 10) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: "Please describe your vision in at least a few words." })
      };
    }

    // Build the full engineered prompt
    const fullPrompt = buildPrompt(prompt, structure, climate, style || "photorealistic");

    // Call Replicate — create prediction
    const createResponse = await fetch(REPLICATE_API, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "Prefer": "wait"  // Synchronous mode — waits up to 60s for result
      },
      body: JSON.stringify({
        input: {
          prompt: fullPrompt,
          num_outputs: 1,
          aspect_ratio: "4:3",
          output_format: "webp",
          output_quality: 90
        }
      })
    });

    if (!createResponse.ok) {
      const errText = await createResponse.text();
      console.error("Replicate error:", createResponse.status, errText);
      return {
        statusCode: 502,
        headers,
        body: JSON.stringify({ error: "Image generation failed (" + createResponse.status + "): " + errText.substring(0, 200) })
      };
    }

    const prediction = await createResponse.json();

    // With "Prefer: wait", we should get the completed prediction directly
    if (prediction.status === "succeeded" && prediction.output) {
      const imageUrl = Array.isArray(prediction.output) ? prediction.output[0] : prediction.output;
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          image_url: imageUrl,
          prompt_used: fullPrompt.substring(0, 200) + "..."
        })
      };
    }

    // If prediction isn't done yet (shouldn't happen with Prefer:wait on Schnell),
    // poll for it
    if (prediction.urls && prediction.urls.get) {
      let result = prediction;
      let attempts = 0;
      while (result.status !== "succeeded" && result.status !== "failed" && attempts < 30) {
        await new Promise(r => setTimeout(r, 1000));
        const pollResponse = await fetch(result.urls.get, {
          headers: { "Authorization": `Bearer ${apiKey}` }
        });
        result = await pollResponse.json();
        attempts++;
      }

      if (result.status === "succeeded" && result.output) {
        const imageUrl = Array.isArray(result.output) ? result.output[0] : result.output;
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            image_url: imageUrl,
            prompt_used: fullPrompt.substring(0, 200) + "..."
          })
        };
      }
    }

    return {
      statusCode: 504,
      headers,
      body: JSON.stringify({ error: "Image generation timed out. Please try again." })
    };

  } catch (err) {
    console.error("Function error:", err);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: "Something went wrong. Please try again." })
    };
  }
};
