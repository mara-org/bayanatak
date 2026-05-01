from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Optional

from .data import (
    CITIES,
    FIRST_NAMES,
    PAYMENT_METHODS,
    PRODUCTS,
    SAUDI_MOBILE_PREFIXES,
    STREETS,
    TEST_LAST_NAMES,
)


@dataclass(frozen=True)
class GenerateOptions:
    count: int = 10
    seed: Optional[int] = None
    city: Optional[str] = None
    phone_mode: str = "safe"


def generate_users(options: GenerateOptions) -> list[dict[str, Any]]:
    rng = random.Random(options.seed)
    return [_user_record(rng, index + 1, options) for index in range(options.count)]


def generate_checkouts(options: GenerateOptions) -> list[dict[str, Any]]:
    rng = random.Random(options.seed)
    return [_checkout_record(rng, index + 1, options) for index in range(options.count)]


def generate_forms(form_type: str, options: GenerateOptions) -> list[dict[str, Any]]:
    if form_type == "signup":
        return [_signup_form(record) for record in generate_users(options)]
    if form_type == "checkout":
        return [_checkout_form(record) for record in generate_checkouts(options)]
    if form_type == "waitlist":
        return [_waitlist_form(record) for record in generate_users(options)]
    raise ValueError(f"unsupported form type: {form_type}")


def city_slugs() -> list[str]:
    return sorted(CITIES)


def _user_record(rng: random.Random, index: int, options: GenerateOptions) -> dict[str, Any]:
    first_ar, first_en = rng.choice(FIRST_NAMES)
    last_ar, last_en = rng.choice(TEST_LAST_NAMES)
    city = _city(rng, options.city)
    user_id = f"TST-{index:04d}"
    email = f"{first_en}.{last_en}.{index:04d}@example.test"
    return {
        "id": user_id,
        "name_ar": f"{first_ar} {last_ar}",
        "name_en": f"{first_en.title()} {last_en.title()}",
        "email": email,
        "phone": _phone(index, rng, options.phone_mode),
        "city": city["name_ar"],
        "city_en": city["name_en"],
        "region": city["region_ar"],
        "is_fake": True,
    }


def _checkout_record(rng: random.Random, index: int, options: GenerateOptions) -> dict[str, Any]:
    user = _user_record(rng, index, options)
    city = _city_by_ar(user["city"])
    item_name_ar, item_sku, price = rng.choice(PRODUCTS)
    quantity = rng.randint(1, 3)
    subtotal = price * quantity
    vat = round(subtotal * 0.15, 2)
    shipping = 0 if subtotal >= 150 else 18
    total = round(subtotal + vat + shipping, 2)
    neighborhood = rng.choice(city["neighborhoods"])
    return {
        "order_id": f"ORD-TST-{index:04d}",
        "customer": user["name_ar"],
        "phone": user["phone"],
        "city": city["name_ar"],
        "neighborhood": neighborhood,
        "address": f"{rng.choice(STREETS)}، {neighborhood}",
        "sku": item_sku,
        "item": item_name_ar,
        "quantity": quantity,
        "subtotal_sar": subtotal,
        "vat_sar": vat,
        "shipping_sar": shipping,
        "total_sar": total,
        "payment_method": rng.choice(PAYMENT_METHODS),
        "delivery_date": _delivery_date(index),
        "is_fake": True,
    }


def _signup_form(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "form_type": "signup",
        "full_name": record["name_ar"],
        "email": record["email"],
        "mobile": record["phone"],
        "city": record["city"],
        "role": "مطور",
        "consent": True,
        "is_fake": True,
    }


def _checkout_form(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "form_type": "checkout",
        "full_name": record["customer"],
        "mobile": record["phone"],
        "city": record["city"],
        "neighborhood": record["neighborhood"],
        "address": record["address"],
        "payment_method": record["payment_method"],
        "is_fake": True,
    }


def _waitlist_form(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "form_type": "waitlist",
        "full_name": record["name_ar"],
        "email": record["email"],
        "city": record["city"],
        "interest": "أدوات مطورين",
        "source": "تويتر",
        "is_fake": True,
    }


def _city(rng: random.Random, slug: Optional[str]) -> dict[str, Any]:
    if slug:
        if slug not in CITIES:
            raise ValueError(f"unsupported city: {slug}")
        return CITIES[slug]
    return CITIES[rng.choice(city_slugs())]


def _city_by_ar(name_ar: str) -> dict[str, Any]:
    for city in CITIES.values():
        if city["name_ar"] == name_ar:
            return city
    return CITIES["riyadh"]


def _phone(index: int, rng: random.Random, mode: str) -> str:
    prefix = rng.choice(SAUDI_MOBILE_PREFIXES)
    suffix = f"{index:07d}"[-7:]
    if mode == "safe":
        return f"{prefix[:2]}X{suffix}"
    if mode == "digits":
        return f"{prefix}{suffix}"
    raise ValueError(f"unsupported phone mode: {mode}")


def _delivery_date(index: int) -> str:
    return (date(2026, 5, 1) + timedelta(days=index % 7)).isoformat()
