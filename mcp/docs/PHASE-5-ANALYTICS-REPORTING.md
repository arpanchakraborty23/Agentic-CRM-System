# Phase 5: Analytics & Reporting

## Objective
Provide real-time sales metrics, dashboards, and exportable reports — from individual rep performance to company-wide forecasts.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Report` | `reports` | Saved report configurations |
| `Dashboard` | `dashboards` | Custom dashboard layouts |
| `SalesMetric` | `sales_metrics` | Pre-computed daily rollups |

## Tools to Create

### Sales Metrics Tools
| Tool | Description |
|------|-------------|
| `get_sales_kpi(start_date, end_date, user_id)` | Revenue, deals won, avg deal size, conversion rate |
| `get_pipeline_velocity(date_range, user_id)` | Avg time per stage, win rate |
| `get_rep_performance(user_id, date_range)` | Individual rep metrics + rank |
| `get_forecast(period)` | Weighted pipeline forecast |
| `get_conversion_funnel(start_date, end_date)` | Lead → MQL → SQL → Won funnel |

### Report Tools
| Tool | Description |
|------|-------------|
| `create_report(name, type, filters, metrics, schedule)` | Build a custom report |
| `run_report(report_id, parameters)` | Execute and return results |
| `list_reports(category, page, limit)` | Saved reports library |
| `export_report(report_id, format)` | Export as CSV / PDF / Excel |
| `schedule_report(report_id, cron, recipients)` | Email report on schedule |

### Dashboard Tools
| Tool | Description |
|------|-------------|
| `create_dashboard(name, widgets, layout)` | Build a dashboard |
| `get_dashboard(dashboard_id)` | Render live widget data |
| `list_dashboards(user_id)` | User's dashboards |
| `update_dashboard(dashboard_id, widgets, layout)` | Rearrange widgets |

### Aggregate Queries
| Tool | Description |
|------|-------------|
| `get_top_deals(limit, stage)` | Biggest active deals |
| `get_aging_deals(threshold_days)` | Deals stuck in stage |
| `get_activity_summary(date_range, user_id)` | Calls, emails, meetings per day |
| `get_lead_source_breakdown(date_range)` | Best-performing channels |
| `get_company_health_score(company_id)` | Engagement score based on activity |

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.reporting_tools import get_sales_kpi, get_pipeline_velocity
async def test():
    kpi = await get_sales_kpi('2026-01-01', '2026-06-20')
    print(kpi)
asyncio.run(test())
"
```
