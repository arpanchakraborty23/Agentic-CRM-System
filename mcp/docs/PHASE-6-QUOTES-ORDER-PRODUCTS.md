# Phase 6: Products, Quotes & Orders

## Objective
Manage product/service catalog, generate quotes from deals, and track orders through fulfillment.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Product` | `products` | Product/service catalog |
| `PriceBook` | `price_books` | Regional/customer pricing tiers |
| `Quote` | `quotes` | Sales quote linked to a deal |
| `QuoteLineItem` | `quote_line_items` | Individual line items on a quote |
| `Order` | `orders` | Won quotes converted to orders |
| `Invoice` | `invoices` | Billing records |

## Tools to Create

### Product & Price Book Tools
| Tool | Description |
|------|-------------|
| `create_product(name, description, unit_price, category, sku, tax_rate)` | Add product to catalog |
| `list_products(category, search, page, limit)` | Product catalog |
| `update_product(product_id, **fields)` | Update pricing, description |
| `create_price_book(name, currency, valid_from, valid_to)` | Define price tier |
| `add_product_to_price_book(price_book_id, product_id, price)` | Set product price in book |
| `get_pricing(product_id, price_book_id)` | Effective price lookup |

### Quote Tools
| Tool | Description |
|------|-------------|
| `create_quote(deal_id, valid_until, terms, discount)` | Generate quote from deal |
| `add_line_item(quote_id, product_id, quantity, unit_price, discount)` | Add product line |
| `list_quotes(deal_id, status, page, limit)` | Quote history for a deal |
| `get_quote(quote_id)` | Full quote with line items + totals |
| `update_quote(quote_id, **fields)` | Edit terms, discount |
| `approve_quote(quote_id, approver_id)` | Internal approval |
| `send_quote(quote_id, email)` | Email quote to customer |
| `convert_quote_to_order(quote_id)` | Accept → create order |

### Order & Invoice Tools
| Tool | Description |
|------|-------------|
| `create_order(quote_id, shipping_address, payment_terms)` | Place order from accepted quote |
| `list_orders(company_id, status, date_range, page, limit)` | Order dashboard |
| `get_order(order_id)` | Order with items + status |
| `update_order_status(order_id, status)` | Shipped, delivered, cancelled |
| `generate_invoice(order_id)` | Create invoice from order |
| `list_invoices(company_id, status, page, limit)` | Accounts receivable view |
| `record_payment(invoice_id, amount, method, reference)` | Record payment received |

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.commerce_tools import create_product, create_quote
async def test():
    p = await create_product('Consulting Package', '4hr strategy session', 2500, 'services')
    print(p)
asyncio.run(test())
"
```
