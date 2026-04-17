"""Replace CONFIG.bpc + bpcMapping + productSystemMap with full catalog."""
import re, json, sys, os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('bpc/full-inline.json', 'r', encoding='utf-8') as f:
    full_bpc = f.read().strip()

# 1. Replace CONFIG.bpc = [...];
pattern = r'CONFIG\.bpc = \[.*?\];'
match = re.search(pattern, html, re.DOTALL)
if not match:
    print("ERROR: CONFIG.bpc not found"); sys.exit(1)
old_bpc = match.group(0)
print(f"Found CONFIG.bpc ({len(old_bpc)} chars)")
html = html[:match.start()] + f'CONFIG.bpc = {full_bpc};' + html[match.end():]
print(f"Replaced with full catalog ({len(full_bpc)} chars)")

# 2. Add missing products to productSystemMap
old_map = '"Other": null\n};'
new_map = ('"Customer Insights Data": "d365ce",\n'
           '  "Customer Insights Journey": "d365ce",\n'
           '  "Customer Voice": "d365ce",\n'
           '  "Azure": "azure",\n'
           '  "Other": null\n};')
if old_map in html:
    html = html.replace(old_map, new_map)
    print("Updated productSystemMap")
else:
    print("WARN: productSystemMap pattern not found")

# 3. Replace CONFIG.bpcMapping
old_start = 'CONFIG.bpcMapping = {'
idx = html.index(old_start)
# Find the closing }; for the mapping
# Need to find the matching close brace
depth = 0
i = idx + len(old_start) - 1  # point to {
end_idx = -1
for j in range(i, len(html)):
    if html[j] == '{':
        depth += 1
    elif html[j] == '}':
        depth -= 1
        if depth == 0:
            # find the ; after
            end_idx = j + 1
            if end_idx < len(html) and html[end_idx] == ';':
                end_idx += 1
            break

if end_idx == -1:
    print("ERROR: Could not find end of bpcMapping"); sys.exit(1)

