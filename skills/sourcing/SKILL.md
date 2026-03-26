---
name: "sourcing"
description: "Global B2B product and supplier sourcing from Alibaba, AliExpress, and other wholesale platforms."
version: "1.0.0"
tools:
  - name: "find_products_and_suppliers"
    description: "Search for high-quality products and verified suppliers based on user requirements."
    parameters:
      type: "object"
      properties:
        query:
          type: "string"
          description: "Detailed description of the product or category to search for."
        intent_type:
          type: "string"
          enum: ["product", "supplier"]
          description: "Whether the focus is on specific products or finding manufacturers/factories."
        moq:
          type: "integer"
          description: "Minimum Order Quantity requirement."
        price_range:
          type: "string"
          description: "Target price range (e.g., '$5-$15')."
      required: ["query", "intent_type"]
---

# Sourcing Skill Logic
The agent uses the provided `query` and `intent_type` to search the B2B ecosystem.
It prioritizes verified suppliers and matches the results against the specified `moq` and `price_range`.

1. **Analysis**: Break down the query into key attributes (material, size, certifications).
2. **Search**: Execute the B2B search engine.
3. **Filtering**: Refine the results based on business constraints.
4. **Ranking**: Order by relevance and supplier reliability.
5. **Output**: Present a curated shortlist with product IDs, names, prices, and MOQs.
