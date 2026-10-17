from fastmcp import FastMCP
from fastmcp.exceptions import McpError,ToolError,ValidationError
from recipes import Recipes



mcp=FastMCP("Roxy Recipe With MCP")
mcp_app=mcp.http_app(path="/")

recipe=Recipes()

mcp.tool(recipe.get_random_recipe,description="Gets a random recipe")
mcp.tool(recipe.get_recipe_by_id,description="Given a recipe ID it return the ID-specific recipe")
mcp.tool(recipe.get_ingredients,description="Retrieves a list of ingredients")
mcp.tool(recipe.get_recipe_by_ingredients,description="Fetch a recipe by at least 1 of the ingredients passed")
mcp.tool(recipe.get_recipes,description="Gets a list of recipes")


