import httpx
from mcp.server.fastmcp import FastMCP
import urllib.parse
from typing import Dict, Any, List

# Initialize FastMCP Server
mcp = FastMCP("OpenStreetMap")

USER_AGENT = "ErrandsOptimizer/1.0"

@mcp.tool()
async def search_places(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search for places using OpenStreetMap Nominatim API (Free Geocoding).
    
    Args:
        query: The name or address of the place (e.g., 'dry cleaner near me')
        limit: Maximum number of results to return
    """
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit={limit}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data:
                results.append({
                    "name": item.get("display_name"),
                    "lat": float(item.get("lat")),
                    "lon": float(item.get("lon")),
                    "osm_id": item.get("osm_id"),
                    "type": item.get("type")
                })
            return results
        except httpx.HTTPError as e:
            return [{"error": f"Failed to search places: {str(e)}"}]

@mcp.tool()
async def calculate_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
    """
    Calculate the driving route between two points using OSRM (Open Source Routing Machine).
    
    Args:
        start_lat: Starting latitude
        start_lon: Starting longitude
        end_lat: Destination latitude
        end_lon: Destination longitude
    """
    # OSRM expects coordinates in lon,lat order
    coordinates = f"{start_lon},{start_lat};{end_lon},{end_lat}"
    url = f"https://router.project-osrm.org/route/v1/driving/{coordinates}?overview=false"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
                route = data["routes"][0]
                return {
                    "distance_meters": route.get("distance"),
                    "duration_seconds": route.get("duration"),
                    "distance_text": f"{route.get('distance') / 1000:.2f} km",
                    "duration_text": f"{route.get('duration') / 60:.1f} mins"
                }
            return {"error": "No route found"}
        except httpx.HTTPError as e:
            return {"error": f"Failed to calculate route: {str(e)}"}

@mcp.tool()
async def get_place_details(osm_id: int) -> Dict[str, Any]:
    """
    Fetch operating hours for a specific place using Overpass API (OSM).
    NOTE: Operating hours are not always available in OSM. The agent should mock or assume
    standard business hours if 'opening_hours' is not returned.
    
    Args:
        osm_id: The OpenStreetMap ID of the place
    """
    query = f"""
    [out:json];
    node({osm_id});
    out tags;
    """
    url = "https://overpass-api.de/api/interpreter"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data={"data": query})
            response.raise_for_status()
            data = response.json()
            
            if "elements" in data and len(data["elements"]) > 0:
                tags = data["elements"][0].get("tags", {})
                return {
                    "name": tags.get("name", "Unknown"),
                    "opening_hours": tags.get("opening_hours", "Not specified in OSM"),
                    "phone": tags.get("phone", "Not specified"),
                    "website": tags.get("website", "Not specified")
                }
            return {"error": "Place details not found"}
        except httpx.HTTPError as e:
            return {"error": f"Failed to fetch place details: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