new_mapping = '''CONFIG.bpcMapping = {
  // Acquire to Dispose (10)
  "10.05": ["fa"],                          // Define asset strategy
  "10.20": ["fa", "proc"],                  // Acquire assets
  "10.40": ["fa"],                          // Manage active assets
  "10.50": ["fa"],                          // Perform asset maintenance
  "10.60": ["fa"],                          // Dispose of assets
  "10.70": ["fa"],                          // Analyze assets
  // Case to Resolution (20)
  "20.10": ["modelapp", "dv"],              // Establish knowledge base
  "20.20": ["modelapp", "dv"],              // Define service operations
  "20.30": ["modelapp", "dv"],              // Intake cases
  "20.40": ["modelapp", "dv"],              // Manage and work on cases
  "20.60": ["modelapp", "dv", "pbirep"],    // Analyze case performance
  // Concept to Market (30)
  "30.05": ["modelapp"],                    // Develop marketing strategy
  "30.15": ["modelapp"],                    // Research and develop offerings
  "30.25": ["modelapp"],                    // Manage service offerings
  "30.35": ["modelapp"],                    // Prepare marketing campaigns
  "30.45": ["modelapp"],                    // Manage marketing campaigns
  "30.55": ["modelapp", "pbirep"],          // Analyze marketing operations
  // Design to Retire (40)
  "40.10": ["inv"],                         // Develop product strategy
  "40.20": ["inv"],                         // Introduce products
  "40.50": ["inv"],                         // Manage active products
  "40.60": ["inv"],                         // Retire products
  "40.90": ["inv", "pbirep"],              // Analyze product performance
  // Forecast to Plan (50)
  "50.15": ["mrp"],                         // Develop business strategy
  "50.20": ["budget", "gl"],                // Conduct financial planning
  "50.25": ["mrp", "sales"],                // Conduct sales and ops planning
  "50.35": ["mrp", "prod"],                 // Execute sales and operations
  "50.65": ["gl", "pbirep"],                // Analyze business performance
  // Hire to Retire (55)
  "55.05": ["hr"],                          // Develop people strategy
  "55.10": ["hr"],                          // Recruit and onboard
  "55.30": ["hr"],                          // Workplace compliance
  "55.40": ["hr"],                          // Performance and growth
  "55.50": ["hr"],                          // Time and attendance
  "55.70": ["hr"],                          // Compensation and benefits
  "55.80": ["hr"],                          // Offboard
  "55.90": ["hr"],                          // Analyze HR
  // Inventory to Deliver (60)
  "60.10": ["wms"],                         // Manage warehouse operations
  "60.20": ["inv"],                         // Maintain inventory levels
  "60.30": ["inv", "wms"],                  // Process inbound goods
  "60.40": ["wms", "inv"],                  // Process outbound goods
  "60.50": ["qual", "inv"],                 // Manage inventory quality
  "60.60": ["transp"],                      // Manage freight
  "60.80": ["wms", "inv"],                  // Analyze warehouse
  // Order to Cash (65)
  "65.05": ["sales", "pricing"],            // Develop sales policies
  "65.20": ["sales", "pricing", "inv", "wms"], // Manage sales orders
  "65.30": ["ar", "gl"],                    // Manage accounts receivable
  "65.50": ["ar"],                          // Manage credit and collections
  "65.60": ["ar", "gl"],                    // Analyze sales performance
  // Plan to Produce (70)
  "70.10": ["prod"],                        // Develop production strategies
  "70.20": ["mrp", "prod"],                 // Plan production
  "70.30": ["prod"],                        // Run production
  "70.60": ["qual", "prod"],                // Control production quality
  "70.70": ["prod"],                        // Analyze production
  // Source to Pay (75)
  "75.10": ["proc"],                        // Develop procurement strategy
  "75.30": ["proc"],                        // Manage supplier relationships
  "75.35": ["proc"],                        // Source and contract goods
  "75.40": ["proc", "inv", "wms"],          // Procure goods and services
  "75.50": ["ap", "gl"],                    // Manage accounts payable
  "75.80": ["proc"],                        // Analyze procurement
  // Project to Profit (80)
  "80.10": ["projops"],                     // Develop project strategy
  "80.20": ["projops"],                     // Manage project contracts
  "80.30": ["projops"],                     // Plan projects
  "80.40": ["projops"],                     // Manage project delivery
  "80.50": ["projops", "gl"],               // Manage project financials
  "80.60": ["projops"],                     // Analyze project performance
  // Prospect to Quote (85)
  "85.15": ["modelapp", "dv"],              // Manage customer relationships
  "85.25": ["modelapp", "dv"],              // Identify and qualify leads
  "85.35": ["sales", "pricing"],            // Define sales strategy
  "85.45": ["modelapp", "dv"],              // Pursue opportunities
  "85.55": ["sales", "pricing"],            // Estimate and quote sales
  "85.65": ["sales", "pbirep"],             // Analyze sales
  // Record to Report (90)
  "90.10": ["gl", "fa", "budget", "tax"],   // Define accounting policies
  "90.25": ["gl"],                          // Manage cash
  "90.30": ["budget", "gl"],                // Manage budgets
  "90.50": ["gl", "tax"],                   // Record financial transactions
  "90.60": ["gl"],                          // Close financial periods
  "90.70": ["gl"],                          // Analyze financial performance
  // Service to Deliver (95)
  "95.05": ["modelapp", "dv"],              // Develop service strategy
  "95.15": ["modelapp", "dv"],              // Plan service work
  "95.25": ["modelapp", "dv"],              // Manage service work
  "95.35": ["modelapp", "dv"],              // Deliver services
  "95.45": ["modelapp", "pbirep"],          // Analyze service performance
  // Administer to Operate (99)
  "99.01": ["lcs", "devops"],               // Implement solutions
  "99.10": ["backup"],                      // Define business continuity
  "99.15": ["lcs"],                         // Manage licensing
  "99.20": ["featmgmt"],                    // Administer system features
  "99.25": ["security", "entra"],           // Manage access and security
  "99.30": ["lcs"],                         // Train users
  "99.35": ["monitor"],                     // Monitor systems
  "99.40": ["dmf"],                         // Manage background jobs
  "99.45": ["pacloud"],                     // Manage notifications
  "99.50": ["lcs"],                         // Uptake software releases
  "99.55": ["dmf", "dv"],                   // Manage data
  "99.60": ["purview", "defender"],          // Manage compliance
  "99.65": ["lcs", "monitor"]               // Support systems
};'''

html = html[:idx] + new_mapping + html[end_idx:]
print(f"Replaced bpcMapping (94 L2 areas)")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done. File: {len(html)} chars")
