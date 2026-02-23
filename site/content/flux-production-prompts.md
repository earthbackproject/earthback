# Earthback — Flux Production Prompts
*Approved for platform use · v1.0 · Feb 2026*
*For LoRA training dataset generation and profile photo reproduction*

---

## ComfyUI Settings (all characters)

| Setting | Value |
|---------|-------|
| Model | flux1-dev-fp8.safetensors |
| Steps | 25 |
| CFG | 1.0 |
| Sampler | euler |
| Scheduler | simple |
| Resolution | 896 × 1152 |
| Denoise | 1.0 |
| Negative prompt | none (Flux ignores negative prompts) |

**T5 encoder note:** Use `t5xxl_fp16.safetensors` if VRAM allows (offloads to system RAM automatically). Better prompt adherence than the quantized version, especially for complex scene descriptions.

**Multi-GPU note:** Run two ComfyUI instances simultaneously with `--cuda-device 0` and `--cuda-device 1` to generate two characters in parallel.

---

## Style anchor (prepend to all character prompts)

```
Documentary portrait photograph, 35mm film, real person.
```

This does most of the work that a negative prompt would do in SD/SDXL. Always lead with it.

---

---

## ✅ APPROVED — James Osei · @james.osei

**Status:** Platform-ready · Approved Feb 2026
**Character:** Earthback trainer, 34, Ghanaian, Accra region

### Profile photo prompt
```
Documentary portrait photograph, 35mm film, real person. A 34-year-old Ghanaian man, mid-thirties, lean athletic build, warm intelligent eyes, calm confident expression with a slight smile, slight stubble. Standing in front of an open shipping container converted into a workshop, Accra region Ghana. Interior of container visible behind him showing hanging tools, shelving, material samples, warm interior light. Bright West African midday sun, slight haze, red laterite earth ground. Dark work t-shirt, cargo pants, practical clothing. Shallow depth of field, natural light only, photojournalism style.
```

### LoRA training notes
- Trigger word: `JAMES_OSEI_EB`
- Target dataset: 15–20 images
- Vary: lighting (midday harsh, golden hour, overcast, interior workshop), framing (head-and-shoulders, half-body, three-quarter), expression (smiling, focused, teaching, listening)
- Keep consistent: lean build, Ghanaian features, short cropped hair, slight stubble, dark skin tone, practical work clothing
- Key props to include in training images: shipping container, red laterite earth, tools, hempcrete materials, groups of trainees

---

---

## ✅ APPROVED — Lena Hartmann · @lena.hartmann

**Status:** Platform-ready · Approved Feb 2026
**Character:** German expat builder (found Earthback via game), 31, Tafraoute Morocco

### Profile photo prompt
```
Documentary portrait photograph, 35mm film, real person. A 31-year-old German woman, practical reddish-brown hair tied back loosely, hands and forearms with dried clay and earth on them, expression of genuine delight and surprise. Leaning against a hand-built cob wall that fills the right side of the frame — irregular surface, visible straw fiber in the earth, ochre brown color, clearly handmade. Tafraoute Morocco, Anti-Atlas pink granite mountains in background, dry blue sky, arid landscape. Worn grey t-shirt, no jewelry, practical field clothing, slightly disheveled. Late afternoon golden hour light, warm and directional. Photojournalism style, shallow depth of field, natural light only.
```

### LoRA training notes
- Trigger word: `LENA_HARTMANN_EB`
- Target dataset: 15–20 images
- Vary: activity (building, mixing cob, foot-mixing, resting, examining wall), lighting (golden hour, harsh midday, overcast), framing (working shots, portrait, full body)
- Keep consistent: reddish-brown hair, blue-grey eyes, mid-thirties European features, practical worn clothing, earth/clay on hands
- Key props: cob wall, Anti-Atlas mountains, Moroccan landscape, mixing materials, hand tools

---

---

## PENDING — Remaining 10 Characters

*Use prompts below. Run and approve before LoRA training.*

