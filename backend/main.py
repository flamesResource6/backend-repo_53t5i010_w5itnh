from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents, get_document
from schemas import Product, Order

app = FastAPI(title="Windstruck API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Windstruck API running"}


@app.get("/products", response_model=List[Product])
def list_products(tag: Optional[str] = None, featured: Optional[bool] = None):
    filter_dict = {}
    if tag:
        filter_dict["tags"] = tag
    if featured is not None:
        filter_dict["featured"] = featured
    return get_documents("product", filter_dict, limit=100)


@app.get("/products/{slug}", response_model=Product)
def get_product(slug: str):
    docs = get_documents("product", {"slug": slug}, limit=1)
    if not docs:
        raise HTTPException(404, "Product not found")
    return docs[0]


class CreateOrderRequest(BaseModel):
    items: List[dict]
    email: str


@app.post("/orders")
def create_order(payload: CreateOrderRequest):
    # In a real app you'd compute totals from product prices; simplified here
    total = 0.0
    for item in payload.items:
        qty = int(item.get("quantity", 1))
        price = float(item.get("price", 0))
        total += qty * price

    order = Order(items=payload.items, total=total, email=payload.email)
    created = create_document("order", order.dict(by_alias=True))
    return {"status": "ok", "order": created}


# Seed endpoint for demo purposes
@app.post("/seed")
def seed():
    if get_documents("product", {}, limit=1):
        return {"status": "ok", "message": "Already seeded"}

    demo_products = [
        {
            "name": "Gale Tee",
            "slug": "gale-tee",
            "price": 32.0,
            "images": [
                "https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1600&auto=format&fit=crop",
            ],
            "description": "Ultra-soft cotton tee inspired by coastal winds.",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["White", "Navy"],
            "featured": True,
            "tags": ["tops", "new"],
        },
        {
            "name": "Zephyr Hoodie",
            "slug": "zephyr-hoodie",
            "price": 68.0,
            "images": [
                "https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1600&auto=format&fit=crop",
            ],
            "description": "Lightweight fleece hoodie for breezy evenings.",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Black", "Heather Grey"],
            "featured": True,
            "tags": ["hoodies", "bestseller"],
        },
        {
            "name": "Drift Joggers",
            "slug": "drift-joggers",
            "price": 58.0,
            "images": [
                "https://images.unsplash.com/photo-1548883354-94bc2cbc1098?q=80&w=1600&auto=format&fit=crop",
            ],
            "description": "Tapered fit joggers with breathable stretch fabric.",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Charcoal", "Navy"],
            "featured": False,
            "tags": ["bottoms"],
        },
    ]

    for p in demo_products:
        create_document("product", p)

    return {"status": "ok", "message": "Seeded demo products"}
