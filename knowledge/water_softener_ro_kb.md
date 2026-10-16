---
source_id: KB-WS-RO
title: Stoupons Water Softener & RO Systems Knowledge Base
doc_type: product_knowledge
version: "1.0"
effective_date: 2026-10-15
status: approved
original_file: knowledge/originals/Stoupons_Water_Softener_RO_Internal_Knowledge_Base.pdf
category: water_treatment
---

<!--
Converted from the approved PDF (see original_file). Wording is kept as in the
source. One "## " section = one retrievable chunk. Optional per-section
metadata goes in a "<!- - meta: {...} - ->" line right under the heading.

Sections intentionally NOT included as retrievable text:
  1 Purpose, 20 Knowledge Governance  -> internal; governance is enforced by
                                         ingest.py (only status: approved is indexed)
  16 Structured Product Configuration -> will become the order schema (Agents #2 / #6)
  17 AI / RAG Guardrails              -> agent RULES, built into agents/knowledge/prompts.py
  18 Recommended RAG Metadata         -> used as the per-section metadata below
-->

# Stoupons Water Softener & RO Systems Knowledge Base

## Water softener capacity options (48K, 64K, 96K)
<!-- meta: {product: water_softener, feature: capacity} -->
| Capacity | Configuration | Customer-Friendly Description |
|---|---|---|
| 48,000 grain | One-tank water softener system | Entry capacity option for homes whose usage can be supported by a 48K system. |
| 64,000 grain | One-tank XL system | Higher-capacity one-tank option for households with greater water-softening needs. |
| 96,000 grain | Two-tank water softener system | Highest-capacity option currently documented for Stoupons; suited to larger or higher-usage homes when appropriate. |

Final capacity selection should be based on the customer's household needs, water usage, and installation considerations.

## Water softener technology options (Standard, Bluetooth, Wi-Fi)
<!-- meta: {product: water_softener, feature: technology} -->
Capacity and technology are separate product choices. Stoupons currently documents three technology levels:
1. Standard
2. Bluetooth
3. Wi-Fi

Example configuration: Capacity: 64,000 grains; Technology: Bluetooth.

Stoupons classification (simple customer labels): Standard = Manual, Bluetooth = Semi-automatic, Wi-Fi = Fully automatic.

## Standard water softener (Manual system)
<!-- meta: {product: water_softener, technology: standard} -->
The Standard Water Softener is the basic manual-control option.
- Has approximately 2-inch LED display.
- Two or three physical control buttons.
- Uses default settings with basic manual adjustment.
- No mobile application.
- No remote-access capability.
- Controls are more mechanical and less app-oriented than the Bluetooth and Wi-Fi options.

Recommended use: rental properties, investment properties, or customers who prefer simple controls and do not need smart monitoring.

Stoupons classification: Standard = Manual system.

## Bluetooth water softener (Semi-automatic system) and its mobile app
<!-- meta: {product: water_softener, technology: bluetooth} -->
The Bluetooth Water Softener includes a mobile application. The customer can connect to the system when the phone is within Bluetooth range.

Supported app functions:
- Salt level: view the salt level and reset/update the level after adding salt.
- Water hardness: view and adjust supported hardness settings when the customer feels the water is too hard or too soft.
- Regeneration cycle: view or adjust supported regeneration timing.
- Additional supported system settings may be viewed or updated through the app.

Bluetooth limitation: Bluetooth is range-limited. Once the customer moves outside Bluetooth communication range, the active app connection is lost.

Stoupons classification: Bluetooth = Semi-automatic system.

## Regeneration cycle: how often it runs and changing the time
<!-- meta: {product: water_softener, feature: regeneration} -->
Regeneration is the water-softener cleaning cycle. Based on the product information supplied to Stoupons, it may typically run about every two to three weeks depending on water usage. It commonly runs around 2:00 AM; if the operating noise is inconvenient, the supported time can be adjusted. On the Bluetooth and Wi-Fi systems, supported regeneration timing can be viewed or adjusted through the app.

## Wi-Fi water softener (Fully automatic system)
<!-- meta: {product: water_softener, technology: wifi} -->
The Wi-Fi Water Softener is the most connected and automated option currently documented by Stoupons. It includes an additional hub/connectivity device that connects to the customer's home internet.
- Includes the supported functionality available with the Bluetooth option.
- Can provide supported remote access while the home internet and system connection are available.
- Includes additional leak-detection functionality.
- Designed for greater automation and remote monitoring.

Stoupons classification: Wi-Fi = Fully automatic system.

## Wi-Fi leak detection and automatic water shut-off
<!-- meta: {product: water_softener, technology: wifi, feature: leak_detection} -->
The Wi-Fi package includes leak-detection devices that may be placed near the water softener and the RO system. When a monitored leak is detected, the leak device communicates with the water-softener system so the system can automatically shut off the water without waiting for the homeowner to take manual action.

## Technology comparison: Standard vs Bluetooth vs Wi-Fi
<!-- meta: {product: water_softener, feature: technology} -->
| Feature | Standard | Bluetooth | Wi-Fi |
|---|---|---|---|
| Physical controls | Yes | Yes | Yes |
| Approx. 2-inch LED display | Yes | Yes | Yes |
| Mobile app | No | Yes | Yes |
| View/update supported app settings | No | Yes | Yes |
| Salt-level monitoring | No | Yes | Yes |
| Hardness adjustment through app | No | Yes | Yes |
| Regeneration timing through app | No | Yes | Yes |
| Remote access beyond Bluetooth range | No | No | Yes |
| Leak detection | No | No | Yes |
| Automatic leak response | No | No | Yes |
| Stoupons classification | Manual | Semi-automatic | Fully automatic |

## Reverse osmosis (RO) system options: Tank and Tankless
<!-- meta: {product: reverse_osmosis} -->
Stoupons currently documents two primary RO configurations:
1. Tank RO System
2. Tankless RO System

## Tank RO system
<!-- meta: {product: reverse_osmosis, ro_type: tank} -->
- Typically includes approximately four to five physical filters.
- Stores approximately 3 to 3.5 gallons of filtered water.
- Uses a storage tank, so it requires more under-sink space.
- Filtered water is stored and ready for use.
- Because water is already stored, the initial faucet flow/pressure can be stronger than a tankless system.

## Tankless RO system
<!-- meta: {product: reverse_osmosis, ro_type: tankless} -->
- Uses three long filter cartridges.
- Stoupons internally considers the configuration approximately equivalent to six filtration stages.
- Requires an electrical connection.
- Produces filtered water on demand instead of storing it in a traditional large tank.
- Has a modern, modular design.
- Generally requires less under-sink space than a tank system.
- Because it produces water on demand, its water-flow characteristics can differ from a stored-water tank system.

## Tank vs Tankless RO comparison: which one should I choose?
<!-- meta: {product: reverse_osmosis, feature: ro_comparison} -->
| Feature | Tank RO | Tankless RO |
|---|---|---|
| Water storage | Yes | No traditional large storage tank |
| Approx. stored capacity | 3-3.5 gallons | On-demand production |
| Electricity | Generally not required for basic stored-water delivery | Required |
| Physical filter configuration | Approx. 4-5 filters | 3 long cartridges |
| Stoupons filtration description | Based on installed configuration | Approx. 6 filtration stages |
| Under-sink space | More | Less |
| Design | Traditional | Modern / modular |
| Water delivery | Stored filtered water | Filtered on demand |

Neither option should automatically be described as universally better. The recommendation should consider cabinet space, electrical availability, water-use preferences, and the customer's preferred design.

## Optional alkaline filter for RO systems
<!-- meta: {product: reverse_osmosis, feature: alkaline_filter} -->
An alkaline filter is an optional add-on and can be paired with either a Tank RO or a Tankless RO system.

Approved customer answer: "Alkaline filtration is available as an optional upgrade for both Tank and Tankless RO systems. We can check your selected package to confirm whether it is included or available as an add-on."

AI agents should not make unapproved medical, mineral-content, pH, or health-benefit claims about alkaline filtration.

## RO faucet color options
<!-- meta: {product: reverse_osmosis, feature: faucet_color} -->
Customers can choose one RO faucet finish from the following options: Black, Gold, Steel, Nickel.

The selected finish should be recorded as part of the order, subject to availability.

## Water softener warranty: how long is it?
<!-- meta: {product: water_softener, policy: warranty, warranty_period: 10_years} -->
Stoupons customers receive a lifetime warranty on the water softener system. For Stoupons purposes, the life of the water softener is defined as up to 10 years from the applicable installation date.

Approved customer answer: "Your water softener comes with a lifetime warranty. Stoupons defines the lifetime of the water softener as up to 10 years."

Agents should not promise coverage for a specific part, labor charge, repair, replacement, damage, or exclusion unless that detail is separately documented in an approved warranty policy.

## Water softener warranty: what is covered and what is not covered
<!-- meta: {product: water_softener, policy: warranty, warranty_period: 10_years} -->
As the Water softener stays in garage or outside home, any damages caused by human error such as accidents (breaking something) does not get covered under warranty. Only Electrical and mechanical failures are covered.

WARRANTY: For the LIFETIME of the system, the system will not rust, leak, corrode, burst, or in any other manner fail to perform proper functions. Our Specialists Insures a Lifetime Warranty on all parts involved in the whole home water treatment system. The customer will never purchase any replacement hardware for the Whole Home System. For the LIFETIME of the Media, the MEDIA BED is guaranteed to be free of defects in materials and workmanship to reduce chlorine and chloramine, as well as produce soft water.

## Labor warranty and service calls after installation
<!-- meta: {product: water_softener, policy: warranty} -->
For the first 12 months after installation, Specialist insures a full labor warranty. Service Calls after 12 months will result in a trip charge dependent on the customer's location.

## FAQ: What is the difference between Bluetooth and Wi-Fi?
<!-- meta: {doc_type: faq, product: water_softener, feature: technology} -->
Bluetooth lets you view and adjust supported settings through the app while you are within Bluetooth range. Wi-Fi connects through your home internet, supports remote access, and includes additional leak-detection functionality.

## FAQ: Should I choose Tank or Tankless RO?
<!-- meta: {doc_type: faq, product: reverse_osmosis, feature: ro_comparison} -->
A Tank RO stores approximately 3 to 3.5 gallons of filtered water and uses more under-sink space. A Tankless RO produces water on demand, requires electricity, and has a more compact, modern design.

## FAQ: What faucet colors are available?
<!-- meta: {doc_type: faq, product: reverse_osmosis, feature: faucet_color} -->
Black, Gold, Steel, and Nickel, subject to availability.

## FAQ: How long is the warranty?
<!-- meta: {doc_type: faq, product: water_softener, policy: warranty} -->
The water softener includes a lifetime warranty, which Stoupons defines as up to 10 years.