---

### Tom Westhall · @tom.westhall
*Hemp farmer, 47, Willamette Valley Oregon*
Trigger word: `TOM_WESTHALL_EB`

```
Documentary portrait photograph, 35mm film, real person. A 47-year-old white American man, weathered face, salt-and-pepper stubble, strong calloused hands. Standing in a hemp field in late summer, Willamette Valley Oregon. Tall hemp stalks 3 to 4 meters high slightly blurred behind him. Overcast Pacific Northwest light, soft and diffuse. Worn canvas jacket, flannel shirt underneath. Calm direct expression, not performing for the camera, just present. Shallow depth of field, photojournalism style, Fujifilm grain, warm earth tones.
```

---

### Rosa Mendez · @rosa.mendez
*Architect, 38, Costa Rica, Osa Peninsula*
Trigger word: `ROSA_MENDEZ_EB`

```
Documentary portrait photograph, 35mm film, real person. A 38-year-old Costa Rican woman, dark hair pulled back, observant precise expression with warmth. Standing in partial shade of a bamboo structure under construction, Osa Peninsula Costa Rica. Tropical humid light, dappled. Practical clothing, measuring tape clipped to belt. Behind her a bamboo frame in process, dense green tropical forest visible through the structure gaps. Slight humidity haze. Photojournalism style, natural light, medium shot.
```

---

### Mei Lin · @mei.lin
*Community developer, 29, Mindanao Philippines*
Trigger word: `MEI_LIN_EB`

```
Documentary portrait photograph, 35mm film, real person. A 29-year-old Filipino woman, short practical dark hair, thoughtful expression, standing at a community meeting in rural Mindanao Philippines. A large hand-drawn land map on paper behind her. Natural light, interior exterior mix. Simple practical clothing. The kind of person running the meeting not giving a speech. Medium shot, photojournalism style, warm tropical light.
```

---

### Elena Vasquez · @elena.vasquez
*Tribal housing coordinator, 52, Pueblo of Acoma New Mexico*
Trigger word: `ELENA_VASQUEZ_EB`

```
Documentary portrait photograph, 35mm film, real person. A 52-year-old Native American woman, Pueblo descent, strong face, deep eyes with twenty years of experience behind them. Standing outside at Pueblo of Acoma New Mexico, mesa landscape, adobe structures, high desert background. Simple practical work clothing. Direct gaze, patient authoritative presence. Late afternoon golden hour, New Mexico deep blue sky with clouds. Documentary portrait, natural light only.
```

---

### Amara Diallo · @amara.diallo
*Master builder, 41, Thiès Senegal*
Trigger word: `AMARA_DIALLO_EB`

```
Documentary portrait photograph, 35mm film, real person. A 41-year-old West African man, Senegalese, master builder, strong capable hands, expression of calm mastery. Standing in front of a completed rammed earth structure in Thiès Senegal. Bright West African afternoon light, slight dust in the air. Practical work clothing. The rammed earth structure behind him is clearly his work — he knows every layer of it. Medium shot, documentary photography, warm earth tones, real dust and light.
```

---

### Marcus Webb · @marcus.webb
*Retired civil engineer, 61, Eastern Kentucky*
Trigger word: `MARCUS_WEBB_EB`

```
Documentary portrait photograph, 35mm film, real person. A 61-year-old white American man, retired civil engineer, solidly built, reading glasses pushed up on forehead, gray hair, skeptic's eyes that have become a believer's eyes. Standing beside a hempcrete wall he built himself, Eastern Kentucky farmland behind him. Morning light, overcast. Flannel shirt, work boots. The wall is clearly handmade — good but not perfect. Documentary photography, quiet earned pride without posing.
```

---

### Kenji Nakamura · @kenji.nakamura
*Mycelium researcher, 35, Japanese, Delft Netherlands*
Trigger word: `KENJI_NAKAMURA_EB`

