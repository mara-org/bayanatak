from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, Optional

from .generator import GenerateOptions, city_slugs, generate_checkouts, generate_forms, generate_users
from .reporters import render


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        records = args.func(args)
        output = render(records, args.format)
        if args.output:
            Path(args.output).write_text(output + "\n", encoding="utf-8")
        else:
            print(output)
        return 0
    except ValueError as exc:
        print(f"خطأ: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bayanatak",
        description="بيانات اختبار سعودية وهمية للمطورين، محلية وبدون API.",
    )
    parser.add_argument("--version", action="version", version="bayanatak 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    user = subparsers.add_parser("user", help="توليد مستخدمين وهميين")
    add_common_options(user)
    user.set_defaults(func=_users)

    checkout = subparsers.add_parser("checkout", help="توليد طلبات شراء وهمية")
    add_common_options(checkout)
    checkout.set_defaults(func=_checkouts)

    form = subparsers.add_parser("form", help="توليد بيانات نماذج جاهزة")
    add_common_options(form)
    form.add_argument(
        "--type",
        choices=["signup", "checkout", "waitlist"],
        default="signup",
        help="نوع النموذج",
    )
    form.set_defaults(func=_forms)

    parser.set_defaults(func=_default)
    return parser


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--count", type=_positive_count, default=10, help="عدد السجلات")
    parser.add_argument("--seed", type=int, default=None, help="رقم لتثبيت النتائج")
    parser.add_argument("--city", choices=city_slugs(), default=None, help="مدينة محددة")
    parser.add_argument(
        "--phone-mode",
        choices=["safe", "digits"],
        default="safe",
        help="safe يعطي أرقام غير قابلة للاتصال، digits لاختبار validators محليا",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="صيغة المخرجات",
    )
    parser.add_argument("--output", default="", help="حفظ التقرير في ملف")


def _default(args: argparse.Namespace) -> list[dict]:
    args.count = 10
    args.seed = None
    args.city = None
    args.phone_mode = "safe"
    args.format = "table"
    args.output = ""
    return generate_users(_options(args))


def _users(args: argparse.Namespace) -> list[dict]:
    return generate_users(_options(args))


def _checkouts(args: argparse.Namespace) -> list[dict]:
    return generate_checkouts(_options(args))


def _forms(args: argparse.Namespace) -> list[dict]:
    return generate_forms(args.type, _options(args))


def _options(args: argparse.Namespace) -> GenerateOptions:
    return GenerateOptions(
        count=args.count,
        seed=args.seed,
        city=args.city,
        phone_mode=args.phone_mode,
    )


def _positive_count(value: str) -> int:
    count = int(value)
    if count < 1 or count > 500:
        raise argparse.ArgumentTypeError("count must be between 1 and 500")
    return count


Command = Callable[[argparse.Namespace], list[dict]]


if __name__ == "__main__":
    raise SystemExit(main())
