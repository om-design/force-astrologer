# Force Astrologer MCP API

This document describes the API endpoints (tools) provided by the Force Astrologer MCP server.

All endpoints accept and return JSON.  
**Note:** This service is for novelty and entertainment purposes only.

---

## Endpoints / Tools

### 1. `generate_chart`

**Description:**  
Generate a Force astrology chart based on birth data.

**POST** `/generate_chart`

**Input:**
```json
{
  "name": "Optional, user's name",
  "birth_date": "YYYY-MM-DD",
  "birth_time": "HH:MM",           // Optional
  "birth_location": "City, Country" // Optional
}
```
Output:
```
{
  "sign": "The Seeker",
  "planets": {
    "Twin Moons": "The Guardian",
    "Red Star": "The Trickster"
  },
  "houses": {
    "First House": "The Path",
    "Second House": "The Forge"
  },
  "lore": "You are guided by the Seeker's curiosity and the Guardian's wisdom..."
}
```
2. get_horoscope
Description:
Retrieve a daily, weekly, or monthly horoscope for a Force sign.

POST /get_horoscope

Input:
```
{
  "sign": "The Seeker",
  "period": "daily" // or "weekly", "monthly"
}
```
Output:
```
{
  "horoscope": "Today, the Force flows with opportunity. Trust your instincts and seek new horizons..."
}
```
3. compatibility
Description:
Analyze compatibility between two Force signs.

POST /compatibility

Input:
```
{
  "sign1": "The Seeker",
  "sign2": "The Guardian"
}
```
Output:
```
{
  "score": 82,
  "narrative": "The Seeker and the Guardian form a dynamic duo, balancing curiosity with wisdom..."
}
```
4. explain_sign
Description:
Get the lore and archetype for a Force sign.

POST /explain_sign

Input:
```{
  "sign": "The Seeker"
}
```
Output:
```
{
  "lore": "The Seeker is ever-curious, drawn to the mysteries of the cosmos and the call of adventure..."
}
```
5. explain_planet
Description:
Get the lore and energetic meaning for a Force planet.

POST /explain_planet

Input:
```
{
  "planet": "Twin Moons"
}
```
Output:
```
{
  "lore": "The Twin Moons represent duality, intuition, and the balance of light and shadow..."
}
```
---
General Notes
All endpoints return JSON.
All lore, signs, and planets are original or parodic, for entertainment only.
For error handling, responses will include an error field if input is invalid.

Example Usage

Generate a chart:
```
curl -X POST http://localhost:8000/generate_chart \
  -H "Content-Type: application/json" \
  -d '{"name":"Rey","birth_date":"1999-05-04"}'
```
For more details or integration help, see the main README.md or contact the maintainer.