```
Documentary portrait photograph, 35mm film, real person. A 35-year-old Japanese man, researcher, precise and slightly reserved, small genuine smile. Holding a mycelium composite panel sample — off-white slightly textured organic material. Standing in a clean workshop or materials lab, Delft Netherlands. Northern European window light, soft and diffuse. Lab coat or practical work clothes. Curious careful expression. Documentary photography, natural light.
```

---

### Priya Sharma · @priya.sharma
*Solar integration specialist, 44, Queensland Australia*
Trigger word: `PRIYA_SHARMA_EB`

```
Documentary portrait photograph, 35mm film, real person. A 44-year-old Australian woman of South Indian descent, practical and direct expression, standing on a standing seam metal roof in Queensland Australia. Solar panels clip-mounted behind her, no penetrations visible. Intense bright Australian sun, harsh and clear. Work clothing, completely at ease at height. Medium shot, photojournalism style, deep Queensland blue sky.
```

---

### Dara Okonkwo · @dara.okonkwo
*Community land trust organizer, 33, Detroit Michigan*
Trigger word: `DARA_OKONKWO_EB`

```
Documentary portrait photograph, 35mm film, real person. A 33-year-old Black American woman, community organizer, sharp and warm expression. Standing on a vacant lot in Detroit mid-transformation — straw bale wall frames visible behind her, foundation poured nearby. Detroit urban landscape: brick buildings, empty lots, overcast Midwest sky. Practical clothing. Direct purposeful expression. Documentary photography, urban, real, photojournalism style.
```

---

### Sam Torres · @sam.torres
*3D printer technician, 26, Phoenix Arizona*
Trigger word: `SAM_TORRES_EB`

```
Documentary portrait photograph, 35mm film, real person. A 26-year-old Latino-American man, young, technically sharp, genuine enthusiasm. Crouching beside the extrusion head of a large 3D construction printer in a desert workshop, Phoenix Arizona. The printer is mid-print, hempcrete being extruded in visible layers. Harsh Arizona sunlight through workshop opening. Work clothes with dried hempcrete on them. Excited but professional expression. Documentary photography style, real equipment.
```

---

---

## LoRA Training Pipeline

### When to train
Train after all 12 character profile photos are approved. Priority order:
1. James Osei — most active in platform narrative, key game NPC
2. Lena Hartmann — bridge character, game + real world crossover
3. Amara Diallo — high craft post frequency, distinctive setting
4. Tom Westhall, Rosa Mendez — next most active feed presence

### Dataset per character
- 15–20 images total
- Mix: 5–6 portrait/profile, 5–6 working/action, 3–4 environmental/context
- All generated with character's approved prompt as base, varied by:
  - Time of day / lighting
  - Framing (close, medium, full body)
  - Activity (working, teaching, resting, examining)
  - Expression (focused, pleased, explaining, listening)

### Caption format
```
TRIGGER_WORD_EB, [age] [ethnicity] [gender], [activity], [location], documentary photography, 35mm
```
Example: `JAMES_OSEI_EB, 34 year old Ghanaian man, teaching hempcrete mixing to trainees, Accra Ghana, documentary photography, 35mm`

### Training settings (Kohya / flux-train)
- Network: LoRA rank 16, alpha 8
- Learning rate: 1e-4 (unet), 5e-5 (text encoder — skip T5, train CLIP-L only)
- Steps: ~1500–2000 per character
- Batch size: 1 (12GB VRAM)
- Resolution: 896×1152 to match generation target

### Output naming
Save as: `earthback_[name]_v1.safetensors`
Example: `earthback_james_osei_v1.safetensors`

---

## Platform image specs

| Use | Size | Format |
|-----|------|--------|
| Profile photo (circular crop) | 400 × 400px | PNG |
| Feed post avatar | 48 × 48px | PNG |
| Social media card | 1200 × 630px | PNG/JPG |
| In-game character reference | 512 × 768px | PNG |

---

*Next: generate and approve remaining 10 characters, then begin LoRA training datasets*
