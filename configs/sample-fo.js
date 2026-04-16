// Sample D365 F&O CONFIG — copy into index.html between CONFIGURATION markers
const CONFIG = {
  meta: {
    title: "Project End-state Roadmap",
    subtitle: "Application Architecture \u2014 Target State",
    badge: "SOLUTION BLUEPRINT",
    version: "2.0",
    date: "April 2026",
    viewpoint: "Application Architecture"
  },

  systems: {
    d365fo:   { name: "Dynamics 365 F&O",   color: "var(--sys-d365fo)",   hoverColor: "var(--sys-d365fo-hover)" },
    d365ce:   { name: "Dynamics 365 CE",     color: "var(--sys-d365ce)",   hoverColor: "var(--sys-d365ce-hover)" },
    power:    { name: "Power Platform",      color: "var(--sys-power)",    hoverColor: "var(--sys-power-hover)" },
    azure:    { name: "Azure Services",      color: "var(--sys-azure)",    hoverColor: "var(--sys-azure-hover)" },
    fabric:   { name: "Microsoft Fabric",    color: "var(--sys-fabric)",   hoverColor: "var(--sys-fabric-hover)" },
    external: { name: "External System",     color: "var(--sys-external)", hoverColor: "var(--sys-external-hover)" },
    custom:   { name: "Custom Development",  color: "var(--sys-custom)",   hoverColor: "var(--sys-custom-hover)" },
    infra:    { name: "Infrastructure",      color: "var(--sys-infra)",    hoverColor: "var(--sys-infra-hover)" },
    config:   { name: "Configuration",       color: "var(--sys-config)",   hoverColor: "var(--sys-config-hover)" },
    isv:      { name: "ISV Solution",        color: "var(--sys-isv)",      hoverColor: "var(--sys-isv-hover)" },
    pingala:  { name: "Pingala Accelerator", color: "var(--sys-pingala)",  hoverColor: "var(--sys-pingala-hover)" }
  },

  layers: [
    {
      id: "d365modules",
      name: "D365 Functional Modules",
      subtitle: "Finance & Operations application modules in scope",
      bg: "var(--layer-bg-1)",
      accent: "var(--sys-d365fo)",
      groups: [
        {
          name: "Finance",
          components: [
            { id: "gl",      name: "General Ledger",   system: "d365fo", status: "in-scope", desc: "Chart of accounts, journals, allocations, financial dimensions, consolidation" },
            { id: "ap",      name: "Accounts Payable",  system: "d365fo", status: "in-scope", desc: "Vendor invoices, payment proposals, settlements, aging, 3-way matching" },
            { id: "ar",      name: "Accounts Recv.",    system: "d365fo", status: "in-scope", desc: "Customer invoicing, collections, credit management, payment journals" },
            { id: "fa",      name: "Fixed Assets",      system: "d365fo", status: "in-scope", desc: "Asset lifecycle, depreciation books, revaluation, disposal" },
            { id: "budget",  name: "Budgeting",         system: "d365fo", status: "in-scope", desc: "Budget planning, budget control, forecast positions, allocation rules" },
            { id: "tax",     name: "Tax Engine",        system: "isv",    status: "isv",      desc: "Vertex or Avalara tax calculation, compliance reporting, e-invoicing" }
          ]
        },
        {
          name: "Supply Chain",
          components: [
            { id: "proc",    name: "Procurement",       system: "d365fo", status: "in-scope", desc: "Purchase requisitions, RFQs, purchase orders, vendor collaboration" },
            { id: "sales",   name: "Sales Orders",      system: "d365fo", status: "in-scope", desc: "Quotations, order entry, allocation, picking, packing, invoicing" },
            { id: "pricing", name: "Pricing Engine",    system: "d365fo", status: "in-scope", desc: "Trade agreements, price groups, discounts, rebates" },
            { id: "inv",     name: "Inventory Mgmt",    system: "d365fo", status: "in-scope", desc: "On-hand management, reservations, quality management, batch/serial tracking" },
            { id: "wms",     name: "WMS Advanced",      system: "d365fo", status: "in-scope", desc: "Wave processing, work creation, mobile device flows, location directives" },
            { id: "transp",  name: "Transport Mgmt",    system: "d365fo", status: "future",   desc: "Load planning, rate routing, freight reconciliation" }
          ]
        },
        {
          name: "Manufacturing",
          components: [
            { id: "prod",    name: "Production",        system: "d365fo", status: "in-scope", desc: "Production orders, BOMs, routes, shop floor execution" },
            { id: "mrp",     name: "Master Planning",   system: "d365fo", status: "in-scope", desc: "MRP runs, planned orders, demand forecasting, safety stock" },
            { id: "qual",    name: "Quality Mgmt",      system: "d365fo", status: "future",   desc: "Quality orders, test groups, non-conformance, quarantine" }
          ]
        },
        {
          name: "Project & HR",
          components: [
            { id: "projops", name: "Project Ops",       system: "d365fo", status: "in-scope", desc: "Project contracts, WBS, timesheets, expense management" },
            { id: "hr",      name: "Human Resources",   system: "d365fo", status: "out-scope", desc: "Worker management, benefits, leave, compensation" }
          ]
        }
      ]
    },
    {
      id: "d365toolbox",
      name: "D365 Configuration & Toolbox",
      subtitle: "Platform capabilities, data management, extensibility",
      bg: "var(--layer-bg-2)",
      accent: "var(--sys-config)",
      groups: [
        {
          name: "Data Management",
          components: [
            { id: "dmf",    name: "Data Entities",   system: "d365fo", status: "in-scope", desc: "DMF framework, composite entities, recurring integrations, staging" },
            { id: "odata",  name: "OData / REST",    system: "d365fo", status: "in-scope", desc: "RESTful endpoints, batch operations, change tracking" },
            { id: "dualwr", name: "Dual-write",      system: "d365fo", status: "in-scope", desc: "Near real-time sync between F&O and Dataverse" },
            { id: "cdc",    name: "Change Tracking",  system: "d365fo", status: "in-scope", desc: "Incremental sync via SQL change tracking on data entities" }
          ]
        },
        {
          name: "Platform Config",
          components: [
            { id: "featmgmt",name: "Feature Mgmt",   system: "config", status: "in-scope", desc: "Feature flighting, preview features, one version policy" },
            { id: "legal",  name: "Legal Entities",  system: "config", status: "in-scope", desc: "Multi-company setup, shared data policies, number sequences" },
            { id: "security",name: "Security Roles",  system: "config", status: "in-scope", desc: "Duties, privileges, role-based access, SoD analysis" },
            { id: "wf",     name: "Workflow",        system: "config", status: "in-scope", desc: "Approval workflows, conditional routing, escalation" }
          ]
        },
        {
          name: "Dev & Extensibility",
          wide: true,
          components: [
            { id: "ext",    name: "Extensions / X++", system: "d365fo", status: "in-scope", desc: "CoC, augmentation, event handlers \u2014 no overlayering" },
            { id: "lcs",    name: "LCS / Admin",     system: "d365fo", status: "in-scope", desc: "Lifecycle Services, environment mgmt, telemetry, updates" },
            { id: "er",     name: "Electronic Rep.",  system: "d365fo", status: "in-scope", desc: "ER format designer, configurable reporting, regulatory updates" }
          ]
        }
      ]
    },
    {
      id: "power",
      name: "Power Platform & Custom Apps",
      subtitle: "Low-code extensions, process automation, citizen dev",
      bg: "var(--layer-bg-3)",
      accent: "var(--sys-power)",
      groups: [
        {
          name: "Power Apps",
          components: [
            { id: "modelapp",name: "Model-driven",   system: "power", status: "in-scope", desc: "Dataverse-backed apps for structured data, forms, views" },
            { id: "canvas", name: "Canvas Apps",     system: "power", status: "in-scope", desc: "Pixel-perfect mobile/tablet apps, connectors, offline" },
            { id: "portal", name: "Power Pages",     system: "power", status: "future",   desc: "External-facing portals, authentication, web forms" }
          ]
        },
        {
          name: "Automation",
          components: [
            { id: "pacloud",name: "Cloud Flows",     system: "power", status: "in-scope", desc: "Event-driven automation, approval flows, 1000+ connectors" },
            { id: "padesk", name: "Desktop Flows",   system: "power", status: "future",   desc: "RPA for legacy systems, UI automation, attended/unattended" },
            { id: "copilot",name: "Copilot Studio",  system: "power", status: "future",   desc: "AI chatbots, conversational actions, GPT plugins" }
          ]
        },
        {
          name: "Dataverse",
          components: [
            { id: "dv",     name: "Dataverse",       system: "power", status: "in-scope", desc: "Common data model, business logic, security, audit" },
            { id: "dvvirt", name: "Virtual Tables",  system: "power", status: "in-scope", desc: "Real-time view of F&O data in Dataverse without replication" }
          ]
        }
      ]
    },
    {
      id: "integration",
      name: "Integration Layer",
      subtitle: "Azure integration services, middleware, API management",
      bg: "var(--layer-bg-4)",
      accent: "var(--sys-azure)",
      groups: [
        {
          name: "API Management",
          components: [
            { id: "apim",   name: "Azure APIM",     system: "azure", status: "in-scope", desc: "Central API gateway, rate limiting, policies, developer portal" },
            { id: "appreg", name: "App Registrations",system: "azure", status: "in-scope", desc: "OAuth2 service principals, managed identities, cert auth" }
          ]
        },
        {
          name: "Messaging & Orchestration",
          wide: true,
          components: [
            { id: "sbus",   name: "Service Bus",    system: "azure", status: "in-scope", desc: "Queues, topics, dead-letter, sessions, at-least-once delivery" },
            { id: "logapp", name: "Logic Apps",      system: "azure", status: "in-scope", desc: "Workflow orchestration, B2B connectors, AS2/EDIFACT" },
            { id: "func",   name: "Azure Functions", system: "azure", status: "in-scope", desc: "Serverless compute, event triggers, custom transformations" },
            { id: "adf",    name: "Data Factory",    system: "azure", status: "in-scope", desc: "ETL/ELT pipelines, data flows, copy activities, scheduling" },
            { id: "evgrid", name: "Event Grid",      system: "azure", status: "in-scope", desc: "Event routing, push delivery, system topic subscriptions" }
          ]
        }
      ]
    },
    {
      id: "analytics",
      name: "Data & Analytics",
      subtitle: "Lakehouse, real-time analytics, business intelligence",
      bg: "var(--layer-bg-5)",
      accent: "var(--sys-fabric)",
      groups: [
        {
          name: "Microsoft Fabric",
          wide: true,
          components: [
            { id: "lakehouse",name: "Lakehouse",     system: "fabric", status: "in-scope", desc: "Delta Lake storage, SQL analytics endpoint, OneLake" },
            { id: "dataflow",name: "Dataflows Gen2", system: "fabric", status: "in-scope", desc: "Low-code data prep, Power Query, scheduled refresh" },
            { id: "notebook",name: "Notebooks",      system: "fabric", status: "in-scope", desc: "Spark notebooks, Python/Scala, ML workloads" },
            { id: "pipeline",name: "Data Pipelines", system: "fabric", status: "in-scope", desc: "Orchestration, copy, dataflow activities, monitoring" },
            { id: "semmodel",name: "Semantic Model", system: "fabric", status: "in-scope", desc: "DirectLake, import/composite mode, DAX measures" }
          ]
        },
        {
          name: "Power BI",
          components: [
            { id: "pbirep", name: "Reports",        system: "fabric", status: "in-scope", desc: "Interactive dashboards, paginated reports, subscriptions" },
            { id: "pbigw",  name: "Gateway",        system: "fabric", status: "in-scope", desc: "On-prem data gateway, DirectQuery, scheduled refresh" }
          ]
        }
      ]
    },
    {
      id: "infra",
      name: "Infrastructure & Security",
      subtitle: "Identity, governance, monitoring, DevOps",
      bg: "var(--layer-bg-6)",
      accent: "var(--sys-infra)",
      groups: [
        {
          name: "Identity & Access",
          components: [
            { id: "entra",  name: "Entra ID",       system: "infra", status: "in-scope", desc: "SSO, MFA, conditional access, PIM, guest access" },
            { id: "b2c",    name: "Azure AD B2C",   system: "infra", status: "future",   desc: "External identity for portals, social login, custom policies" }
          ]
        },
        {
          name: "Security & Compliance",
          components: [
            { id: "kv",     name: "Key Vault",      system: "infra", status: "in-scope", desc: "Secrets, certificates, keys, RBAC, soft delete" },
            { id: "defender",name: "Defender",        system: "infra", status: "in-scope", desc: "Threat protection, CSPM, security posture, alerts" },
            { id: "purview",name: "Purview",         system: "infra", status: "future",   desc: "Data governance, catalog, sensitivity labels, lineage" }
          ]
        },
        {
          name: "Operations",
          wide: true,
          components: [
            { id: "monitor",name: "Azure Monitor",  system: "infra", status: "in-scope", desc: "Log Analytics, Application Insights, alerts, dashboards" },
            { id: "devops", name: "Azure DevOps",    system: "infra", status: "in-scope", desc: "Repos, pipelines, boards, test plans, artifacts" },
            { id: "backup", name: "Backup & DR",     system: "infra", status: "in-scope", desc: "Azure Backup, geo-redundancy, RTO/RPO policies" }
          ]
        }
      ]
    }
  ],

  sidebars: {
    left: {
      title: "Pingala Accelerators",
      items: [
        { id: "pin-integ", name: "IntegrationsPIN",  desc: "Config-driven integration engine, 7 channels, 9-state machine, auto-retry" },
        { id: "pin-dme",   name: "Data Movement Engine", desc: "Zero-code ETL, 140x throughput, row-level traceability" },
        { id: "pin-sec",   name: "SecurityPIN",      desc: "Automated SoD analysis, role mining, security governance" },
        { id: "pin-ai",    name: "AI Methodology",   desc: "AI-assisted SDD drafting, test generation, analysis acceleration" },
        { id: "pin-test",  name: "Test Automation",   desc: "RSAT integration, regression suites, data-driven scenarios" },
        { id: "pin-alm",   name: "ALM Pipeline",      desc: "CI/CD for X++, automated build, deploy, smoke test" }
      ]
    },
    right: {
      title: "External Systems",
      items: [
        { id: "ext-bank",  name: "Banking (ISO 20022)", desc: "Payment files, bank statements, reconciliation" },
        { id: "ext-edi",   name: "EDI Partners",     desc: "EDIFACT/X12, orders, invoices, ASNs" },
        { id: "ext-tax",   name: "Tax Authority",    desc: "VAT reporting, SAF-T, Intrastat, e-invoicing" },
        { id: "ext-einv",  name: "E-invoicing",      desc: "Peppol, country-specific formats, archival" },
        { id: "ext-doc",   name: "Document Archive",  desc: "SharePoint, ECM, document management" },
        { id: "ext-crm",   name: "CRM / D365 CE",    desc: "Customer 360, opportunity mgmt, case handling" },
        { id: "ext-legacy",name: "Legacy ERP",        desc: "Data migration source, historical reference" }
      ]
    }
  },

  connections: [
    { from: "dmf",       to: "pin-dme",    label: "Migration data",     type: "data" },
    { from: "odata",     to: "apim",       label: "REST APIs",          type: "integration" },
    { from: "dualwr",    to: "dv",         label: "Near real-time sync",type: "integration" },
    { from: "apim",      to: "ext-bank",   label: "Payment files",      type: "external" },
    { from: "apim",      to: "ext-edi",    label: "EDI messages",       type: "external" },
    { from: "logapp",    to: "ext-tax",    label: "Tax filings",        type: "external" },
    { from: "sbus",      to: "func",       label: "Event processing",   type: "integration" },
    { from: "adf",       to: "lakehouse",  label: "Data ingestion",     type: "data" },
    { from: "lakehouse", to: "semmodel",   label: "DirectLake",         type: "data" },
    { from: "semmodel",  to: "pbirep",     label: "Reports",            type: "data" },
    { from: "gl",        to: "adf",        label: "Financial data",     type: "data" },
    { from: "sales",     to: "adf",        label: "Sales data",         type: "data" },
    { from: "wms",       to: "adf",        label: "Warehouse data",     type: "data" },
    { from: "pin-integ", to: "apim",       label: "Managed integrations",type: "integration" },
    { from: "pin-sec",   to: "security",   label: "SoD analysis",       type: "integration" },
    { from: "entra",     to: "apim",       label: "OAuth tokens",       type: "integration" },
    { from: "kv",        to: "func",       label: "Secrets",            type: "integration" },
    { from: "monitor",   to: "logapp",     label: "Diagnostics",        type: "integration" }
  ]
};